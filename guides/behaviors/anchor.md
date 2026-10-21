# Event Sheet Pitfalls: Anchor

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- Under *Scale outer* the screen shows more than the *Viewport size* on its
  longer side, split evenly. A parallax 0, 0 layer is centred on the original
  viewport too. So a HUD placed at the top of the viewport stays at the top
  of the design area, not at the top of a taller screen, and the layout
  beyond the viewport shows on the sides. Pin an edge HUD with the Anchor
  behavior on that layer. In a layout of the viewport's size, the game stays
  centred only with *Unbounded scrolling* on. Bounded, the camera keeps the
  layout's left and top edges on the screen's, so the game slides left or up
  from the centred HUD. If a backdrop must reach the screen's sides, give
  it Anchor with *Left edge* Viewport left and *Right edge* Viewport right.
  The right edge resizes it to the screen's width, so lay it out a little
  wider than the viewport, not thousands of pixels past the layout. A shaking
  camera moves the viewport, and 20 px past each side covers a shake of 8.
  Anchor moves a left edge without resizing. So if a piece grows to one side
  only, its other end fixed, set it under *On start of layout* OR Browser *On
  resized*. Set its width to `Self.BBoxRight - ViewportLeft(layer) + 20`,
  then its X to `ViewportLeft(layer) - 20`. [manual:
  behavior-reference/anchor.md; observed in a game project, a 430×932
  portrait export switched to *Scale outer* and shown at 560×380 and 300×700
  in Chrome, 2026-09-30; the Anchor backdrop and the one-sided piece
  previewed at 900×500 and 330×800 and after a resize, r504, 2026-09-30;
  a 1920×1080 one-screen layout previewed at 1600×700, r495.2, 2026-10-08:
  bounded, `scrollX` was 1234 and the world layer's viewport started at 0
  while the HUD layer's started at -274; unbounded, both started at -274]
