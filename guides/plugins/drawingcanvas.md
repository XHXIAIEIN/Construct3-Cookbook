# Event Sheet Pitfalls: Drawing canvas

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- If *Convex* is off, Drawing Canvas *Fill polygon* draws nothing when two
  consecutive points of the polygon coincide. A closing point that repeats
  the first point is such a pair. The rest of the sheet keeps running, and
  no error is logged. If *Convex* is on, the same points fill. So add a
  closing point only if it is a point of its own, or count the points in a
  variable and loop over that count. A convex shape can also tick *Convex*.
  [observed in a game project, r502 preview, 2026-09-24; observed in a
  minimal project, r504 preview, 2026-10-02: a square filled 5776 pixels,
  the same square with its first point, a middle point or a closing point
  repeated filled 0, and all three filled 5776 with *Convex* on; r507 beta
  drawCommand.js removes repeated consecutive points when *Convex* is off]
- *Fill poly*, *Outline poly* and *Dashed outline poly* draw every point
  added since the last *Reset poly*, and they keep the points. So a loop
  that adds the corners of one piece and fills it on each iteration fills
  one polygon that grows along the whole path: each fill draws every
  earlier piece again inside a shape that is no longer the piece. Run
  *Reset poly* before the first *Add poly point* of each polygon.
  [manual: plugin-reference/drawing-canvas.md; observed in a game project,
  r506.3 preview, 2026-10-28]
- *Line*, *Dashed line*, *Outline poly* and *Dashed outline poly* take a
  butt or a square line cap and no other, and one thickness per action. So
  a thick polyline drawn as one *Line* per segment shows a notch on the
  outside of every bend, and a ribbon whose width changes along its length
  cannot be a line at all. Fill such a path as quads instead: at each
  point, take the direction from the point before to the point after,
  turn it a quarter turn, and scale it to half the width there, which
  gives the point's two edge points. Then fill each piece between two
  neighbouring points with four *Add poly point* actions and *Fill poly*,
  after a *Reset poly*. Keep the points and their edge offsets in an Array
  with one column per point. [schema `drawingcanvas.json`, `line-cap`:
  butt | square; observed in a game project, r506.3 preview, 2026-10-28]
- Draw the shapes of one layer on one Drawing Canvas, back to front in the
  order of the events, not on one full-screen canvas each. In a game
  project, five full-screen canvases with 4x MSAA, one per ribbon and each
  cleared every tick, became one canvas with 4x MSAA that draws all five
  ribbons. With the pointer moving, the ticks per second at an unlimited
  frame rate went from 2417 to 2774, and GPU use at pixel ratio 2 from
  0.10 to 0.13 down to 0.03. [observed in a game project, headless Chrome
  preview at 1280x720, medians of three rounds, 2026-10-28]
- *Antialiasing* costs every pixel of the canvas on every frame, so on a
  canvas the size of a large screen it slows the whole game. In a game
  project at about 3840x2054 device px, 2x or 4x MSAA on one full-screen
  canvas held the preview at about 92 fps, with frames of 7 and 14 ms
  alternating, where the same canvas without it ran at 144 fps. At
  1280x720, off, 2x and 4x measured alike. Leave *Antialiasing* off on a
  large canvas unless its edges need it, and measure at the size of the
  player's screen before turning it on. [manual:
  plugin-reference/drawing-canvas.md, "Antialiasing"; observed in a game
  project, r506.3 preview, 2026-10-28]
