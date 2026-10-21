# Event Sheet Pitfalls: Moving toward a target

Sources and the rule for adding an entry are in the index,
[pitfalls/README.md](README.md).

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
- Follow does not chase. It replays the target's recorded movement after a
  time or distance delay, so the follower takes the path that the target
  took and never cuts toward the target. Use Follow for a trailing companion
  or a snake's body, not for an enemy.
  [manual: behavior-reference/follow.md]
