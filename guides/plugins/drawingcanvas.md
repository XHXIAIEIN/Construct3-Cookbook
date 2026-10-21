# Event Sheet Pitfalls: Drawing canvas

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- If *Convex* is off, Drawing Canvas *Fill polygon* draws nothing when two
  consecutive points of the polygon coincide. A closing point that repeats
  the first point is such a pair. The rest of the sheet keeps running, and
  no error is logged. If *Convex* is on, the same points fill. So add a
  closing point only if it is a point of its own, or count the points in a
  variable and loop over that count. A convex shape can also tick *Convex*.
  [observed in a game project, r502 preview, 2026-09-24; observed in a
  minimal project, r504 preview, 2026-10-02: a square filled 5776 pixels,
  the same square with its first point, a middle point or a closing point
  repeated filled 0, and all three filled 5776 with *Convex* on; r507 beta
  drawCommand.js removes repeated consecutive points when *Convex* is off]
