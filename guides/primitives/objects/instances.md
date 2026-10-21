# Event Sheet Pitfalls: Object instances

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../../pitfalls.md).

- Angles are in degrees. 0 faces right and angles increase clockwise, so 90
  points down, 180 left and 270 (or -90) up. 360 is 0 again, so a bullet
  fired at 360 goes right, and `random(360)` is a full turn. `sin`, `cos` and
  `angle` take and return degrees. Some expressions return -180..180 and
  others 0..360. So compare angles with `anglediff`, *Is between angles* or
  *Is clockwise from*, never with `<`. Normalise with `(a + 360) % 360` only
  where a value must land in 0..360. [manual:
  tips-and-guides/common-conventions.md "Units";
  system-reference/system-expressions.md "Math";
  system-reference/system-conditions.md "Is between angles"]

- A sprite is drawn facing right at angle 0. So art painted pointing up
  points a quarter turn counter-clockwise of its target after *Set angle
  toward position*. Paint it facing right, or add the same 90 degrees in
  every *Set angle*. Do not add a different correction in each event.
  [consequence of the same convention;
  Rotate's speed is positive clockwise: manual behavior-reference/rotate.md
  "Speed"]

- A sprite's origin is image point 0, the point X, Y and rotation refer to.
  The editor puts it at the centre (`originX`, `originY` 0.5 in the layout
  file), so a sprite at the layout's edge shows half. For a muzzle or a
  hinge, position by an image point (*Spawn another object* takes one). Move
  the origin in the image editor, not by an offset in events. [manual:
  interface/animations-editor.md "Image points"; official example layouts]
