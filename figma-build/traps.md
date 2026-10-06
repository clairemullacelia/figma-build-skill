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

## Capture
- Every captured section arrives named "Section (<page title>)", and the node ids do not follow
  the order of `jobs.json`. Match each one by the node id in its own completed
  `generate_figma_design` result (or by height), then rename it before flattening.
- A capture into a file that already has the color variables arrives with its fills already
  bound to them. The bind step then binds 0, which is correct, not a failure. Check one fill's
  `boundVariables` before worrying.

## Process
- Screenshot inside `use_figma` with `node.screenshot({scale:0.3})`; several per call is fine.
- Page context resets every call: `await figma.setCurrentPageAsync(page)` at the top of each.

## Reading a file back into code
- A capture is a picture of the page, not the page. It loses what code does: an overlay, a
  coded drawing, hover, click-to-enlarge, a fold. For a section that already exists live, build
  from the live code and apply only the designer's Figma edits. Build from the Figma only what
  is new.
- Diff every text layer against the live text before building. A missing row is a question, not
  an assumption. A layer pushed below its section's clip edge is hidden in Figma but not deleted.
- Get original images with `download_assets` (`rawImages`), not `get_screenshot`, which returns
  1x and is capped at the node's size. Match each fill to a local file by pixel size.
- Deleting a child can reflow a CSS grid that places parts by explicit row. Keep an invisible
  zero-height placeholder in the removed slot, then screenshot to prove the order.
