"""Hook geometry check (numbers only): quadratic hook paths from the side to a
side pad versus a centre-parked glove and a straight jab, using the engine's
radius formulas at 1280x720 (scripts/opera_boxing_surface.gd at 22df5b75)."""
import math
W, H = 1280.0, 720.0
def bez(p0, c, p1, t):
    return ((1-t)**2*p0[0] + 2*(1-t)*t*c[0] + t*t*p1[0], (1-t)**2*p0[1] + 2*(1-t)*t*c[1] + t*t*p1[1])
def r_fist(t): return 160.0*(0.78 + 0.25*t)*0.34
RG_MAX = 168.0*1.30*0.34
hook_L = ((0.30*W, 0.26*H), (0.10*W, 0.50*H), (0.37*W, 0.80*H))   # from Roshan's left side to her left pad
hook_R = tuple((W - p[0], p[1]) for p in hook_L)
jab = ((0.50*W, 0.22*H), (0.50*W, 0.50*H), (0.50*W, 0.80*H))      # straight to the chest emblem
def min_gap(glove, path):
    return min(math.dist(glove, bez(*path, k/400)) - (RG_MAX + r_fist(k/400)) for k in range(401))
centre = (0.50*W, 0.62*H)
side = (0.33*W, 0.62*H)
print("centre-parked glove (640,446): hook-left gap %.0f px, hook-right gap %.0f px, jab gap %.0f px" % (
    min_gap(centre, hook_L), min_gap(centre, hook_R), min_gap(centre, jab)))
print("left-side glove (422,446): hook-left gap %.0f px, jab gap %.0f px, hook-right gap %.0f px" % (
    min_gap(side, hook_L), min_gap(side, jab), min_gap(side, hook_R)))
L = sum(math.dist(bez(*hook_L, k/200), bez(*hook_L, (k+1)/200)) for k in range(200))
print("hook arc length %.0f px vs jab %.0f px; at the jab's 528 px/s the hook needs %.2f s" % (L, 0.58*H, L/528))
for name, mm in (("tablet", 0.1842), ("phone", 0.0927)):
    print(f"{name}: hook end pad is {0.13*W*mm:.0f} mm beside the chest emblem")
