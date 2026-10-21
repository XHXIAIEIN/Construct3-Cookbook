# Event Sheet Pitfalls: Movements behaviors

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- 8 Direction moves only by its controls: the arrow keys, *Simulate
  control* and *Set vector X/Y*. It has no action that sets an angle of
  motion or moves toward a position. It does not steer around obstacles,
  and a Solid only blocks it. So give an enemy that chases the player
  another behavior, and choose that behavior by the ground between them:
  - Open ground: use Move To, and run *Move to object* with the player in
    *Every tick* or on a short *Every X seconds*. The action takes the
    target's position when it runs and does not track the target
    afterwards. *Set angle of motion* is an action of Move To, not of 8
    Direction.
  - Walls in the way: use Pathfinding. Run *Find path* to the player's
    position about every second, and run *Move along path* in *On path
    found*. The behavior calculates the path in the background, so the path
    is not ready in the tick of *Find path*. A *Find path* in every tick
    costs a lot of CPU.
  - Keep 8 Direction only if the enemy must move like the player. Then, in
    each tick, compare the positions and *Simulate control* left or right
    and up or down.
  [manual: behavior-reference/8-direction.md, move.md, pathfinding.md]

- *Simulate control* acts in the tick it runs, as if the control were held
  for that tick. So put it in an event whose condition stays true while the
  control is held, such as Keyboard *Key is down*. In an *On key pressed*
  event the player moves for one tick and stops. [manual:
  behavior-reference.md "Custom controls", the tip that the input events
  must be continually true]

- *Default controls* is a property of each instance, and every instance
  with it on moves with the arrow keys. A crate given Platform to be pushed,
  or an enemy given 8 Direction, has it on by default and walks with the
  player. In each layout, turn it off on every instance that the player
  does not steer: `"default-controls": false` in the instance's behavior
  properties. Move those objects with *Simulate control*. The
  `construct3-agent-plugin` skill's `check_project.py` warns when instances
  of two object types in one layout have it on. [manual:
  behavior-reference/platform.md, 8-direction.md, car.md and
  tile-movement.md "Default controls"]
