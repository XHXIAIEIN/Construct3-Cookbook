# Event Sheet Pitfalls: Turret

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

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
