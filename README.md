# futly logo concepts

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
