# Event Sheet Pitfalls: Coordinates and angles

Sources and the rule for adding an entry are in the index,
[pitfalls/README.md](README.md).

- The origin (0, 0) is the top-left of the layout, and Y grows downwards.
  So up is `Y - n`, gravity pulls towards +Y, and the top of the screen is
  the smallest Y. [manual: tips-and-guides/common-conventions.md "Units"]
- Angles are in degrees. 0 faces right and angles increase clockwise, so
  90 points down, 180 left and 270 (or -90) up. 360 is 0 again, so a
  bullet fired at 360 goes right, and `random(360)` is a full turn. `sin`,
  `cos` and `angle` take and return degrees. Some expressions return
  -180..180 and others 0..360. So compare angles with `anglediff`, *Is
  between angles* or *Is clockwise from*, never with `<`. Normalise with
  `(a + 360) % 360` only where a value must land in 0..360. [manual:
  tips-and-guides/common-conventions.md "Units";
  system-reference/system-expressions.md "Math";
  system-reference/system-conditions.md "Is between angles"]
- `anglelerp(a, b, x)` turns from `a` to `b` by the shorter way. If `b`
  moves while `x` runs from 0 to 1, the direction of turn can reverse. An
  example is an angle that eases back to a rest angle beside an aim that
  follows the pointer. In the tick where `b` passes the opposite of `a`,
  the shorter way reverses, and the angle jumps by up to 360 × `x`
  degrees. Instead, ease an offset from the moving angle. Store the start
  offset as `angle - aim`, then write
  `aim + anglelerp(startOffset, restOffset, x)`. Both offsets stay fixed,
  so the direction cannot reverse, and the result turns with the aim.
  [manual: system-reference/system-expressions.md
  "anglelerp"; the shorter way and its reversal observed in a game project,
  r495.2 preview, 2026-10-14: a sword easing back to rest beside the aim
  jumped between 126 and 176 degrees in one tick when the pointer passed the
  opposite direction early in the ease. With offsets, no tick turned it by
  more than the aim's turn plus the ease's step]
- A sprite is drawn facing right at angle 0. So art painted pointing up
  points a quarter turn counter-clockwise of its target after *Set angle
  toward position*. Paint the art facing right, or add the same 90 degrees
  in every *Set angle*. Do not add a different correction in each event.
  [consequence of the same convention;
  Rotate's speed is positive clockwise: manual behavior-reference/rotate.md
  "Speed"]
- A Bullet's angle of motion and the object's angle are two separate
  values. They change together only while the behavior's *Set angle*
  property is on. 8 Direction and Car have the same property. The Bullet
  moves by a velocity vector. *Set angle of motion* turns that vector and
  keeps its length, so at speed 0 it does nothing. *Set speed* from speed
  0 then starts a vector at angle 0, and the object moves right. So a
  projectile that is created at speed 0 and gets *Set angle of motion*,
  then *Set speed*, flies right whatever its angle. Set the speed first,
  then the angle of motion. [manual:
  behavior-reference/bullet.md "Set angle", "Set angle of motion",
  "AngleOfMotion"; behavior-reference/8-direction.md "Set angle"; Ashley in
  Scirra/Construct-bugs#6105: by design, set the angle of motion again after
  the speed; runtime: exported c3runtime.js r504, Bullet `_SetAngleOfMotion`
  multiplies the new direction by the vector's length, and `_SetSpeed` sets
  dx to the speed and dy to 0 when the length is 0; observed in a game
  project, r504 preview, 2026-10-05: in recorded frames every projectile flew
  right, and with the two actions swapped each flew along its angle]
- A sprite's origin is image point 0. X, Y and the rotation refer to this
  point. The editor puts it at the centre (`originX`, `originY` 0.5 in the
  layout file), so a sprite at the layout's edge shows only half of its
  image. For a muzzle or a hinge, position by an image point. *Spawn
  another object* takes one. Move the origin in the image editor, not by
  an offset in events. [manual:
  interface/animations-editor.md "Image points"; official example layouts]
- Tile movement counts in grid cells, not pixels. *Set grid position* and
  *Can move to* take a column and a row, and `GridX` and `GridY` return
  them. So *Set grid position* to another object's X of 640 sends the
  object to column 640, far off the layout. Convert a layout position with
  `round((X - offset X) / grid width)`, and convert Y the same way with
  the grid height. The object's origin lands on
  `offset X + column × grid width`, with no half cell added. So an object
  that fills its cell has its origin at the top-left.
  [manual: behavior-reference/tile-movement.md, the origin
  aligned with the grid, "Can move to", "Set grid position", "GridX";
  observed in a copy of the official example template-tile-based-game,
  stable r495.2 preview, 2026-10-04: a 32 × 32 grid at offset 0, *Set grid
  position* (3, 2) put the origin at (96, 64)]
- `ViewportLeft`, `ViewportWidth` and the other viewport expressions take
  a layer, because a parallaxed or scaled layer shows a different
  rectangle. Write `ViewportLeft("HUD")`. `LayoutWidth` is the whole
  layout. `ViewportWidth(layer)` is the part on screen, in layout
  coordinates. `OriginalViewportWidth` is the project's *Viewport size*
  property. [manual:
  system-reference/system-expressions.md "Viewport", "Layout";
  plugins/system.json: every `Viewport*` expression has a `layer` parameter]
- Under *Scale outer*, the screen shows more than the *Viewport size* on
  its longer side, and the extra area is split evenly between the two
  sides. A parallax 0, 0 layer is centred on the original viewport too. So
  a HUD placed at the top of the viewport stays at the top of the design
  area, not at the top of a taller screen. The layout beyond the viewport
  shows on the sides. If a HUD must sit at a screen edge, give it the
  Anchor behavior on that layer. In a layout of the viewport's size, the
  game stays centred only with *Unbounded scrolling* on. With bounded
  scrolling, the camera keeps the layout's left and top edges on the
  screen's left and top edges. So the game shifts left or up from the
  centred HUD. If a backdrop must reach the screen's sides, give it Anchor
  with *Left edge* Viewport left and *Right edge* Viewport right. The right
  edge resizes the backdrop to the screen's width. So lay it out a little
  wider than the viewport, not thousands of pixels past the layout. A
  shaking camera moves the viewport, and 20 px past each side covers a
  shake of 8. Anchor moves a left edge without resizing. So if a piece
  grows to one side only, with its other end fixed, set it under *On start
  of layout* OR Browser *On resized*. Set its width to
  `Self.BBoxRight - ViewportLeft(layer) + 20`, then its X to
  `ViewportLeft(layer) - 20`. [manual:
  behavior-reference/anchor.md; observed in a game project, a 430×932
  portrait export switched to *Scale outer* and shown at 560×380 and 300×700
  in Chrome, 2026-09-30; the Anchor backdrop and the one-sided piece
  previewed at 900×500 and 330×800 and after a resize, r504, 2026-09-30;
  a 1920×1080 one-screen layout previewed at 1600×700, r495.2, 2026-10-08:
  bounded, `scrollX` was 1234 and the world layer's viewport started at 0
  while the HUD layer's started at -274; unbounded, both started at -274]
- Drag & Drop moves the dragged instance only when the pointer moves. It
  sets the position to the pointer minus the grab offset. A tick without
  movement writes nothing. A *Set position* on the dragged instance holds
  while the finger rests, but the next move overwrites it. So if the look
  must trail the finger or lift above it, put that look on a child that
  the events position. Drops and overlaps still use the dragged instance.
  [runtime: exported
  c3runtime.js r503, `Behaviors.DragnDrop` `_OnMove`, called from the
  `pointermove` dispatch only; observed in a game project, r503 preview,
  2026-09-29]
