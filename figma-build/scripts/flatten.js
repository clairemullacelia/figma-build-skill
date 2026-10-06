// Paste into a use_figma call. Turns a captured section (nested auto layout) into one flat frame:
// every text, image and wrapper-free leaf keeps its exact place; every wrapper that painted a
// ground or a stroke becomes a plain rectangle "<name> · ground"; empty wrappers are deleted.
// Proved identical by screenshot on a real multi-section case study page.
//
// Usage inside the call:
//   const S = (await figma.getNodeByIdAsync(CAPTURED_ID)).clone();
//   column.appendChild(S); flatten(S); S.name = '04 Branding · the logo';
//   S.clipsContent = true; S.layoutSizingHorizontal = 'FIXED';
//
// Fonts: moving and resizing a text needs no font load, so labels in fonts Figma's cloud lacks
// (Menlo) survive. Never set textAutoResize, characters or fills on those here.

const abs = n => { const t = n.absoluteTransform; return { x: t[0][2], y: t[1][2] }; };
const hasText = n => n.type === 'TEXT' || ('findOne' in n && !!n.findOne(x => x.type === 'TEXT'));
const paintVis = arr => Array.isArray(arr) && arr.some(p => p.visible !== false && (p.opacity === undefined || p.opacity > 0));
const decor = n => paintVis(n.fills)
  || (paintVis(n.strokes) && (typeof n.strokeWeight !== 'number' || n.strokeWeight > 0)) // strokeWeight can be figma.mixed
  || (Array.isArray(n.effects) && n.effects.length > 0);

function flatten(S, width = 1440) {
  const so = abs(S); const items = [];
  (function collect(n) {
    for (const c of n.children) {
      if (!c.visible) continue;
      if (c.type === 'TEXT' || !('children' in c) || !hasText(c)) items.push({ kind: 'move', n: c }); // a leaf, or an image/vector group kept whole
      else { if (decor(c)) items.push({ kind: 'bg', n: c }); collect(c); }
    }
  })(S);
  // record every position BEFORE moving anything: moving reflows the auto-layout parents
  for (const it of items) { const a = abs(it.n); it.x = a.x - so.x; it.y = a.y - so.y; it.w = it.n.width; it.h = it.n.height; }
  const H = S.height; S.layoutMode = 'NONE'; S.resize(width, H);
  const orig = [...S.children];
  for (const it of items) {
    if (it.kind === 'bg') {
      const r = figma.createRectangle(); S.appendChild(r);
      r.name = it.n.name.replace(/^(Spacing|Block|Group|Text) · /, '') + ' · ground';
      r.resize(Math.max(1, it.w), Math.max(1, it.h)); r.x = it.x; r.y = it.y;
      r.fills = it.n.fills; r.strokes = it.n.strokes;
      if (typeof it.n.strokeWeight === 'number') r.strokeWeight = it.n.strokeWeight;
      else { try { r.strokeTopWeight = it.n.strokeTopWeight; r.strokeBottomWeight = it.n.strokeBottomWeight; r.strokeLeftWeight = it.n.strokeLeftWeight; r.strokeRightWeight = it.n.strokeRightWeight; } catch (e) {} }
      try { r.topLeftRadius = it.n.topLeftRadius; r.topRightRadius = it.n.topRightRadius; r.bottomLeftRadius = it.n.bottomLeftRadius; r.bottomRightRadius = it.n.bottomRightRadius; } catch (e) {}
      r.effects = it.n.effects; r.opacity = it.n.opacity;
    } else {
      const n = it.n; S.appendChild(n); n.x = it.x; n.y = it.y;
      if (n.type !== 'TEXT' || n.textAutoResize !== 'WIDTH_AND_HEIGHT') {
        if (Math.abs(n.width - it.w) > 0.5 || Math.abs(n.height - it.h) > 0.5) { try { n.resize(Math.max(1, it.w), Math.max(1, it.h)); } catch (e) {} }
      }
    }
  }
  const moved = new Set(items.filter(i => i.kind === 'move').map(i => i.n.id));
  for (const o of orig) if (!moved.has(o.id)) o.remove();
}

// After edits, size a section to its content:
function fit(S, pad = 120) { let m = 0; for (const c of S.children) m = Math.max(m, c.y + c.height); S.resize(S.width, Math.ceil(m + pad)); }
