# Event Sheet Pitfalls: How events work

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../../pitfalls.md).

- A type and its family are picked separately, so narrowing Sprite `Piece`
  never narrows its family `Pieces`. Use this for two picks of one type in
  one event. Refer to the name the caller narrowed (see
  [Functions](functions.md)). [manual: project-primitives/objects/families.md
  "Picking families in events"]

- A condition that picks a type evaluates its expression once for each
  candidate. In it, the type's own name and every member of its container
  read the candidate under test, not the instance an outer event picked.
  So in `For each enemyBase`, a sub-event `Pick all enemyBase`, then
  `Pick enemyBase by evaluating abs(enemyBase.X -
  EnemyStats.Get("swapTo")) < 30` compares each enemy with its own
  `swapTo`, with `EnemyStats` in `enemyBase`'s container. To compare every
  candidate with one value, store the value in a local variable before the
  pick, `toX = EnemyStats.Get("swapTo")`, and write `abs(enemyBase.X - toX)
  < 30`. [manual: system-reference/system-conditions.md "Pick by evaluate";
  observed in a game project, r504 preview, 2026-10-05: the enemy in the
  target column was not picked and stayed, and with the target X stored in
  a local first it moved]

- Sub-events run after the parent's actions, so the sub-event's conditions
  see a change those actions made (collisions re-enabled). [manual:
  project-primitives/events/sub-events.md]

- *Destroy* releases the instance only at the end of the top-level event,
  and until then `Count` still includes it. So the event that destroys the
  last brick still reads `Brick.Count` as 1. Test "none left" in a
  top-level event of its own. [manual: system-reference/system-actions.md
  "Unload images" note "destroying objects does not really release them
  until the end of the next top-level event"; runtime: exported
  c3runtime.js r504, `Count` is `GetInstanceCount()` plus the instances
  pending creation, and `DestroyInstance` defers the removal]

- A condition that picks no instance of a type stops its event, and System
  *Pick all* is false when the type has no instance. So `PickedCount = 0`
  never holds below a pick of that type. Under *Pick all Key*, a sub-event
  that tests `Key.PickedCount = 0` never runs, not even when the last key
  is gone. Test "none left" with `Key.Count = 0` in *Compare two values*,
  in an event that does not pick Key. [manual:
  project-primitives/events/how-events-work.md, the actions "do not run at
  all" when no instance meets the conditions; runtime: exported
  c3runtime.js r504, `PickAll` returns false when `GetInstanceCount()` is 0]

- *Destroy* does not detach a child from its parent. The runtime releases the
  instance only at the end of the top-level event. Until then *Compare child
  count*, *Has children*, `ChildCount` and *Pick children* still see it. So
  if one sub-event destroys a child, the next sub-event of the same trigger
  still counts it. Count the type you mean with *Pick children* plus
  `PickedCount`, or count from a later top-level event. [manual:
  system-reference/system-actions.md "Unload images" note "destroying objects
  does not really release them until the end of the next top-level event";
  runtime: exported c3runtime.js, `DestroyInstance` defers, `GetChildCount`
  is `GetChildren().length`; observed in a game project, 2026-09-17]

- A condition on an object holds when one instance passes it, and the next
  condition tests only the instances it kept. So a row of three cells
  written as `Cell: Row = 0`, `Cell: Column = 0`, `Cell: Value = 1`,
  `Cell: Column = 1`, ... never holds: no cell has Column 0 and Column 1.
  And `Cell: Value ≠ 0` holds once any cell is filled, not when all are.
  To test that several instances agree, narrow once and count:
  `Cell: Row = 0`, `Cell: Value = 1`, `System: Cell.PickedCount = 3`; the
  board is full when `Cell: Value ≠ 0` keeps `Cell.Count` of them. A
  diagonal is System *Pick by evaluate* `Cell.Row = Cell.Column`, the other
  `Cell.Row + Cell.Column = 2`. [manual:
  project-primitives/events/how-events-work.md, conditions filter the
  picked instances progressively; found in a QQ bot's tic-tac-toe sheet,
  2026-10-06, whose wins and draw were written so; observed in a copy of
  it, stable editor preview, 2026-10-06: row 0 and the diagonal filled, the
  counts held for row 0 and the diagonal and not for row 1 or a full
  board, and `Cell: Value ≠ 0` alone held]

- Deactivating a group stops its events, including its triggers, and nothing
  else. Behaviors, timers and tweens it started keep running. So it turns a
  phase off but does not pause. [manual: system-reference/system-actions.md
  "Set group active"; examples: every pause is *Set time scale* 0]

- A created instance is picked in its own event and that event's sub-events,
  and *Pick by unique ID* finds it anywhere. No other condition (*Pick all*,
  *Pick random instance*, *Compare instance variable*, overlap) finds it among
  all instances until the top-level event that created it has ended, or the
  outermost trigger. So a function called after the creating function in the
  same event does not see the new instances. *Pick children*, *Pick parent*
  and *Pick nth child* are the exception: while the type they pick is not
  narrowed, they add the instances still waiting to be created, and `Count`
  counts them. Fix the order in one of these ways:
  - If the later function acts on the instances that were there before,
    such as sliding a queue of cards along, call it before the creation.
  - If it needs values of the new instance, set them in the creating
    function while the new instance is picked, or pass `UID`.
  - Otherwise pick from a later top-level event or trigger.
  - If no later event or trigger runs the step, as after an AJAX *On
    completed* that builds a screen, put *Wait 0* before it. The step then
    runs at the start of the next tick, and the new instances show for one
    frame before it (see [System](../../plugins/system.md)).

  `check_project.py` warns if one list of
  actions creates instances, directly or through a function, and then calls a
  function that picks them by a condition. [Ashley in
  Scirra/Construct-bugs#3554 (2019) and #5178 (2021); runtime: exported
  c3runtime.js r503, `EventSheet.Run` calls `FlushPendingInstances()` after
  each top-level event, `_ExecuteTrigger` after the outermost trigger;
  exported c3runtime.js r504, `PickChildren`, `PickParent`, `PickNthChild`
  and `Count` add `instancesPendingCreateForObjectClass` when the picked
  type's SOL is select-all, and no other condition in the file reads that
  list; observed in a game
  project, r504 preview, 2026-10-05: two enemies created when a third died
  were not found by the overlap test that restarted the attackers in the
  same event, so an attacker stopped; observed in a game project, 2026-10-15:
  calling the function that slides the existing cards before the one that
  creates the new card cleared both `check_project.py` warnings, and the
  queue moved as before; observed in a demo project, r506.3 preview,
  2026-10-20: an AJAX *On completed* created twelve Text instances in a *For*
  sub-event, and a later sub-event ran *Wait 0* and then a function whose
  *Compare instance variable* picked and recoloured the three of one row]
