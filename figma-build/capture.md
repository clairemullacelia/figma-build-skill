# Capture mode: the thing exists

The live thing is the source. Every style, spacing, label and caption comes from it; nothing is
redrawn.

## Steps

1. **Read the copy and the order.** The user's doc (whatever holds the copy) and the brief. List
   every section of the target order and where each comes from: a live section, half of one, or
   new. Show the user that table before building when the order differs from the live page.
2. **Capture.** If the file already holds a capture of the current page, use it. Otherwise:
   serve a production build locally, call `generate_figma_design` once per section for a capture
   id, write `jobs.json` (`url`, `selector`, `id` per section), and run
   `python3 <this skill's folder>/scripts/capture.py jobs.json` (needs Google
   Chrome; set `CHROME` to its binary if it is not in /Applications). One frame per section.
   Never paste Figma's script into the site's source.
3. **Set up the target page.** A fresh page first in the file; the previous layout renamed as an
   archive. A variable collection named for the system (e.g. "Portfolio colors"), one variable
   per token in the site's CSS, each with its CSS name in the description and narrow scopes
   (fills, text, strokes). A NEED note component in a "Components" section left of the column.
4. **Flatten into the column.** Create the column (vertical auto layout, spacing 0, fixed width,
   hugging height, ground bound to the paper variable). For each section in order: clone the
   captured frame, append it, run `flatten` from [scripts/flatten.js](scripts/flatten.js), name it
   `NN Chapter · part`. Batches of about eight sections per call; return each section's children
   (name, id, x, y, size) for the edit pass. Screenshot one flattened section against its original
   first: they should be identical.
5. **Cut and split.** A section that holds two parts of the new order is cloned twice, and each
   clone deletes the other part and shifts up. Retired material (old structure labels, step
   numerals of a retired walk) is deleted, never hidden.
6. **Edit the copy** to the doc: load the text's own fonts, set `characters`; a bold lead is
   `setRangeFontName(0, lead.length, {family, style:'Bold'})`. Then `fit` the section.
7. **New parts are clones of captured parts**: a row heading, a body, an image frame, a caption,
   a placeholder ground. Clone, place, set words and fills. They carry the page's exact type and
   color. New sections are new frames in the column built only from such clones.
8. **Bind colors**: walk the column; every SOLID fill whose hex equals a token is replaced by
   `setBoundVariableForPaint` with its variable. Skip brand swatches that are content. Texts in
   fonts the cloud lacks throw here: count them and name them in the About card.
9. Finish per SKILL.md.

## Splitting a captured section

Line up the cut by the children list from step 4: everything above the cut y stays in one clone,
everything below in the other. Shift the kept half so its first element sits where the
section's top padding was.
