# Event Sheet Pitfalls: Drawing canvas

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- Drawing Canvas *Fill polygon* with *Convex* off draws nothing if two
  consecutive points of the polygon coincide, including a closing point that
  repeats the first one. The rest of the sheet runs on, with no error logged.
  With *Convex* on, the same points fill. Add a closing point only if it is a
  point of its own, or count the points in a variable and loop over that. A
  convex shape can also tick *Convex*. [observed in a game project, r502
  preview, 2026-09-24; observed in a minimal project, r504 preview,
  2026-10-02: a square filled 5776 pixels, the same square with its first
  point, a middle point or a closing point repeated filled 0, and all three
  filled 5776 with *Convex* on; reported as Scirra/Construct-bugs#9292, open]
