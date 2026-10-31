from pathlib import Path
import json,subprocess,shutil
p=Path(__file__).resolve().parents[1]
a=r'C:\Program Files\Aseprite\Aseprite.exe';ff=r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffmpeg.exe'
d=p/'comparison';d.mkdir(exist_ok=True)
subprocess.run([a,'-b','--script-param','root='+str(p),'--script',str(p/'scripts/native_comparison.lua')],check=True,timeout=180)
subprocess.run([ff,'-v','error','-framerate','24','-i',str(d/'frames/%04d.png'),'-frames:v','41','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart','-y',str(d/'native_four_takes.mp4')],check=True,timeout=180)
(d/'mapping.json').write_text(json.dumps({'columns':['base_two_pass','temporal_retake','anti_blur_nag','temporal_48fps'],'column_native_dimensions':[576,832],'comparison_native_dimensions':[2304,832],'fps':24,'frames':41,'source_indices':{'base_two_pass':list(range(41)),'temporal_retake':list(range(41)),'anti_blur_nag':list(range(41)),'temporal_48fps':list(range(0,81,2))},'no_spatial_resampling':True,'no_interpolation':True,'no_pixel_repair':True,'temporal48_original_display_seconds':81/48,'comparison_display_seconds':41/24,'temporal48_final_display_extension_seconds':1/48},indent=2)+'\n')
print('NATIVE_COMPARISON_EXPORTED',flush=True)
