from pathlib import Path
import sys,json,torch,types
root=Path(r"C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\ComfyUI\0.34.0\ComfyUI_windows_portable\ComfyUI")
sys.path.insert(0,str(root));sys.path.insert(0,str(Path(__file__).parent));sys.argv=[sys.argv[0],"--cpu"]
import comfy.options;comfy.options.enable_args_parsing()
from study_nodes import StudyLTXAdaIN,StudyChunkFeedForward
from comfy.ldm.lightricks.model import FeedForward,CrossAttention
import comfy.ops
from ltx_nag_vendor import ltxv_crossattn_forward_nag
torch.manual_seed(7)
x=torch.randn(2,128,6,12,16);r=torch.randn(2,128,6,6,8)*2+3
y=StudyLTXAdaIN().apply({"samples":x},{"samples":r})[0]["samples"]
expected=torch.empty_like(x)
for n in range(2):
 for c in range(128):expected[n,c]=(x[n,c]-x[n,c].mean())/x[n,c].std()*r[n,c].std()+r[n,c].mean()
adain_error=float((y-expected).abs().max());assert torch.allclose(y,expected,atol=2e-6,rtol=2e-6)
ff=FeedForward(32,32,operations=comfy.ops.manual_cast,dtype=torch.float32,device="cpu").eval()
with torch.no_grad():
 for z in ff.parameters():z.uniform_(-.1,.1)
x=torch.randn(2,1031,32)
expected=ff(x);actual=torch.cat([ff(z) for z in x.split(128,dim=1)],dim=1)
ff_error=float((expected-actual).abs().max());assert torch.allclose(actual,expected,atol=2e-6,rtol=2e-6)
a=CrossAttention(64,64,heads=2,dim_head=32,operations=comfy.ops.manual_cast,dtype=torch.float32,device="cpu").eval()
with torch.no_grad():
 for name,z in a.named_parameters():z.fill_(1) if 'norm' in name else z.uniform_(-.1,.1)
x=torch.randn(1,47,64);context=torch.randn(1,23,64);a.nag_context=torch.randn(1,19,64);a.nag_scale=1.;a.nag_alpha=.25;a.nag_tau=2.5;a.inplace=True
stock=a(x,context);same=ltxv_crossattn_forward_nag(a,x,context);nag_identity_error=float((stock-same).abs().max());assert torch.allclose(stock,same,atol=2e-6,rtol=2e-6)
a.nag_scale=5.;guided=ltxv_crossattn_forward_nag(a,x,context);delta=float((guided-stock).abs().mean());assert delta>0 and torch.isfinite(guided).all()
result={"status":"PASS","actual_installed_comfy_classes":True,"adain_max_abs_error":adain_error,"ff_chunk_max_abs_error":ff_error,"nag_scale1_stock_max_abs_error":nag_identity_error,"nag_scale5_mean_abs_change":delta,"limits":"Small CPU tensors verify arithmetic/interface, not GGUF GPU quality or performance."}
Path(__file__).resolve().parents[1].joinpath("environment/adapter_math_verification.json").write_text(json.dumps(result,indent=2)+"\n");print(result)
