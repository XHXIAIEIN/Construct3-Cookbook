# Event Sheet Pitfalls: Solid

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- A Solid blocks while its behavior is enabled, through the collision
  polygon of its current frame. So a door that only plays an open
  animation keeps blocking wherever its frames' polygons reach. When the
  door opens, disable its Solid with *Set enabled*, or destroy it. [manual:
  behavior-reference/solid.md "Is enabled", "Set enabled";
  behavior-reference/platform.md, the collision polygon changing as an
  animation plays]
