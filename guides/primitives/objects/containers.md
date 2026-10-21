# Event Sheet Pitfalls: Containers

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../../pitfalls.md).

- Container members are created, destroyed and picked together. Hierarchy
  children are not picked with their parent, so use *Pick children*. [manual:
  project-primitives/objects/containers.md;
  plugin-reference/common-features/common-conditions.md "Hierarchy"]

- A container belongs to an object type, and picking a family never picks it.
  With `HPBar` in `Enemy`'s container, `On clicked Enemies` then `HPBar: Set
  width` sets every bar. Pick the type from the family in a sub-event,
  `Enemy: Pick by unique ID Enemies.UID`, and the container is picked with
  it. Add one such sub-event per member type, under `For each Enemies` if
  several are picked. The same pick by UID reaches a second family of the
  instance, whose variables and behaviors the first family's events cannot
  see. [Construct-bugs#7485, open; example: elemental-conveyors event 35,
  `Draggable` picked by `Base.UID`]

- Inside a container, an expression that names another member reads the
  member of the same instance, in an action and in a condition, with no pick
  and no *For each*. So `Fill: Set width to clamp(Frame.hp / Frame.maxHp, 0,
  1) * (Frame.Width - 4)` in an *Every tick* event sets each fill from its own
  frame, and `Fill: Compare width > <the same expression>` picks each fill
  that is wider than its own frame's value. A custom action called with a
  parameter that reads one instance's variable, `SetMax(Frame.maxHp + 300)`,
  needs *For each* `Frame` among the calling event's conditions, so that each
  bar passes its own value. The custom action itself runs once for the picked
  instances (see [Functions](../events/functions.md)). [the manual describes the pairing
  for picks only, project-primitives/objects/containers.md "What containers
  do"; observed in a minimal project, stable editor preview, 2026-10-07: seven
  object types in one container, three instances with maximum hp 300, 1000
  and 3000 and a frame 448 px wide; the fills were 222, 377.4 and 421.8 px at
  hp 150, 850 and 2850, and the call under *For each* passed 600, 1300 and
  3300. Fills of 88.8, 399.6 and 355.2 px were given targets of 44.4, 377.4
  and 370 px, under `Fill: Width > target`, which sets the width at once, and
  `Fill: Width < target - 0.5`, which starts a tween. One tick later the
  first two were at their targets and the third was growing. A read of any
  one frame would have tweened the first fill or set the third at once]

- A data object (Dictionary, JSON) in a container gives each instance its own
  copy, picked with its type as above. If stats come from a data file, use it
  instead of a growing list of instance variables. [manual:
  project-primitives/objects/containers.md "data storage objects"]
