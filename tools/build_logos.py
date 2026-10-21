"""Generate futly logo concepts as outlined SVGs (no font dependencies)."""
import json, os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONTS = os.environ.get('FUTLY_FONTS', os.path.join(os.path.dirname(__file__), '..', 'fonts'))
OUT = sys.argv[1] if len(sys.argv) > 1 else 'concepts'

_cache = {}
def font(name):
    if name not in _cache:
        _cache[name] = TTFont(os.path.join(FONTS, name + '.ttf'))
    return _cache[name]

def glyph_runs(fname, text, size, tracking=0):
    """Return list of (char, path_d, bounds) per glyph plus total bounds."""
    f = font(fname); gs = f.getGlyphSet(); cmap = f.getBestCmap()
    s = size / f['head'].unitsPerEm
    x, out = 0, []
    for ch in text:
        g = cmap[ord(ch)]
        t = (s, 0, 0, -s, x, 0)
        p = SVGPathPen(gs); b = BoundsPen(gs)
        gs[g].draw(TransformPen(p, t)); gs[g].draw(TransformPen(b, t))
        out.append((ch, p.getCommands(), b.bounds, x))
        x += gs[g].width * s + tracking
    xs = [r[2] for r in out if r[2]]
    tb = (min(b[0] for b in xs), min(b[1] for b in xs), max(b[2] for b in xs), max(b[3] for b in xs))
    return out, tb

def wordmark(fname, size, tracking, fill, skip=()):
    runs, tb = glyph_runs(fname, 'futly', size, tracking)
    d = ''.join(r[1] for r in runs if r[0] not in skip)
    return f'<path fill="{fill}" d="{d}"/>', runs, tb

def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n')

# ---------- icons, all drawn in a 100x100 box ----------

def icon_pin(c):
    # Location pin holding a top-down pitch: "find a turf near you".
    return (f'<path fill="{c["primary"]}" d="M50 96 L23.3 61 A34 34 0 1 1 76.7 61 Z" stroke="{c["primary"]}" stroke-width="4" stroke-linejoin="round"/>'
            f'<g fill="none" stroke="{c["line"]}" stroke-width="3.4" stroke-linecap="round">'
            f'<rect x="27" y="26" width="46" height="30" rx="3"/>'
            f'<path d="M50 26 V56"/><circle cx="50" cy="41" r="6.5"/></g>'
            f'<circle cx="50" cy="41" r="1.9" fill="{c["line"]}"/>')

def icon_chalk_f(c):
    # An F chalked like pitch markings; the middle arm ends in the kick-off circle.
    return (f'<rect width="100" height="100" rx="24" fill="{c["primary"]}"/>'
            f'<g fill="none" stroke="{c["line"]}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M33 78 V24 H69"/><path d="M33 51 H49"/></g>'
            f'<circle cx="60.5" cy="51" r="11" fill="none" stroke="{c["line"]}" stroke-width="7"/>'
            f'<circle cx="60.5" cy="51" r="3" fill="{c["line"]}"/>')

def icon_stripes(c, fname='saira'):
    # Mowed-turf stripes behind a forward-leaning f.
    stripes = ''.join(
        f'<rect x="{-60 + i*20}" y="-30" width="10" height="170" fill="{c["stripe"]}"/>' for i in range(12))
    runs, tb = glyph_runs(fname, 'f', 92)
    gw, gh = tb[2]-tb[0], tb[3]-tb[1]
    tx, ty = 50 - (tb[0] + gw/2), 50 - (tb[1] + gh/2)
    return (f'<defs><clipPath id="tile-{c["id"]}"><rect width="100" height="100" rx="24"/></clipPath></defs>'
            f'<g clip-path="url(#tile-{c["id"]})"><rect width="100" height="100" fill="{c["primary"]}"/>'
            f'<g transform="rotate(28 50 50)">{stripes}</g></g>'
            f'<path transform="translate({tx:.2f} {ty:.2f})" fill="{c["line"]}" d="{runs[0][1]}"/>')

def icon_slot(c):
    # Calendar page with a pitch line and a tick: "booked".
    return (f'<rect x="10" y="16" width="80" height="76" rx="18" fill="{c["primary"]}"/>'
            f'<rect x="28" y="7" width="9" height="20" rx="4.5" fill="{c["accent"]}"/>'
            f'<rect x="63" y="7" width="9" height="20" rx="4.5" fill="{c["accent"]}"/>'
            f'<path d="M10 38 H90" stroke="{c["accent"]}" stroke-width="5"/>'
            f'<path d="M32 63 L45 75 L69 50" fill="none" stroke="{c["line"]}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')

def goal_u(fname, size, c, x0=0):
    """The 'u' of the wordmark, read top-down as a goal, with the ball inside."""
    runs, tb = glyph_runs(fname, 'u', size)
    _, d, b, _ = runs[0]
    # ball sits in the counter, just above the bowl
    cx = (b[0] + b[2]) / 2
    stem = size * 0.215
    r = (b[2] - b[0] - 2*stem) / 2 * 0.78
    cy = b[3] - stem - r - size * 0.02
    return d, b, (cx, cy, r)

def icon_goal(c, fname='unbounded'):
    # The u alone, read top-down as a goal mouth with the ball in the net.
    return (f'<rect width="100" height="100" rx="24" fill="{c["primary"]}"/>'
            f'<path d="M29 25 V53 A21 21 0 0 0 71 53 V25" fill="none" stroke="{c["line"]}" stroke-width="15" stroke-linecap="round"/>'
            f'<circle cx="50" cy="52" r="9" fill="{c["accent"]}"/>')

# ---------- concepts ----------

CONCEPTS = [
    dict(id='pitch-pin', name='Pitch Pin', font='outfit', icon=icon_pin, tracking=-1,
         primary='#14904F', line='#FFFFFF', ink='#0C3A23', ink_dark='#F2F7F1'),
    dict(id='chalk-f', name='Chalk F', font='unbounded', icon=icon_chalk_f, tracking=0,
         primary='#0F6E3E', line='#F4F8EC', ink='#0F2A1C', ink_dark='#F4F8EC'),
    dict(id='matchday-stripes', name='Matchday Stripes', font='saira', icon=icon_stripes, tracking=0,
         primary='#1C9A52', stripe='#23AE5E', line='#FFFFFF', ink='#0B3320', ink_dark='#F1F8F0'),
    dict(id='booked-slot', name='Booked Slot', font='bricolage', icon=icon_slot, tracking=-1.5,
         primary='#14233F', accent='#2DC26B', line='#FFFFFF', ink='#14233F', ink_dark='#EEF3FA',
         dark=dict(primary='#243A66')),
    dict(id='goal-u', name='Goal U', font='unbounded', icon=icon_goal, tracking=0,
         primary='#0E1F17', line='#FFFFFF', accent='#3DDC7A', ink='#0E1F17', ink_dark='#F3F7F4',
         ball='#18A957', dark=dict(primary='#18A957', accent='#0E1F17')),
]

def lockup(c, ink, ball=None):
    """Icon (100 tall) + wordmark, text block vertically centred on the icon."""
    size = 100
    body_w, runs, tb = wordmark(c['font'], size, c['tracking'], ink,
                                skip=('u',) if c['id'] == 'goal-u' else ())
    asc = -tb[1]                      # ascender height above baseline
    target = 62                       # ascender height in icon units
    s = target / asc
    baseline = 50 + target/2 + (4 if c['id'] == 'goal-u' else 0)
    gap = 24
    tx = 100 + gap - tb[0]*s
    extra = ''
    if c['id'] == 'goal-u':
        u = next(r for r in runs if r[0] == 'u')
        d, b, (cx, cy, r) = goal_u(c['font'], size, c)
        extra = (f'<g transform="translate({u[3]:.2f} 0)"><path fill="{ink}" d="{d}"/>'
                 f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{ball or c["ball"]}"/></g>')
    width = tx + tb[2]*s + 4
    body = (f'<g>{c["icon"](c)}</g>'
            f'<g transform="translate({tx:.2f} {baseline:.2f}) scale({s:.4f})">{body_w}{extra}</g>')
    return svg(round(width, 1), 100, body, 'futly')

def wordmark_only(c, ink, ball=None):
    size = 100
    body_w, runs, tb = wordmark(c['font'], size, c['tracking'], ink,
                                skip=('u',) if c['id'] == 'goal-u' else ())
    extra = ''
    if c['id'] == 'goal-u':
        u = next(r for r in runs if r[0] == 'u')
        d, b, (cx, cy, r) = goal_u(c['font'], size, c)
        extra = (f'<g transform="translate({u[3]:.2f} 0)"><path fill="{ink}" d="{d}"/>'
                 f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{ball or c["ball"]}"/></g>')
    pad = 4
    w, h = tb[2]-tb[0] + 2*pad, tb[3]-tb[1] + 2*pad
    body = f'<g transform="translate({pad - tb[0]:.2f} {pad - tb[1]:.2f})">{body_w}{extra}</g>'
    return svg(round(w, 1), round(h, 1), body, 'futly')

manifest = []
for c in CONCEPTS:
    d = os.path.join(OUT, c['id']); os.makedirs(d, exist_ok=True)
    files = {
        'icon.svg': svg(100, 100, c['icon'](c), 'futly'),
        'lockup.svg': lockup(c, c['ink']),
        'lockup-on-dark.svg': lockup({**c, **c.get('dark', {})}, c['ink_dark'], ball=c.get('accent')),
        'icon-on-dark.svg': svg(100, 100, c['icon']({**c, **c.get('dark', {})}), 'futly'),
        'wordmark.svg': wordmark_only(c, c['ink']),
    }
    for n, s in files.items():
        open(os.path.join(d, n), 'w').write(s)
    manifest.append({'id': c['id'], 'name': c['name']})
print(json.dumps(manifest))
