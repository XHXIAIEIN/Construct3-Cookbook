# Event Sheet Pitfalls: Tween

Sources and the rule for adding an entry are in the index,
[pitfalls/README.md](README.md).

- If Tween cannot tween a property directly, use a value tween. Run
  *Tween (value)* with a start, an end and a time. Then, in an event with
  *Is playing "tag"*, apply `Self.Tween.Value("tag")` with *Set effect
  parameter*, *Set Z height* or *Set angle*. The tween computes the eased
  value, and the action only reads it. A one-property angle tween to
  `Self.Angle + 360` does not turn the instance. So for a full turn, use a
  value tween from `Self.Angle` to `Self.Angle + 360`, and apply it with
  *Set angle*. [manual: behavior-reference/tween.md "Tween
  (value)", "Value"; example: abductractor ("ReduceLuminosity", "SmashCorn");
  the angle case: github.com/Scirra/Construct-feature-requests/issues/547,
  closed expired]
- *On finished* and *On any finished* fire before *Destroy on complete*
  destroys the instance. So the finish trigger of a death tween can read the
  instance's position, pick its container and spawn objects there. But an
  *On any finished* written for the tweens that settle an instance also runs
  for the tween that destroys it. So give each ending its own tag, and react
  to that tag. [runtime: exported c3runtime.js r503, Tween `_FinishTriggers`
  triggers `OnTweensFinished` and `OnAnyTweensFinished`, then calls
  `DestroyInstance` when `GetDestroyInstanceOnComplete()`; observed in a game
  project, r503 preview, 2026-09-29: sparks spawned from
  `On Tween "collapse" finished` at the shrunk enemy's position, its
  container's hitbox still picked]
- A tween on a property (position, size, angle, opacity, any tween but
  *Tween (value)*) stops every tween that already runs on that property of
  the instance, whatever their tags. A stopped tween never finishes, so it
  runs neither *On finished* nor *Destroy on complete*. So any later size
  tween, such as a landing squash, cancels a death tween that shrinks the
  instance to 0 and destroys it. The instance is then never destroyed. To
  destroy a dying instance, use a Timer on the instance or a *Wait*, and let
  the tween change only its look. Or start no other size tween on a dying
  instance. [runtime: exported
  c3runtime.js r504, Tween `CreateTween` calls `ReleaseTweens(property)`
  unless `Maps.IsValueId`; observed in a game project, r504 preview,
  2026-10-01: an enemy killed while still falling started `die collapse` (size
  to 0, destroy on complete), its landing squash started a size tween 0.15 s
  later, the collapse was gone from `allTweens()` at once, and the enemy
  stayed at full size with collisions off until the stage was stuck]
- A second *Tween (value)* with the tag of a value tween that still plays
  runs beside the first one. `Value(tag)` reads the first tween until it
  ends. So a count restarted mid-way shows the old count's number for the
  rest of the old tween's time, then jumps to the new count's number. Put
  *Stop* for the tag before the restart.
  [runtime: exported c3runtime.js r504, Tween `CreateTween` calls
  `ReleaseTweens(property)` unless `Maps.IsValueId`; observed in a minimal
  project, stable editor preview, 2026-10-08: a score counting from 0 to 6
  got a gain of 10 when the count read 5.3; without the *Stop* its text
  stayed 6 for 0.18 s while the second count, from 6 to 16, passed 11, then
  jumped to 12]
- `Tween.Value(tag)` returns 0 after the tween finishes, not the end value.
  The runtime releases a finished tween, and the expression returns 0 when
  no tween of the tag is left. So a finished value tween cannot hold a
  state, such as a piece that stays enlarged while it is dragged. Write each
  animated channel as its remaining amount: a value tween from the full
  amount to 0. Then, every tick, derive the size or position and add
  `Value(tag)` to it. A channel then adds nothing when it has ended or was
  never started. Channels that different events start add up, and none of
  them overwrites another. [runtime:
  exported c3runtime.js r503, Tween `Exps.Value` returns
  `GetTweenIncludingWaitingForRelease(tag)` or 0, `_FinishTriggers` calls
  `ReleaseTween`; observed in a game project, r503 preview, 2026-09-29]
- A one-property or two-property tween adds each tick's change to its
  property. It does not set the property to the eased value. The runtime
  names the properties `offsetX`, `offsetWidth` and so on, and calls
  `OffsetWidth(change)`. So a *Set width* or *Set X* while such a tween
  plays stays in effect, and the tween adds the rest of its change on top.
  The tween then misses its end value by the amount that the *Set* moved
  the property. If an event sets the same property while the tween may
  still run, add *NOT Is playing "tag"* to that event, or *Stop* the tween
  before the *Set*. An example is a level setup that sets a bar's width
  while the bar's own tween plays. [runtime: exported c3runtime.js r503,
  Tween property track `"offsetWidth"` setter calls `t.OffsetWidth(e)` with
  the tick's change; observed in a game project, r503 preview, 2026-09-29: a
  progress bar tweened from 416 to 20 px over 0.55 s, set to 20 by the next
  level's setup at 0.6 s of the tween's 0.67 s, ended at 2 px]
- After *Stop*, a channel reads 0 only from the next tick. The runtime puts
  the stopped tween on a list that it releases at the end of the tick. So
  `Value(tag)`, `Progress` and `Time` still read the stopped tween for the
  rest of that tick, and events after the *Stop* see the value where it
  stopped. If one action list stops one channel and starts another, one
  frame therefore draws both. This blends a crouch into the jump that
  releases it, instead of a frame of the rest pose between them. The
  expressions find active tweens first, so after a *Stop* and a restart
  under the same tag, they read the restarted tween at once. [runtime: exported
  c3runtime.js r503, Tween `StopTweens` calls `ReleaseTween`, which moves the
  tween to `_waitingForReleaseTweens`, emptied in `Tick2`; `Exps.Value` reads
  `GetTweenIncludingWaitingForRelease`, whose list puts active tweens first;
  observed in a game project, r503 preview, 2026-09-29: a crouch channel
  stopped as the jump squash started read 1 in that frame, 0 in the next]
- A width tween can end with the width slightly below its end value. The
  width and the end value then both print 355.2, but `Width < target`
  still holds. So an event with
  `Width < target` and `NOT Is playing "grow"` starts a tween of zero
  distance each time the last one ends. That tween counts as playing for
  its whole 0.3 s, so a real change of the target in that time starts no
  tween. Write two events instead. The first starts the tween on a
  comparison with a tolerance, `Width < target - 0.5`. The second covers
  the gap that the tolerance leaves: with `Width < target` and
  `NOT Is playing "grow"`, it sets the width to `target`. A trail tested
  with `Width > target` has the same gap and needs the same two events.
  [observed in a minimal project, stable editor preview,
  2026-10-07: three bars with a growth tween each; two of them held a
  zero-distance tween in a loop, and when a heal raised their target they
  grew 0.19 s late, only after the loop's current tween ended, while the
  third bar, which had no such loop, started at once. Found by listing each
  bar's tweens every tick, `[...inst.behaviors.Tween.allTweens()]`, with the
  `tags` and `progress` of each]
