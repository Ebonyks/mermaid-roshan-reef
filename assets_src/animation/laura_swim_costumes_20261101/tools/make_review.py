"""Build honest normal-speed comparison media from actual native frames."""
from pathlib import Path
import json, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FFMPEG = Path('C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe')
ORDER = ['original','chef','farmer','doctor','teacher','painter','astronaut','detective','geologist','candymaker','nursery','boxer','racer','popstar','ballet','magician']
LABELS = {'candymaker':'Candy maker','popstar':'Pop star'}


def font(size):
    return ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',size)


def encode(path, frames):
    args = [str(FFMPEG),'-y','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size','1280x720','-framerate','30','-i','pipe:0','-vf','setsar=1','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(path)]
    process = subprocess.Popen(args,stdin=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
    try:
        for frame in frames:
            process.stdin.write(frame.tobytes())
    finally:
        process.stdin.close()
    error = process.stderr.read().decode(errors='replace')
    assert process.wait()==0,error


def main():
    sources = json.loads((ROOT/'sources.json').read_text())
    lookup = {theme:g['group'] for g in sources['groups'] for theme in g['themes']}
    review = ROOT/'review'
    review.mkdir(exist_ok=True)
    background = Image.new('RGB',(1280,720),(224,239,243))
    draw = ImageDraw.Draw(background)
    draw.rectangle((0,0,1280,52),fill=(19,48,65))
    draw.text((22,10),'Roshan swimming — Laura-led front-view prototype',font=font(23),fill='white')
    draw.text((22,687),'Same skeleton, motion, scale and timing • Provisional costumes; defects remain under review',font=font(17),fill=(29,66,83))

    def grid(themes, frame, clip='travel', overview=False):
        canvas = background.copy()
        pen = ImageDraw.Draw(canvas)
        columns,rows = (4,4) if overview else (2,2)
        width,height = 1280//columns,628//rows
        size = 156 if overview else 306
        for index,theme in enumerate(themes):
            group = lookup[theme]
            image = Image.open(ROOT/f'raw_render/{group}/{theme}/{clip}/{frame:04}.png').convert('RGBA')
            image = image.resize((size,size),Image.Resampling.LANCZOS)
            x=(index%columns)*width+(width-size)//2
            y=54+(index//columns)*height
            canvas.paste(image,(x,y),image)
            title = LABELS.get(theme,theme.capitalize())
            pen.text(((index%columns)*width+18,y+3),title,font=font(15 if overview else 20),fill=(24,57,74))
        return canvas

    for page in range(4):
        themes=ORDER[page*4:page*4+4]
        encode(review/f'comparison_{page+1}.mp4',(grid(themes,i) for i in range(216)))
        grid(themes,18).save(review/f'costumes_page_{page+1}.jpg',quality=95)
    encode(review/'all_16_swimming.mp4',(grid(ORDER,i,overview=True) for i in range(216)))
    grid(ORDER,18,overview=True).save(review/'all_16_overview.jpg',quality=95)
    # One readable large figure for judging acting before comparing smaller costumes.
    def hero_frames():
        for index in range(216):
            canvas = background.copy()
            image=Image.open(ROOT/f'raw_render/{lookup["original"]}/original/travel/{index:04}.png').convert('RGBA').resize((650,650),Image.Resampling.LANCZOS)
            canvas.paste(image,(315,36),image)
            pen=ImageDraw.Draw(canvas)
            pen.text((28,88),'Original outfit',font=font(27),fill=(24,57,74))
            pen.text((28,133),'Tail-led push → generous glide',font=font(21),fill=(24,57,74))
            pen.text((28,164),'Quiet hands → supported settle',font=font(21),fill=(24,57,74))
            yield canvas
    encode(review/'basic_swimming.mp4',hero_frames())
    # Direct cuts between synchronized four-costume pages; no retiming or altered native pixels.
    concat = review/'comparison_concat.txt'
    concat.write_text(''.join("file 'comparison_%d.mp4'\n"%i for i in range(1,5)),encoding='utf-8',newline='\n')
    subprocess.run([str(FFMPEG),'-y','-v','error','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(review/'costume_comparison.mp4')],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
    mapping={'native_fps':30,'loop_source_frames':55,'loop_playback_frames':54,'loop_duration_seconds':1.8,'travel_source_frames':217,'travel_playback_frames':216,'travel_duration_seconds':7.2,'source_endpoint_policy':'Last endpoint capture is retained for seam/settle checks; normal-speed review maps frame0 through215 for exactly7.2s.','comparison_order':ORDER,'pages':4,'costume_comparison_seconds':28.8,'all16_overview':'Small overview only; four-up and large original are the readable review lanes.'}
    (ROOT/'evidence/review_mapping.json').write_text(json.dumps(mapping,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('NORMAL_SPEED_REVIEW_READY',review,flush=True)


if __name__=='__main__':
    main()
