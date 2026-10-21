# futly logo concepts

## Identity v2: geometric ball-terminal f (current)

`brand-v2/` holds a geometric identity built from bars and one radius pair
(outer radius = 2 × stroke, inner = 1 × stroke), after the balance of the
Futspot reference (not its shapes). The f's ball terminal is the ball,
placed on the hook's centre line a quarter-stroke past its end.

- `futly-symbol-black.svg`, `futly-wordmark-black.svg`
- `futly-lockup-{chalk-volt,black,white}.svg`: symbol spans ascender to baseline, gap 1.5 strokes
- `slides/`: six 1080×1350 presentation slides (SVG + PNG)

Built by `tools/build_geo.py` and `tools/build_geo_slides.py` (needs `shapely`
for the outlined grid slide). Colours: pitch-night #141A17, chalk #EEF1EC,
volt #C8F23C (the ball only).

## futly brand v1.0 (pixel)

`brand/` holds the refined identity, built by `tools/build_brand.py`:
a custom pixel wordmark (10 px x-height, 2 px strokes, 1 px corner steps,
extended proportions after the user's reference) and an indigo-to-violet
floodlight beam centred on the t.

- `futly-wordmark-{white,black,indigo}.svg`: the logo
- `futly-signature.svg`: wordmark with its beam, transparent background
- `futly-app-icon.svg` / `futly-app-icon-flat.svg`: app icon (flat for small sizes)
- `futly-symbol-black.svg`: one-colour f
- `futly-hero.svg`: launch artwork (uses a grain filter; not a logo master)

Colours: Night #06070A, Floodlight #3A34FF, Afterglow #8E4BFF, Chalk #F4F4F7,
beam #14109E → #3A34FF → #8E4BFF.

## Round 3: professional concepts (current)

`concepts/round3/` holds three concepts built with the logo-design skill on
one pixel system (`tools/build_round3.py`), drawn black first and tested
(`sheets/test-sheet.png`). Earlier iterations are kept as `-v1`/`-v2`/`-v3`.

- **A, Slot f (recommended):** booked cells in a 5×5 booking grid spell a
  lowercase f; the single round cell at its foot is the ball. A fused
  small-size cut (`a-slot-f-symbol-small.svg`) is for 16–24 px.
- **B, Full Time:** f and t share one crossbar, the "FT" every scoreboard
  shows at full time.
- **C, Net u:** the u, seen from above, is a goal with the ball in the net.

## Round 2: scoreboard pixel

`concepts/scoreboard-pixel/` holds a custom pixel wordmark for futly, after the
user's reference: white letters on a pixel grid with a vertical light bar
behind them, built like the lights on a stadium scoreboard.

- `hero-<colour>.svg`: wordmark over the light bar (`night-match`, `floodlight`, `scoreboard-amber`)
- `hero-led-<colour>.svg`: the same, with LED-bulb letters
- `icon-<colour>.svg`: app icon, pixel f on the light bar
- `led-white.svg`, `led-amber.svg`: dot-matrix wordmark on a scoreboard panel
- `wordmark-white.svg`, `wordmark-ink.svg`: plain wordmark for dark and light backgrounds

The letters are drawn as pixel grids in `tools/build_pixel.py` (no fonts
needed); run `python3 tools/build_pixel.py` to regenerate.

## Round 1

Five logo directions for futly, a platform for booking turfs. Each folder in
`concepts/` holds outlined SVGs (no font files needed):

- `icon.svg`: the symbol on its own (app icon, favicon, avatar)
- `icon-on-dark.svg`: symbol tuned for dark backgrounds
- `lockup.svg`: symbol + wordmark on light backgrounds
- `lockup-on-dark.svg`: symbol + wordmark on dark backgrounds
- `wordmark.svg`: the name on its own

| Concept | Idea |
| --- | --- |
| `chalk-f` | The F of futly drawn as pitch markings, middle arm ending in the kick-off circle. **Recommended.** |
| `pitch-pin` | A map pin holding a top-down pitch: "there's a turf near you". |
| `matchday-stripes` | Mowed-turf stripes behind a forward-leaning italic f. |
| `goal-u` | The u in futly, seen from above, is a goal with the ball in the net. |
| `booked-slot` | A calendar page with a tick, in navy and turf green: "your slot is booked". |

## Regenerating

`tools/build_logos.py` draws every file. It needs `fonttools` and these Google
Fonts TTFs in `fonts/` (or a folder named by `FUTLY_FONTS`): `outfit.ttf`
(Outfit 600), `unbounded.ttf` (Unbounded 700), `saira.ttf` (Saira 800 italic),
`bricolage.ttf` (Bricolage Grotesque 700).

```sh
pip install fonttools
python3 tools/build_logos.py concepts
```

## Logo design skill

`.claude/skills/logo-design/` is the
[logo-design skill](https://github.com/kaankiziltug/logo-design-skill) (v1.4.5,
MIT), vendored so Claude Code sessions in this repo can use it. Its PNG
renderer needs `pip install cairosvg` (or librsvg / Inkscape).
