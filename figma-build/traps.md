# Figma traps that cost time

Each was hit in a real build. Add new ones the session they happen.

## Fonts
- **Figma's cloud runtime has no Menlo** (or other Mac system fonts). Moving, resizing and
  deleting such a text works; `characters`, `textAutoResize`, fills and text styles throw. Leave
  those layers as captured; new mono text uses a cloud font (Source Code Pro) named in the About
  card as a stand-in.
- Check style names with `listAvailableFontsAsync` before loading ("SemiBold" vs "Semi Bold").

## Layout
- **A height change on a layer inside a component copy is silently ignored** (`resize` returns the
  old size). Make the component a fixed-height frame whose image FILLs it, and resize the copy.
- A component built from other component copies has the same problem one level down: use loose
  copies side by side instead.
- `resize(w, h)` on a hugging copy freezes its height: set `primaryAxisSizingMode = 'AUTO'` after.
- `strokeWeight` can be `figma.mixed` (a symbol): test `typeof === 'number'` before comparing.
- An automatic "push down whatever overlaps" pass wrecks side-by-side layouts. Fix overlaps by eye
  from the screenshot.

## Images
- `upload_assets` frames arrive 400 × 300 whatever the image's shape. Read the true size with
  `figma.getImageByHash(hash).getSizeAsync()`.
- POST uploads as multipart (`-F file=@name`) so the file name becomes the layer name.
- `upload_assets` with `nodeIds` cannot target a layer inside a component copy: upload loose, then
  copy the `imageHash` into the copy by script.
- SVGs using `currentColor` import empty or black: replace it with a hex before uploading.
- **Crop file names lie** (`new-hero.jpg` was the shawarma band). Contact-sheet every set first.

## Shell
- zsh does not split `$list` into words in a `for` loop: run upload loops under `bash -c` with
  arrays.
- `sips -c` crops from the center and `--cropOffset` does not move it. To keep the top of a
  capture, crop with Python (Pillow) or take the shot with `scripts/shot.py --clip-sel`.
- `sips -Z` ignores EXIF orientation; check portrait photos after resizing.

## Process
- Screenshot inside `use_figma` with `node.screenshot({scale:0.3})`; several per call is fine.
- Page context resets every call: `await figma.setCurrentPageAsync(page)` at the top of each.
