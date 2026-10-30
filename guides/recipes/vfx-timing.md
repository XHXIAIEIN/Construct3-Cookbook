# Effect timing

A hit effect reads as a hit when its shape, its brightness and its length
agree on one beat. This page gives the frame counts of that beat and the
Construct way to build each. For the wind-up, the animation and the sounds
of the attack that the effect belongs to, read
[attack-feel.md](attack-feel.md). For the shake, the hit stop and the
squash around it, read [feel.md](feel.md). In a pixel-art game, also read
[pixel-art-vfx.md](pixel-art-vfx.md): it fades the shapes by steps and
keeps the additive blend for the glow.

The numbers come from the decoded frames of seven published effect reels:
4,468 frames at 60 fps, so 16.7 ms a frame, from 2.4 s to 27.9 s each.
Each rule ends with the kind of its evidence:

- `frames`: read from those frames. The reels are not this project's and
  carry their encoder's blur, so a count is a target to match, not a
  property of the engine.
- `derived`: computed from the counts.
- `inferred`: a reading that the frames do not state, so a starting point
  to tune.
- `observed`: what a probe project showed in a Construct preview.

Count in frames, not seconds. Every key moment of the reels falls on a
whole frame, with a remainder under 0.1 ms, so their times were set on a
frame grid rather than drawn as a continuous curve. A frame is 16.7 ms at
60 fps and 33.3 ms at 30 fps, so a count in seconds drifts between the two.

## The four parts of one effect

- One effect runs as four parts: a rise, a peak, a fall and a tail. In
  the reels a hit effect runs 30 to 32 frames. Its rise is 6 to 8 frames,
  its peak 2 to 3, its fall to half the gain 5 to 6, and its tail to a
  twentieth of the gain 4 to 6. [frames]
- Count the decay as the fall and the tail together: 9 to 12 frames,
  longer than the rise's 6 to 8. An effect whose rise and decay have one
  length reads as a sprite that blinks, not as a hit that lands. [derived]
- Those four parts cover 18 to 20 frames, about 60 % of the effect. The
  rest is an ember under a twentieth of the gain, which a player reads as
  the hit fading rather than as part of it. [frames, derived]
- Place the peak where the damage lands, not at the end of the effect.
  Everything after the peak is the consequence of the hit. [inferred]
- So the rise runs before the damage, and the effect's first frame comes
  6 to 8 frames before it. A sweep layer, such as a trail that draws the
  swing, carries that rise. The burst layers, such as the flash, the
  impact shape and the sparks, start on the damage and reach full opacity
  in 1 to 3 frames ([attack-feel.md](attack-feel.md)). Without a sweep
  layer, the effect rises in those 1 to 3 frames. Its rise-to-fall ratio
  then falls under 1.0, and the effect blinks. [derived, inferred]
- A pixel-art impact built without a sweep layer has a rise-to-fall ratio
  of 0 to 0.17 ([pixel-art-vfx.md](pixel-art-vfx.md)). [observed in a
  probe project, r506.3 preview, 2026-10-30: six impacts]
- After the peak on the damage, the effect runs another 22 to 26 frames,
  0.37 to 0.43 s. [derived]
- One effect repeats on a cycle of 106 frames, 1.77 s, with a spread of
  one frame over five repeats. When the same effect plays again, reuse its
  numbers instead of retuning each repeat. [frames]

## The ratio of the rise to the fall

The rise is the frames from the effect's first frame to its brightest
frame. The fall is the frames from that peak until the brightness reaches
half of what the effect added. Their ratio separates two kinds of effect,
and the reels hold no effect between them:

| The effect | Rise : fall | In the reels |
|------------|-------------|--------------|
| An impact: a slash, a blow, a spark burst | 1.0 to 2.0 | 1.00, 1.17, 1.33, 1.40, 1.60 |
| A charge or an ambient field: a beam, a tornado, an aura | 4.4 to 5.4 | 4.43, 5.40 |

- For an impact, bring the brightness to its peak in 6 to 8 frames and
  take 5 to 6 frames to fall to half. In a hit, the sweep layer carries
  that rise before the damage. [frames]
- For a charge, take 27 to 31 frames to rise and 5 to 7 to fall. A charge
  that falls as slowly as it rises reads as a lamp, not as a release.
  [frames]
- An ambient field such as an aura has no single peak: its rise runs past
  70 frames and the effect holds instead of ending. Treat it as a state
  with its own on and off, not as a one-shot effect. [frames]

## The area's first frame

- An effect reaches most of its area in its first two frames. In the
  reels the covered area grows 5.7 times over 8 frames, and the first of
  those frames takes 43 % of the whole growth. [frames, derived]
- So create the layer near its full size and let it fade, instead of
  growing it from nothing. A layer that grows over its whole life spends
  the frames after the hit still getting bigger, when the player has
  already read the hit. [inferred]
- Keep the layer's width and let its height fall first. In the reels the
  long axis of the covered shape stays within 22° of the same direction
  for the whole effect, while the short axis closes by 44 % in one frame
  near the end. A shape that shrinks evenly in both directions reads as a
  ball, not as a slash. [frames, derived]

## Two layers that end apart

- Give the effect at least two layers whose lives end apart: a solid shape
  that carries the hit, and debris that outlives it. [frames, inferred]
- The reels show the handover in one frame: the short axis of the covered
  shape closes 44 % while the long axis moves 9 %, and the count of bright
  specks rises to its highest at the same moment. One layer cannot change
  one dimension and hold the other, so the solid shape ended and the
  debris took over. [frames, derived]
- Read that handover as the effect's own test. Measure the covered shape
  each frame; when one axis falls by more than a third while the other
  holds within a tenth, the layers are ending apart as intended.
  [inferred]

## The radius that closes before it opens

- Close the effect before it opens. Measured as the brightness-weighted
  radius about the effect's centre, the reels run 117.3 → 109.7 → 118.2
  over one effect: 7.6 units in, then 8.5 out. [frames]
- Keep the closing distance fixed across repeats. Five repeats of one
  effect closed by 7.6, 7.7, 7.5, 7.3 and 7.3 units, a spread of 0.4.
  A closing distance that changes per repeat reads as noise. [frames]
- In Construct, move the layer's origin or its image offset inward over
  the rise and outward over the fall, or scale it about its centre with a
  Tween whose value dips below 1 before the peak. [inferred]

## The colour set

- Choose the effect's colour from a set of two or three hues for the
  whole game, not per effect. The reels' dominant hues fall in three
  groups, 68° to 82°, 188° to 248° and 308°, with nothing between them.
  A free choice per effect would spread the hues evenly. [frames, derived]
- Hold one hue through an effect. In the reels the dominant hue of a
  repeated effect does not move across five repeats. [frames]
- Give the brightest part of the effect its own colour. The reels keep a
  near-white core inside a saturated edge, so the shape reads at a glance
  against any background. [frames, inferred]

## Building it in Construct

- Store each part as a count of frames, then convert once:
  `RiseFrames / 60`, `FallFrames / 60`. Keep the counts in one place, such
  as globals or a JSON file, so a change of frame rate changes one
  conversion and not every Tween. [inferred]
- Run the four parts on Tween (one property) on *Size* and *Opacity*, with
  *Destroy on complete* on the longer of the two. Set the rise on the
  *Size* tween to 2 frames or less, as the area rule above says.
  ([pitfalls: Tween](../behaviors/tween.md)) [inferred]
- Create the sweep layer `RiseFrames / 60` before the damage, at opacity
  0. Tween its *Opacity* to 100 over the rise. On the damage, start its
  fall with a second *Opacity* tween, which stops the rising one, so the
  peak lands on the tick of the damage. Create the burst layers in the
  same tick. For a melee hit, [attack-feel.md](attack-feel.md), "Hit
  effects and damage numbers", gives the events. [inferred]
- Give the debris its own object and its own Tween, with a life 10 to 11
  frames longer than the solid shape. Do not run both from one Tween: the
  handover needs the two lives to end apart. [inferred]
- Set the effect's *Blend mode* to *Additive* on the solid shape and leave
  the debris normal, so the shape adds to the background and the specks
  keep their own colour. In a pixel-art game, keep the shape normal and
  put the glow on its own additive sprite
  ([pixel-art-vfx.md](pixel-art-vfx.md)). [inferred]
- For a charge, drive the brightness with a Tween (value) channel that
  reaches 1 at 27 to 31 frames and falls in 5 to 7, and read the channel
  into the layer's opacity every tick. So a second charge starts while the
  last one still falls ([feel.md](feel.md), "several effects on one body").
  [inferred]

## Measuring a recorded effect

- To check an effect of this project, record it at 60 fps with nothing
  else moving, then measure each frame: the mean brightness, the frame to
  frame difference, and the area that differs from a background plate.
  The four counts and the ratio above then follow from the frames.
  [inferred]
- Record at least as fast as the shortest part. The counts are frames of
  the recording, so a recording at half the game's rate halves every part
  and rounds each half on its own: one impact, rendered at 60 fps and then
  at 30, reads 7 / 2 / 5 and then 4 / 1 / 2, and its ratio drifts from
  1.40 to 2.00. A charge's longer parts survive the halving, 28 / 6
  reading 14 / 3. A recorder that writes 30 fps can check a charge but not
  an impact's ratio. [derived]
- Leave out a title card. A reel that opens on a white card shows a
  brightness jump at the cut, and a measure that reads the whole clip
  takes that cut for the effect's peak. Start the measure after the cut.
  [frames]
- Measure the covered area against a background plate, not against the
  previous frame. A layer that holds still still counts as covered, and a
  measure of change alone misses it. [inferred]
- Record the effect alone, or crop to it. A measure of a whole game screen
  carries the scene's own brightness: in the reels, an effect that covers
  about a tenth of the screen moves the whole screen's brightness by 1 %,
  and the half-gain point then lands wherever the scene happens to sit.
  The counts above come from effects on a plain background. [frames]
- Read a ratio outside both rows as a shape, not a number. Under 1.0 the
  effect rises and falls in about one length, so it blinks; lengthen the
  fall, or give it a tail. Over 5.4 it holds after its peak, so it reads as
  a state; cut the peak short, or build it as an ambient field with its own
  on and off. [inferred]
