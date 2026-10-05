"""Experimental saved-latent decode only; does not modify the pinned decoder source."""
import json,time,hashlib
from pathlib import Path
import torch
import nodes
R=Path(r'H:\MermaidReefTools\LocalVideo\ltx25')

class FocusDecoderAblation:
    @classmethod
    def INPUT_TYPES(cls):
        return {'required':{'samples':('LATENT',),'vae':('VAE',),'steps':('INT',{'default':1,'min':1,'max':2})}}
    RETURN_TYPES=('IMAGE',);FUNCTION='decode';CATEGORY='Mermaid/source-study'
    def decode(self,samples,vae,steps):
        model=vae.first_stage_model
        assert type(model).__name__=='CausalDiffusionVAE','Wrong decoder class'
        decoder=model.decoder;old=decoder.default_inference_timesteps
        assert old.tolist()==[1.0],'Unexpected publisher default schedule'
        start=time.monotonic();before=samples['samples'].clone()
        torch.cuda.reset_peak_memory_stats()
        decoder.default_inference_timesteps=torch.linspace(1.0,1.0/steps,steps,device=old.device,dtype=old.dtype)
        schedule=decoder.default_inference_timesteps.tolist()
        try:
            images=nodes.VAEDecodeTiled().decode(vae,samples,256,64,64,8)[0]
            assert torch.isfinite(images).all() and tuple(images.shape)==(41,832,576,3)
            assert torch.equal(before,samples['samples']),'Latent changed during decode'
        finally:
            decoder.default_inference_timesteps=old
        source=Path(__import__(model.__class__.__module__,fromlist=['__file__']).__file__)
        report={'status':'DECODE_EXECUTION_PASS','steps':steps,'schedule':schedule,'default_schedule':old.tolist(),
                'decoder_class':type(model).__name__,'decoder_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                'noise_seed':0,'same_video_latent_unchanged':True,'new_transformer_generation':False,
                'elapsed_seconds':time.monotonic()-start,'peak_torch_allocated_bytes':torch.cuda.max_memory_allocated(),
                'experimental':steps==2,'publisher_recommended':steps==1,'quality_accepted':False}
        path=R/'results/focus_decoder_ablation';path.mkdir(exist_ok=True)
        (path/f'steps_{steps}.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        print('FOCUS_DECODER',json.dumps(report),flush=True)
        return (images,)

NODE_CLASS_MAPPINGS={'FocusDecoderAblation':FocusDecoderAblation}
