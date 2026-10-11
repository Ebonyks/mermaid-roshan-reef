"""Read-only native raster inspection; writes JSON evidence, never image pixels."""
from pathlib import Path
import hashlib, json, math
import argparse
import numpy as np
from PIL import Image

parser=argparse.ArgumentParser();parser.add_argument('--draft',default='full_wave_draft_05');args=parser.parse_args()
base=Path(__file__).resolve().parent / args.draft
assert base.resolve().parent==Path(__file__).resolve().parent,'Draft must be a direct child study folder'
record=json.loads((base/"joint_geometry.json").read_text(encoding="utf-8-sig"))
profile=json.loads((base/"recipe_profile.json").read_text(encoding="utf-8-sig"))
relaxed_refined='relaxed_outline' in profile
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def unit(p):
    p=np.asarray(p,float);return p/np.linalg.norm(p)
def xy(p):return [round(float(z),3) for z in p]
def skin(c):
    r,g,b=map(int,c[:3]);return r>=244 and 180<=g<=243 and 120<=b<=226 and g-b>=13
def center(im,target,direction):
    n=np.array([-direction[1],direction[0]])
    hits=[]
    for q in np.arange(-21,21.01,.25):
        p=target+n*q;x,y=np.floor(p).astype(int)
        if 0<=x<im.shape[1] and 0<=y<im.shape[0] and skin(im[y,x]):hits.append(q)
    if not hits:return None
    # A contiguous transverse skin run nearest the proposed segment center.
    runs=[];run=[hits[0]]
    for z in hits[1:]:
        if z-run[-1]>.26:runs.append(run);run=[]
        run.append(z)
    runs.append(run);run=min(runs,key=lambda a:min(abs(z) for z in a))
    if min(abs(z) for z in run)>4:return None
    return target+n*(run[0]+run[-1])/2
def line(points,d):
    points=np.asarray(points);mean=points.mean(axis=0)
    _,_,v=np.linalg.svd(points-mean);axis=v[0]
    if axis@d<0:axis=-axis
    return mean,axis
def intersect(a,da,b,db):
    mat=np.column_stack([da,-db])
    if abs(np.linalg.det(mat))<.04:return None
    return a+da*np.linalg.solve(mat,b-a)[0]

frames=[];minmargin=1e9
for f in record["frames"]:
    n=f["source_index"];p=base/f"{n:04d}.png";im=np.array(Image.open(p).convert("RGB"))
    out={"frame":n,"native_sha256":sha(p),"painted":f["painted"]}
    if not f["painted"]:
        out["status"]="SOURCE_RGB_ENDPOINT_REPLACED_BY_WHOLE_APPROVED_K0_IN_FINAL_DERIVATIVE"
        frames.append(out);continue
    S,E,W=np.array(f["shoulder"]),np.array(f["elbow"]),np.array(f["wrist"])
    du,df=unit(E-S),unit(W-E);ang=math.radians(f["angles"]["hand"])
    dh=np.array([math.cos(ang),math.sin(ang)]);nh=np.array([-dh[1],dh[0]])
    upper=[center(im,S+(E-S)*t,du) for t in (.35,.5,.65)]
    fore=[center(im,E+(W-E)*t,df) for t in (.3,.5,.7)]
    valid=all(p is not None for p in upper+fore)
    elbow=None
    if valid:
        a,da=line(upper,du);b,db=line(fore,df);elbow=intersect(a,da,b,db)
    wrist=center(im,W,df)
    reach=f["analytic_lengths"]["hand_target"]
    tips=[];hand=[]
    for y in range(max(0,int(W[1]-105)),min(im.shape[0],int(W[1]+106))):
        for x in range(max(0,int(W[0]-105)),min(im.shape[1],int(W[0]+106))):
            delta=np.array([x+.5,y+.5])-W;s=float(delta@dh);u=float(delta@nh)
            c=im[y,x];r,g,b=map(int,c)
            gray=im[y,4].astype(int)
            colored=(max(abs(c.astype(int)-gray))>=30 and max(r,g,b)-min(r,g,b)>=10)
            if colored and -.5<=s<=reach+10 and abs(u)<=45:
                hand.append((x,y));minmargin=min(minmargin,x,y,im.shape[1]-1-x,im.shape[0]-1-y)
                if abs(u)<=6 and reach-11<=s<=reach+10:tips.append((s,x+.5,y+.5))
    tip=None
    if tips:
        furthest=max(a[0] for a in tips)
        tip=np.mean([[x,y] for s,x,y in tips if furthest-s<=.6],axis=0)
    out.update({
        "authored_shoulder":xy(S),"shoulder_observation":"hidden under retained frill; authored center, not falsely reclassified as measured",
        "raster_upper_cross_section_centers":[xy(p) if p is not None else None for p in upper],
        "raster_fore_cross_section_centers":[xy(p) if p is not None else None for p in fore],
        "raster_elbow_axis_intersection":xy(elbow) if elbow is not None else None,
        "raster_wrist_cross_section_center":xy(wrist) if wrist is not None else None,
        "raster_longest_tip":xy(tip) if tip is not None else None,
        "hand_open":f["hand_open"],"hand_openness":f["hand_openness"],
        "nominal_authored_w3_cell":{"upper":25.0625,"fore":25.0625,"open_hand":65.651*.3125},
        "elbow_observed_vs_target_native_px":round(float(np.linalg.norm(elbow-E)),3) if elbow is not None else None,
        "wrist_observed_vs_target_native_px":round(float(np.linalg.norm(wrist-W)),3) if wrist is not None else None,
        "observed_tip_from_observed_wrist_cell":round(float(np.linalg.norm(tip-wrist))*.3125,3) if wrist is not None and tip is not None else None,
        "hand_raster_bounds_native":[min(x for x,y in hand),min(y for x,y in hand),max(x for x,y in hand),max(y for x,y in hand)] if hand else None,
        "measurement_uncertainty_native_px":{"shoulder":4,"elbow":2,"wrist":1.5,"tip":1.5},
        "status":"MODEL_VISUAL_AND_READ_ONLY_RASTER_EVIDENCE; FINAL_RGBA_REVIEW_PENDING",
    })
    frames.append(out)
result={"schema":"reef.native-painted-raster-observation.v1","source_master_sha256":sha(base/"wave_native_rgb.aseprite"),
    "authored_geometry_sha256":sha(base/"joint_geometry.json"),"review_type":"model observation plus read-only raster measurement; not human acceptance",
    "method":"Pillow/NumPy read-only native RGB; skin transverse centers, fitted segment-axis elbow intersection, middle-fingertip color envelope; no image pixels written",
    "scope":"39 painted complete native cels; RGB endpoints belong to original source and are separately replaced as whole drawings in final derivative",
    "minimum_hand_pixel_canvas_margin_native":minmargin,"canvas":[768,896],"whole_mapping_scale":.3125,
    "visual_sequence_review":{"contact_sheets":"review/native_arm_contact_00_07.png through40_40.png; rows left-to-right, then top-to-bottom",
        "complete_hand_contours":"All39 painted cels viewed in ordered native crop contacts; four unequal fingers/opposed thumb connected, no cropped fingertip or lowering-hand smear found",
        "attachments":("Connected arm/frill boundary; earlier cuff rectangle and bodice-side warm old-arm strip removed. Tiny original native curl antialiasing is separate from that rejected strip." if profile.get('erase_preserved_old_skin') else "Connected arm enters native frill; cuff and body-side remnants require independent native review."),
        "style_limitation":("Fresh contour is cleaner than original opposite arm; filled shallow-valley relaxed fingers with warmer lighter contour remove the prior comb defect in ordered native review; final256/full-speed style review remains pending" if relaxed_refined else "Fresh contour is cleaner than original opposite arm; narrow relaxed fingers have darker graphic outlines than K0; final256/full-speed style review remains pending"),
        "motion_limitation":"Frame-step order inspected; no normal-speed delivery playback claimed here"},"frames":frames,"human_acceptance":False}
(base/"native_raster_geometry_observation.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8",newline="\n")
open_lengths=[f["observed_tip_from_observed_wrist_cell"] for f in frames if f.get("hand_open") and f.get("observed_tip_from_observed_wrist_cell")]
print(json.dumps({"frames":len(frames),"hand_margin_native":minmargin,"open_hand_cell_range":[min(open_lengths),max(open_lengths)],
    "elbow_fit_missing":[f["frame"] for f in frames if f.get("painted") and f.get("raster_elbow_axis_intersection") is None],
    "output":str(base/"native_raster_geometry_observation.json")}))
