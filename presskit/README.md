# Press Kit Site

`index.html` is a single self-contained page (inline CSS, Google Fonts for Bebas Neue + Inter,
images in `screenshots/`). No build step, no framework, no backend needed.

Layout follows the classic presskit() convention (the Streets of Rage 4 press kit format):
sticky left nav rail, right column running Factsheet -> Description -> History -> Features ->
Videos -> Screenshots -> Logo & Icon -> About -> Contact -> Launch List, restyled in the
game's dark void / lavender / neon palette.

`screenshots.zip` is the press download bundle (gallery + logos). Regenerate it whenever the
screenshots folder changes:

```bash
cd presskit && python -c "
import zipfile, os
with zipfile.ZipFile('screenshots.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for fn in sorted(os.listdir('screenshots')):
        if fn.endswith('.png'):
            z.write('screenshots/' + fn, 'misfunction_presskit/' + fn)
"
```

The wordmark PNGs (`logo_stacked_white`, `logo_stacked_pink`, `logo_horizontal_white`) were
rendered from `assets/fonts/BebasNeue-Regular.ttf` via PIL - re-render or replace once the
final title art exists.

## Turn on email signups (5 min, free)

1. Make a free account at https://buttondown.com (free to 100 subscribers).
2. In `index.html`, find the `<form action="...embed-subscribe/MISFUNCTION-LIST-NAME">` tag
   (search for `MISFUNCTION-LIST-NAME` - it appears twice).
3. Replace both occurrences with your Buttondown username.
4. Done. Signups land in your Buttondown list with double opt-in and unsubscribe handled.

Until that's done the form submits to a dead endpoint - the mailto fallback line under it is
the safety net, so nothing breaks for visitors.

## Put it live on GitHub Pages (5 min, free)

Option A - dedicated repo (cleanest URL):
1. Create a new GitHub repo, e.g. `misfunction-presskit`.
2. Copy this whole `presskit/` folder's contents into it (`index.html`, `screenshots/`).
3. Repo Settings -> Pages -> Source: "Deploy from a branch", branch: `main`, folder: `/ (root)`.
4. Live at `https://<your-username>.github.io/misfunction-presskit/`.

Option B - serve from this repo:
1. Rename `presskit/` to `docs/` **only if the `Docs/` folder doesn't conflict** - Windows is
   case-insensitive so they'd collide on this machine. Safer: leave it as `presskit/` and use
   Settings -> Pages -> branch `main`, folder: `/ (root)` won't work since it serves repo root.
   Recommended: Option A. If you do want it in-repo, `Docs/` must go first - not worth it.

Custom domain later (~£10/yr): point `misfunction.game` or similar at the Pages site via a
CNAME file. Not needed day one - the github.io URL is fine inside emails and the deck.

## Content notes

- Everything on the page is copy-pasted from `Active Pitch/fact_sheet.md` and the v3 deck,
  so when the deck changes, this file should follow (search for the fact/mode/quote text).
- Screenshots are pre-art-pass captures. After the art pass, drop new PNGs into `screenshots/`
  with the same filenames and the page updates itself.
- The Stroop demo card ("BLUE" in green ink) is pure CSS - no image - so it can't go stale.
- To add the deck PDF as a download: copy `misfunction_pitch.pdf` into this folder and add
  `<a class="btn ghost" href="misfunction_pitch.pdf">Press kit PDF</a>` to the hero button row.
