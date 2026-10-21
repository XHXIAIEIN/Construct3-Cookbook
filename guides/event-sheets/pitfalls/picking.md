# Event Sheet Pitfalls: Picking

Sources and the rule for adding an entry are in the index,
[pitfalls/README.md](README.md).

- An instance with collisions disabled fails every overlap and collision
  test, in both directions. To take a dragged or tweening instance out of
  these tests, disable its collisions instead of setting an `isMoving`
  flag. [manual: plugin-reference/sprite.md "Set collisions enabled";
  scripting/scripting-reference/object-interfaces/iworldinstance.md
  `isCollisionEnabled`]
- A Solid blocks through the collision polygon of its current frame while
  its behavior is enabled. So a door that only plays an open animation
  keeps blocking wherever the polygons of its frames reach. When the door
  opens, disable its Solid with *Set enabled*, or destroy the door.
  [manual: behavior-reference/solid.md "Is enabled", "Set enabled";
  behavior-reference/platform.md, the collision polygon changing as an
  animation plays]
- A Solid stops a Platform object at its edge, so the two touch and do not
  overlap. *Is overlapping* stays false while the player stands on a Solid
  floor or walks into a Solid wall. So an event that pushes the crate the
  player stands against never runs. To test touching, use *Is overlapping
  at offset* with 1 pixel towards the Solid. That is (1, 0) for a wall on
  the right and (0, 1) for the floor. The offset moves the object that the
  condition belongs to, so a test from the crate's side takes the opposite
  sign. *On collision* still fires, because the behavior registers the
  collision when it pushes the object out. [manual:
  plugin-reference/common-features/common-conditions.md "Is overlapping at
  offset"; observed in a copy of the official example follow-rewind-time,
  stable r495.2 preview, 2026-10-04: a Platform player held against a Solid
  wall on a Solid floor, *Is overlapping* false, at offset (1, 0) and
  (0, 1) true; observed in the platformer template with a Solid door,
  stable r495.2 preview, 2026-10-09: *Is overlapping* the door never held,
  at offset (1, 0) it did; runtime: exported c3runtime.js, Platform calls
  `RegisterCollision` after `PushOutSolidAxis`]
- Bullet *Bounce off object* moves the ball out of the object at once. So
  an *On collision* with that object in a later event of the same tick
  finds no overlap and does not run. So feedback in events of its own with
  the same *On collision*, such as a sound, a squash, sparks or a hit
  freeze, runs only above the event that bounces, or as actions of that
  event. Put these events above it, because the collision events are
  tested in sheet order. [manual:
  behavior-reference/bullet.md "Bounce off object"; observed in a pong
  project, r506 preview, 2026-10-15: feedback groups each with Ball *On
  collision with* the paddles, below the event that bounces, on a paddle
  hit the time scale, the paddle's width and the Sparks count did not
  change; the same groups above it, all three changed]
- While a dragged or tweening instance has collisions disabled, the slot
  where it will land reads as empty until it lands. This includes the slot
  that it is flying back to. The drop events rely on this. But an event
  that fills empty slots by itself, such as a buy button or a spawn,
  creates an instance there. Then the returning instance lands on top of
  it. Make such an event wait while the player drags any instance or any
  landing tween plays. [observed in a
  game project, r504 preview, 2026-10-01: a piece dropped back on its slot,
  the buy button pressed within its 0.2 s snap, the bought weapon landed on
  the piece]
- Events pick a type and its family separately, so narrowing Sprite
  `Piece` never narrows its family `Pieces`. Use this to make two picks of
  one type in one event. In a function, refer to the name that the caller
  narrowed (see [Functions](functions.md)). [manual:
  project-primitives/objects/families.md "Picking families in events"]
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
  member that belongs to the same instance. This holds in an action and in
  a condition, with no pick and no *For each*. So `Fill: Set width to
  clamp(Frame.hp / Frame.maxHp, 0, 1) * (Frame.Width - 4)` in an *Every
  tick* event sets each fill from its own frame. And `Fill: Compare width >
  <the same expression>` picks each fill that is wider than the value of
  its own frame. A custom action can take a parameter that reads a
  variable of one instance, as in `SetMax(Frame.maxHp + 300)`. Then the
  calling event needs *For each* `Frame` among its conditions, so that each
  bar passes its own value. The custom action itself runs once for the
  picked instances (see [Functions](functions.md)). [the manual describes
  the pairing for picks only, project-primitives/objects/containers.md
  "What containers do"; observed in a minimal project, stable editor
  preview, 2026-10-07: seven object types in one container, three
  instances with maximum hp 300, 1000 and 3000 and a frame 448 px wide;
  the fills were 222, 377.4 and 421.8 px at hp 150, 850 and 2850, and the
  call under *For each* passed 600, 1300 and 3300. Fills of 88.8, 399.6
  and 355.2 px were given targets of 44.4, 377.4 and 370 px, under
  `Fill: Width > target`, which sets the width at once, and
  `Fill: Width < target - 0.5`, which starts a tween. One tick later the
  first two were at their targets and the third was growing. A read of any
  one frame would have tweened the first fill or set the third at once]
- A condition that picks a type evaluates its expression once for each
  candidate. In it, the type's own name and every member of its container
  read the candidate under test, not the instance that an outer event
  picked. For example, `EnemyStats` is in `enemyBase`'s container. In `For
  each enemyBase`, a sub-event `Pick all enemyBase`, then `Pick enemyBase
  by evaluating abs(enemyBase.X - EnemyStats.Get("swapTo")) < 30` compares
  each enemy with its own `swapTo`. To compare every candidate with one
  value, store the value in a local variable before the pick, `toX =
  EnemyStats.Get("swapTo")`. Then write `abs(enemyBase.X - toX) < 30`.
  [manual: system-reference/system-conditions.md "Pick by evaluate";
  observed in a game project, r504 preview, 2026-10-05: the enemy in the
  target column was not picked and stayed, and with the target X stored in
  a local first it moved]
- *Pick children* picks only among the instances of the child type that
  are already picked. If the child type is in the parent's container,
  narrowing the parent narrows the child type at the same time. For
  example, `PieceArt` is in `Piece`'s container. In `Piece: On drop`,
  `PieceArt` is already the art of the dragged piece. So `Pieces: Pick
  children PieceArt` finds nothing on the piece under it. Give the child
  type a family of its own, `Arts` with the one member `PieceArt`. Then
  pick children of the family, because its picks are kept apart from the
  container's. [runtime: exported
  c3runtime.js r503, `AnySDK.PickChildren` keeps the child class's current
  picks unless they are all of it, then applies the result to the child's
  container; observed in a game project, r503 preview, 2026-09-28: the merge
  target's body was not picked until the pick went through a one-member
  family]
- *Pick parent* with *Which* set to *Own* looks only one level up. With
  `Robot → Arm → Hand`, `Hand: Pick parent Robot (own)` picks nothing,
  because `Hand`'s own parent is `Arm`. Then the event's actions never run,
  and no error shows. If the parent you name is not the direct one, set
  *Which* to *All*. *Pick children* with *All* works the same way down the
  hierarchy.
  [manual: plugin-reference/common-features/common-conditions.md "Pick
  parent"; observed in a game project, r504 preview, 2026-09-30: a deploy
  flag cleared from `On Tween "hop" finished` through `Pick parent base
  (own)` stayed set, and the piece never started attacking until the pick was
  changed to *All*]
- A data object, such as a Dictionary or a JSON, gives each instance its
  own copy if it is in a container. Events pick that copy with its type,
  as above. If stats come from a data file, keep them in such a data
  object instead of a growing list of instance variables. [manual:
  project-primitives/objects/containers.md "data storage objects"]
- Sub-events run after the parent's actions, so the conditions of a
  sub-event see a change that those actions made, such as collisions
  enabled again. [manual:
  project-primitives/events/sub-events.md]
- A hierarchy child can be on a different layer from its parent, because
  the connection belongs to the instances, not to the layers. A child on a
  lower layer stays a child. So a lifted parent can draw above everything
  while its parts stay under an outline. [releases: beta.json, "hierarchy
  information not duplicated properly if connections were setup between
  instances in different layers"; observed in a game project, 2026-09-17;
  observed in a minimal project, r504 preview, 2026-10-02: a child on
  another layer than its parent kept the parent and moved 40 px with it]
- *ChildCount*, *Compare child count* and *Has children* count every
  attached child of any type. So a second child type on the same parent
  changes every count that meant one type. To get the top index of one
  type, use *Pick children* and then *Pick highest/lowest* (highest) on
  that type. Or count in a *For each* over the picked children.
  [manual: plugin-reference/common-features/common-expressions.md
  "ChildCount", common-conditions.md "Compare child count"; observed in a
  game project, 2026-09-17]
- *Destroy* releases the instance only at the end of the top-level event,
  and until then `Count` still includes it. So the event that destroys the
  last brick still reads `Brick.Count` as 1. Test "none left" in a
  top-level event of its own. [manual: system-reference/system-actions.md
  "Unload images" note "destroying objects does not really release them
  until the end of the next top-level event"; runtime: exported
  c3runtime.js r504, `Count` is `GetInstanceCount()` plus the instances
  pending creation, and `DestroyInstance` defers the removal]
- A condition that picks no instance of a type stops its event. System
  *Pick all* is false when the type has no instance. So `PickedCount = 0`
  never holds below a pick of that type. Under *Pick all Key*, a sub-event
  that tests `Key.PickedCount = 0` never runs, not even when the last key
  is gone. Test "none left" with `Key.Count = 0` in *Compare two values*,
  in an event that does not pick Key. [manual:
  project-primitives/events/how-events-work.md, the actions "do not run at
  all" when no instance meets the conditions; runtime: exported
  c3runtime.js r504, `PickAll` returns false when `GetInstanceCount()` is 0]
- *Destroy* does not detach a child from its parent. The runtime releases
  the instance only at the end of the top-level event. Until then *Compare
  child count*, *Has children*, `ChildCount` and *Pick children* still see
  it. So if one sub-event destroys a child, the next sub-event of the same
  trigger still counts it. To count one type, use *Pick children* and then
  `PickedCount`, or count in a later top-level event. [manual:
  system-reference/system-actions.md "Unload images" note "destroying objects
  does not really release them until the end of the next top-level event";
  runtime: exported c3runtime.js, `DestroyInstance` defers, `GetChildCount`
  is `GetChildren().length`; observed in a game project, 2026-09-17]
- Turret *Add object to target* takes an object type or a family as a
  whole, and it ignores the instances that the event picked. So a turret
  given a family narrowed to the other team still aims at every member of
  the family, its own team included. To target by an instance variable,
  leave out *Add object to target* and acquire one picked instance. While
  the turret has no target, run *For each* turret and narrow the family to
  the instances that the turret may target. Then *Pick nearest* to the
  turret and *Acquire target* that family. *Acquire target* takes the
  picked instance and ignores an instance out of range. The turret keeps
  the target until the target leaves range or is destroyed. Then the event
  picks again. [manual: behavior-reference/turret.md "Add object to target",
  "Acquire target"; observed in a minimal project, stable editor preview,
  2026-10-04: two turrets, two teams in one family told apart by an instance
  variable; with *Add object to target* after narrowing to the other team,
  both turrets aimed at their own team in 240 of 240 samples over 12 s; with
  *Acquire target* on the picked nearest enemy, 0 of 240, while a hull of
  their own team was nearer in 159]
- A condition on an object holds when one instance passes it, and the next
  condition tests only the instances that it kept. So a row of three cells
  written as `Cell: Row = 0`, `Cell: Column = 0`, `Cell: Value = 1`,
  `Cell: Column = 1`, ... never holds, because no cell has Column 0 and
  Column 1. Also, `Cell: Value ≠ 0` holds as soon as one cell is filled,
  not only when all cells are filled. To test that several instances
  agree, narrow once and count: `Cell: Row = 0`, `Cell: Value = 1`,
  `System: Cell.PickedCount = 3`. The board is full when `Cell: Value ≠ 0`
  keeps `Cell.Count` of the cells. Pick one diagonal with System *Pick by
  evaluate* `Cell.Row = Cell.Column`, and the other with
  `Cell.Row + Cell.Column = 2`. [manual:
  project-primitives/events/how-events-work.md, conditions filter the
  picked instances progressively; found in a QQ bot's tic-tac-toe sheet,
  2026-10-06, whose wins and draw were written so; observed in a copy of
  it, stable editor preview, 2026-10-06: row 0 and the diagonal filled, the
  counts held for row 0 and the diagonal and not for row 1 or a full
  board, and `Cell: Value ≠ 0` alone held]
