# Event Sheet Pitfalls: Expressions

Sources and the rule for adding an entry are in the index,
[pitfalls/README.md](README.md).

- `Self` is the object of the condition or action that holds the expression.
  A System condition or action has no such object, and this includes *For
  Each (ordered)*. So if `Self` is in one, the editor refuses to open the
  project with `Invalid use of 'self'`. Write the object name instead:
  order *For each Segment* by `Segment.IID`, not by `Self.IID`. [editor
  message `Invalid use of 'self'`; observed in a game
  project, 2026-09-22]
- The editor reads a local variable, a global variable or a function
  parameter as a system expression if it has the name of one. For example,
  the editor reads a local number `mid` passed as `Functions.Measure(mid)`
  as the text function `mid()`. Then it refuses the whole project with
  `Invalid expressions ... parameter 0 does not take 'string'`. A parameter
  `round` used as `"Round " & round` stops the editor with
  `'round' does not accept 0 parameters`, but the project opens with
  `roundNo`. Give each variable and parameter a name that no system
  expression has (`probe`, not `mid`; not `left`, `right`, `len`, `find`,
  `max`, `min`, `abs`, `round`). `check_project.py` refuses both kinds of
  name.
  [plugins/system.json, expression `mid`; observed in a game project, r495.2
  editor, 2026-09-23; the parameter case observed in a game project, r504
  editor, 2026-09-30; both in minimal projects, r504 editor, 2026-10-02]
- The editor matches variable names without regard to case. A local named
  like a global hides the global in the local's scope. For example, a local
  string `count` declared in an event hides the global constant `COUNT` in
  that event's sub-events. So `COUNT - 1` there uses the string. The editor
  then refuses the whole project with `Type mismatch: - does not work with
  'string' and 'number'` and names the sub-event. Two locals such as `step`
  and `STEP` do not both keep their names if one is in the other's list or
  in a list below it. When the editor opens the project, it renames the one
  that comes later in the sheet, here `STEP` to `STEP2`. Every use of
  either name then refers to `step`. Two globals both keep their names, and
  every event refers to the one declared first. Give each variable a name
  that differs from every variable in its scope by more than its case
  (`countText` beside `COUNT`). `check_project.py` refuses each of these.
  It also warns about a local of the same type as the global, because that
  local hides the global too. [observed in a game project, r502 editor,
  2026-09-24; the renaming in
  minimal projects, r495.2 and r504 editors, 2026-10-05]
- `lerp(Self.X, Target.X, 0.1)` moves a different fraction per second at
  different framerates, and it ignores the time scale. If the third argument
  is a constant and the first is last tick's result, write `lerp(a, b, 1 -
  f^dt)` with `f` in (0, 1). The common approximation `f * dt` is not exact.
  The same holds for `anglelerp`. [manual:
  system-reference/system-expressions.md "dt", linking the delta-time
  tutorial, section "Lerp"; examples: magic-feather, surface-jump]
- If the factor comes from the engine, `lerp` needs no time of its own.
  Examples are `Self.Tween.Value("Attack")` in labyrinth, a timeline value,
  `unlerp` of a slider thumb and `Car.Speed / Car.MaxSpeed` in
  abductractor. These are mappings rather than tweens, so leave them as
  they are. [examples: labyrinth,
  abductractor]
- `lerp` and `unlerp` do not clamp their result. `lerp(0, 100, 1.5)` is
  150, and `unlerp` of a value outside its range goes past 0 or 1. Remap a
  range with `lerp(lo, hi, unlerp(a, b, v))`. If `v` can leave `[a, b]`,
  wrap it in `clamp`. [manual:
  system-reference/system-expressions.md "lerp", "unlerp", "clamp"; cheat
  sheet "Useful expressions and formulas", Remapping a range]
- `%` is the remainder and keeps the sign of the left operand, so `-1 % 5` is
  `-1`. To wrap an index that steps backwards, use `(n % max + max) % max`.
  [manual: project-primitives/events/expressions.md "%"; cheat sheet "Useful
  expressions and formulas", Wrapping around a number]
- Construct evaluates `%` before `*`, so `a * b % c` is `a * (b % c)`. The
  test `loopindex("i") * 100 % 1000 = 0` reads as
  `loopindex("i") * 100 = 0`, and it holds for no iteration of a loop that
  starts at 1. Put the product in parentheses:
  `(loopindex("i") * 100) % 1000 = 0`. [observed in a minimal project,
  stable editor preview, 2026-10-07: a loop drew a line 4 px wide where the
  test held and 2 px wide otherwise; with the parentheses the wide lines
  stood at 1000, 2000 and 3000, and without them every line was 2 px wide]
- An expression is a number or a text, with no null or undefined, and a
  missing value reads as the number 0. These all give 0: `Array.At`
  outside the array, `Dictionary.Get` of a key that is not there,
  `Function.ReturnValue` of the deprecated Function plugin when nothing set
  it, and a Timer's `CurrentTime` after a one-off timer fired. `Array.IndexOf`
  gives -1, `int("33xx")` is 33 and `int("xx33")` is 0. So `= 0` cannot
  tell an empty slot from a missing one. Test *Has key*, *Contains value*
  or `Array.Width` first, or use
  `Dictionary.GetDefault(key, fallback)`. [manual:
  plugin-reference/array.md "At", "IndexOf"; plugin-reference/dictionary.md
  "Get", "GetDefault", "Has key"; plugin-reference/function.md
  "ReturnValue"; behavior-reference/timer.md "CurrentTime";
  system-reference/system-expressions.md "int", "float"]
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
- Dictionary *Set key* changes only an existing key and silently ignores
  a missing one. *Add key* creates a key or overwrites it, so write gates
  and counters with *Add key*. [manual: plugin-reference/dictionary.md
  "Add key", "Set key"; runtime: `scripts/c3runtime.js` of an exported
  r503/r504 web build, `SetKey(t,e){this._data.has(t)&&...}`, `AddKey`]
- JSON `Type(path)` reads `"undefined"` for a path that is not there. For
  other paths it reads `"array"`, `"object"`, `"number"`, `"string"`,
  `"boolean"` or `"null"`. So an expression can test whether a path
  exists, as in `"layers." & name & (JSON.Type("layers." & name &
  ".alt") = "array" ? ".alt" : ".main")`. *Has key* does that only as a
  condition. [runtime: exported c3runtime.js
  r504, JSON `_GetTypeOf` returns `_JSONTypeOf` of the value, `typeof` for
  anything but null and arrays]
- *For* runs from its start index to its end index inclusive, and counts down
  if the end is below the start. So `For 0 to count - 1` over an empty list
  runs for 0 and -1. `For first to last` with `first` past `last` runs
  backwards over unwanted indexes. Put `count > 0`, or `first <= last`, among
  the same event's conditions before the loop. [runtime: exported
  c3runtime.js r504, `_For` takes the `--e` branch when the end is below the
  start]
- A local variable placed as a sub-event or in a group is visible to every
  event at its level, before or after it. It is also visible to the
  sub-events of these events, but not to the parent's own actions. Set it
  in a sibling block with no conditions, then read it in the other blocks.
  If it is not static, it resets to its initial value every time events
  enter its scope. [manual:
  project-primitives/events/variables.md "Local variables", "Static and
  constant variables"; example: galactic-blocks, group Controls, `StoredY`;
  observed in a minimal project, r506.2 editor, 2026-10-16: an event whose
  own action set a local declared among its sub-events stopped the open
  with `cannot find event variable`, and `check_project.py` refuses it as
  not in scope]
- *Set mesh point* in *Relative* mode adds to the current position of the
  point, not to its default position. So a derivation that runs every tick
  accumulates. Derive with *Absolute* and normalised coordinates, which
  run 0..1 across the object box and may go past it. A texture value of -1
  leaves the texture position unchanged. [manual:
  plugin-reference/common-features/common-actions.md "Set
  mesh point"]
- A mesh pulled into a trapezoid in X and Y bends every straight line of
  its image. Each cell draws as two triangles, and the image follows each
  triangle separately, so a line kinks where it crosses a diagonal. More
  points make the kinks shorter but never remove them. Also, rows spaced
  evenly show no depth. Moving the top points sideways gives a skew, a
  parallelogram. Pulling them in gives a trapezoid, which looks like a
  plane seen at an angle only with depth. For that plane, leave X and Y at
  their defaults and give the near row a Z with *Set mesh point*
  (mesh-z-elevation). Put the object on a layer whose *Rendering mode* is
  *3D*, under the layout's *Perspective* projection, as
  [3d-layers.md](../recipes/3d-layers.md) says. Then the lines stay
  straight and the rows get closer towards the far edge. A 2x2 mesh is
  enough for this. The raised row draws larger than the object box, so
  size or place the object for the tilted shape. [observed 2026-10-18 in a
  preview, r506.2
  editor, 778x511 viewport: on a Sprite with a 16x12 grid image, an 8x8
  mesh with its top row pulled in by 0.3 on each side drew zigzag lines and
  even rows; a 2x2 or 8x8 mesh with x and y at their defaults and z 600 on
  the bottom row drew straight lines and rows closer towards the top; manual:
  scripting/scripting-reference/object-interfaces/iworldinstance.md
  "setMeshPoint"]
- The JSON plugin reads a path as keys separated by dots. So it looks for
  a key with a dot in it, such as `"menu.title"`, as `menu` and then
  `title` inside `menu`, and *Has key* fails. In the path, escape a dot
  with a backslash, `my\.key`, and escape a backslash in a key with two,
  `my\\key`. An expression string has only the doubled quote as an escape,
  so write `"my\.key"` as it is. Keys without dots need none of this. A
  Dictionary reads every key whole. [manual:
  plugin-reference/json.md "Escaping",
  project-primitives/events/expressions.md on double quotes; observation in
  a studied project, 2026-10-06]
- A variable at the root of a sheet, outside every group and event, is a
  global. Every sheet of every layout reads it, whether that sheet is
  included or not, and it keeps its value between layouts. Only a variable
  inside a group or under an event is local. So put a variable meant for
  one sheet into a group at the top of that sheet. Make it *static* if it
  must keep its value from tick to tick. [manual:
  project-primitives/events/variables.md "Variables at the
  root level of the event sheet ... become global variables", "Global
  variables"; observed in a minimal project, r506.2 preview, 2026-10-16: a
  root variable of a sheet no layout uses read its value from the layout's
  sheet]
- `tokencount("", ",")` is 1, not 0, and `tokencount("a,", ",")` is 2. The
  count is the number of separators plus one, whatever the text is. So
  *Repeat tokencount(list, ",")* over an empty list runs once, with
  `tokenat` reading `""`. Test `list ≠ ""` among the event's conditions
  before the loop, or skip an empty token inside it. [manual:
  system-reference/system-expressions.md "tokencount", which gives only a
  non-empty example; observed in a minimal project, r506.2 preview,
  2026-10-16: `tokencount("", ",")` read 1, `tokencount("a", ",")` 1,
  `tokencount("a,b", ",")` 2 and `tokencount("a,", ",")` 2]
- A local that is not static resets to its initial value whenever events
  enter its scope, and events enter a group's scope every tick. So a value
  set in one trigger is gone when a trigger in a later tick reads it. Such
  triggers are Timer *On timer*, AJAX *On completed*, JSON *On parse
  success* and a tween's *On finished*. The later trigger reads the
  initial value, and nothing warns. In the tick of the trigger that set
  the value, the value is still there. Make the local static, or keep the
  value in a global or an instance variable.
  [manual: project-primitives/events/variables.md "Static and constant
  variables", "reset to their initial value whenever entering their scope
  (usually every tick)"; observed in a minimal project, r506.2 preview,
  2026-10-16: a group's local set to 5 in *On start of layout* read 5 in
  the same event and 0 in *On timer* 0.3 s later, while a static local
  beside it read 5]
- *Set value* with a text on a number variable parses the text. This holds
  for a global, a local and an instance variable. A text that starts with
  a number stores that number: `"12"` and `"12px"` store 12, and `"1.5"`
  stores 1.5. A text that starts with no number, such as `"abc"`, stores
  NaN, not 0. NaN prints as `NaN` and fails every comparison, `= 0` and
  `< 1` included. `NaN + 1` is NaN. So a `= 0` guard never catches NaN,
  and NaN spreads through every sum. Convert the text first with
  `int(text)` or `float(text)`, which give 0 for a text without a number.
  Or declare the variable as text. [observed in a minimal project, r506.2
  preview, 2026-10-16: a number global and a number instance variable set
  to `"abc"` held NaN, `numStr & ""` read `"NaN"`, `numStr = 0` and
  `numStr < 1` both read 0, `numStr + 1` NaN; `"12"` and `"12px"` stored
  12, `"1.5"` 1.5]
- A local is visible to every event at its level, before or after its
  declaration. But the declaration is an event of its own. When the tick
  reaches it, a local that is not static goes back to its initial value.
  So a value that an event above the declaration writes is gone for the
  events below the declaration. This holds in a group and among sub-events
  alike, and nothing warns. A static local keeps its value through its
  declaration. Declare a local above the first event that writes it.
  [manual:
  project-primitives/events/variables.md "Local variables", which says only
  that events at the same level can access it; observed in a minimal
  project, r506.2 preview, 2026-10-16: an event above the declaration set a
  group's local to 5 and read 5, the event below the declaration read 0
  every tick, the same among the sub-events of one event; a static local
  counted up above its declaration read the same count below it]
