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
