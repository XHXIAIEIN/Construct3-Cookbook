# Event Sheet Pitfalls: Containers

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../../pitfalls.md).

- The members of a container are created, destroyed and picked together.
  Picking a parent does not pick its hierarchy children, so pick them with
  *Pick children*. [manual:
  project-primitives/objects/containers.md;
  plugin-reference/common-features/common-conditions.md "Hierarchy"]

- A container belongs to an object type, and picking a family never picks
  it. For example, with `HPBar` in `Enemy`'s container, `On clicked
  Enemies` followed by `HPBar: Set width` sets every bar. Pick the type
  from the family in a sub-event, `Enemy: Pick by unique ID Enemies.UID`.
  This also picks the container of the type. Add one such sub-event for
  each member type. If the event picks several instances, put the
  sub-events under `For each Enemies`. The same pick by UID reaches a
  second family of the instance. The events of the first family cannot see
  the variables and behaviors of that second family. [Construct-bugs#7485,
  open; example: elemental-conveyors event 35, `Draggable` picked by
  `Base.UID`]

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

- A data object, such as a Dictionary or a JSON, gives each instance its
  own copy if it is in a container. Events pick that copy with its type,
  as above. If stats come from a data file, keep them in such a data
  object instead of a growing list of instance variables. [manual:
  project-primitives/objects/containers.md "data storage objects"]
