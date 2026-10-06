---
name: figma-build
description: Build a Figma file a designer or a team can edit and drag freely. Two ways in. A thing that already exists (a live page, an app screen) is captured and edited, never redrawn. A loose idea (notes, a brief, a sketch, a doc; a page, menu, poster, package, slide) is laid out as styled loose parts for the designer to arrange. Use when the user says "put this in Figma", "lay this out in Figma", "rebuild the Figma file", or wants an idea set up in Figma. Phone layouts too: 390 wide, on their own page.
---

# figma-build

The user is the designer. This skill sets up the **parts** and the **column** they design with:
it lays out real copy, real assets and real styles as **flat** layers, and the designer makes
the calls.

## First question: does the thing exist?

Ask it of the request before anything else, and say the answer to the user in one line.

- **It exists** (a live page, a running screen, a shipped print piece with a source file):
  **capture mode**. Read [capture.md](capture.md). The live thing is the source of every style
  and detail.
- **It does not exist yet** (an idea, notes, a sketch, a brief, a list): **idea mode**. Read
  [idea.md](idea.md).
- Both (an existing page with new sections): capture mode for what exists, idea mode for the
  new parts, built from clones of captured parts.

## Phone (390 wide)

Phone is part of this skill. One width: **390**.

- **Its own page**: "<name> · Phone". The desktop page is never touched.
- **A live page at phone width**: capture mode at 390 (see capture.md, "Phone"). Sections keep
  the desktop section names.
- **A page that exists only in Figma**: ask the user each time. Build desktop live and capture
  the phone, or restack the desktop Figma into a 390 column before any code.
- **App screens** (a web app, or a mobile app that runs in a browser): capture at 390 × 844
  signed in, with a saved sign-in (capture.md, "Signed-in pages"). Each screen gets a drawn
  status bar as its own deletable layer. Parts the phone draws itself (keyboard, share sheet,
  system alerts) become named empty slots.
- **A new phone idea**: idea mode, 390 × 844 frame.
- **Building code from a phone layout**: a phone change must not touch desktop. Media-query
  overrides only, and desktop proven unchanged at 1440 by screenshot.

## Rules for both modes

- **Styles come from the thing's own system.** A case study about a client's shop wears the
  portfolio's styles; the shop's colors and fonts appear only as content (swatches, specimens,
  screenshots). When a brief line contradicts what the page plainly is, ask before building.
- **Copy first.** Copy comes from the user's doc or brief. Missing copy is drafted into a doc for
  their edit before anything visual. Gaps left at build time become **NEED notes** in place.
- **Flat.** The file is one **column**: a vertical auto-layout frame whose children are the
  sections, so a section reorders by drag in the Layers panel. Inside a section every text,
  image and ground is its own layer placed by x and y, with no auto layout. Small repeated parts
  (a NEED note, a price row) are components that stack only inside themselves.
- **Styles are built in.** Colors are variables in one collection named for the system, read from
  its source (the site's CSS, a brand file). Every fill that matches a token is bound to it.
- **Look at every image before placing it.** Crop file names lie. Lay a set out on one HTML page
  and screenshot it with `scripts/shot.py` to check it in one picture.
- **Keep, never delete.** A previous layout becomes an archive page ("Archive · <date> <what>").
- **The designer's decisions are locked.** Build the order and copy they gave; a better idea is a
  sentence to them, not a change in the file.

## Finishing

The build is done when all of these hold:

1. Every section in the given order is in the column, every word matches the source copy, and
   every gap is a NEED note or a named empty slot.
2. An **About this file** card sits right of the column: how to reorder, move, swap images, which
   variables and styles exist, what the NEED notes are, what is TO CHECK (stand-in fonts, matched
   colors).
3. **Checked by picture**: each section screenshotted at about 0.3 and compared to its source or
   brief, then the whole column once. Each fix gets one more screenshot. Overlaps, clipped text,
   wrong crops and misnamed images are fixed before reporting.
4. The user gets the link to the page, what it holds, what is theirs to do, and what the check
   did not cover.
5. A new Figma trap goes into [traps.md](traps.md) the same session.

Figma API traps that cost time before: [traps.md](traps.md). Read it before the first `use_figma`
call of a build.
