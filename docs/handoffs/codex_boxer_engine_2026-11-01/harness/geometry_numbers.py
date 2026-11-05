"""Numbers-only geometry for the Boxer at 22df5b75 (formulas copied from
scripts/opera_boxing_surface.gd). Prints physical sizes on the two target
devices, lane separation versus blocking reach, and counter retraction."""
import math

W, H = 1280.0, 720.0
MM = {"tablet (Lenovo Tab M11)": 0.1842, "phone (6.4in 2400x1080)": 0.0927}
GAIN = (2.4, 1.15)


def rest(h):
    return (W * (0.31 if h == 0 else 0.69), H * 0.84)


def incoming(p, side):
    o = (W * (0.43 if side == 0 else 0.57), H * 0.20)
    e = (W * (0.46 if side == 0 else 0.54), H * 0.86)
    return (o[0] + (e[0] - o[0]) * p, o[1] + (e[1] - o[1]) * p)


def r_fist(p):
    return 160.0 * (0.78 + p * 0.25) * 0.34


def depth(h, at, target):
    r = rest(h)
    route = (target[0] - r[0], target[1] - r[1])
    L = math.hypot(*route)
    d = ((at[0] - r[0]) * route[0] + (at[1] - r[1]) * route[1]) / (L * L)
    return min(1.0, max(0.0, d))


def r_glove(h, at, target):
    return 168.0 * (0.92 + depth(h, at, target) * 0.38) * 0.34


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


IMP_TARGET = (W * 0.5, H * 0.43)

print("SIZES (stage px -> mm)")
for name, mm in MM.items():
    print(f"  {name}: painted glove {168*0.92:.0f}-{168*1.30:.0f}px = {168*0.92*mm:.1f}-{168*1.30*mm:.1f} mm;"
          f" glove contact diameter {2*r_glove(0, rest(0), IMP_TARGET):.0f}-{2*168*1.30*0.34:.0f}px ="
          f" {2*r_glove(0, rest(0), IMP_TARGET)*mm:.1f}-{2*168*1.30*0.34*mm:.1f} mm;"
          f" fist contact diameter {2*r_fist(0):.0f}-{2*r_fist(1):.0f}px = {2*r_fist(0)*mm:.1f}-{2*r_fist(1)*mm:.1f} mm;"
          f" counter target radius 78/96/114px = {78*mm:.1f}/{96*mm:.1f}/{114*mm:.1f} mm; belt radius 56px = {56*mm:.1f} mm")

print("LANES (x at top/middle/bottom of flight)")
for p in (0.0, 0.5, 1.0):
    a, b = incoming(p, 0), incoming(p, 1)
    print(f"  p={p:.1f}: left x={a[0]:.0f} right x={b[0]:.0f} separation={b[0]-a[0]:.0f}px"
          f" (tablet {(b[0]-a[0])*0.1842:.1f} mm); fist radius {r_fist(p):.0f}px")


def blocks_both(at, h, target):
    best = []
    for side in (0, 1):
        g = min(dist(at, incoming(k / 400.0, side)) - (r_glove(h, at, target) + r_fist(k / 400.0))
                for k in range(401))
        best.append(g)
    return best[0] <= 0 and best[1] <= 0


print("CENTRE PARKING: glove centred on x=640 blocks both lanes at these heights (imp target):")
print("  " + " ".join(f"y{y}={'yes' if blocks_both((640.0, y), 0, IMP_TARGET) else 'no'}" for y in range(150, 700, 50)))


def sep_needed():
    # Smallest symmetric bottom/top lane offset from centre where no single
    # glove position can block both lanes (uses max glove radius 74 px).
    rg = 168.0 * 1.30 * 0.34
    for half in range(40, 400, 2):
        # worst case: glove midway between the lanes at the same height
        rf = r_fist(1.0)
        if half > rg + rf:
            return half, rg, rf
    return None


half, rg, rf = sep_needed()
print(f"LANE SPACING NEEDED: each lane at least {half}px from the centre line (separation >= {2*half}px,"
      f" {2*half/W:.2f} of stage width; tablet {2*half*0.1842:.0f} mm, phone {2*half*0.0927:.0f} mm)"
      f" so one max-size glove ({rg:.0f}px) cannot touch both fists ({rf:.0f}px). Current: 64-90px from centre.")

print("COUNTER RETRACTION (imp open; ready when glove is farther than target r + glove r + 24px)")
for assist, tr in ((0, 78), (2, 114)):
    for p in (0.2, 0.4, 0.6, 0.8):
        g = incoming(p, 0)
        need = tr + r_glove(0, g, IMP_TARGET) + 24.0
        d = dist(g, IMP_TARGET)
        back = max(0.0, need - d)
        print(f"  assist {assist}: glove blocked at left-lane p={p:.1f} ({g[0]:.0f},{g[1]:.0f}) is {d:.0f}px from target;"
              f" must pull back {back:.0f}px first (tablet {back*0.1842:.0f} mm, phone thumb ~{back/GAIN[1]*0.0927:.0f}-{back/GAIN[0]*0.0927:.0f} mm)")

print("TRAVEL (glove px; tablet finger mm = glove mm; phone thumb mm = glove/gain)")
moves = {
    "rest->left lane middle (p=0.5)": (rest(0), incoming(0.5, 0)),
    "rest->imp counter target": (rest(0), IMP_TARGET),
    "rest->far jab pad (0.54,0.34)": (rest(0), (W * 0.54, H * 0.34)),
    "left lane p=0.5 -> right lane p=0.5": (incoming(0.5, 0), incoming(0.5, 1)),
    "jab re-arm: pad -> within 110px of rest": ((W * 0.43, H * 0.32), None),
}
for name, (a, b) in moves.items():
    if b is None:
        d = dist(a, rest(0)) - 110.0
        dx, dy = abs(a[0] - rest(0)[0]), abs(a[1] - rest(0)[1])
    else:
        d = dist(a, b)
        dx, dy = abs(b[0] - a[0]), abs(b[1] - a[1])
    thumb = math.hypot(dx / GAIN[0], dy / GAIN[1]) * 0.0927 * (d / max(1.0, math.hypot(dx, dy)))
    print(f"  {name}: {d:.0f}px; tablet {d*0.1842:.0f} mm; phone thumb {thumb:.0f} mm")

print("TIME BUDGET (Title Imp, seconds from windup start to fist arrival): 2.05 normal, 2.50 assisted")
for label, rt, speed in (("quick", 0.60, 180), ("typical", 0.76, 120), ("slow", 1.10, 80)):
    mm = dist(rest(0), incoming(0.5, 0)) * 0.1842
    t = rt + 0.08 + 0.15 + mm / speed
    print(f"  {label}: react {rt:.2f}s + choose 0.08s + reach {0.15 + mm/speed:.2f}s to mid-lane = {t:.2f}s"
          f"")
print("COUNTER WINDOW BUDGET: 1.70 s normal, 2.20 s assisted")
for label, rt, speed in (("quick", 0.60, 180), ("typical", 0.76, 120), ("slow", 1.10, 80)):
    punch_mm = 130 * 0.1842
    retract_mm = 60 * 0.1842
    direct = rt + 0.15 + punch_mm / speed
    with_retract = direct + 0.15 + retract_mm / speed
    print(f"  {label}: direct punch {direct:.2f}s; with a pull-back first {with_retract:.2f}s")
