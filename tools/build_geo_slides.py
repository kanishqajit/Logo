"""Presentation slides (1080x1350) for futly v2: symbol, logo grid, wordmark, lockup, icon, in play."""
import importlib.util, math, os, sys
from shapely.geometry import box, Point, Polygon
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('geo', os.path.join(HERE, 'build_geo.py'))
geo = importlib.util.module_from_spec(spec); spec.loader.exec_module(geo)
f2 = geo.f2

OUT = sys.argv[1] if len(sys.argv) > 1 else 'brand-v2/slides'
W, H = 1080, 1350
BG, CHALK, LINE, CIRC, VOLT, MUTED = '#141A17', '#EEF1EC', '#28302C', '#36403B', '#C8F23C', '#7E8A83'
FONT = "Manrope, 'Helvetica Neue', Arial, sans-serif"

def ring_poly(cx, cy, R, r, a0, a1, n=96):
    outer = [geo.pt(cx, cy, R, a0 + (a1 - a0)*i/n) for i in range(n + 1)]
    inner = [geo.pt(cx, cy, r, a1 - (a1 - a0)*i/n) for i in range(n + 1)]
    return Polygon(outer + inner)

def poly_path(g):
    polys = getattr(g, 'geoms', [g])
    d = ''
    for p in polys:
        for ring in [p.exterior, *p.interiors]:
            pts = list(ring.coords)
            d += 'M' + 'L'.join(f'{x:.2f} {y:.2f}' for x, y in pts) + 'Z'
    return d

# symbol geometry, rebuilt as shapes so it can be outlined as one union
_, M = geo.centred_symbol()
s, R, r, cx, cy = M['s'], M['R'], M['r'], M['cx'], M['cy']
stem_l, top, bottom = M['stem_l'], M['top'], M['bottom']
BAR_L, BAR_R = 2*geo.U, 3*geo.U
letter = unary_union([ring_poly(cx, cy, R, r, 90, 180), box(stem_l, cy - 0.5, stem_l + s, bottom),
                      box(stem_l - BAR_L, cy, stem_l + s + BAR_R, cy + s)])
ballg = Point(M['bx'], M['by']).buffer(M['rb'], 128)

def frame(label, num, body, bg=BG, fg=CHALK, sub=MUTED):
    t = (f'<text x="40" y="58" font-family="{FONT}" font-size="22" font-weight="500" fill="{fg}">futly</text>'
         f'<text x="{W/2}" y="58" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="700" letter-spacing="4" fill="{fg}">{label}</text>'
         f'<text x="40" y="{H - 40}" font-family="{FONT}" font-size="20" font-weight="500" fill="{sub}">2026</text>'
         f'<text x="{W - 40}" y="{H - 40}" text-anchor="end" font-family="{FONT}" font-size="20" font-weight="500" fill="{sub}">{num}</text>')
    return geo.svg(W, H, f'<rect width="{W}" height="{H}" fill="{bg}"/>{body}{t}', f'futly {label.lower()}')

def symbol_fill(scale, ox, oy, ink=CHALK, ball=VOLT):
    parts, _ = geo.centred_symbol()
    letter_d = ''.join(v for k, v in parts.items() if k != 'ball')
    return (f'<g transform="translate({f2(ox)} {f2(oy)}) scale({f2(scale)})"><path fill="{ink}" d="{letter_d}"/>'
            f'<path fill="{ball}" d="{parts["ball"]}"/></g>')

# ---- 01 symbol
def slide_symbol():
    sc = 2.6
    return frame('SYMBOL', '01', symbol_fill(sc, W/2 - 128*sc, H/2 - 128*sc - 10))

# ---- 02 logo grid: only lines the mark is really built from
def slide_grid():
    sc = 2.6
    ox, oy = W/2 - 128*sc, H/2 - 128*sc - 10
    X = lambda v: ox + v*sc
    Y = lambda v: oy + v*sc
    g = []
    xs = [stem_l - BAR_L, stem_l, stem_l + s, cx, M['bx'], stem_l + s + BAR_R]
    ys = [top, top + s, cy, cy + s, M['by'], bottom]
    for x in xs:
        g.append(f'<line x1="{f2(X(x))}" x2="{f2(X(x))}" y1="0" y2="{H}" stroke="{LINE}" stroke-width="1.5"/>')
    for y in ys:
        g.append(f'<line y1="{f2(Y(y))}" y2="{f2(Y(y))}" x1="0" x2="{W}" stroke="{LINE}" stroke-width="1.5"/>')
    circ = lambda x, y, rad, w=1.5, col=CIRC, dash='': (
        f'<circle cx="{f2(X(x))}" cy="{f2(Y(y))}" r="{f2(rad*sc)}" fill="none" stroke="{col}" stroke-width="{w}"{dash}/>')
    # the hook's radius pair, its centre line (dashed) and the ball's clearance (dotted)
    g.append(circ(cx, cy, R)); g.append(circ(cx, cy, r))
    g.append(circ(cx, cy, M['mid'], 1.5, CIRC, ' stroke-dasharray="6 8"'))
    g.append(circ(cx, cy - M['mid'], M['rb'] + s/4, 1.5, CIRC, ' stroke-dasharray="3 6"'))
    out = (f'<g transform="translate({f2(ox)} {f2(oy)}) scale({f2(sc)})" fill="none" stroke="{CHALK}" '
           f'stroke-width="{f2(2.4/sc)}" stroke-linejoin="round"><path d="{poly_path(letter)}"/><path d="{poly_path(ballg)}"/></g>')
    notes = (f'<text x="40" y="{H - 110}" font-family="{FONT}" font-size="18" fill="{MUTED}">One radius pair (R = 2s, r = s) draws every curve.</text>'
             f'<text x="40" y="{H - 82}" font-family="{FONT}" font-size="18" fill="{MUTED}">The ball rides the hook’s centre line, a quarter-stroke past its end.</text>')
    return frame('LOGO GRID', '02', ''.join(g) + out + notes)

# ---- 03 wordmark with its metrics
def slide_wordmark():
    d, w, _ = geo.wordmark_parts()
    sc = (W - 240) / w
    ox = (W - w*sc)/2
    hh = (geo.BASE + geo.DESC)*sc
    oy = H/2 - hh/2
    g = []
    for y, lab in ((geo.TOP, 'ascender'), (geo.XT, 'x-height'), (geo.BASE, 'baseline'), (geo.BASE + geo.DESC, 'descender')):
        yy = oy + y*sc
        g.append(f'<line x1="0" x2="{W}" y1="{f2(yy)}" y2="{f2(yy)}" stroke="{LINE}" stroke-width="1.5"/>')
        g.append(f'<text x="40" y="{f2(yy - 10)}" font-family="{FONT}" font-size="15" letter-spacing="1.5" fill="{MUTED}">{lab.upper()}</text>')
    body = ''.join(g) + f'<g transform="translate({f2(ox)} {f2(oy)}) scale({f2(sc)})"><path fill="{CHALK}" d="{d}"/></g>'
    body += (f'<text x="40" y="{H - 110}" font-family="{FONT}" font-size="18" fill="{MUTED}">Custom letters from the same bars and rings as the symbol.</text>'
             f'<text x="40" y="{H - 82}" font-family="{FONT}" font-size="18" fill="{MUTED}">Stroke 24 on a 100 x-height. No font file needed.</text>')
    return frame('WORDMARK', '03', body)

# ---- 04 lockup, dark over chalk
def lockup_group(height, ox, oy, ink, ball):
    """Symbol letter spans ascender to baseline of the wordmark; gap is 1.5 wordmark strokes."""
    d, w, _ = geo.wordmark_parts()
    parts, m = geo.centred_symbol()
    letter_h = m['bottom'] - m['top']                 # symbol f, top of hook to foot of stem
    s_sc = height / letter_h
    ws = height / (geo.BASE - geo.TOP)               # wordmark scale: ascender to baseline = height
    sym = symbol_fill(s_sc, ox - m['left']*s_sc, oy - m['top']*s_sc, ink, ball)
    wx = ox + (m['right'] - m['left'])*s_sc + 1.5*geo.WS*ws
    return sym + f'<g transform="translate({f2(wx)} {f2(oy)}) scale({f2(ws)})"><path fill="{ink}" d="{d}"/></g>', wx + w*ws - ox

def slide_lockup():
    h = 120
    g, width = lockup_group(h, 0, 0, CHALK, VOLT)
    ox = (W - width)/2
    top = f'<g transform="translate({f2(ox)} {H/4 - h/2 + 30})">{g}</g>'
    g2, _ = lockup_group(h, 0, 0, BG, '#141A17')
    bottom = (f'<rect x="0" y="{H/2}" width="{W}" height="{H/2}" fill="{CHALK}"/>'
              f'<g transform="translate({f2(ox)} {3*H/4 - h/2 - 10})">{g2}</g>')
    return frame('LOCKUP', '04', top + bottom, sub=MUTED).replace(
        f'fill="{MUTED}">2026', f'fill="#5B655F">2026').replace(f'fill="{MUTED}">04', 'fill="#5B655F">04')

# ---- 05 app icon
def icon_svg(size, x, y, radius_frac=0.225):
    sc = size/256
    rad = size*radius_frac
    inner = symbol_fill(0.78, 128 - 128*0.78, 128 - 128*0.78 + 2, CHALK, VOLT)
    return (f'<g transform="translate({f2(x)} {f2(y)}) scale({f2(sc)})">'
            f'<rect width="256" height="256" rx="{f2(rad/sc)}" fill="#1E2622"/>{inner}</g>')

def slide_icon():
    big = 460
    body = icon_svg(big, (W - big)/2, 330)
    xs, row_y = [], 900
    sizes = [180, 120, 87, 60, 40]
    total = sum(sizes) + 40*(len(sizes) - 1)
    x = (W - total)/2
    for sz in sizes:
        body += icon_svg(sz, x, row_y + (180 - sz))
        body += f'<text x="{f2(x + sz/2)}" y="{row_y + 214}" text-anchor="middle" font-family="{FONT}" font-size="15" fill="{MUTED}">{sz}</text>'
        x += sz + 40
    return frame('APP ICON', '05', body)

# ---- 06 in play: booking pass
def slide_play():
    card_w, card_h = 760, 980
    cx0, cy0 = (W - card_w)/2, 200
    g, lw = lockup_group(52, 0, 0, CHALK, VOLT)
    body = (f'<rect x="{cx0}" y="{cy0}" width="{card_w}" height="{card_h}" rx="44" fill="#1C2420"/>'
            f'<g transform="translate({cx0 + 56} {cy0 + 56})">{g}</g>'
            f'<text x="{cx0 + card_w - 56}" y="{cy0 + 100}" text-anchor="end" font-family="{FONT}" font-size="20" font-weight="700" letter-spacing="3" fill="{VOLT}">BOOKED</text>'
            f'<line x1="{cx0 + 56}" x2="{cx0 + card_w - 56}" y1="{cy0 + 180}" y2="{cy0 + 180}" stroke="{LINE}" stroke-width="2"/>'
            f'<text x="{cx0 + 56}" y="{cy0 + 260}" font-family="{FONT}" font-size="46" font-weight="700" fill="{CHALK}">Greenfield Arena</text>'
            f'<text x="{cx0 + 56}" y="{cy0 + 305}" font-family="{FONT}" font-size="24" fill="{MUTED}">Pitch 2 · 5-a-side · Floodlit</text>')
    cells = [('DATE', 'Fri 24 Oct'), ('KICK-OFF', '20:00'), ('SQUAD', '10 / 10'), ('YOUR SHARE', '₹120')]
    for i, (k, v) in enumerate(cells):
        x = cx0 + 56 + (i % 2)*330
        y = cy0 + 400 + (i // 2)*140
        body += (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="17" letter-spacing="2" fill="{MUTED}">{k}</text>'
                 f'<text x="{x}" y="{y + 52}" font-family="{FONT}" font-size="40" font-weight="600" fill="{CHALK}">{v}</text>')
    # pitch diagram drawn with the brand's radius pair
    px0, py0, pw, ph = cx0 + 56, cy0 + 700, card_w - 112, 220
    body += (f'<g fill="none" stroke="{CIRC}" stroke-width="3"><rect x="{px0}" y="{py0}" width="{pw}" height="{ph}" rx="14"/>'
             f'<line x1="{px0 + pw/2}" x2="{px0 + pw/2}" y1="{py0}" y2="{py0 + ph}"/>'
             f'<circle cx="{px0 + pw/2}" cy="{py0 + ph/2}" r="48"/></g>'
             f'<circle cx="{px0 + pw/2}" cy="{py0 + ph/2}" r="12" fill="{VOLT}"/>')
    return frame('IN PLAY', '06', body)

def build():
    os.makedirs(OUT, exist_ok=True)
    slides = {'01-symbol.svg': slide_symbol(), '02-logo-grid.svg': slide_grid(), '03-wordmark.svg': slide_wordmark(),
              '04-lockup.svg': slide_lockup(), '05-app-icon.svg': slide_icon(), '06-in-play.svg': slide_play()}
    for n, v in slides.items():
        open(os.path.join(OUT, n), 'w').write(v)
    return slides

def lockup_masters(out_dir):
    """Horizontal lockup files, height 256 with the letters spanning 200."""
    for name, ink, ball in (('futly-lockup-chalk-volt.svg', CHALK, VOLT), ('futly-lockup-black.svg', '#0F1412', '#0F1412'),
                            ('futly-lockup-white.svg', '#FFFFFF', '#FFFFFF')):
        g, width = lockup_group(200, 0, 28, ink, ball)
        open(os.path.join(out_dir, name), 'w').write(geo.svg(round(width + 1, 1), 256 + 40, g))

if __name__ == '__main__':
    print('\n'.join(build()))
    lockup_masters(os.path.dirname(OUT))
