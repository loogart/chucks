# Chuck × Loogart — Bon appétit!

A standalone red mascot page with the original Chuck artwork, planted feet, a burger-toss loop, and an unboxed greeting above the mascot. The button leads to https://loogart.com/.

Live site: https://loogart.github.io/chucks/

## Edit and preview

`index.html` is the published homepage. `bon-appetit.html` is the identical standalone page at its own URL. Both include their fonts, styling and animated SVG, so either file also works by itself offline. Keep these two files in sync after editing.

```sh
python3 -m http.server 4173
```

Open http://localhost:4173. The headline, button label and destination are near the start of the body. The button arrow is inline SVG; the greeting is plain text. Reduced-motion preferences show a static mascot and greeting.

The earlier Bootstrap restaurant website remains in Git history; existing supporting assets are retained in this repository.

## Publish

GitHub Pages publishes from the `main` branch, root folder. `.nojekyll` keeps this a plain static site. Commits to `main` update the live page.

## Credits

Original logo, mascot and website design: [Loogart](https://loogart.com).
