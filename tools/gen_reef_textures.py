#!/usr/bin/env python3
"""Generate original, seamless CC0 PBR detail textures for the reef:
   coral (polyp surface) and algae (sea-plant blades). 1024px, col+nrm+rgh.
   Authored procedurally -> license is ours / CC0."""
import numpy as np
from PIL import Image, ImageFilter

N = 1024
rng = np.random.default_rng(7)

def to_img(a):  # float[0..1] HxWxC or HxW -> uint8 image
    a = np.clip(a, 0, 1)
    if a.ndim == 2:
        return Image.fromarray((a*255).astype(np.uint8), "L")
    return Image.fromarray((a*255).astype(np.uint8), "RGB")

def height_to_normal(h, strength=2.5):
    # seamless gradient via np.roll
    gx = (np.roll(h,-1,1) - np.roll(h,1,1)) * strength
    gy = (np.roll(h,-1,0) - np.roll(h,1,0)) * strength
    nz = np.ones_like(h)
    nl = np.sqrt(gx*gx + gy*gy + nz*nz)
    nx, ny, nz = -gx/nl, -gy/nl, nz/nl
    # OpenGL normal map (Y up): R=x, G=y, B=z, mapped 0..1
    out = np.stack([nx*0.5+0.5, ny*0.5+0.5, nz*0.5+0.5], -1)
    return out

def fbm(scale, octaves=5, seed=0):
    r = np.random.default_rng(seed)
    acc = np.zeros((N,N)); amp=1.0; tot=0.0; s=scale
    for _ in range(octaves):
        # low-res white noise, tiled & smoothly upscaled => seamless
        g = r.integers(0, 256, size=(s, s)).astype(np.float32)/255.0
        img = Image.fromarray((g*255).astype(np.uint8)).resize((N,N), Image.BICUBIC)
        acc += amp*(np.asarray(img,dtype=np.float32)/255.0)
        tot += amp; amp*=0.5; s*=2
    return acc/tot

def seamless_voronoi(cells):
    """Return (f1 distance normalized, cell-id) — seamless via wrapped points."""
    pts = rng.random((cells*cells, 2))
    # jitter on a grid for even coverage
    gx, gy = np.meshgrid(np.arange(cells), np.arange(cells))
    base = np.stack([gx.ravel(), gy.ravel()], -1)/cells
    pts = (base + (rng.random((cells*cells,2))-0.5)*(0.9/cells)) % 1.0
    ys, xs = np.mgrid[0:N, 0:N].astype(np.float32)/N
    P = np.stack([xs, ys], -1).reshape(-1,2)
    f1 = np.full(P.shape[0], 1e9); idn = np.zeros(P.shape[0], np.int32)
    for i,(px,py) in enumerate(pts):
        dx = np.abs(P[:,0]-px); dx = np.minimum(dx, 1-dx)
        dy = np.abs(P[:,1]-py); dy = np.minimum(dy, 1-dy)
        d = dx*dx+dy*dy
        m = d<f1; f1=np.where(m,d,f1); idn=np.where(m,i,idn)
    return np.sqrt(f1).reshape(N,N), idn.reshape(N,N), pts

# ---------------- CORAL ----------------
def make_coral():
    d, idn, pts = seamless_voronoi(14)          # fewer, larger polyps
    dn = d/ (d.max())
    dome = np.clip(1.0 - dn*1.6, 0, 1)           # rounded polyp tops (denser fill)
    dome = dome**0.45                            # plump, rounded
    # central pore pit at each polyp top
    pore = np.clip((dome-0.86)/0.14, 0, 1)
    grain = fbm(64, 6, seed=11)                  # fine surface grain
    micro = fbm(256, 3, seed=21)
    h = dome*0.85 + grain*0.14 + micro*0.04
    h = h - pore*0.45                            # punch the pore pit
    h = np.clip(h,0,1)
    h_img = Image.fromarray((h*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))
    h = np.asarray(h_img,dtype=np.float32)/255.0

    # albedo: bright warm coral so per-species tint multiplies cleanly
    base = np.array([0.96, 0.90, 0.85])          # polyp tops (near-white warm)
    crev = np.array([0.66, 0.52, 0.58])          # soft mauve crevice (lighter)
    porec= np.array([0.98, 0.66, 0.62])          # coral-pink pore ring
    ao = np.clip(dome*1.1,0,1)[...,None]
    col = crev + (base-crev)*ao
    # pink ring around each pore
    ring = np.clip((dome-0.6)/0.22,0,1)*(1-pore)
    col = col*(1-0.32*ring[...,None]) + porec*0.32*ring[...,None]
    # gentle per-polyp hue variation
    cellrng = np.random.default_rng(99)
    tint = cellrng.random((pts.shape[0],3))*0.12+0.94
    col = col * tint[idn]
    col = np.clip(col,0,1)

    nrm = height_to_normal(h, strength=3.6)
    # roughness: matte coral, wet pore centres glossier
    rgh = np.clip(0.84 - ring*0.2 + (1-grain)*0.05, 0.42, 0.95)
    return to_img(col), to_img(nrm), to_img(rgh)

# ---------------- ALGAE / SEA PLANT ----------------
def make_algae():
    ys, xs = np.mgrid[0:N,0:N].astype(np.float32)/N
    # vertical blades: sine field in x, wobbling with low-freq noise in y
    wob = (fbm(16,4,seed=5)-0.5)*0.06
    blades = 26
    phase = (xs + wob)*blades*np.pi*2
    blade = (np.sin(phase)*0.5+0.5)                # 0..1 across blades
    blade = blade**1.6
    edge = np.clip((blade-0.18)/0.82,0,1)          # blade body vs gap
    # central vein per blade (where sin near +1)
    vein = np.clip((blade-0.82)/0.18,0,1)
    fibre = fbm(96,5,seed=8)                        # along-blade fibre
    h = edge*0.7 + vein*0.18 + fibre*0.12
    # vertical streak variation (some blades taller/darker)
    streak = fbm(32,3,seed=14)
    h = np.clip(h*(0.7+0.5*streak),0,1)
    h_img = Image.fromarray((h*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.5))
    h = np.asarray(h_img,dtype=np.float32)/255.0

    # albedo: mid sea-green/olive so tint shows; veins lighter, gaps dark
    leaf = np.array([0.40, 0.52, 0.34])
    veinc= np.array([0.62, 0.72, 0.46])
    gap  = np.array([0.10, 0.16, 0.14])
    col = gap + (leaf-gap)*edge[...,None]
    col = col*(1-vein[...,None]*0.6) + veinc*vein[...,None]*0.6
    col = col*(0.8+0.4*streak[...,None])
    col = np.clip(col*(0.92+0.16*fibre[...,None]),0,1)

    nrm = height_to_normal(h, strength=2.2)
    rgh = np.clip(0.9 - vein*0.15, 0.5, 0.97)
    return to_img(col), to_img(nrm), to_img(rgh)

out = "assets/terrain/"
for name, fn in [("up_coral", make_coral), ("up_algae", make_algae)]:
    c,n,r = fn()
    c.save(out+name+"_col.jpg", quality=92)
    n.save(out+name+"_nrm.jpg", quality=94)
    r.save(out+name+"_rgh.jpg", quality=90)
    print("wrote", name)

# previews (small, tiled 2x2 to check seam) for self-review
def tile_preview(path, tag):
    im = Image.open(path).resize((256,256))
    canv = Image.new("RGB",(512,512))
    for yy in range(2):
        for xx in range(2):
            canv.paste(im,(xx*256,yy*256))
    canv.save("/tmp/prev_"+tag+".png")
tile_preview(out+"up_coral_col.jpg","coral_col")
tile_preview(out+"up_coral_nrm.jpg","coral_nrm")
tile_preview(out+"up_algae_col.jpg","algae_col")
tile_preview(out+"up_algae_nrm.jpg","algae_nrm")
print("previews done")
