from pathlib import Path
import subprocess,json
p=Path(__file__).resolve().parents[1];ff=r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffmpeg.exe'
source=p.parent/'ltx_registered_wave_20261004/results/figure_wide_slow/preview.mp4'
inputs=[source,p/'results/ltxv_guide_standard/assembled.mp4',p/'results/ltxv_guide_strong/assembled.mp4']
labels=['Original rejected whole-figure take','LTX-Video 2B guide strength 1','LTX-Video 2B guide strength 2']
new=p/'results/ltx23_retake_lowmem/assembled.mp4'
if new.exists():inputs.append(new);labels.append('LTX-2.3 low-memory retake (upscaled)')
args=[ff,'-hide_banner','-loglevel','error','-y']
for item in inputs:args+=['-i',str(item)]
filters=[]
for i,label in enumerate(labels):filters.append(f'[{i}:v]scale=448:256,pad=448:288:0:32:color=white,drawtext=fontfile=arial.ttf:text=\'{label}\':x=8:y=8:fontsize=13:fontcolor=black[v{i}]')
filters.append(''.join(f'[v{i}]' for i in range(len(inputs)))+f'hstack=inputs={len(inputs)}[out]')
args+=['-filter_complex',';'.join(filters),'-map','[out]','-frames:v','81','-c:v','libx264','-threads','2','-crf','18','-pix_fmt','yuv420p','-an',str(p/'comparison/completed_takes.mp4')]
subprocess.run(args,check=True,timeout=180,cwd=r"C:\Windows\Fonts")
(p/'comparison/encoding.json').write_text(json.dumps({'comparison_input_paths':[str(x.relative_to(p.parent)).replace('\\','/') for x in inputs],'labels':labels,'frames':81,'fps':24,'whole_canvas_preview_scale':[448,256],'no_interpolation':True,'failed_attempts_have_no_footage':True},indent=2)+'\n')
print('COMPARISON_ENCODED',len(inputs),'actual completed takes')
