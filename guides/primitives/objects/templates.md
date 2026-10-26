# Event Sheet Pitfalls: Templates

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../../pitfalls.md).

- A type can be both in the parent's container and among its children in the
  template's hierarchy. Then creating the parent with *Create hierarchy* on
  creates one instance of that type, because the container sibling and the
  hierarchy child are the same new instance. So if a part must be picked
  with the parent and move with it, put the part in both.
  [observed in a game project, r504 preview,
  2026-09-30: a `Card` template with four parts in its container and its
  hierarchy, created six times, left six instances of each part]

- A runtime-created instance takes its properties from an existing instance
  or from the named template. An object with no instance in any layout is
  still created, with its image and size, but its behavior properties read
  0. So a Bullet created that way has speed 0 and never moves, while the
  addon's default is 400. Keep one template instance of each
  runtime-created object in a layout that never runs.
  [same; observed in a minimal project, r504 preview,
  2026-10-02: the Laser of the official example families, its one layout
  instance removed, was created 52×27 and visible with Bullet speed 0; with
  the instance kept, speed 400]

- A replica starts each property that follows its template with the
  template's value, not with the value saved in the replica. Only a
  property edited on the replica itself is its own. The editor turns own
  values back into following ones: *Apply template › Properties only* sets
  the replica's instance variables to the template's values. So an
  instance variable that holds something about one replica, such as the y
  it rests at, can take the template's value without any edit to that
  replica. Set such a variable from events, `Set restY to Self.Y` under
  *On start of layout*, or keep those instances out of templates. What the
  editor writes into replicas is in
  [hand-editing.md](../../project-files/hand-editing.md), "Layouts".
  [manual: project-primitives/objects/templates.md "Terms"; observed in a
  copy of the official example rat-purrsuit, r506.3 editor and preview,
  2026-10-26: a `basic0` replica saved with points 555 and frame 2, both
  following, read 100 and frame 0, the template's; a replica with its own
  points 999 kept 999 through an edit of the template to 777, and *Apply
  template to all replicas › Properties only* set it to 777]

- *TemplateName* of an instance placed as a replica reads the name of its
  template. So events can tell the kinds apart by the template, as
  rat-purrsuit tests `Pickup.TemplateName = "speed"` when the player takes
  a pickup, without an instance variable for the kind. A replica whose
  template name names no template, or is empty, still reads the saved name
  and starts with its own saved values. [official example rat-purrsuit
  `GameEvents`, group "Pickups"; observed in a copy of it, r506.3 preview,
  2026-10-26: the replicas read `basic0`, `basic1` and `speed`; a replica
  whose template name was changed to `gone`, and one with `""`, read those
  and started with their saved points 555 and animation `Pickup2`]
