"""futly v3: slanted kinked bars and a matching oblique wordmark.

Shapes are drawn upright as right-angled polygons, their corners rounded with
cubic quarter-circles, then skewed. Skewing the control points keeps the
curves exact, so the files carry no transforms.
"""
import math, os, random, sys
from shapely.geometry import box
from shapely.ops import unary_union

OUT = sys.argv[1] if len(sys.argv) > 1 else 'brand-v3'
SKEW = 30                         # degrees; the bars lean right
K = 0.5523                        # cubic quarter-circle constant

def f2(v):
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return '0' if s == '-0' else s

def rounded(points, r_out, r_in, skew=SKEW, ox=0, oy=0):
    """Closed right-angled polygon (clockwise on screen) -> skewed path with rounded corners."""
    t = math.tan(math.radians(skew))
    P = lambda x, y: (ox + x - t*y, oy + y)
    n = len(points)
    segs = []
    for i in range(n):
        p, v, q = points[i-1], points[i], points[(i+1) % n]
        din = (v[0]-p[0], v[1]-p[1]); lin = math.hypot(*din); din = (din[0]/lin, din[1]/lin)
        dout = (q[0]-v[0], q[1]-v[1]); lout = math.hypot(*dout); dout = (dout[0]/lout, dout[1]/lout)
        convex = din[0]*dout[1] - din[1]*dout[0] > 0
        r = min(r_out if convex else r_in, lin/2, lout/2)
        a = (v[0] - din[0]*r, v[1] - din[1]*r)
        b = (v[0] + dout[0]*r, v[1] + dout[1]*r)
        c1 = (a[0] + din[0]*r*K, a[1] + din[1]*r*K)
        c2 = (b[0] - dout[0]*r*K, b[1] - dout[1]*r*K)
        segs.append((a, c1, c2, b))
    pt = lambda xy: f'{f2(P(*xy)[0])} {f2(P(*xy)[1])}'
    d = f'M{pt(segs[0][3])}'
    for a, c1, c2, b in segs[1:] + segs[:1]:
        d += f'L{pt(a)}C{pt(c1)} {pt(c2)} {pt(b)}'
    return d + 'Z'

# ------------------------------------------------------------------ bars
def kinked_bar(x, top, bottom, jog, w, d, t):
    """Upright bar whose upper part sits d to the right; the kink's ledge is t tall."""
    return [(x + d, top), (x + d + w, top), (x + d + w, jog), (x + w, jog),
            (x + w, bottom), (x, bottom), (x, jog + t), (x + d, jog + t)]

BAR = dict(w=46, g=19, d=25, t=17, r_out=12, r_in=7)

def mark(bars, ink='#0B0D0A', ox=0, oy=0, **kw):
    """bars: list of (top, bottom, jog). Jogs must not rise left to right, so the channels never pinch."""
    p = {**BAR, **kw}
    d = ''
    for i, (top, bottom, jog) in enumerate(bars):
        x = i*(p['w'] + p['g'])
        d += rounded(kinked_bar(x, top, bottom, jog, p['w'], p['d'], p['t']), p['r_out'], p['r_in'], ox=ox, oy=oy)
    return d

# Primary mark: four bars. The kinks step down left to right like a rising
# scoreline, and the bars grow toward the middle like floodlight towers.
PRIMARY = [(60, 196, 104), (24, 214, 120), (36, 232, 140), (78, 236, 160)]

def mark_bounds(bars, ox=0, oy=0, **kw):
    p = {**BAR, **kw}
    t = math.tan(math.radians(SKEW))
    xs, ys = [], []
    for i, (top, bottom, jog) in enumerate(bars):
        x = i*(p['w'] + p['g'])
        for (px_, py_) in kinked_bar(x, top, bottom, jog, p['w'], p['d'], p['t']):
            xs.append(ox + px_ - t*py_); ys.append(oy + py_)
    return min(xs), min(ys), max(xs), max(ys)

# ------------------------------------------------------------------ wordmark
S = 22                                          # stroke
ASC, XT, BASE, DESC = 0, 36, 100, 124           # y lines (y grows downward)

def letter_polys(ch):
    R = lambda x0, y0, x1, y1: box(x0, y0, x1, y1)
    if ch == 'f':
        shapes, w = [R(12, ASC, 12 + S, BASE), R(12, ASC, 56, ASC + 20), R(0, XT, 46, XT + 20)], 56
    elif ch == 'u':
        shapes, w = [R(0, XT, S, BASE), R(48, XT, 48 + S, BASE), R(0, BASE - 20, 70, BASE)], 70
    elif ch == 't':
        shapes, w = [R(10, 12, 10 + S, BASE), R(0, XT, 46, XT + 20), R(10, BASE - 20, 48, BASE)], 48
    elif ch == 'l':
        # the l carries the bars' kink, so the name shares the mark's one detail
        return kinked_bar(0, ASC, BASE, XT + 6, S, 9, 9), S + 9
    elif ch == 'y':
        shapes, w = [R(0, XT, S, 88), R(0, 68, 70, 88), R(48, XT, 48 + S, DESC + 4), R(4, DESC - 16, 70, DESC + 4)], 70
    g = unary_union(shapes).simplify(0.01)
    pts = list(g.exterior.coords)[:-1]
    # shapely gives counter-clockwise in y-up terms = clockwise on screen? make sure: clockwise on screen
    area = sum(pts[i][0]*pts[(i+1) % len(pts)][1] - pts[(i+1) % len(pts)][0]*pts[i][1] for i in range(len(pts)))
    if area < 0:
        pts = pts[::-1]
    return pts, w

KERN = {'fu': 2, 'ut': 9, 'tl': 9, 'ly': 9}

def wordmark(ox=0, oy=0, r_out=7, r_in=4):
    d, x = '', 0
    word = 'futly'
    for i, ch in enumerate(word):
        pts, w = letter_polys(ch)
        pts = [(px_ + x, py_) for px_, py_ in pts]
        d += rounded(pts, r_out, r_in, ox=ox, oy=oy)
        x += w + KERN.get(word[i:i+2], 0)
    return d, x

def svg(w, h, body, title='futly'):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f2(w)} {f2(h)}" role="img" '
            f'aria-labelledby="title"><title id="title">{title}</title>{body}</svg>\n')

def symbol_svg(ink, bg=None, size=256, pad=34, rx=0):
    x0, y0, x1, y1 = mark_bounds(PRIMARY)
    sc = (size - 2*pad) / max(x1 - x0, y1 - y0)
    ox = (size - (x1 - x0)*sc)/2 - x0*sc
    oy = (size - (y1 - y0)*sc)/2 - y0*sc
    body = f'<rect width="{size}" height="{size}" rx="{rx}" fill="{bg}"/>' if bg else ''
    body += f'<g transform="translate({f2(ox)} {f2(oy)}) scale({f2(sc)})"><path fill="{ink}" d="{mark(PRIMARY)}"/></g>'
    return svg(size, size, body)

def wordmark_svg(ink):
    t = math.tan(math.radians(SKEW))
    d, w = wordmark(ox=t*DESC + 2, oy=2)
    return svg(w + t*DESC + 6, DESC + 8, f'<path fill="{ink}" d="{d}"/>')

def lockup_svg(ink, bg=None):
    """Symbol height = wordmark ascender-to-descender; gap = one bar width."""
    x0, y0, x1, y1 = mark_bounds(PRIMARY)
    H = DESC - ASC
    sc = H / (y1 - y0)
    t = math.tan(math.radians(SKEW))
    sym_w = (x1 - x0)*sc
    pad = 16
    sym = f'<g transform="translate({f2(pad - x0*sc)} {f2(pad - y0*sc)}) scale({f2(sc)})"><path fill="{ink}" d="{mark(PRIMARY)}"/></g>'
    wx = pad + sym_w + BAR['w']*sc*0.55 + t*DESC*0.6
    d, w = wordmark(ox=wx, oy=pad)
    W = wx + w + pad
    body = (f'<rect width="{f2(W)}" height="{H + 2*pad}" fill="{bg}"/>' if bg else '') + sym + f'<path fill="{ink}" d="{d}"/>'
    return svg(W, H + 2*pad, body)

INK, VOLT, CHALK = '#0B0D0A', '#DDFB5A', '#F3F5EE'

def build():
    os.makedirs(OUT, exist_ok=True)
    files = {
        'futly-symbol-ink.svg': symbol_svg(INK),
        'futly-symbol-volt-tile.svg': symbol_svg(INK, VOLT, rx=56),
        'futly-wordmark-ink.svg': wordmark_svg(INK),
        'futly-lockup-ink.svg': lockup_svg(INK),
        'futly-lockup-on-volt.svg': lockup_svg(INK, VOLT),
        'futly-lockup-on-ink.svg': lockup_svg(VOLT, INK),
    }
    for n, s in files.items():
        open(os.path.join(OUT, n), 'w').write(s)
    return files

if __name__ == '__main__':
    print('\n'.join(build()))
