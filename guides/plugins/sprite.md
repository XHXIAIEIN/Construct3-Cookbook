# Event Sheet Pitfalls: Sprite

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- An instance with collisions disabled fails every overlap and collision
  test, in both directions. To take a dragged or tweening instance out of
  these tests, disable its collisions instead of setting an `isMoving`
  flag. [manual: plugin-reference/sprite.md "Set collisions enabled";
  scripting/scripting-reference/object-interfaces/iworldinstance.md
  `isCollisionEnabled`]

- Image point index 0 is the origin. The first image point added is index
  1, and `ImagePointCount` does not count the origin. So a loop over every
  image point runs from 1 to `ImagePointCount` and reads
  `ImagePointX(loopindex)`. A loop that starts at 0 reads the origin and
  misses the last point. A name, as in `ImagePointX("P1")`, reads the same
  point whatever the order of the image points. [manual:
  interface/animations-editor.md "the first image point (number 0) is
  always the origin"; scripting/scripting-reference/plugin-interfaces/sprite.md
  "getImagePointX"; plugin-reference/sprite.md "ImagePointX" says only
  zero-based. observed: r495.2 preview, a Sprite at X 400, 100 px wide,
  origin centred, points P1 and P2 at its left and right edges:
  `ImagePointCount` 2, index 0 400, 1 350, 2 450, 2026-09-23]

- *Set animation* to the animation that already plays does nothing, even
  if it is set to play from the beginning. So set the animation from the
  state in one event. The animation does not restart, so it needs no
  `anim` variable compared before every *Set animation*. To restart the
  animation, use *Start animation* from the beginning. [manual:
  plugin-reference/sprite.md "Set animation"; observed in a game
  project, 2026-09-22]

- *Set animation* to another animation takes the new animation's *Speed*
  and *Repeat to* from the Animations Editor. This holds whether it plays
  from the beginning or from the current frame. So a *Set speed* or a *Set
  repeat-to frame* that runs before it is lost. Run *Set speed* after *Set
  animation*. In *On finished* and *On any finished*, this order is not
  enough, and the entry after the next one applies. [observed in a probe project, r506.3
  preview, 2026-10-30: *Set speed* 20, then *Set animation* to an
  animation of *Speed* 10, read `AnimationSpeed` 10, and the reverse
  order read 20; *Set repeat-to frame* 3, then *Set animation* to an
  animation whose *Repeat to* is 2, read 2 in the script interface's
  `animationRepeatToFrame`; runtime: r506.3 Sprite `_DoChangeAnimation`]

- A looping animation never finishes, so *On finished* and *On any
  finished* never fire for it. An attack, a hurt or a death state that
  ends in *On finished* never ends if its animation has *Loop* on. So turn
  *Loop* off for every animation whose end changes the state. [manual:
  plugin-reference/sprite.md "On any finished", "On finished"]

- In *On finished* and *On any finished*, *Set animation* takes effect on
  the next tick, and it then sets the speed to the new animation's
  *Speed*. So a *Set speed* after it in the same trigger is lost. The *Set
  speed* is also lost after a *Wait 0* between the two actions. It is lost
  in a later event of the same tick too. To give the next animation another
  speed, start the trigger's actions with *Wait 0*, then run *Set
  animation* and *Set speed*. In *On frame changed*, *Set animation* takes
  effect at once, and a *Set speed* after it holds.
  [observed in a probe project, r506.3 preview, 2026-10-30: in *On
  finished*, *Set animation* to an animation of *Speed* 10, then *Set
  speed* 20, read `AnimationSpeed` 20 in that tick and 10 from the next;
  with *Wait 0* between the two actions, or with *Set speed* in a later
  event, 10; with *Wait 0* first, 20; *On any finished* read as *On
  finished*; in *On frame changed*, the new animation's name and
  repeat-to frame and `AnimationSpeed` 20 read at once, and 20 0.3 s
  later; runtime: r506.3 Sprite
  `_SetAnim`, `_FinishAnimation`, `Tick`]

- *On frame changed* fires whenever the shown frame changes, also while
  the animation is stopped. *Set animation* to another animation, *Set
  frame* and *Start animation* from the beginning fire it. It does not
  fire if the frame stays the same: *Set frame* to the current frame,
  *Start animation* on frame 0, or *Set animation* to the animation
  already playing. So a footstep
  sound or a counter in *On frame changed* also runs when an event sets
  the animation or the frame. To act on one frame of the playback, add
  *Compare frame* to that event. [manual: plugin-reference/sprite.md "On
  frame changed" says only "while the animation is playing"; observed in
  a probe project, r506.3 preview, 2026-10-30: on an instance whose
  animation was stopped or had *Speed* 0, each *Set frame* to another
  frame, *Start animation* from the beginning on frame 2 and *Set
  animation* to another animation fired it once; *Set frame* to the
  current frame, *Start animation* from the beginning on frame 0 and *Set
  animation* to the animation already playing did not; runtime: r506.3
  Sprite `_OnFrameChanged`, `_DoChangeAnimFrame`]

- If an animation's frames serve as looks rather than as an animation, set
  the animation's *Speed* to 0. A one-frame animation at the default speed
  5 shows no motion. But with more frames, every created instance plays
  through the frames and stops on the last one, whatever frame *Set frame*
  chose. [observed in a
  game project, r503 preview, 2026-09-28: frames 0 to 2 of a non-looping
  animation at speed 5, every enemy ended on frame 2 until speed was 0]

- *Set frame* to a frame with another image size resizes the instance by
  the ratio of the two image sizes and keeps its scale. It also takes the
  new frame's collision polygon and origin. So a frame drawn wider with
  transparent margins widens the area that the instance overlaps. For
  example, a boss frame three lanes wide is hit by every lane's range,
  although the targeting events stay the same.
  [runtime: exported c3runtime.js r503, Sprite
  `_OnFrameChanged` scales width and height by new/old image size and calls
  `SetSourceCollisionPoly`; observed in a game project, r503 preview,
  2026-09-28: a 72 px enemy set to a 520×216 frame became 260×108 and
  overlapped three 40 px lane ranges]

- A bar grows from its origin. Every filling bar in the examples has its
  origin on the edge that it grows from, (0, 0) or (0, 0.5). A cover that
  hides the bar from the right has its origin at (1, 0.5). With an origin
  of 0.5, a bar grows both ways from the middle. [examples: berry-harvester
  ProgressBar, jetpack FuelBar, flatland-golf PowerBarCover, test-your-might
  MightLevelBar (0.5, 1)]
