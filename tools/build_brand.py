"""futly brand: refined pixel wordmark, light-beam device and app icon."""
import importlib.util, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('px', os.path.join(HERE, 'build_pixel.py'))
px = importlib.util.module_from_spec(spec); spec.loader.exec_module(px)
outline = px.outline

OUT = sys.argv[1] if len(sys.argv) > 1 else 'brand'

# Grid: ascenders rows 0-3, x-height rows 4-13 (10 px), descenders rows 14-17.
# Strokes are 2 px; outer corners and inner joins step by one pixel, like
# bulbs on a scoreboard.
X = ['##..........##'] * 7
GLYPHS = {
    'f': (['...########',
           '..#########',
           '..###......',
           '..##.......'] + ['##########.'] * 2 + ['..##.......'] * 8),
    'u': ([None] * 4 + X + ['###.........##',
                            '##############',
                            '.#############']),
    't': ([None] + ['.##......'] * 3 + ['########.'] * 2 + ['.##......'] * 5 + ['.###.....',
                                                                               '.########',
                                                                               '..#######']),
    'l': (['##....'] * 11 + ['###...',
                             '######',
                             '.#####']),
    'y': ([None] * 4 + X + ['###.........##',
                            '##############',
                            '.#############',
                            '............##',
                            '...........###',
                            '##############',
                            '#############.']),
}
# optical spacing, in pixels, between each pair
KERN = {'fu': 1, 'ut': 2, 'tl': 2, 'ly': 2}
ROWS, XTOP, BASE = 18, 4, 14

def word_cells(text='futly'):
    cells, x = set(), 0
    for i, ch in enumerate(text):
        rows = GLYPHS[ch]
        for r, line in enumerate(rows):
            if line is None: continue
            for c, v in enumerate(line):
                if v == '#': cells.add((x + c, r))
        w = max(len(l) for l in rows if l)
        x += w + (KERN.get(text[i:i+2], 2) if i + 1 < len(text) else 0)
    return cells, x

def glyph_cells(ch):
    return word_cells(ch)

def svg(w, h, body, title='futly'):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" role="img" '
            f'aria-labelledby="title"><title id="title">{title}</title>{body}</svg>\n')

def beam_defs(id_, stops, grain=True):
    d = (f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{stops[0]}" stop-opacity="0"/>'
         f'<stop offset=".18" stop-color="{stops[0]}" stop-opacity=".35"/>'
         f'<stop offset=".55" stop-color="{stops[1]}"/>'
         f'<stop offset="1" stop-color="{stops[2]}"/></linearGradient>')
    if grain:
        d += (f'<filter id="{id_}-grain" x="0" y="0" width="100%" height="100%">'
              f'<feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="4" stitchTiles="stitch"/>'
              f'<feColorMatrix values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 1.2 -.35"/>'
              f'<feComposite in2="SourceGraphic" operator="in"/></filter>')
    return d

BEAM = ('#14109E', '#3A34FF', '#8E4BFF')      # night-match indigo to violet
NIGHT = '#06070A'

def beam(id_, x, y, w, h, grain=True):
    s = f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="url(#{id_})"/>'
    if grain:
        s += f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="url(#{id_})" filter="url(#{id_}-grain)" opacity=".22"/>'
    return s

def glow(id_, x, y, w, h, cy):
    """A soft hotspot where the beam meets the type, like light hitting haze."""
    cx = x + w/2
    return (f'<radialGradient id="{id_}" gradientUnits="userSpaceOnUse" cx="{cx:g}" cy="{cy:g}" r="{h*0.42:g}" '
            f'gradientTransform="translate({cx:g} {cy:g}) scale(.75 1) translate({-cx:g} {-cy:g})">'
            f'<stop offset="0" stop-color="#7C8BFF" stop-opacity=".6"/>'
            f'<stop offset=".6" stop-color="#5A5CFF" stop-opacity=".15"/>'
            f'<stop offset="1" stop-color="#5A5CFF" stop-opacity="0"/></radialGradient>'
            f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="url(#{id_})"/>')

def build():
    os.makedirs(OUT, exist_ok=True)
    cells, width = word_cells()
    files = {}
    U = 10
    for name, ink in (('futly-wordmark-white.svg', '#FFFFFF'), ('futly-wordmark-black.svg', '#06070A'),
                      ('futly-wordmark-indigo.svg', '#3D2BFF')):
        files[name] = svg(width*U, ROWS*U, f'<path fill="{ink}" d="{outline(cells, U)}"/>')

    # Hero, after the reference: word centred on a 4:3 night canvas, beam behind the t.
    W, H, u = 1600, 1200, 11
    ox = (W - width*u)/2
    oy = H/2 - (XTOP + 5)*u                     # centre of the x-height on the canvas centre
    t_x = 11 + KERN['fu'] + 14 + KERN['ut']       # first column of the t
    bw = 224
    bx = ox + (t_x + 1.5)*u - bw/2                # beam centred on the t stem
    body = (f'<defs>{beam_defs("beam", BEAM)}</defs><rect width="{W}" height="{H}" fill="{NIGHT}"/>'
            + beam('beam', bx, 250, bw, 740)
            + glow('glow', bx, 250, bw, 740, H/2 + 30)
            + f'<path fill="#F4F4F7" d="{outline(cells, u, ox, oy)}"/>')
    files['futly-hero.svg'] = svg(W, H, body)

    # Signature lockup: the wordmark with its beam, on a transparent ground.
    su = 10
    sw, sh = width*su + 2*40, 40*su
    sox, soy = 40, sh/2 - (XTOP + 5)*su
    sbx = sox + (t_x + 1.5)*su - 9*su
    files['futly-signature.svg'] = svg(sw, sh,
        f'<defs>{beam_defs("sb", BEAM, False)}</defs>' + beam('sb', sbx, 0, 18*su, sh, False)
        + glow('sg', sbx, 0, 18*su, sh, sh/2 + 30) + f'<path fill="#F4F4F7" d="{outline(cells, su, sox, soy)}"/>')

    # App icon: pixel f standing in the beam.
    f_cells, _ = glyph_cells('f')
    iu = 11
    fx = 128 - 3*iu - 1.5*iu                      # stem (cols 2-3) centred, nudged for the hook
    fy = 128 - (14*iu)/2 - 4
    tile = 'M58 0H198A58 58 0 0 1 256 58V198A58 58 0 0 1 198 256H58A58 58 0 0 1 0 198V58A58 58 0 0 1 58 0Z'
    stem_c = fx + 3*iu
    for name, grain in (('futly-app-icon.svg', True), ('futly-app-icon-flat.svg', False)):
        body = (f'<defs>{beam_defs("ib", BEAM, grain)}<clipPath id="tile"><path d="{tile}"/></clipPath></defs>'
                f'<g clip-path="url(#tile)"><rect width="256" height="256" fill="{NIGHT}"/>'
                + beam('ib', stem_c - 34, 0, 68, 256, grain) + '</g>'
                + f'<path fill="#FFFFFF" d="{outline(f_cells, iu, fx, fy)}"/>')
        files[name] = svg(256, 256, body)
    # One-colour symbol for favicons and stamps: the f alone.
    files['futly-symbol-black.svg'] = svg(256, 256, f'<path fill="#06070A" d="{outline(f_cells, iu, fx, fy)}"/>')

    for n, s in files.items():
        open(os.path.join(OUT, n), 'w').write(s)
    return files, width

if __name__ == '__main__':
    files, width = build()
    print(width, '\n'.join(files))
