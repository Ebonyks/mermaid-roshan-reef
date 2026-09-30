#!/usr/bin/env python3
"""Review-only before/after composites for the castle door highlight rewrite.

Composites, at the 1280x720 stage scale, (a) a replica of today's
scripts/castle_door_cue.gd drawing (dev e7899cc0) and (b) the proposed Door
Guidance v2 concept, over the approved Main Hall master, hall door signs,
Moonflower dormant card and Royal Hall mist wisps. Deterministic; needs Pillow
and numpy; run from the repo root after measure_hall_door_geometry.py:

    python3 audit/door_highlight_rewrite_2026-09-30/render_review_mocks.py

PIL approximation only: antialiasing, blending and exact runtime layering
differ from Godot. These images are design intent, never runtime evidence
(DL-QA-03); Codex must capture the real Mobile-renderer frames.
"""
import math, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from pathlib import Path
REPO=str(Path(__file__).resolve().parents[2])+"/"
S=str(Path(__file__).resolve().parent)+"/"
nat_img=Image.new("RGB",(7280,2048))
for _r in range(2):
    for _c in range(8):
        nat_img.paste(Image.open(REPO+f"assets/flats/castle/main_hall_redraw_2026-08-03/tiles/main_hall_room_led_r{_r}_c{_c}.png").convert("RGB"),(_c*910,_r*1024))
nat=np.asarray(nat_img).astype(np.int32)
K=7280/3344.0; KY=2048/941.0; SC=1280.0/1672.0; N2S=1280.0/3640.0
stage_full=nat_img.resize((2560,720),Image.LANCZOS).convert("RGBA")
PORTALS={
 "family_gallery":(210,300,160,305),"library":(380,300,160,305),"kitchen":(545,300,160,305),
 "opera_hall":(875,180,300,425),"playroom":(1940,300,160,305),"craft_room":(2140,300,160,305),
 "mermaid_pool":(2340,300,160,305),"bubble_bath":(2540,300,160,305),"__royal_hall":(2870,150,350,470)}
SIGNS={"family_gallery":((290,340),1.0),"opera_hall":((1025,225),1.55),"library":((455,340),1.0),
 "kitchen":((620,340),1.0),"playroom":((2015,340),1.0),"craft_room":((2215,340),1.0),
 "mermaid_pool":((2415,340),1.0),"bubble_bath":((2615,340),1.0)}
FOOT={k:(v[0]+v[2]/2, 620.0) for k,v in PORTALS.items()}; FOOT["__royal_hall"]=(3045.0,620.0)
R,G,B=nat[...,0],nat[...,1],nat[...,2]; lum=0.299*R+0.587*G+0.114*B
warm=((R-B)>8)&(lum>120)
def run_edge(row,start,step,limit,want,minrun=4):
    cnt=0
    for i in range(limit):
        xx=start+step*i
        if xx<0 or xx>=row.shape[0]: return None
        if row[xx]==want:
            cnt+=1
            if cnt>=minrun: return xx-step*(minrun-1)
        else: cnt=0
    return None
from collections import deque
def door_masks(pid):
    x,y,w,h=PORTALS[pid]; floor_y = 470.0 if pid=="__royal_hall" else 598.0
    cxn=int((x+w/2)*K); y0=int(y*KY); y1=int(floor_y*KY)
    x0=int((x-12)*K); x1=int((x+w+12)*K); yt=int((y-8)*KY)
    opening=np.zeros((y1-yt, x1-x0),bool)
    first=None
    for yy in range(y0,y1):
        row=warm[yy]
        if row[cxn]: continue
        l=run_edge(row,cxn,-1,int(w*K*0.7),True); r=run_edge(row,cxn,1,int(w*K*0.7),True)
        if l is None or r is None: continue
        opening[yy-yt, max(0,l+1-x0):min(x1-x0,r-x0)]=True
        if first is None: first=(yy,l)
    # silhouette: flood warm pixels from frame just left of opening at mid height
    sub=warm[yt:y1, x0:x1].copy()
    my=int(((y0+y1)//2)); row=warm[my]; l=run_edge(row,cxn,-1,int(w*K*0.7),True)
    seed=(my-yt, l-x0-3)
    sil=np.zeros_like(sub); q=deque([seed]); sil[seed]=True
    while q:
        a,b=q.popleft()
        for da,db in((1,0),(-1,0),(0,1),(0,-1)):
            na,nb=a+da,b+db
            if 0<=na<sub.shape[0] and 0<=nb<sub.shape[1] and sub[na,nb] and not sil[na,nb]:
                sil[na,nb]=True; q.append((na,nb))
    # keep the silhouette within the frame's own column band to avoid balustrade bleed
    return (x0,yt), opening, sil
def to_stage_mask(origin, m, blur=0.0):
    im=Image.fromarray((m*255).astype(np.uint8),"L")
    sw=max(1,int(round(im.width*N2S))); sh=max(1,int(round(im.height*N2S)))
    im=im.resize((sw,sh),Image.LANCZOS)
    if blur: im=im.filter(ImageFilter.GaussianBlur(blur))
    return (origin[0]*N2S, origin[1]*N2S), im
MASKS={pid:door_masks(pid) for pid in PORTALS}
def paste_rgba(dst, src, pos):
    dst.alpha_composite(src,(int(round(pos[0])),int(round(pos[1]))))
def gradient_fill(mask, top_rgba, bot_rgba):
    w,h=mask.size; g=Image.new("RGBA",(w,h))
    px=g.load()
    for j in range(h):
        t=j/max(1,h-1)
        c=tuple(int(top_rgba[i]*(1-t)+bot_rgba[i]*t) for i in range(4))
        for i in range(w): px[i,j]=c
    a=ImageChops.multiply(g.split()[3], mask)
    g.putalpha(a); return g
def star(draw_img, center, r, fill=(255,214,77,255), key=(92,50,115,255), key_w=4):
    cx,cy=center; pts=[]
    for i in range(10):
        a=-math.pi/2+i*math.pi/5; rr=r if i%2==0 else r*0.45
        pts.append((cx+math.cos(a)*rr, cy+math.sin(a)*rr))
    glow=Image.new("RGBA",draw_img.size,(0,0,0,0)); gd=ImageDraw.Draw(glow)
    gd.ellipse([cx-r*1.9,cy-r*1.9,cx+r*1.9,cy+r*1.9],fill=(255,226,140,120))
    draw_img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(r*0.7)))
    d=ImageDraw.Draw(draw_img)
    d.polygon(pts, fill=fill, outline=key, width=key_w)
    hl=[(cx-r*0.18,cy-r*0.55),(cx-r*0.02,cy-r*0.62),(cx-r*0.12,cy-r*0.25)]
    d.polygon(hl, fill=(255,250,225,230))
def base_view(view_left, fairy=True):
    ox=view_left*SC
    fr=stage_full.crop((int(round(ox)),0,int(round(ox))+1280,720)).copy()
    return fr, ox
def add_world_cards(fr, ox, fairy=True, mist=True, royal_event=False):
    if fairy:
        fc=Image.open(REPO+"assets/flats/castle/fairy_conservatory/moonflower_door_closed.png").convert("RGBA")
        s=int(round(1024*0.4896*SC)); fc=fc.resize((s,s),Image.LANCZOS)
        paste_rgba(fr, fc, (1672*SC-ox-s/2, 385*SC-s/2))
    for pid,(pos,scale) in SIGNS.items():
        sg=Image.open(REPO+"assets/flats/castle/main_hall_redraw_2026-08-03/signs/sign_"+pid+".png").convert("RGBA")
        sz=int(round(256*scale*SC)); sg=sg.resize((sz,sz),Image.LANCZOS)
        paste_rgba(fr, sg, (pos[0]*SC-ox-sz/2, pos[1]*SC-sz/2))
    if mist and not royal_event:
        wisp=Image.open(REPO+"assets/sprites/sky_lagoon/sky_lagoon_smoke_wisp_v2.png").convert("RGBA")
        for (px,py,sc_,al,fl) in [(2935,385,1.38,.22,0),(2990,365,1.55,.27,1),(3045,405,1.62,.30,0),(3100,370,1.48,.26,1),(3155,400,1.32,.21,0)]:
            wi=wisp.resize((int(46*sc_*SC),int(256*sc_*SC)),Image.LANCZOS)
            if fl: wi=wi.transpose(Image.FLIP_LEFT_RIGHT)
            r_,g_,b_,a_=wi.split(); a_=a_.point(lambda v:int(v*al*0.46/0.46)); 
            wi=Image.merge("RGBA",(r_.point(lambda v:int(v*.92)),g_.point(lambda v:int(v*.88)),b_,a_))
            paste_rgba(fr, wi, (px*SC-ox-wi.width/2, py*SC-wi.height/2))
# ---------- current cue (from sim_before, same math as castle_door_cue.gd) ----------
def arch_points(w,h,inset,seg=24):
    left=inset; right=max(left+1,w-inset); bottom=max(inset+1,h-inset)
    cy=h*0.34; rx=max(1,(right-left)*0.5); ry=min(max(1,h*0.20),max(1,cy-inset))
    pts=[(left,bottom),(left,cy)]
    for i in range(seg+1):
        a=math.pi+math.pi*i/seg; pts.append((w*0.5+math.cos(a)*rx, cy+math.sin(a)*ry))
    pts.append((right,bottom)); return pts
def rgba(c,a): return (int(c[0]*255),int(c[1]*255),int(c[2]*255),int(max(0,min(1,a))*255))
def current_cue(fr, ox, pid, state, t=1.3):
    x,y,w,h=PORTALS[pid]; r=(x*SC-ox,y*SC,w*SC,h*SC)
    l=max(0,r[0]); tp=max(0,r[1]); rr=min(1280,r[0]+r[2]); b=min(720,r[1]+r[3])
    if rr-l<2 or b-tp<2: return
    W,H=rr-l,b-tp; cue=Image.new("RGBA",(int(math.ceil(W)),int(math.ceil(H))),(0,0,0,0)); d=ImageDraw.Draw(cue)
    if state=="plot":
        pulse=0.5+0.5*math.sin(t*2*math.pi/3.2)
        d.line(arch_points(W,H,4.0), fill=rgba((1,.72,.16),.18+pulse*.16), width=int(round(5+pulse*2)), joint="curve")
        d.line(arch_points(W,H,8.0), fill=rgba((1,.84,.34),.86+pulse*.10), width=3, joint="curve")
        prog=(t/4.6)%1.0; sx=-W*0.45+(W*1.8)*prog; bw=max(1.5,W*0.008)
        for i,c in enumerate([(1,.36,.44),(1,.66,.24),(1,.88,.34),(.42,.88,.62),(.34,.72,1),(.66,.48,1)]):
            st=(sx+i*bw,H-4); d.line([st,(st[0]+W*0.34,4)], fill=rgba(c,.28), width=max(1,int(round(bw))))
        sc_=(W*.5, max(16.0,16+math.sin(t*2*math.pi/3.6)*1.5)); rad=8.5+pulse*1.5; pts=[]
        for i in range(8):
            a=-math.pi*.5+i*2*math.pi/8; q=rad if i%2==0 else rad*.38; pts.append((sc_[0]+math.cos(a)*q, sc_[1]+math.sin(a)*q))
        d.polygon(pts, fill=rgba((1,.9,.44),.98))
    elif state=="blocked":
        d.rectangle([0,0,W,H], fill=rgba((.07,.05,.15),.16))
        for i in range(5):
            ph=t*(.34+i*.025)+i*1.37; cx=((W*(.12+i*.22)+math.sin(ph)*W*.10)%W); cy=H*(.22+(i%3)*.27)+math.cos(ph*.71)*H*.06
            rad=max(18.0,min(W,H)*(.18+(i%2)*.05)); ex=rad*1.75; ey=rad*.52
            blob=Image.new("RGBA",cue.size,(0,0,0,0)); ImageDraw.Draw(blob).ellipse([cx-ex,cy-ey,cx+ex,cy+ey],fill=rgba((.52,.52,.72),.22)); cue.alpha_composite(blob)
        d.line(arch_points(W,H,3.0), fill=rgba((.34,.31,.52),.35), width=2, joint="curve")
    paste_rgba(fr, cue, (l,tp))
# ---------- proposed v2 ----------
def v2_plot(fr, ox, pid, shimmer_phase=0.04):
    origin, opening, sil = MASKS[pid]
    (sx,sy), om = to_stage_mask(origin, opening, blur=0.8)
    pos=(sx-ox, sy)
    # L1 doorway light
    glow=gradient_fill(om,(255,190,70,120),(255,238,170,215))
    paste_rgba(fr, glow, pos)
    # L2 outer halo ring (outside the painted frame+crest silhouette)
    (hx,hy), sm = to_stage_mask(origin, sil|opening)
    pad=26; big=Image.new("L",(sm.width+2*pad, sm.height+2*pad),0); big.paste(sm,(pad,pad))
    dil=big.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(6))
    ring=ImageChops.subtract(dil, big.filter(ImageFilter.MaxFilter(3)))
    halo=Image.new("RGBA",big.size,(255,200,80,0)); halo.putalpha(ring.point(lambda v:int(min(255,v*1.25))))
    # rainbow shimmer segment on the upper-left arc
    hw,hh=big.size; cx0,cy0=hw/2, hh*0.30
    rb=[(255,94,112),(255,168,62),(255,224,86),(108,224,158),(88,184,255),(168,122,255)]
    arr=np.array(halo); aa=arr[...,3].astype(float)
    ys,xs=np.nonzero(aa>0)
    for yy,xx in zip(ys,xs):
        ang=(math.atan2(yy-cy0, xx-cx0)+math.pi)/(2*math.pi)  # 0..1
        u=(ang-shimmer_phase)%1.0
        if u<0.30:
            c=rb[min(5,int(u/0.30*6))]; arr[yy,xx,0:3]=c
    halo=Image.fromarray(arr,"RGBA")
    paste_rgba(fr, halo, (hx-ox-pad, hy-pad))
    # L5 threshold light pool
    fx,fy=FOOT[pid]; tl=Image.new("RGBA",(220,80),(0,0,0,0)); ImageDraw.Draw(tl).ellipse([30,26,190,54],fill=(255,226,150,120))
    paste_rgba(fr, tl.filter(ImageFilter.GaussianBlur(7)), (fx*SC-ox-110, 603*SC-40))
def v2_resting(fr, ox, pid):
    origin, opening, sil = MASKS[pid]
    (sx,sy), om = to_stage_mask(origin, opening, blur=0.8)
    mist=gradient_fill(om,(150,142,190,92),(186,180,220,128))
    paste_rgba(fr, mist, (sx-ox, sy))
    # static fog bank at the threshold
    w,h=om.size; fog=Image.new("RGBA",(w+40,70),(0,0,0,0)); fd=ImageDraw.Draw(fog)
    for (cx,cy,r) in [(0.22,38,20),(0.5,34,25),(0.78,39,20),(0.36,46,16),(0.64,47,16)]:
        fd.ellipse([20+w*cx-r*0.8,cy-r*0.55,20+w*cx+r*0.8,cy+r*0.55],fill=(196,190,226,150))
    paste_rgba(fr, fog.filter(ImageFilter.GaussianBlur(3)), (sx-ox-20, sy+h-50))
def dormant_fog(fr, ox):
    fog=Image.new("RGBA",(330,80),(0,0,0,0)); fd=ImageDraw.Draw(fog)
    for (cx,cy,r) in [(60,44,26),(120,38,32),(185,40,34),(250,44,27),(95,52,20),(215,53,20)]:
        fd.ellipse([cx-r,cy-r*0.55,cx+r,cy+r*0.55],fill=(196,190,226,150))
    paste_rgba(fr, fog.filter(ImageFilter.GaussianBlur(3)), (1672*SC-ox-165, 620*SC-58))
def v2_star_over(fr, ox, pid):
    pos,scale=SIGNS.get(pid,((FOOT[pid][0],230),1.0))
    top = pos[1]*SC - 44*scale if pid in SIGNS else 150*SC
    star(fr,(pos[0]*SC-ox, top-30), 28)
def edge_beacon(fr, side, y=300, sign_pid=None):
    x = 1280-92 if side=="right" else 92
    lay=Image.new("RGBA",fr.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
    d.ellipse([x-66,y-66,x+66,y+66],fill=(255,222,140,110))
    fr.alpha_composite(lay.filter(ImageFilter.GaussianBlur(12)))
    d=ImageDraw.Draw(fr)
    d.ellipse([x-50,y-50,x+50,y+50],fill=(253,246,232,255),outline=(92,50,115,255),width=5)
    d.ellipse([x-42,y-42,x+42,y+42],outline=(255,196,64,255),width=5)
    ax = x+62 if side=="right" else x-62; s=1 if side=="right" else -1
    d.polygon([(ax+s*22,y),(ax-s*6,y-24),(ax-s*6,y+24)],fill=(255,206,77,255),outline=(92,50,115,255),width=4)
    if sign_pid:
        sg=Image.open(REPO+"assets/flats/castle/main_hall_redraw_2026-08-03/signs/sign_"+sign_pid+".png").convert("RGBA").crop((64,64,192,192)).resize((74,74),Image.LANCZOS)
        fr.alpha_composite(sg,(x-37,y-37))
        star(fr,(x+30,y-34),13,key_w=3)
    else:
        star(fr,(x,y),26)
def save(fr,name): fr.convert("RGB").save(S+name, quality=88)
def squint(fr): 
    s=fr.convert("RGB").resize((320,180),Image.BILINEAR).resize((640,360),Image.NEAREST); return s
# Scene A: Day One beat 1 (Bubble Bath plot) at dev spawn camera (view_left 1179)
VL=1179.0
states_A={"playroom":"blocked","craft_room":"blocked","mermaid_pool":"blocked","bubble_bath":"plot"}
fr,ox=base_view(VL); add_world_cards(fr,ox)
for pid,st in states_A.items(): current_cue(fr,ox,pid,st)
current_cue(fr,ox,"__royal_hall","blocked")
save(fr,"current_day_one_bubble_bath_entry.jpg"); _sq_before=squint(fr)
fr,ox=base_view(VL)
for pid,st in states_A.items():
    (v2_plot if st=="plot" else v2_resting)(fr,ox,pid)
add_world_cards(fr,ox)   # signs/mist/fairy above the door light (z order: light 5 < signs 68)
dormant_fog(fr,ox)
v2_star_over(fr,ox,"bubble_bath")
save(fr,"concept_day_one_bubble_bath_entry.jpg"); _sq_after=squint(fr)
_pair=Image.new("RGB",(_sq_before.width*2+12,_sq_before.height),(20,20,30)); _pair.paste(_sq_before,(0,0)); _pair.paste(_sq_after,(_sq_before.width+12,0)); _pair.save(S+"squint_quarter_scale_current_vs_concept.jpg", quality=90)
# Scene B: free play entry, Royal Hall story event armed, camera at left
fr,ox=base_view(0.0); add_world_cards(fr,ox,royal_event=True); save(fr,"current_free_play_royal_event_entry.jpg")
fr,ox=base_view(0.0); add_world_cards(fr,ox,royal_event=True); edge_beacon(fr,"right"); save(fr,"concept_free_play_royal_event_entry.jpg")
# Scene C: Day One, child wandered left while Mermaid Pool is the plot door (view_left 0)
fr,ox=base_view(0.0); 
for pid in ["family_gallery","library","opera_hall"]: current_cue(fr,ox,pid,"blocked")
add_world_cards(fr,ox); save(fr,"current_day_one_wandered_left.jpg")
fr,ox=base_view(0.0)
for pid in ["family_gallery","library","opera_hall"]: v2_resting(fr,ox,pid)
add_world_cards(fr,ox); edge_beacon(fr,"right",sign_pid="mermaid_pool"); save(fr,"concept_day_one_wandered_left.jpg")
print("wrote review composites to", S)
