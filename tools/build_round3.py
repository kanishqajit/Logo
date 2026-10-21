"""futly round 3: three concepts on one pixel system, drawn black-first on a 256 canvas."""
import importlib.util, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('px', os.path.join(HERE, 'build_pixel.py'))
px = importlib.util.module_from_spec(spec); spec.loader.exec_module(px)

OUT = sys.argv[1] if len(sys.argv) > 1 else 'concepts/round3'
INK = '#000000'

def svg(w, h, body, title='futly logo'):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" role="img" '
            f'aria-labelledby="title"><title id="title">{title}</title>{body}</svg>\n')

# ---------- A: Slot f -------------------------------------------------------
# A 5x5 booking grid (cell 40, gap 8, origin 12). The booked cells spell a
# lowercase f (stepped top, like the wordmark); the one round cell at its foot
# is the ball.
CELL, GAP, ORG, RX = 40, 8, 12, 9
F_CELLS = [(0, 2), (0, 3), (0, 4), (1, 1), (2, 0), (2, 1), (2, 2), (2, 3), (3, 1), (4, 1)]
BALL = (4, 3)

def cell_xy(r, c):
    return ORG + c*(CELL+GAP), ORG + r*(CELL+GAP)

def slot_f(ink=INK, ball=None, grid=None):
    parts = []
    if grid:
        lit = set(F_CELLS) | {BALL}
        for r in range(5):
            for c in range(5):
                if (r, c) not in lit:
                    x, y = cell_xy(r, c)
                    parts.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RX}" fill="{grid}"/>')
    for r, c in F_CELLS:
        x, y = cell_xy(r, c)
        parts.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RX}" fill="{ink}"/>')
    x, y = cell_xy(*BALL)
    # a circle reads smaller than a rounded square of the same width: overshoot ~5 %
    parts.append(f'<circle cx="{x + CELL/2:g}" cy="{y + CELL/2:g}" r="21" fill="{ball or ink}"/>')
    return ''.join(parts)

def slot_f_small(ink=INK, ball=None):
    """Below ~32 px the gaps close up, so the small cut fuses the cells into one f."""
    cells = set(F_CELLS)
    rects = []
    for r, c in cells:
        x, y = cell_xy(r, c)
        w = CELL + (GAP if (r, c + 1) in cells else 0)
        h = CELL + (GAP if (r + 1, c) in cells else 0)
        rects.append(f'M{x} {y}h{w}v{h}h{-w}Z')
    bx, by = cell_xy(*BALL)
    return (f'<path fill="{ink}" d="{''.join(rects)}"/>'
            f'<circle cx="{bx + CELL/2:g}" cy="{by + CELL/2:g}" r="22" fill="{ball or ink}"/>')

# ---------- B: Floodlight ---------------------------------------------------
# The pixel f cut through a vertical light beam: where they overlap the beam
# is knocked out, so the mark stays one colour (evenodd).
FT_U = 12

def ft_cells():
    """f and t share one crossbar: FT, full time on every scoreboard."""
    f_cells, _ = px.cells('f')
    t_cells, _ = px.cells('t')
    cells = set(f_cells) | {(c + 10, r) for c, r in t_cells} | {(9, 4), (9, 5)}
    return cells, 18, 15

def ft_mark(ink=INK, tile=None, beam=None):
    cells, w, h = ft_cells()
    u = FT_U
    ox, oy = (256 - w*u)/2, (256 - h*u)/2 - 4
    d = px.outline(cells, u, ox, oy)
    if tile is None:
        return f'<path fill="{ink}" d="{d}"/>'
    tile_d = 'M56 0H200A56 56 0 0 1 256 56V200A56 56 0 0 1 200 256H56A56 56 0 0 1 0 200V56A56 56 0 0 1 56 0Z'
    body = f'<path fill="{tile}" d="{tile_d}"/>'
    if beam:
        bx = ox + 10.5*u                   # beam rises behind the t stem
        body += (f'<defs><linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{beam[0]}" stop-opacity="0"/>'
                 f'<stop offset=".5" stop-color="{beam[0]}"/><stop offset="1" stop-color="{beam[1]}"/></linearGradient>'
                 f'<clipPath id="tile"><path d="{tile_d}"/></clipPath></defs>'
                 f'<rect clip-path="url(#tile)" x="{bx:g}" y="0" width="{5*u:g}" height="256" fill="url(#beam)"/>')
    return body + f'<path fill="{ink}" d="{d}"/>'

# ---------- C: Net u --------------------------------------------------------
# The u of futly seen from above is a goal; a round ball rests in the net.
NET_SYMBOL = ['###......###'] * 8 + ['####....####',
                                   '############',
                                   '.##########.']

def net_u(ink=INK, ball=None, u=18, ox=None, oy=None, symmetric=True):
    if symmetric:
        cells = {(c, r) for r, line in enumerate(NET_SYMBOL) for c, v in enumerate(line) if v == '#'}
    else:                                  # the wordmark keeps its own u
        u_cells, _ = px.cells('u')
        cells = {(c, rr - 4) for c, rr in u_cells}
    w, h = 12*u, 11*u
    ox = (256 - w)/2 if ox is None else ox
    oy = (256 - h)/2 - 2 if oy is None else oy
    cy_row, r = 5.6, 2.45
    body = f'<path fill="{ink}" d="{px.outline(cells, u, ox, oy)}"/>'
    body += f'<circle cx="{ox + 6*u:g}" cy="{oy + cy_row*u:g}" r="{r*u:g}" fill="{ball or ink}"/>'
    return body

# ---------- wordmark + lockups ---------------------------------------------
WU = 12                                   # wordmark unit: 19 rows -> 228 tall
def wordmark(ink=INK, ox=0, oy=0, net=False, ball=None, beam=False):
    cells, width = px.cells()
    if net:
        u_start = 11
        cells = {(c, r) for c, r in cells if not (u_start <= c < u_start + 12)}
    d = px.outline(cells, WU, ox, oy)
    body = ''
    if beam:
        # beam behind the t stem (word cols 26-28), knocked out where it meets the letters
        bx = ox + 25*WU
        body = (f'<path fill="{ink}" fill-rule="evenodd" d="M{bx:g} {oy - 3*WU:g}H{bx + 5*WU:g}V{oy + 22*WU:g}H{bx:g}Z{d}"/>')
    else:
        body = f'<path fill="{ink}" d="{d}"/>'
    if net:
        body += net_u(ink, ball, u=WU, ox=ox + 11*WU, oy=oy + 4*WU, symmetric=False)
    return body, width*WU

def lockup(symbol_body, ink=INK, net=False, ball=None):
    oy = 128 - 9.5*WU                     # x-height centred on the symbol
    gap = 60
    wm, ww = wordmark(ink, 256 + gap, oy, net=net, ball=ball)
    return svg(256 + gap + ww, 256, f'<g id="symbol">{symbol_body}</g><g id="wordmark">{wm}</g>')

def wordmark_only(ink=INK, beam=False):
    pad = 3*WU + 8 if beam else 0
    wm, ww = wordmark(ink, 0, pad, beam=beam)
    return svg(ww, 19*WU + 2*pad, wm)

def build():
    os.makedirs(OUT, exist_ok=True)
    files = {
        'a-slot-f-symbol.svg': svg(256, 256, slot_f()),
        'a-slot-f-lockup.svg': lockup(slot_f()),
        'a-slot-f-symbol-small.svg': svg(256, 256, slot_f_small()),
        'b-ft-symbol.svg': svg(256, 256, ft_mark()),
        'b-ft-lockup.svg': wordmark_only(),
        'c-net-u-symbol.svg': svg(256, 256, net_u()),
        'c-net-u-lockup.svg': wordmark_only_net(),
    }
    for n, s in files.items():
        open(os.path.join(OUT, n), 'w').write(s)
    return files

def wordmark_only_net(ink=INK, ball=None):
    wm, ww = wordmark(ink, 0, 0, net=True, ball=ball)
    return svg(ww, 19*WU, wm)

if __name__ == '__main__':
    print('\n'.join(build()))
