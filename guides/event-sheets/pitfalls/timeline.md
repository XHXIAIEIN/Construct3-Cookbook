# Event Sheet Pitfalls: Timeline

Sources and the rule for adding an entry are in the index,
[pitfalls/README.md](README.md). If you read or write a timeline or a
custom ease in the project files, read "Timelines and custom eases" in
[project-files/hand-editing.md](../project-files/hand-editing.md).

- In *Relative* mode, a numeric property track changes its property by the
  step of each tick, `Offset…(value − last value)`. The last value starts at
  0 when playback starts forward. So a keyframe's value is an offset from
  the instance's value at the start of playback, not a position. Two
  relative timelines on one instance add up. If an event sets the same
  property every tick, only that tick's step of the timeline stays on it. On
  a hierarchy child with the timeline's *Transform* on, X, Y and angle are
  offsets in the parent's frame. So the child keeps following a parent that
  events move every tick. Animate a part's position and angle relative to
  its parent, and let events set its size. Make each move start and end at
  0, so that layered and replayed moves leave no offset. [runtime: exported
  c3runtime.js r504,
  `NumericInterpolationAdapterForTimeline.ChangeProperty` calls
  `_Setter(t - GetLastValue())` in relative mode, `SetInitialState` sets the
  last value to 0 when playing forward, the `offsetX` setter calls
  `OffsetX(e, GetTransformWithSceneGraph())`, which adds to the local offset
  of a child; observed in a game project, r504 preview, 2026-09-30: a sword
  parented to a body placed by events every tick kept its slash pose, and an
  idle sway and a slash timeline on the same sword added up]
- An angle keyframe's direction, `clockwise` or `anti-clockwise`, holds for
  the segment that starts at that keyframe, whatever the two values of the
  segment are. If the direction disagrees with the shorter way to the next
  value, the instance turns the long way: from 0 to +90°, *Anti-clockwise*
  turns −270°. *Closest* takes the shorter way, and *Revolutions* adds full
  turns. So if a generator writes the keyframes, make it set each keyframe's
  direction from the sign of the change to the next keyframe: a positive
  change is clockwise. [runtime: exported c3runtime.js r504, the angle
  adapter's `Interpolate` switches on `GetDirection()` to `C3.angleLerp`,
  `C3.angleLerpClockwise` or `C3.angleLerpAntiClockwise`; observed in a game
  project, r504 preview, October 2026: a bow keyframe from 300° to 390° set
  *Anti-clockwise* spun the bow 270° backwards]
- *Set instance* applies only to the next *Play*. If several instances are
  picked, one *Play* starts a copy of the timeline for each of them, all
  with the same tags. So every copy responds to the same *Set time* or
  *Stop*. Set one instance at a time in a *For each*, and give each copy its
  own tag, such as `"slash-" & Self.UID`. Do not use a timeline's name as a
  tag, because `Time`, `TotalTime` and `KeyframeTime` look up names before
  tags. A later *Play* of the same timeline for the same instance reuses its
  copy, and it does nothing while that copy plays. To restart the copy,
  *Set time* 0, then *Resume*. [runtime: r504 preview, Timeline plugin
  `_PlayTimelineSyncAndReturnPromises` takes one picked instance per track at
  a time, finds a copy with `GetTimelineOfTemplateForInstances` or makes one
  with `CreateFromTemplate`, then `SetTags(tags)` and `Play()`;
  `TimelineState.Play` returns false while `_IsPlaying()`; `Exps.Time` tries
  `GetTimelinesByName` before `GetTimelinesByTags`; observed in a game
  project, r504 preview, 2026-09-30: three swords, one copy of each of two
  timelines per sword, each reached by its own tag]
- To find an instance's copy of a timeline, the runtime looks for a copy
  whose name, such as `HeroAttack:3`, contains the timeline's name. So a
  timeline named `Attack` also matches the copies of `HeroAttack` played on
  that instance. If two timelines play on the same object, name them so
  that neither name contains the other. [runtime: exported
  c3runtime.js r504, `TimelineManager.GetTimelineOfTemplateForInstances` tests
  `t.GetName().includes(e.GetName())`; reported as Scirra/Construct-bugs#9288,
  closed 2026-10-01 as fixed in the next beta after r504]
- *Stop* moves the playhead back to 0 and applies that pose in the same
  tick. So if a relative timeline stops midway, it takes its offsets back.
  This also holds when the timeline is paused, set by *Set time*, playing
  backwards or layered with another relative timeline on the instance. A
  finished timeline ignores *Stop* and keeps its end pose, so the offsets of
  a relative track stay on the instance. *Set time* 0 takes them back.
  *Pause* keeps the pose where it is. *Resume* does nothing after a
  non-looping timeline has reached its end, so first move the playhead back
  with *Set time*. [runtime: r504 preview,
  Timeline plugin `StopTimeline` calls `Reset()`, `PauseTimeline` calls
  `Stop()`; `TimelineState.Reset` returns when `IsComplete()`, `_CanResume` is
  false when the time is at the total time; observed in a game project, r504
  preview, 2026-09-30: the second slash only started after *Set time* 0 moved
  the playhead off the end; observed in a minimal project, r495.2 and r504
  preview, 2026-10-01: a relative X track at +121 px and an angle track at
  −57°, on a hierarchy child too, read 0 in the tick of *Stop* from each of
  those states, and a finished one kept +484 px after *Stop* and read 0 after
  *Set time* 0. The finished case was reported as Scirra/Construct-bugs#9287,
  closed 2026-09-30: the next beta after r504 sets the time to 0 on *Stop* of
  a timeline that is not playing; *Set time* 0 works in both]
- *Set time* pauses a playing timeline at the time that it sets. After a
  *Play* in the same action list, it takes the timeline off the schedule and
  applies the pose. So *Play* followed by *Set time* creates an instance's
  copy without playing it. *Set time* triggers *On time set*, never *On
  keyframe reached*. So if *Set time* moves the playhead across a tagged
  keyframe, the keyframe's events do not run. [runtime: exported
  c3runtime.js r504, `TimelineState.SetTime` stops a playing timeline and
  deschedules a scheduled one, then interpolates with the ticking flag off;
  `TrackState.MaybeTriggerKeyframeReachedConditions` returns when not ticking;
  observed in a game project, r504 preview, 2026-09-30]
- *On keyframe reached* picks no instance. If copies play on several
  instances, put the instance's UID in the tags, and pick the instance back
  from `Timeline.TimelineTags`. For the tags `sword-move-146`, use
  `Pick by unique ID int(tokenat(Timeline.TimelineTags, 2, "-"))`. [manual:
  plugin-reference/timeline-controller.md "On keyframe reached",
  "TimelineTags"; runtime: r504 preview, `Cnds.OnKeyframeReached` only
  compares the reached keyframe's tags; observed in a game project, r504
  preview, 2026-09-30]
- *On keyframe reached* runs before the track writes the values of that
  tick. So in the trigger, the instance still holds the previous tick's
  pose, part of the way into the segment that ends at the keyframe. If
  actions must read the keyframe's pose, such as to launch a sprite from a
  sword held overhead, put *Wait 0* before them. They then run at the start
  of the next tick, after the runtime has applied and drawn the keyframe's
  pose. *Wait 0* exists for this case (see
  [Wait and time scale](wait-and-time-scale.md)). [runtime: exported
  c3runtime.js r504, `TrackState.Interpolate` calls
  `MaybeTriggerKeyframeReachedConditions`, which fires the triggers
  synchronously through `OnKeyframeReached`, before the property tracks'
  `Interpolate`; observed in a game project, r504 preview, 2026-10-01: a
  sprite created at a sword's position in the trigger started 12 px off the
  pose drawn at the keyframe, and after *Wait 0* matched it within 1 px;
  reported as Scirra/Construct-bugs#9291: in the trigger `Time` reads the
  keyframe's time while a discrete track still holds the value before the
  keyframe; closed 2026-10-01, to be fixed in the first beta after the next
  stable release, where the *Wait 0* is no longer needed]
- A negative playback rate plays a timeline back to 0, and the timeline
  finishes there. If a windup is cancelled midway, *Set playback rate* −3
  takes the pose back smoothly, and a relative timeline ends with its
  offsets gone. Set a positive rate again before the next *Resume*, because
  otherwise that *Resume* restarts the timeline backwards from the end.
  [runtime: exported c3runtime.js r504, `TimelineState.Tick`
  stops at 0 when the rate is negative; `SetInitialState` starts a complete
  timeline from 0 or from its total time by the sign of the rate; observed in
  a game project, r504 preview, 2026-09-30: a slash stopped at 0.206 s, set to
  −3, was back at 0 and finished 0.08 s later]
- If a timeline played forward to its end and stopped there, *Resume*
  cannot play it backwards. While the timeline is not playing, the runtime
  counts it as playing forward at any playback rate. So a timeline stopped
  at its total time is at the end of a forward pass, and it cannot resume.
  To take back a pose held at the end, first *Set time* to
  `TotalTime(tag) - 0.001`. Then set a negative rate and *Resume*. This 1 ms
  moves a relative track by the distance that its last segment covers in
  that time, which is nothing under an ease that flattens at the end. If the
  timeline is still playing, set the negative rate and *Resume* directly.
  [runtime: exported c3runtime.js r504,
  `TimelineState.IsForwardPlayBack` returns `!IsPlaying() || playbackRate >
  0`, `_CanResume` returns false when forward and `GetTime() >=
  GetTotalTime()`; observed in a game project, r504 preview, 2026-09-30: a
  sword pose held at the end of its 0.36 s stayed put while events set rate −2
  and *Resume*d it, and after *Set time* 0.359 the same actions took it back
  to 0 in 0.18 s]
- A copy that *Resume* or *Play* starts is playing at once, but its
  playhead reads 0 until the timeline ticks it. So an event later in the
  same tick, or an action resumed after a *Wait*, sees `Time` 0 with *Is
  playing* true. To test whether a move is under way, use *Is playing*,
  because `Time > 0` misses a move that started in this tick. [observed in
  a game project, r504 preview,
  2026-10-01: a pose timeline resumed in one event read `Time` 0 in a later
  event of the same tick, which took it for idle and did not take it back
  under a new move; sampled after that tick, the copy read `Time` 0 and
  *Is playing* true]
- Rewind a copy only if `Time > 0`. If its playhead reads 0, *Set time* 0
  instead, which takes the copy off the schedule without moving the
  instance. This holds even if *Is playing* is true because the copy was
  resumed earlier in the same tick. A negative rate set before the copy
  starts makes it start backwards from its total time. A relative track then
  takes its end pose as already applied. So the track subtracts that pose on
  the way back to 0 and leaves the offset on the instance permanently.
  [runtime: exported c3runtime.js
  r504, `TrackState.SetInitialState` starts at `GetLocalTotalTime()` when the
  timeline is not playing forward, and
  `NumericInterpolationAdapterForTimeline.SetInitialState` sets a relative
  track's last value to `GetValueAtTime()` instead of 0; observed in a game
  project, r504 preview, 2026-10-02: a rest pose ending at +40° was resumed
  and, later in the same tick, rewound at −2 by an event that tested
  *Is playing*; each time the sword was left 40° off, 80° after two stage
  clears, and with the `Time > 0` test and *Set time* 0 no sword drifted over
  the same run]
- A negative playback rate fires *On keyframe reached* for every tagged
  keyframe that it passes on the way back, with the same tags as the forward
  pass. So a move rewound at −4 runs its keyframe events again, such as a
  jump or a burst of sparks. The keyframe trigger cannot read the playback
  rate. So if an event must run only on the forward pass, make it test a
  flag such as `rewinding`. Set the flag in the event that starts the
  rewind, and clear it at the forward *Resume*. [runtime: exported
  c3runtime.js r504,
  `TrackState.MaybeTriggerKeyframeReachedConditions` has an `else` branch for
  `!IsForwardPlayBack()` that calls `OnKeyframeReached` for the keyframe at or
  above the new time; observed in a game project, r504 preview, 2026-10-02]
- A timeline follows the system time scale while its *Use system
  timescale* property is on, which is the default. So *Set time scale* 0.1
  for a hit stop slows the timeline with everything else, and a strike
  stops at the moment that it lands. The timeline's playback rate
  multiplies the time scale. [manual:
  project-primitives/timelines/timeline.md "Use system timescale"; runtime:
  exported c3runtime.js r504, `TimelineState.Tick` advances by
  `dt × timeScale × playbackRate` when `GetUseSystemTimescale()`; observed in
  a game project, r504 preview, 2026-09-30: during a 0.1 hit stop the playhead
  advanced 0.005 s while the game time advanced 0.004 s]
