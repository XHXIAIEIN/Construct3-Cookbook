# Event Sheet Pitfalls: Turret

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- Turret *Add object to target* takes an object type or a family as a
  whole. The instances the event picked do not matter, so a turret given a
  family narrowed to the other team still aims at every member, its own team
  included. To target by an instance variable, leave *Add object to target*
  out and acquire one picked instance: while the turret has no target, *For
  each* turret, narrow the family to the instances it may target, *Pick
  nearest* to the turret, then *Acquire target* that family. *Acquire target*
  takes the picked instance and ignores one out of range. The turret keeps
  the target until it leaves range or is destroyed, and the event then picks
  again. [manual: behavior-reference/turret.md "Add object to target",
  "Acquire target"; observed in a minimal project, stable editor preview,
  2026-10-04: two turrets, two teams in one family told apart by an instance
  variable; with *Add object to target* after narrowing to the other team,
  both turrets aimed at their own team in 240 of 240 samples over 12 s; with
  *Acquire target* on the picked nearest enemy, 0 of 240, while a hull of
  their own team was nearer in 159]
