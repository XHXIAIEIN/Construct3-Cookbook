# Event Sheet Pitfalls: Array

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- `Array.IndexOf` and `Array.LastIndexOf` search along X only, and no
  expression searches along Y. To find the row of a value in a column, loop
  *System: For* from 0 to `Array.Height - 1`. Test *Compare at XY* with
  `loopindex`, keep the index and *Stop loop*. Or search in a script with
  `getAt(x, y)`. *Stop loop* stops *For*, *For each* and *Repeat*, but not
  Array *For each element*. So a search written with *For each element*
  visits every element and keeps the last match. [schema: Array `indexof` "Find
  first X index of matching value"; System `stop-loop` "Stop any currently
  running loop (for, for each, repeat)"; observed in a probe project, r506.3
  preview, 2026-10-20: with *Stop loop* at index 1, *For each element* over
  five elements ran five times and *For* from 0 to 4 ran twice]
