# Exact dedicated NAG implementation excerpt from ComfyUI-KJNodes, MIT.
# See KJ_LICENSE.txt and environment/nag_source_reference.json for revision.
import types
import torch
import comfy
import comfy.model_management as mm
import comfy.ldm.modules.attention as _comfy_attn
from comfy_api.latest import io
def _compute_attention(self, query, context, attn_precision=None, transformer_options={}, mask=None):
    """Compute attention and return the result. Cleans up intermediate tensors.

    When `mask` is non-None, bypass wrap_attn and call attention_pytorch directly —
    sage and similar backends drop arbitrary masks.
    """
    k = self.k_norm(self.to_k(context)).to(query.dtype)
    v = self.to_v(context).to(query.dtype)
    if mask is None:
        x = comfy.ldm.modules.attention.optimized_attention(query, k, v, heads=self.heads, attn_precision=attn_precision, transformer_options=transformer_options).flatten(2)
    else:
        x = comfy.ldm.modules.attention.attention_pytorch(query, k, v, heads=self.heads, mask=mask, attn_precision=attn_precision, _inside_attn_wrapper=True, transformer_options=transformer_options).flatten(2)
    del k, v
    return x

def nag_attention(self, query, context_positive, nag_context, attn_precision=None, transformer_options={}, mask=None):
    # mask (e.g. PromptRelay's temporal routing) only applies to the real-context, not NAG context
    x_positive = _compute_attention(self, query, context_positive, attn_precision, transformer_options, mask=mask)
    x_negative = _compute_attention(self, query, nag_context, attn_precision, transformer_options)
    return x_positive, x_negative

def normalized_attention_guidance(self, x_positive, x_negative):
    if self.inplace:
        nag_guidance = x_negative.mul_(self.nag_scale - 1).neg_().add_(x_positive, alpha=self.nag_scale)
        del x_negative
    else:
        nag_guidance = x_negative * (self.nag_scale - 1)
        del x_negative
        nag_guidance = (x_positive * self.nag_scale).sub_(nag_guidance)

    norm_positive = torch.norm(x_positive, p=1, dim=-1, keepdim=True)
    norm_guidance = torch.norm(nag_guidance, p=1, dim=-1, keepdim=True)

    scale = norm_guidance / norm_positive
    torch.nan_to_num_(scale, nan=10.0)
    mask = scale > self.nag_tau
    del scale

    adjustment = (norm_positive * self.nag_tau) / (norm_guidance + 1e-7)
    del norm_positive, norm_guidance

    nag_guidance.mul_(torch.where(mask, adjustment, 1.0))
    del mask, adjustment

    if self.inplace:
        return nag_guidance.sub_(x_positive).mul_(self.nag_alpha).add_(x_positive)
    else:
        nag_guidance.mul_(self.nag_alpha)
        return nag_guidance.add_(x_positive * (1 - self.nag_alpha))

#region NAG
def ltxv_crossattn_forward_nag(self, x, context, mask=None, transformer_options={}, **kwargs):

    if mask is None:
        mask_provider = transformer_options.get("promptrelay_mask_fn")
        if mask_provider is not None:
            mask = mask_provider(x.shape[1], context.shape[1], x.dtype, x.device, transformer_options)

    # Single or [pos, neg] pair
    if context.shape[0] == 1:
        x_pos, context_pos = x, context
        x_neg, context_neg = None, None
    else:
        x_pos, x_neg = torch.chunk(x, 2, dim=0)
        context_pos, context_neg = torch.chunk(context, 2, dim=0)

    # Positive
    q_pos = self.q_norm(self.to_q(x_pos))
    del x_pos

    x_positive, x_negative = nag_attention(self, q_pos, context_pos, self.nag_context, attn_precision=self.attn_precision, transformer_options=transformer_options, mask=mask)
    del context_pos, q_pos

    x_pos_out = normalized_attention_guidance(self, x_positive, x_negative)
    del x_positive, x_negative

    # Negative
    if x_neg is not None and context_neg is not None:
        q_neg = self.q_norm(self.to_q(x_neg))
        k_neg = self.k_norm(self.to_k(context_neg))
        v_neg = self.to_v(context_neg)

        x_neg_out = comfy.ldm.modules.attention.optimized_attention(q_neg, k_neg, v_neg, heads=self.heads, attn_precision=self.attn_precision, transformer_options=transformer_options)
        out = torch.cat([x_pos_out, x_neg_out], dim=0)
    else:
        out = x_pos_out

    if self.to_gate_logits is not None:
        gate_logits = self.to_gate_logits(x)  # (B, T, H)
        b, t, _ = out.shape
        out = out.view(b, t, self.heads, self.dim_head)
        gates = 2.0 * torch.sigmoid(gate_logits)  # zero-init -> identity
        out = out * gates.unsqueeze(-1)
        out = out.view(b, t, self.heads * self.dim_head)

    return self.to_out(out)


class LTXVCrossAttentionPatch:
    def __init__(self, context, nag_scale, nag_alpha, nag_tau, inplace=True):
        self.nag_context = context
        self.nag_scale = nag_scale
        self.nag_alpha = nag_alpha
        self.nag_tau = nag_tau
        self.inplace = inplace

    def __get__(self, obj, objtype=None):
        # Create bound method with stored parameters
        def wrapped_attention(self_module, *args, **kwargs):
            self_module.nag_context = self.nag_context
            self_module.nag_scale = self.nag_scale
            self_module.nag_alpha = self.nag_alpha
            self_module.nag_tau = self.nag_tau
            self_module.inplace = self.inplace

            return ltxv_crossattn_forward_nag(self_module, *args, **kwargs)
        return types.MethodType(wrapped_attention, obj)

class LTX2_NAG(io.ComfyNode):

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="LTX2_NAG",
            display_name="LTX2 NAG",
            category="KJNodes/ltxv",
            description="https://github.com/ChenDarYen/Normalized-Attention-Guidance",
            is_experimental=True,
            inputs=[
                io.Model.Input("model"),
                io.Float.Input("nag_scale", default=11.0, min=0.0, max=100.0, step=0.001, tooltip="Strength of negative guidance effect"),
                io.Float.Input("nag_alpha", default=0.25, min=0.0, max=1.0, step=0.001, tooltip="Mixing coefficient in that controls the balance between the normalized guided representation and the original positive representation."),
                io.Float.Input("nag_tau", default=2.5, min=0.0, max=10.0, step=0.001, tooltip="Clipping threshold that controls how much the guided attention can deviate from the positive attention."),
                io.Conditioning.Input("nag_cond_video", optional=True),
                io.Conditioning.Input("nag_cond_audio", optional=True),
                io.Boolean.Input("inplace", default=True, optional=True, tooltip="If true, modifies tensors in place to save memory. Leads to different numerical results which may change the output slightly."),
            ],
            outputs=[
                io.Model.Output(display_name="model"),
            ],
        )

    @classmethod
    def execute(cls, model, nag_scale, nag_alpha, nag_tau, nag_cond_video=None, nag_cond_audio=None, inplace=True) -> io.NodeOutput:
        if nag_scale == 0:
            return io.NodeOutput(model)

        device = mm.get_torch_device()
        offload_device = mm.unet_offload_device()
        dtype = model.model.manual_cast_dtype
        if dtype is None:
            dtype = model.model.diffusion_model.dtype

        model_clone = model.clone()

        diffusion_model = model_clone.get_model_object("diffusion_model")
        img_dim = diffusion_model.inner_dim
        audio_dim = diffusion_model.audio_inner_dim

        context_video = context_audio = None

        if nag_cond_video is not None:
            context_video = nag_cond_video[0][0].to(device, dtype)
            vid_split = getattr(diffusion_model, "cross_attention_dim", None)
            if vid_split is not None and context_video.shape[-1] == vid_split + diffusion_model.audio_cross_attention_dim:
                context_video = context_video[:, :, :vid_split]
            if diffusion_model.caption_proj_before_connector and diffusion_model.caption_projection_first_linear:
                diffusion_model.caption_projection.to(device)
                context_video = diffusion_model.caption_projection(context_video)
                diffusion_model.caption_projection.to(offload_device)
            if hasattr(diffusion_model, "video_embeddings_connector"):
                diffusion_model.video_embeddings_connector.to(device)
                context_video = diffusion_model.video_embeddings_connector(context_video)[0]
                diffusion_model.video_embeddings_connector.to(offload_device)
            context_video = context_video.view(1, -1, img_dim)
            for idx, block in enumerate(diffusion_model.transformer_blocks):
                patched_attn2 = LTXVCrossAttentionPatch(context_video, nag_scale, nag_alpha, nag_tau, inplace=inplace).__get__(block.attn2, block.__class__)
                model_clone.add_object_patch(f"diffusion_model.transformer_blocks.{idx}.attn2.forward", patched_attn2)

        if nag_cond_audio is not None and diffusion_model.audio_caption_projection is not None:
            context_audio = nag_cond_audio[0][0].to(device, dtype)
            vid_split = getattr(diffusion_model, "cross_attention_dim", None)
            if vid_split is not None and context_audio.shape[-1] == vid_split + diffusion_model.audio_cross_attention_dim:
                context_audio = context_audio[:, :, vid_split:]
            if diffusion_model.caption_proj_before_connector and diffusion_model.caption_projection_first_linear:
                diffusion_model.audio_caption_projection.to(device)
                context_audio = diffusion_model.audio_caption_projection(context_audio)
                diffusion_model.audio_caption_projection.to(offload_device)
            if hasattr(diffusion_model, "audio_embeddings_connector"):
                diffusion_model.audio_embeddings_connector.to(device)
                context_audio = diffusion_model.audio_embeddings_connector(context_audio)[0]
                diffusion_model.audio_embeddings_connector.to(offload_device)
            context_audio = context_audio.view(1, -1, audio_dim)
            for idx, block in enumerate(diffusion_model.transformer_blocks):
                patched_audio_attn2 = LTXVCrossAttentionPatch(context_audio, nag_scale, nag_alpha, nag_tau, inplace=inplace).__get__(block.audio_attn2, block.__class__)
                model_clone.add_object_patch(f"diffusion_model.transformer_blocks.{idx}.audio_attn2.forward", patched_audio_attn2)

        return io.NodeOutput(model_clone)


