from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def structure(im):
    assert im.mode=="RGBA","RGBA required"
    assert im.size==(1024,1024),"1024 square required"
    a=im.getchannel("A")
    b=a.point(lambda v:255 if v>=16 else 0).getbbox()
    assert b is not None,"empty object"
    assert min(b[0],b[1],1024-b[2],1024-b[3])>=4,"object clipped or stray opaque edge"
    n=sum(v>=16 for v in a.getdata())
    assert 0.01<n/(1024*1024)<0.85,"empty or scene-filled canvas"
    return {"alpha_bounds":list(b),"coverage":round(n/(1024*1024),4)}
def main():
    jobs=json.loads((HERE/"generation_jobs.json").read_text(encoding="utf-8"))
    exports=json.loads((HERE/"runtime_exports.json").read_text(encoding="utf-8"))["exports"]
    controls=[]
    im=Image.open(ROOT/exports[0]["runtime"].removeprefix("res://")).convert("RGBA")
    for label,bad in [("empty",Image.new("RGBA",im.size)),("wrong_size",im.resize((512,512))),("opaque_backdrop",Image.new("RGBA",im.size,"white"))]:
        try: structure(bad)
        except AssertionError: controls.append(label)
        else: raise AssertionError("Negative control accepted: "+label)
    edge=im.copy();edge.putpixel((0,512),(255,0,0,255))
    try: structure(edge)
    except AssertionError: controls.append("stray_edge_pixel")
    else: raise AssertionError("Stray-edge control accepted")
    report={"negative_controls_rejected":controls,"assets":[]}
    for job,exp in zip(jobs["jobs"],exports):
        assert job["id"]==exp["id"]
        src=ROOT/exp["source"].removeprefix("res://")
        dst=ROOT/exp["runtime"].removeprefix("res://")
        assert digest(src)==exp["source_sha256"]==job["attempts"][0]["native_sha256"],"source hash drift"
        assert digest(dst)==exp["runtime_sha256"],"runtime hash drift"
        for ref in job["packet"]["source_motif_references"]: assert digest(ROOT/ref["path"])==ref["sha256"],"reference hash drift"
        assert hashlib.sha256(job["prompt"].encode()).hexdigest()==job["prompt_sha256"]
        assert "mipmaps/generate=true" in Path(str(dst)+".import").read_text(encoding="utf-8")
        report["assets"].append({"id":job["id"],"runtime_sha256":digest(dst),**structure(Image.open(dst))})
    (HERE/"structural_validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    board=Image.new("RGB",(560,len(exports)*138),(222,231,233))
    draw=ImageDraw.Draw(board)
    for row,exp in enumerate(exports):
        pic=Image.open(ROOT/exp["runtime"].removeprefix("res://")).convert("RGBA")
        pic=pic.crop(tuple([exp["content_rect"][0],exp["content_rect"][1],exp["content_rect"][0]+exp["content_rect"][2],exp["content_rect"][1]+exp["content_rect"][3]]))
        pic.thumbnail((112,112))
        silhouette=Image.new("RGBA",pic.size,(0,0,0,255));silhouette.putalpha(pic.getchannel("A"))
        board.paste(pic,(200,row*138+12),pic)
        board.paste(silhouette,(390,row*138+12),silhouette)
        draw.text((10,row*138+52),exp["id"],fill="black")
    board.save(HERE/"review"/"object_112_silhouettes.png")
    captures=HERE/"review"/"candidate"
    files=sorted(captures.glob("*.png"))
    for group in range(0,len(files),6):
        sheet=Image.new("RGB",(1280,6//2*400),(27,39,54))
        draw=ImageDraw.Draw(sheet)
        for j,path in enumerate(files[group:group+6]):
            thumb=Image.open(path).convert("RGB")
            thumb.thumbnail((630,355))
            x=(j%2)*640;y=(j//2)*400
            sheet.paste(thumb,(x,y+30))
            draw.text((x+8,y+8),path.stem,fill="white")
        sheet.save(HERE/"review"/("sheet_%02d.jpg"%(group//6+1)),quality=90)
    print("RACER_VISUAL_STRUCTURE|ALL OK|assets=%d|negative_controls=%d|captures=%d"%(len(exports),len(controls),len(files)))
if __name__=="__main__":main()
