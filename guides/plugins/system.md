# Event Sheet Pitfalls: System

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- *Wait* does not stop a loop. The remaining iterations run in the same
  tick. The actions after the *Wait* run later, once per iteration, with
  the picked instances of that iteration. So a staggered effect is
  `Wait 0.1 * loopindex`. If a loop must pause between iterations, use a
  Timer or a function called from *On timer*.
  [manual: system-reference/system-actions.md "Wait";
  examples: arcade-shooter, layout-transition]

- A *Wait* keeps the instances its event picked. The actions after it act
  on those instances, even if other events pick or create instances during
  the wait. An instance destroyed during the wait drops out. So *Wait 2
  seconds* then *Destroy* in one action list destroys the instance that
  started the wait. It needs no stored UID and no *Pick by unique ID*. If
  the event picked several instances, the actions after the wait run on
  all of them.
  [runtime: exported c3runtime.js r503, `ScheduledWait._Init` saves the
  SOL of every object type and the wait restores it when it resumes; read
  from source, not observed; construct.net tutorial system-wait-action-63,
  "Wait remembers picked objects"]

- *Wait for previous actions* waits only for asynchronous actions. The
  manual names it "Wait for previous actions to complete". The editor
  marks asynchronous actions with an icon: Tween actions, AJAX requests,
  Local Storage, *Snapshot canvas*. The other actions before it have
  already finished. A function call counts only if the function is marked
  *Asynchronous* (`functionIsAsync` in the sheet). The caller then waits
  for the function's own *Wait* actions. It waits for the asynchronous
  actions in the function only if the function ends with *Wait for
  previous actions*. The mark changes nothing in the function itself. A
  function without it runs its *Wait* and the actions after it in the same
  way, but the caller's *Wait for previous actions* returns at once. So if
  a caller must wait for what a function does after a *Wait*, mark the
  function *Asynchronous*. [manual:
  system-reference/system-actions.md "Wait for previous actions to
  complete", project-primitives/events/functions.md "Asynchronous
  functions"; example: avalanche, sheets Stalagmite and Credits; observed in
  a minimal project, r506.2 preview, 2026-10-16: a function with *Wait 0.5*
  then *Set value*, called before *Wait for previous actions* and a read of
  the value, gave the read 0 with the flag off and 1 with it on, and set
  the value half a second later either way]

- A *Wait* delays only the actions after it in its own block and that
  block's sub-events. A sibling event, or the next sub-event of the same
  parent, runs at once. So if *Wait for previous actions* is alone in
  sub-event 1 and *Destroy* is in sub-event 2, *Destroy* runs before the
  tween ends. Put the asynchronous action, the wait and the actions after
  it in one action list. [manual:
  system-reference/system-actions.md "Wait", "Wait for previous actions to
  complete": "before continuing on to the next action or sub-events. Other
  events continue to run in the meantime."]

- A *Wait* with *Use time scale* on never ends while the time scale is 0.
  So turn *Use time scale* off on the wait that resumes the game. For the
  UI tweens of the pause, use *Set object time scale* 1 on the fader, the
  buttons and the manager object. [manual: system-reference/system-actions.md
  "Wait", "Set object time scale"; example: airborne-explorer, In-Game Menu]

- *Wait 0* resumes at the start of the next tick, not at the end of the event
  or the sheet. The current tick first runs all its events and is drawn. Then
  the rest of the event runs one frame late, before the next tick's behaviors
  and events. This holds in an included sheet and in a function too. The
  rest of the event keeps the picks
  saved at the *Wait*, minus destroyed instances, and restores function
  parameters and function locals. It also runs at time scale 0, and a layout
  change cancels it. *Wait for previous actions* with nothing to wait for
  resumes at the same point. Leave *Wait 0* out, because the next top-level
  event can pick a created instance and a destroyed one is gone by then (see
  [How events work](../primitives/events/how-events-work.md)). Instead, initialise in *On
  created* or the creating event, pass `UID`, or put the dependent step in a
  later top-level event or trigger. Use *Wait 0* only if a trigger fires
  before the tick finishes what it reports, or if no later event or trigger
  runs a step that picks the instances a trigger created. For example, *On
  keyframe reached* fires before the keyframe's values are written (see
  [Timeline controller](timeline.md)). Ashley's tutorial says "until the end of the
  event sheet", which is Construct 2 wording. [runtime: exported c3runtime.js
  r503, `Wait` calls `AddScheduledWait`, `RunScheduledWaits` is called only
  from `Step_BeforePreTick`, ahead of `Step_RunEventsEtc` and `Render`;
  `ScheduledWait._Init` saves SOL, parameters and locals;
  `ClearAllScheduledWaits` on layout end; read from source, not observed.
  Ashley: "rarely any need to use Wait 0 seconds", forum
  construct-2/general-discussion-17/wait-59374; *Wait for previous actions*
  "always runs at the end of the tick", Scirra/Construct-bugs#3948;
  construct.net tutorial system-wait-action-63, updated 2019]

- *Set time scale* 0 also stops every animation. So a cutscene, an
  ultimate's full-screen animation or a pause menu's own animation stops
  with the battle. Pause with *Set time scale* 0, then *Set object time
  scale* 1 on the object that must keep playing. In the Sprite's *On
  finished* for that animation, run *Set time scale* 1 and *Restore object
  time scale* on the object. *Set object time scale* also drives the
  object's animation, but the manual names only its behaviors and its
  `dt`.
  [manual: system-reference/system-actions.md "Set object time scale";
  observed in effects-screen-blend, r495.2 preview, 2026-10-09: at time
  scale 0, a 15 fps explosion whose instances got time scale 1 from a
  script, the value the action sets, went from frame 7 to 22
  in 1 s, and the other explosion stayed on frame 7]

- A hit stop is *Set time scale* 0.1, *Wait* and *Set time scale* 1 in one
  block. A smooth ramp is a *Tween (value)* on any object, read into *Set
  time scale* while the tween *Is playing*.
  [examples: segmented-boss-fight BossHeath;
  samuroof Credits `Camera.Tween.Value("TimeScaleChange")`; eventide `1 -
  PauseUI.Tween.Progress("ShowPause")`]

- Two such hit stops can overlap, as with a critical hit that also kills,
  or two lanes that resolve in one tick. Then each stop restores the time
  scale when its own *Wait* ends. So the shorter stop ends the longer one
  early. Count the running stops in a variable: add 1 before the *Wait*
  and subtract 1 after it. Set the time scale to 1 only when the count is
  back to 0. Do not compare a `wallclocktime` deadline after the *Wait* in
  place of the count. An unscaled *Wait* counts the runtime's wall time.
  This is the sum of each tick's clamped `dt`, taken at the start of the
  tick. But `wallclocktime` is `Date.now()`, read mid-tick. So if a stop
  starts a few milliseconds into a busy tick, its deadline has not passed
  when its *Wait* ends. Then the time scale stays at 0.1 until the next
  hit stop. [manual:
  system-reference/system-expressions.md "wallclocktime"; runtime: exported
  c3runtime.js r504, `wallclocktime` returns `(Date.now() - GetStartTime()) /
  1e3`, `Wait` with *Use time scale* off calls `InitWallTimer`, `_wallTime`
  adds `_dt1`, clamped to `_maxDt` 1/30; observed in a game project, r504
  preview, 2026-10-02: a 0.05 s crit stop and a 0.08 s kill stop in one tick
  lasted 0.05 s with no deadline and 0.08 s with one; a 0.08 s stop called 8
  to 16 ms into a tick stayed at 0.1 in 20 of 20 runs with the
  `wallclocktime` deadline and in 0 of 20 with the count, which still lasted
  0.08 s for the overlapping pair]

- A hit stop slows every tween and every `dt` on game time. So a tween
  that starts on the audio clock to end on a beat ends late. The delay is
  0.9 of the length of each stop inside the tween, and overlapping stops
  add their delays. Set the time scale of the tween's object to 1 for that
  tween, and restore it with *Restore object time scale* in *On finished*.
  If a per-tick blend must keep real time, divide `dt` by `timescale`.
  [manual:
  system-reference/system-actions.md "Set object time scale", "Restore
  object time scale"; system-reference/system-expressions.md "dt",
  "timescale"; observed in a game project, r504 preview, 2026-10-02: an
  elite dropped from 0.35 s before a beat to land on it landed 0.13 s late
  when two kills fell inside the drop, and 1 ms early to 7 ms late with its
  time scale at 1; a `1 - exp(-dt / 0.1)` blend on game time kept a progress
  icon nodding at full depth through a 0.1 s kill stop]

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

- *For* runs from its start index to its end index inclusive, and counts down
  if the end is below the start. So `For 0 to count - 1` over an empty list
  runs for 0 and -1. `For first to last` with `first` past `last` runs
  backwards over unwanted indexes. Put `count > 0`, or `first <= last`, among
  the same event's conditions before the loop. [runtime: exported
  c3runtime.js r504, `_For` takes the `--e` branch when the end is below the
  start]

- `tokencount("", ",")` is 1, not 0, and `tokencount("a,", ",")` is 2. The
  count is the number of separators plus one, whatever the text is. So
  *Repeat tokencount(list, ",")* over an empty list runs once, with
  `tokenat` reading `""`. Test `list ≠ ""` among the event's conditions
  before the loop, or skip an empty token inside it. [manual:
  system-reference/system-expressions.md "tokencount", which gives only a
  non-empty example; observed in a minimal project, r506.2 preview,
  2026-10-16: `tokencount("", ",")` read 1, `tokencount("a", ",")` 1,
  `tokencount("a,b", ",")` 2 and `tokencount("a,", ",")` 2]

- `anglelerp(a, b, x)` turns from `a` to `b` by the shorter way. If `b`
  moves while `x` runs from 0 to 1, the direction of turn can reverse. An
  example is an angle that eases back to a rest angle beside an aim that
  follows the pointer. In the tick where `b` passes the opposite of `a`,
  the shorter way reverses, and the angle jumps by up to 360 × `x`
  degrees. Instead, ease an offset from the moving angle. Store the start
  offset as `angle - aim`, then write
  `aim + anglelerp(startOffset, restOffset, x)`. Both offsets stay fixed,
  so the direction cannot reverse, and the result turns with the aim.
  [manual: system-reference/system-expressions.md
  "anglelerp"; the shorter way and its reversal observed in a game project,
  r495.2 preview, 2026-10-14: a sword easing back to rest beside the aim
  jumped between 126 and 176 degrees in one tick when the pointer passed the
  opposite direction early in the ease. With offsets, no tick turned it by
  more than the aim's turn plus the ease's step]

- `rgbEx` and `rgba` take each channel from 0 to 100, and `rgbEx255` and
  `rgba255` take each channel from 0 to 255. `rgbEx` clamps a channel past
  100, so a colour written on the 0-255 scale draws paler. In one demo, a
  blue drew pale, and grey lines of `#DEDEDE` drew white. Write a fixed
  colour as `HexColor("#RRGGBB")` and a computed colour as
  `rgbEx255(r, g, b)`. Do not use the deprecated `rgb`. [manual:
  system-reference/system-expressions.md "rgbEx"; observed in an Array
  IndexOfY demo, r506.3 preview, 2026-10-20]

- *Set canvas size* changes the size of the viewport and, with it, the
  project's *Window size*. So if a 4:3 game is shown inside a 16:9 window,
  its viewport grows and shows more of the layout at the sides. To keep the
  game where it was, *Scroll to position* back to the centre of the play
  area. Cover the extra width on each side with a bar sprite on the top
  layer. [plugins/system.json
  `set-canvas-size`, "also altering the 'Window size' project property";
  observation in a studied project, 2026-10-06]

- *Create object* picks only the new instance, plus the created children if
  *Create hierarchy* is on. It creates the container siblings too. The new
  instance's families are not picked. So a family action after *Create
  object* in the same action list acts on every other instance of the
  family and misses the new one. If an action must reach the new instance
  through the family, use *System: Pick last created* with the family in a
  sub-event. The manual names this as the way to pick a created instance
  from its family. [manual: system-reference/system-actions.md
  "Create object"; system-reference/system-conditions.md "Pick last created";
  observed in a minimal project, r504 preview, 2026-10-02: `Create object
  BladeEnemy` then `Enemies: Set X 777` moved the 19 instances already there
  and not the new one; *Pick last created Enemies* in a sub-event picked the
  new one alone]

- *Create object* is a System action, so it runs once per event, however many
  instances are picked. `Slot.X` in its parameters reads the first picked
  instance. A custom action runs once with all the caller's picks. So
  `Slot: Spawn enemy` over three picked slots creates one enemy, at the
  first slot. If each picked instance must create one, put *For each*
  among the conditions of the custom action's block or of the event. Or
  use the object's own *Spawn another object*.
  [manual: system-reference/system-conditions.md "For Each" "force
  the event to apply once per instance";
  project-primitives/events/custom-actions.md "Picking"; observed in a game
  project, r503 preview, 2026-09-28: a custom action on 3 picked slots
  created 1 instance, 3 once the block held *For each*]

- If the template name is empty, *Create object* copies the instance of the
  type that is listed first in the first layout, in project order, that
  holds one. The current layout and the uids do not affect the choice. So a
  type placed in several layouts, or several times in one, is created with
  that one instance's frame, size and opacity. An edit to that instance in
  the editor changes every runtime creation. A template instance in a later
  layout is never read. Mark one instance as a template and name it in
  *Create object*. If *Create hierarchy* is on, the new instance also gets
  that template's children. A name that no template has falls back to the
  first instance. [manual: system-reference/system-actions.md "Create
  object", "rather than an arbitrary instance";
  project-primitives/objects/templates.md "Runtime actions"; observed in a
  minimal project, r506.2 preview, 2026-10-16: the first layout held two
  instances of a type on one layer and the second layout one. Creation in
  either layout copied the instance that came first in the first layout's
  file, 64×64 opaque at frame 0 or 128×128 half-opaque at frame 1 as the
  two were swapped, never the second layout's own 32×32 one, which had the
  lowest uid. The named template copied the named instance]

- *Create hierarchy* creates the children on the layer of the new parent,
  not on the layers where the template's children sit. So a template whose
  children sit on another layer also creates in a layout without that
  layer, and there the children go on the parent's layer. If children must
  sit on a layer of their own, move them there with *Move to layer* after
  the creation. [observed in a minimal project, r506.2
  preview, 2026-10-16: a parent whose child sat on the layer "Parts",
  created with *Create hierarchy* on the layer "Game" in that layout and in
  a layout without "Parts", got its child on "Game" both times, with no
  error]

- A layout loads the images of the objects placed in it when it starts. An
  object that only events create, with its template in a layout that never
  runs, loads its images when it is created. The game keeps running, and
  the instance draws nothing until the images arrive. So a picture the size
  of the screen shows a moment late, and an object that must cover
  something flickers. A small picture is ready by the next tick. If events
  create a large picture, put *Load object images* in *On start of layout*.
  Or place an instance in that layout and destroy it at the start. [manual:
  tips-and-guides/memory-usage.md "Layout-by-layout loading",
  tips-and-guides/importing-c2-projects.md, system-reference/system-actions.md
  "Load object images"; observed in a probe project, r495.2 preview,
  2026-10-08: a 1920×1080 Sprite created by a script mid-game had no texture
  for 62 to 100 ms, 6 to 10 ticks, with no tick longer than usual; placed
  in the layout or loaded at the start, it had one at once, and a 160×160
  one by the next tick]

- *Restart layout* and *Go to layout* bring the layout's instances back as
  placed. They keep every global variable and static local at its current
  value. So a countdown, a score or a count that a round starts from still
  holds its end value when the layout runs again. If a global countdown
  restarted the layout at 0, it is 0 on the next run, so it restarts the
  layout every tick. Set such a value under *On start of layout*. Or, where
  the game starts over, run *Reset global variables*, and *Reset static*
  for static locals. A countdown works better as a Timer on an object of
  the layout, started under *On start of layout*. The restart recreates the
  object with no timer running, so nothing is left to set back. [manual:
  system-reference/system-actions.md "Restart layout", "Go to layout",
  "Reset global variables"; project-primitives/events/variables.md "Static
  and constant variables"; behavior-reference/timer.md; observed in preview,
  2026-09-28]
