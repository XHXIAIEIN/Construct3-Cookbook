# Event Sheet Pitfalls: Solid

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- A Solid blocks through the collision polygon of its current frame while
  its behavior is enabled. So a door that only plays an open animation
  keeps blocking wherever the polygons of its frames reach. When the door
  opens, disable its Solid with *Set enabled*, or destroy the door.
  [manual: behavior-reference/solid.md "Is enabled", "Set enabled";
  behavior-reference/platform.md, the collision polygon changing as an
  animation plays]
