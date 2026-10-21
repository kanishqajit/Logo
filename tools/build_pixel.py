"""futly scoreboard wordmark: hand-drawn pixel glyphs, traced into clean SVG outlines."""
import os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else 'concepts/scoreboard-pixel'

# Rows run from the ascender line (row 0) down. The x-height covers rows 4-14,
# so the baseline sits under row 14 and descenders reach row 18. Verticals are
# three pixels wide, horizontals two, and every corner is stepped by one pixel,
# like the bulbs on a stadium scoreboard.
STEM = ['###......###'] * 8
GLYPHS = {
    'f': (0, ['...######',
              '..#######',
              '..###....',
              '..###....',
              '#########',
              '#########'] + ['..###....'] * 9),
    'u': (4, STEM + ['####.....###',
                     '############',
                     '.###########']),
    't': (1, ['.###....'] * 3 + ['########',
                                 '########'] + ['.###....'] * 6 + ['.####...',
                                                                   '.#######',
                                                                   '..######']),
    'l': (0, ['###..'] * 12 + ['####.',
                               '#####',
                               '.####']),
    'y': (4, STEM + ['####.....###',
                     '############',
                     '.###########',
                     '.........###',
                     '........####',
                     '############',
                     '###########.']),
}
GAP = 2

def cells(text='futly'):
    """Filled (col, row) cells for the word, plus its width in pixels."""
    out, x = set(), 0
    for ch in text:
        top, rows = GLYPHS[ch]
        for r, line in enumerate(rows):
            for c, v in enumerate(line):
                if v == '#':
                    out.add((x + c, top + r))
        x += len(GLYPHS[ch][1][0]) + GAP
    return out, x - GAP

def outline(filled, unit, ox=0, oy=0):
    """Trace the union of unit squares into closed polygons (nonzero winding)."""
    edges = {}
    for (c, r) in filled:
        # clockwise edges of the cell; shared edges cancel out
        for a, b, n in (((c, r), (c+1, r), (c, r-1)), ((c+1, r), (c+1, r+1), (c+1, r)),
                        ((c+1, r+1), (c, r+1), (c, r+1)), ((c, r+1), (c, r), (c-1, r))):
            if n not in filled:
                edges.setdefault(a, []).append(b)
    paths = []
    while edges:
        start = next(iter(edges)); pts = [start]; cur = start
        while True:
            nxt = edges[cur].pop()
            if not edges[cur]: del edges[cur]
            if nxt == start: break
            pts.append(nxt); cur = nxt
        # drop collinear points
        simp = [p for i, p in enumerate(pts)
                if not ((pts[i-1][0] == p[0] == pts[(i+1) % len(pts)][0]) or
                        (pts[i-1][1] == p[1] == pts[(i+1) % len(pts)][1]))]
        paths.append('M' + 'L'.join(f'{ox + x*unit:g} {oy + y*unit:g}' for x, y in simp) + 'Z')
    return ''.join(paths)

def leds(filled, unit, ox, oy, cols, rows, lit, unlit, r=0.36):
    dots = []
    for row in range(rows[0], rows[1]):
        for col in range(cols[0], cols[1]):
            on = (col, row) in filled
            if not on and not unlit: continue
            dots.append(f'<circle cx="{ox + (col+.5)*unit:g}" cy="{oy + (row+.5)*unit:g}" r="{r*unit:g}" fill="{lit if on else unlit}"/>')
    return ''.join(dots)

PALETTES = {
    # name: (gradient stops top->bottom, background)
    'night-match': (['#2B2BFF', '#3D3BFF', '#8B4DFF'], '#08090C'),
    'floodlight':  (['#0E9F55', '#14C46A', '#B9EE3A'], '#070B09'),
    'scoreboard-amber': (['#FF8A1F', '#FFA51F', '#FF4D2E'], '#0B0907'),
}

def bar(id_, stops, x, y, w, h):
    return (f'<defs><linearGradient id="g-{id_}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{stops[0]}" stop-opacity="0"/>'
            f'<stop offset=".45" stop-color="{stops[1]}"/>'
            f'<stop offset="1" stop-color="{stops[2]}"/></linearGradient>'
            f'<filter id="n-{id_}" x="0" y="0" width="100%" height="100%">'
            f'<feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="7"/>'
            f'<feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .55 0"/>'
            f'<feComposite in2="SourceGraphic" operator="in"/></filter></defs>'
            f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="url(#g-{id_})"/>'
            f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="url(#g-{id_})" filter="url(#n-{id_})" opacity=".18"/>')

def svg(w, h, body, label='futly'):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" role="img" '
            f'aria-label="{label}"><title>{label}</title>{body}</svg>\n')

def build():
    os.makedirs(OUT, exist_ok=True)
    word, width = cells()
    rows = 19
    files = {}

    # plain wordmarks, 10 units per pixel
    for name, ink in (('wordmark-white.svg', '#FFFFFF'), ('wordmark-ink.svg', '#0A0C0B')):
        files[name] = svg(width*10, rows*10, f'<path fill="{ink}" d="{outline(word, 10)}"/>')

    # hero lockups after the reference: word centred, light bar behind the t
    W, H, u = 736, 552, 5.75
    ox, oy = (W - width*u) / 2, H/2 - 9.5*u
    t_mid = 11 + 14 + 2.5        # f(9)+gap, u(12)+gap, centre of the t stem
    bw = 17*u
    for pal, (stops, bg) in PALETTES.items():
        body = (f'<rect width="{W}" height="{H}" fill="{bg}"/>'
                + bar(pal, stops, ox + t_mid*u - bw/2, 110, bw, 330)
                + f'<path fill="#FFFFFF" d="{outline(word, u, ox, oy)}"/>')
        files[f'hero-{pal}.svg'] = svg(W, H, body)
        led_body = (f'<rect width="{W}" height="{H}" fill="{bg}"/>'
                    + bar(f'l-{pal}', stops, ox + t_mid*u - bw/2, 110, bw, 330)
                    + leds(word, u, ox, oy, (0, width), (0, rows), '#FFFFFF', None, r=0.42))
        files[f'hero-led-{pal}.svg'] = svg(W, H, led_body)

    # LED dot-matrix version: lit bulbs on a faint panel of unlit ones
    pad = 2
    for pal, lit in (('white', '#FFFFFF'), ('amber', '#FFB21F')):
        w, h = (width + 2*pad)*10, (rows + 2*pad)*10
        body = (f'<rect width="{w}" height="{h}" rx="14" fill="#0B0D0C"/>'
                + leds(word, 10, pad*10, pad*10, (0, width), (0, rows), lit, '#1C211E'))
        files[f'led-{pal}.svg'] = svg(w, h, body)

    # app icon: pixel f on the light bar
    f_cells, _ = cells('f')
    iu = 4.4
    fx, fy = 50 - 9*iu/2, 50 - 15*iu/2
    for pal, (stops, bg) in PALETTES.items():
        body = (f'<defs><clipPath id="c-{pal}"><rect width="100" height="100" rx="22"/></clipPath></defs>'
                f'<g clip-path="url(#c-{pal})"><rect width="100" height="100" fill="{bg}"/>'
                + bar(f'i-{pal}', stops, fx + 3.5*iu - 18, 0, 36, 100) + '</g>'
                + f'<path fill="#FFFFFF" d="{outline(f_cells, iu, fx, fy)}"/>')
        files[f'icon-{pal}.svg'] = svg(100, 100, body)

    for n, s in files.items():
        open(os.path.join(OUT, n), 'w').write(s)
    return sorted(files)

if __name__ == '__main__':
    print('\n'.join(build()))
