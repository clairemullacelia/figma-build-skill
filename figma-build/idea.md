# Idea mode: the thing does not exist yet

Input can be anything loose: a paragraph, a voice-note transcript, a doc, a photo of a
sketch, reference screenshots, a feature list. Output can be anything with a frame: a web page, an
app screen, a menu, a poster, packaging, a sticker, a slide, a sign. The job is the **parts**:
every real element, styled from a real system, laid out loose so the designer arranges them. Options to
pick from are the failure; one plain starting arrangement is the floor, the designer's arrangement is
the design.

## Steps

1. **Pin down the thing.** What it is, its frame, who it is for, where it lives (screen, print,
   wall). Ask only what the input leaves open, in one round, in plain words. The frame comes from
   the medium:

   | Medium | Frame |
   |---|---|
   | Web page | 1440 wide, height grows |
   | Phone screen | 390 × 844 |
   | Letter / A4 print | 612 × 792 / 595 × 842 (points) |
   | Anything measured in inches | inches × 72, named with the real size ("Menu · 8.5 × 14 in") |

   Print pieces get a 9 pt bleed frame and a safe-area frame as locked guides.

2. **Copy first.** If the words do not exist, draft them in a doc from the user's input only (no
   invented claims, no invented numbers) and wait for their edit. Gaps they leave become NEED notes.

3. **The style source.** Ask which system it wears: a site, an app, a brand file, or something
   else. When the user names one, read its tokens from its source (CSS, brand README,
   design log) into a variable collection and text styles named for it. When none exists, ask, and
   offer a **starter kit** as the second option: three to five colors and two type pairings taken
   from their references or the subject, laid out as a kit page they edit. They pick or rewrite it;
   only then does it become variables and styles. The kit is a proposal on its own page, never
   applied to the parts unasked.

4. **Inventory the parts.** Every piece of copy (from the doc), every image and mark (from the
   repo or their uploads, each one looked at before use), every repeated element (a price row, a
   card, a label, a button). Real assets upload with `upload_assets` and are resized to their true
   aspect (see traps.md). A missing asset is a named gray slot ("[photo of the counter]").

5. **Build the parts page.** A section "Parts" left of the frame, grouped by kind: Copy (each
   block its own text layer, in its text style), Images, Marks, Components (repeated elements as
   components, stacking only inside themselves), Styles (the color chips and type specimens of the
   system). Everything named for what it is.

6. **One plain arrangement.** The frame gets every part once, in reading order, on the system's
   ground, flat (each layer placed by x and y, sections as plain frames in the column for anything
   long). It is a starting point they can tear up, so it stays plain: the system's own scale and
   spacing, nothing clever. If they gave a sketch, it sits under everything as a locked layer at 30%
   opacity named "Your sketch (reference, locked)", and the arrangement follows it.

7. **Hand over and read back.** Finish per SKILL.md, then wait. When they say it is arranged, read
   the frame back (structure plus screenshot) and build what they made. If it becomes a live page,
   capture mode takes over from then on.
