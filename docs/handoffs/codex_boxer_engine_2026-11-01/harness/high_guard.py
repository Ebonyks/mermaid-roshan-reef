"""Which guard positions in the Title Imp lanes register as a punch on the imp's
closed guard (formulas from scripts/opera_boxing_surface.gd at 22df5b75)."""
import math
exec(open("geometry_numbers.py").read().split('print("SIZES')[0])

def seg_hits_disc(a0, a1, h, target, tr, steps=400):
    for k in range(steps + 1):
        t = k / steps
        p = (a0[0] + (a1[0]-a0[0])*t, a0[1] + (a1[1]-a0[1])*t)
        if dist(p, target) <= tr + r_glove(h, p, target):
            return True
    return False

def registers(h, start, end, target, tr):
    route = (target[0]-start[0], target[1]-start[1])
    L = math.hypot(*route); d = (route[0]/L, route[1]/L)
    forward = (end[0]-start[0])*d[0] + (end[1]-start[1])*d[1]
    if forward <= 0.01 or forward < 40.0:
        return False
    f = 40.0 / forward
    s = (start[0] + (end[0]-start[0])*f, start[1] + (end[1]-start[1])*f)
    return seg_hits_disc(s, end, h, target, tr)

for side, h in ((0, 0), (1, 1)):
    row = []
    for tr, label in ((78, "assist0"), (114, "assist2")):
        hits = [p/20 for p in range(0, 21) if registers(h, rest(h), incoming(p/20, side), IMP_TARGET, tr)]
        row.append(f"{label}: guard at lane p<={max(hits):.2f} counts as a punch" if hits else f"{label}: none")
    print(f"{'left' if side == 0 else 'right'} lane, own glove from rest:", "; ".join(row))
