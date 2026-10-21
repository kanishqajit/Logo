# futly logo concepts

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
