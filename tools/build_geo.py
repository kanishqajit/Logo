"""futly v2: a geometric f whose ball terminal is the ball, plus a matching wordmark.

Everything is built from three primitives: bars, quarter/half rings and circles.
All subpaths are drawn clockwise so overlaps union cleanly under nonzero fill.
"""
import math, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else 'brand-v2'

def f2(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')

def bar(x, y, w, h):
    return f'M{f2(x)} {f2(y)}H{f2(x + w)}V{f2(y + h)}H{f2(x)}Z'

def pt(cx, cy, r, a):
    t = math.radians(a)
    return cx + r*math.cos(t), cy - r*math.sin(t)

def ring(cx, cy, R, r, a0, a1):
    """Ring sector between angles a0 < a1 (degrees, counter-clockwise from +x), drawn clockwise."""
    large = 1 if a1 - a0 > 180 else 0
    ox1, oy1 = pt(cx, cy, R, a1); ox0, oy0 = pt(cx, cy, R, a0)
    ix0, iy0 = pt(cx, cy, r, a0); ix1, iy1 = pt(cx, cy, r, a1)
    return (f'M{f2(ox1)} {f2(oy1)}A{f2(R)} {f2(R)} 0 {large} 1 {f2(ox0)} {f2(oy0)}'
            f'L{f2(ix0)} {f2(iy0)}A{f2(r)} {f2(r)} 0 {large} 0 {f2(ix1)} {f2(iy1)}Z')

def disc(cx, cy, r):
    return (f'M{f2(cx)} {f2(cy - r)}A{f2(r)} {f2(r)} 0 0 1 {f2(cx)} {f2(cy + r)}'
            f'A{f2(r)} {f2(r)} 0 0 1 {f2(cx)} {f2(cy - r)}Z')

# ---------------------------------------------------------------- the mark
# Stroke s; the hook is a quarter ring (outer R = 2s+..) whose centre sits on
# the stem's top. The ball rides the hook's mid-radius circle, 45 deg on from
# the cut, as if the curl just released it.
def f_geometry(s, R, top, stem_bottom, bar_l, bar_r, ball_gap=None, ball_scale=1.15, ox=0, ball=True):
    r = R - s
    cx, cy = ox + R, top + R                     # stem's left edge = cx - R = ox
    stem_l = cx - R
    parts = {
        'hook': ring(cx, cy, R, r, 90, 180),
        'stem': bar(stem_l, cy - 0.5, s, stem_bottom - cy + 0.5),
    }
    xh = cy                                      # crossbar sits right under the hook's centre line
    parts['crossbar'] = bar(stem_l - bar_l, xh, s + bar_l + bar_r, s)
    mid = (R + r)/2
    rb = s/2*ball_scale
    gap = s/4 if ball_gap is None else ball_gap
    # place the ball on the hook's mid-radius circle so its edge sits `gap` past the cut
    sweep = 2*math.degrees(math.asin((rb + gap) / (2*mid)))
    bx, by = pt(cx, cy, mid, 90 - sweep)
    if ball:
        parts['ball'] = disc(bx, by, rb)
    meta = dict(cx=cx, cy=cy, R=R, r=r, mid=mid, bx=bx, by=by, rb=rb, stem_l=stem_l, s=s,
                left=stem_l - bar_l, right=max(bx + rb if ball else cx, stem_l + s + bar_r), top=top, bottom=stem_bottom)
    return parts, meta

# Symbol on a 256 grid with unit u = 16: stroke 3u, hook R = 6u.
U = 16
S_SYM = 3*U
def symbol_parts(ox=0, oy=0):
    return f_geometry(S_SYM, 6*U, oy + 1*U, oy + 15*U, bar_l=2*U, bar_r=3*U, ox=ox)

def centred_symbol():
    parts, m = symbol_parts()
    dx = 128 - (m['left'] + m['right'])/2
    return symbol_parts(ox=dx)

# ---------------------------------------------------------------- wordmark
# x-height 100, stroke 24, ascender 40 above, descender 40 below.
WS, XH, ASC, DESC = 24, 100, 40, 40
TOP, XT, BASE = 0, ASC, ASC + XH                # y of ascender line, x-height line, baseline
GAP = 18

def g_f(x):
    parts, m = f_geometry(WS, 2*WS, TOP, BASE, bar_l=16, bar_r=26, ox=x + 16, ball=False)
    # crossbar on the x-height line
    parts['crossbar'] = bar(m['stem_l'] - 16, XT, WS + 16 + 26, WS)
    return parts, x + 16 + WS + 26, m      # advance ends at the crossbar; the ball overhangs the u

def g_u(x, w=96):
    R = w/2; r = R - WS; cy = BASE - R
    return {'l': bar(x, XT, WS, cy - XT + 0.5), 'r': bar(x + w - WS, XT, WS, BASE - XT),
            'bowl': ring(x + R, cy, R, r, 180, 360)}, x + w

def g_t(x):
    R = 2*WS; r = R - WS
    stem_l = x + 18; cx, cy = stem_l + R, BASE - R
    return {'stem': bar(stem_l, XT - 26, WS, cy - (XT - 26) + 0.5), 'bar': bar(x, XT, 18 + WS + 26, WS),
            'foot': ring(cx, cy, R, r, 180, 270)}, x + 18 + WS + 26

def g_l(x):
    return {'stem': bar(x, TOP, WS, BASE - TOP)}, x + WS

def g_y(x, w=96):
    R = w/2; r = R - WS; cy = BASE - R
    dcy = BASE + DESC - R
    return {'l': bar(x, XT, WS, cy - XT + 0.5), 'r': bar(x + w - WS, XT, WS, dcy - XT + 0.5),
            'bowl': ring(x + R, cy, R, r, 180, 360), 'tail': ring(x + R, dcy, R, r, 270, 360)}, x + w

def wordmark_parts():
    out, x = [], 0
    p, x, fm = g_f(x); out.append(p); x += GAP - 4           # the f's open right side needs less room
    p, x = g_u(x); out.append(p); x += GAP
    p, x = g_t(x); out.append(p); x += GAP - 4
    p, x = g_l(x); out.append(p); x += GAP
    p, x = g_y(x); out.append(p)
    d = ''.join(v for part in out for v in part.values())
    return d, x, fm

def svg(w, h, body, title='futly'):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f2(w)} {f2(h)}" role="img" '
            f'aria-labelledby="title"><title id="title">{title}</title>{body}</svg>\n')

def symbol_svg(ink='#000', ball=None, bg=None, radius=0):
    parts, m = centred_symbol()
    body = ''
    if bg:
        body += f'<rect width="256" height="256" rx="{radius}" fill="{bg}"/>'
    letter = ''.join(v for k, v in parts.items() if k != 'ball')
    body += f'<path fill="{ink}" d="{letter}"/><path fill="{ball or ink}" d="{parts["ball"]}"/>'
    return svg(256, 256, body)

def wordmark_svg(ink='#000', pad=0):
    d, w, fm = wordmark_parts()
    H = BASE + DESC
    body = f'<g transform="translate({pad} {pad})"><path fill="{ink}" d="{d}"/></g>'
    return svg(w + 2*pad, H + 2*pad, body)

def build():
    os.makedirs(OUT, exist_ok=True)
    files = {
        'futly-symbol-black.svg': symbol_svg('#0F1412'),
        'futly-wordmark-black.svg': wordmark_svg('#0F1412'),
    }
    for n, s in files.items():
        open(os.path.join(OUT, n), 'w').write(s)
    return files

if __name__ == '__main__':
    print('\n'.join(build()))
