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
- *Fill polygon*, *Draw polygon outline* and *Draw dashed polygon
  outline* draw every point added since the last *Reset polygon*, and they
  keep the points after they draw. So a loop that adds the corners of one
  piece and fills it on each iteration draws every earlier piece again with
  the new one, as one polygon that grows along the path. Run *Reset
  polygon* before the first *Add polygon point* of each polygon.
  [manual: plugin-reference/drawing-canvas.md; observed in a game project,
  r506.3 preview, 2026-10-28]
- *Draw line*, *Draw dashed line* and the polygon outline actions take a
  butt or a square line cap and no other, and one thickness per action. A
  thick polyline drawn as one *Draw line* per segment therefore shows a
  notch on the outside of every bend. A ribbon whose width changes along
  its length cannot be a line at all. Fill such a path as pieces instead:
  1. Keep the points in an Array with one column per point, and a row for
     each coordinate of the offset to the edge.
  2. At each point, take the direction from the point before to the point
     after, turn it a quarter turn, and scale it to half the width there.
     That offset, added and subtracted, gives the point's two edge points.
  3. For each pair of neighbouring points, run *Reset polygon*, four *Add
     polygon point* actions at their edge points, and *Fill polygon*.

  [schema `drawingcanvas.json`, `line-cap`: butt | square; observed in a
  game project, r506.3 preview, 2026-10-28]
- Draw the shapes of one layer on one Drawing Canvas, back to front in the
  order of the events, not on one full-screen canvas each. One canvas that
  draws every shape costs less than one canvas per shape, each cleared
  every tick. [observed in a game project, headless Chrome preview at
  1280x720, 2026-10-28: five full-screen canvases with 4x MSAA, one per
  ribbon, against one canvas with 4x MSAA that drew all five; with the
  pointer moving, medians of three rounds went from 2417 to 2774 ticks per
  second at an unlimited frame rate, and GPU use at pixel ratio 2 from
  0.10-0.13 to 0.03]
- *Antialiasing* works on every pixel of the canvas on every frame, so on
  a canvas the size of a large screen it holds the frame rate below the
  display's. Leave it off on a large canvas unless its edges need it, and
  measure at the size of the player's screen before you turn it on.
  [manual: plugin-reference/drawing-canvas.md, "Antialiasing"; observed in
  a game project, r506.3 preview, 2026-10-28: at about 3840x2054 device
  px, 2x or 4x MSAA on one full-screen canvas held the preview at about 92
  fps, frames of 7 and 14 ms alternating, against 144 fps without it; at
  1280x720, off, 2x and 4x measured alike]
