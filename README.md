# Chuck’s casse-croûte

A one-page restaurant website built with Bootstrap 5.3.8, original Chuck’s artwork, and lightweight SVG and viewport animation.

Live site: https://loogart.github.io/chucks/

## Edit and preview

All menu items, hours, contact details and links are ordinary HTML in `index.html`. Branding is in `style.css`; interactions are in `script.js`. Bootstrap and fonts are bundled locally. No installation or build step is needed.

```sh
python3 -m http.server 4173
```

Open http://localhost:4173. See `EDITING.txt` for the full editing guide.

## Artwork and motion

The character SVGs are in `assets/`. `tools/rig-chef.py` regenerates the animated and static mascot variants. The footer version has white burger buns and a viewBox aligned to the character’s soles. The header logo animates on hover and keyboard focus. Reduced-motion preferences are respected.

## Publish

GitHub Pages can publish directly from the `main` branch, root folder. `.nojekyll` keeps this a plain static site. Future commits to `main` update the live site.

## Credits

Logo and website design: [Loogart](https://loogart.com). Restaurant content and photos: Chuck’s casse-croûte. Bootstrap retains its bundled MIT license in `vendor/bootstrap/LICENSE.txt`.
