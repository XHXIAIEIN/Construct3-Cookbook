# Event Sheet Pitfalls: Pathfinding

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- *Find path* can fail. Then *On failed to find path* fires instead of
  *On path found*, and the object stops. A cell is either all obstacle or
  all free, so a gap narrower than the cell size is closed for the path
  while Line of Sight still sees through it. Take an enemy that chases
  while it sees the player and moves only in *On path found*. If the player
  waits behind such a gap, the enemy stands still for good. Handle
  *On failed to find path*: treat it as a lost sight of the player, or send
  the enemy back to its patrol. [manual: behavior-reference/pathfinding.md
  "Cell size", "On failed to find path"; example: stealth-example, event
  sheet 1, *On failed to find path* sends a chasing guard back to its
  waypoint; observed in a test project, r506.3 preview, 2026-10-24: a
  player behind a 30 px gap that Line of Sight saw through kept an enemy
  in its chase state, standing still; runtime: r506.3
  `behaviors/movements/pathfinding/c3runtime/runtime.js`, `_DoFindPath`
  sets `_isMoving` to false when no path is found]

- A *Find path* while *Is calculating path* is true does not cancel the
  calculation. The old path still fires *On path found* or *On failed to
  find path*, and then the new one is calculated and fires its own
  trigger. The object keeps moving along its old path in the meantime, so
  its *On arrived* can fire during the new calculation. So a patrol's *On
  arrived*, which picks the next point, can turn a guard that has just
  seen the player back to its patrol. Add `NOT Is calculating path` to *On
  arrived*. When the chase starts, run *Find path* to the player at once,
  not only on the chase's repeating timer, so the guard does not walk on
  along its patrol path first. [manual: behavior-reference/pathfinding.md
  "Find path", "Is calculating path"; example: stealth-example, event sheet
  1, both *On arrived* events test `NOT Is calculating path`; runtime:
  r506.3 `behaviors/movements/pathfinding/c3runtime/runtime.js`, `_FindPath`
  waits for the running calculation and then calculates the last position
  asked for, and `Tick` fires `OnArrived` while `_isMoving` holds; read
  from source, not observed]
