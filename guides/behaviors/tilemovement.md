# Event Sheet Pitfalls: Tile movement

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- Tile movement counts in grid cells, not pixels. *Set grid position* and
  *Can move to* take a column and a row, and `GridX` and `GridY` return
  them. So *Set grid position* to another object's X of 640 sends the
  object to column 640, far off the layout. Convert a layout position with
  `round((X - offset X) / grid width)`, and Y the same way with the grid
  height. The object's origin lands on `offset X + column × grid width`,
  with no half cell added. So an object that fills its cell has its origin
  at the top-left. [manual: behavior-reference/tile-movement.md, the origin
  aligned with the grid, "Can move to", "Set grid position", "GridX";
  observed in a copy of the official example template-tile-based-game,
  stable r495.2 preview, 2026-10-04: a 32 × 32 grid at offset 0, *Set grid
  position* (3, 2) put the origin at (96, 64)]
