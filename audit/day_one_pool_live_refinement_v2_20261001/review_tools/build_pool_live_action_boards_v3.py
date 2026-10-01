from pathlib import Path
import hashlib, json
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
folder = root/'audit/day_one_pool_live_refinement_v2_20261001/native_actions_1280_v3'
receipt_path=folder/'ACTION_RECEIPT.json'
receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
out=folder/'inspection_boards'
assert not out.exists(), 'Preserve existing boards.'
out.mkdir()
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
boards=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for action in receipt['actions']:
    start,end=action['start_frame'],action['end_frame_exclusive']
    for chunk in range(start,end,10):
        indices=list(range(chunk,min(chunk+10,end)))
        board=Image.new('RGB',(1280,384*((len(indices)+1)//2)), '#faf4e8')
        draw=ImageDraw.Draw(board)
        for cell, index in enumerate(indices):
            record=receipt['frames'][index]
            source=folder/record['path']
            assert sha(source)==record['sha256']
            image=Image.open(source).convert('RGB')
            assert image.size==(1280,720)
            x,y=(cell%2)*640,(cell//2)*384
            draw.text((x+5,y+4),f"#{index:04d}  {record['elapsed_wall_ms']}ms  drop={record.get('drop_time','-')}",font=font,fill='#252b4c')
            board.paste(image.resize((640,360),Image.Resampling.LANCZOS),(x,y+24))
        path=out/f"item_{action['requested_item']:02d}_frames_{indices[0]:04d}_{indices[-1]:04d}.webp"
        board.save(path,lossless=True,quality=100)
        boards.append({'path':path.relative_to(folder).as_posix(),'sha256':sha(path),'item':action['requested_item'],'frame_indices':indices,'dimensions':list(board.size)})
(out/'MANIFEST.json').write_text(json.dumps({'schema':'reef.full-action-inspection-boards.v1','receipt_sha256':sha(receipt_path),'boards':boards,'frame_count':sum(len(b['frame_indices']) for b in boards),'qualification':'Audit only: every one of424 action frames included once, in original order, whole-canvas50% uniform normalization with exterior labels. Original lossless1280x720 frames retained. No subject editing/delivery pixels or continuous-video review claim.'},indent=2)+'\n',encoding='utf-8')
print('Created',len(boards),'boards covering',sum(len(b['frame_indices']) for b in boards),'action frames')
