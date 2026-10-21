# Event Sheet Pitfalls: 3D model

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- A 3D model's *Set progress*, the script's `animationProgress` setter and
  `setAnimationProgress` change nothing while the clip plays or is paused.
  The manual says that they set the progress of the current animation, but
  they work after the clip is stopped or has finished. In r505,
  *Play* of a playing clip also leaves the clip where it is, whatever
  progress it is given. So an attack that plays a clip longer than its
  interval shows a swing only on every second attack. r506 starts the clip
  at the given progress. To restart a clip in r505 and r506, stop it with
  *Stop*, the script's `stop()` or `setAnimationPlaying(false, clip)`, then
  *Play* it. A clip stays playing after *Play* switches to another clip.
  *Stop* and `stop()` then stop only the clip played last, although the
  description of *Stop* says that it stops any animations. So *Is playing*
  with the first clip's name and `isAnimationPlaying` stay true, and so
  does the script's `isPlaying`. *Play* cuts to the new clip in one tick
  unless its *Transition duration* (r505) is set. A clip cannot transition
  into itself, so consecutive attacks that should blend take turns between
  two copies of the clip. In r505 and r506, the script's
  `getAnimationProgress(name)` throws a TypeError, so read
  `animationProgress` instead. [manual: plugin-reference/3d-model.md "Set
  progress"; scripting/scripting-reference/plugin-interfaces/3d-model.md
  "animationProgress"; schema r506: *Stop* "Stop any animations"; observed
  in a minimal project with a generated glTF, r505 beta and r506,
  2026-10-14: progress stayed at 0.399 after each setter, *Set progress*
  with the clip named included, and in r505 also after *Play* with
  progress 0 or 0.25, which in r506 gave 0 and 0.25; after *Play* "Rest",
  *Play* "Swing" and then *Stop* or `stop()`, `isAnimationPlaying("Rest")`
  stayed true, and in r506 *Is playing* "Rest" too, and `isAnimationPlaying("Swing")` read false; and in a game
  project, r505 beta, 2026-10-14: a 2.0 s attack clip played every 1.6 s
  started at 1.603 s on every second attack, and a frame-by-frame capture
  showed the sword jump 57 to 72 px in one tick at each clip change]
