# figma-build

A [Claude Code](https://claude.com/claude-code) skill that sets up Figma files a designer can
actually design in.

Ask Claude to "put this in Figma" and it builds a file where every text, image and ground is its
own flat layer, colors are real variables, and sections reorder by drag. Claude sets up the parts.
You make the design calls.

Made by [Claire Mull](https://clairemull.com), a product designer, while building her own
portfolio and a shop website with Claude.

## Two ways in

- **The thing exists** (a live web page, an app screen): Claude captures it section by section
  and flattens it. Nothing is redrawn, so type, spacing and color match the real page exactly.
- **It is still an idea** (notes, a brief, a sketch, a doc; a page, a menu, a poster, a
  package): Claude lays out every real part, styled from a real system, loose on the canvas.
  One plain starting arrangement, never a set of options to pick from.

Either way the file ends with an "About this file" card, NEED notes where copy is missing, and a
screenshot check of every section before Claude reports back.

## What you need

- Claude Code
- Figma's official MCP server, connected to Claude Code (Figma's plugin for Claude Code sets it
  up). Capture mode uses its `generate_figma_design` tool; both modes use `use_figma`.
- For capture mode only: Google Chrome and Python 3. On a Mac with Chrome in Applications it
  just works; anywhere else, set `CHROME` to Chrome's binary.

## Install

```sh
git clone https://github.com/clairemullacelia/figma-build-skill.git
cp -r figma-build-skill/figma-build ~/.claude/skills/
```

Restart Claude Code, then ask for something like "lay this brief out in Figma" or "put my
homepage in Figma so I can rearrange it".

## What is inside

| File | What it does |
|---|---|
| `figma-build/SKILL.md` | The rules: flat layers, copy first, styles from the real system |
| `figma-build/capture.md` | Capture mode, step by step |
| `figma-build/idea.md` | Idea mode, step by step |
| `figma-build/traps.md` | Figma API traps found in real builds, so you skip them |
| `figma-build/scripts/capture.py` | Sends page sections to Figma, four at a time |
| `figma-build/scripts/flatten.js` | Turns a captured section into flat layers, pixel for pixel |
| `figma-build/scripts/shot.py` | Full-page screenshots at a real viewport size |

## License

MIT. Use it, change it, share it.
