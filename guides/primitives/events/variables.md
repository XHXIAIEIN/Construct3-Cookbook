# Event Sheet Pitfalls: Event variables

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../../pitfalls.md).

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
