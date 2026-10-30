# Pixel-art effects

If the game is pixel art, read this page beside
[vfx-timing.md](vfx-timing.md) before you build a combat effect. It says
how an effect keeps the palette and the grid while it fades, which layers
it draws on, and the numbers of six combat effects. For the attack that
the effect belongs to, read [attack-feel.md](attack-feel.md).

The numbers come from the TypeScript source of the six Combat effects of
Sprite Fusion's open source effect library, under the MIT licence. Each
effect has its page at `https://www.spritefusion.com/pixel-art-vfx/<slug>`,
with the slugs `explosion`, `impact`, `slash`, `muzzle-flash`, `blood` and
`movement` (dash and blink). Each effect draws on a grid of 2 screen px
per art px. Positions and speeds below are in screen px, and the sizes of
shapes in art px. Each rule ends with the kind of its evidence:

- `code`: read from that source code. It states what the effect draws,
  not how a player reads it.
- `derived`: computed from the code's numbers, at 60 fps.
- `inferred`: the Construct build of a rule, a starting point to tune.
- `observed`: what a probe project that builds the impact showed in a
  Construct preview. The probe draws 2 layout px per art px, with the
  project properties *Sampling* Nearest, *Pixel rounding* on and
  *Fullscreen mode* Integer scale outer. Its palette is the ramp, the
  backdrop and the target's grey.

## Fade by steps, not by opacity

- Keep every pixel of a shape opaque. The effects fade a shape in three
  ways only: they move its colour down a ramp, they remove its pixels by
  an ordered dither, or they end it on a frame. Only soft matter, such as
  smoke, dust and mist, takes partial opacity. [code]
- Give each hue a ramp of 6 to 9 colours, from white through the hue to
  near black. Step a layer down the ramp as it ages:
  - The slash ramp runs from `#ffffff` to `#212f6b` in 7 colours, and the
    slash moves 2.4 colours down it over its life.
  - A spark's head takes the first colour for the first 40 % of its life,
    the second for the next 30 % and the third after that.
  - A floor shockwave steps through 5 colours in 0.5 s.
  - A blood stain dries one colour darker at 0.35 s, 1.4 s and 3.2 s.

  [code]
- Remove pixels by a 4×4 Bayer matrix: a pixel draws while the layer's
  fade value is above the threshold of its cell. The slash's tail
  dissolves over the last 40 % of its length. Debris dithers out over the
  last 25 to 35 % of its life, and a casing on the ground over its last
  0.6 s. [code]
- Construct has no dither effect: its effects include Pixellate and
  Posterize but no dither [schema: c3-schemas/_index.json]. So draw the
  dither steps as frames of the animation, and step the animation instead
  of tweening *Opacity*. Frames drawn with opaque pixels then add no
  colour outside the ramp. [observed in a probe project, r506.3 preview, 2026-10-30: the
  impact's 11 frames with the ring's dither drawn in; with the glow
  hidden, frames 1, 2 and 5 held no colour outside the palette in the
  208 × 208 px around the burst]
- To step the hue without new frames, draw the frames in white and run
  *Set color* with `HexColor("#RRGGBB")` of the ramp's next colour. The
  colour is a tint, so white shows the image's own colours.
  [manual: plugin-reference/common-features/common-actions.md "Set color";
  observed in a probe project, r506.3 preview, 2026-10-30: a white spark
  tinted with `HexColor("#fff3a6")` read 255, 243, 166 in `colorRgb` and
  showed that colour on screen]

## The colour layer and the light layer

- Draw the shape and the glow apart. Each effect writes opaque palette
  pixels to a colour buffer and soft glows to a light buffer that is added
  over the frame. A glow falls off as `(1 - d)²` from its centre. The
  shape itself is never additive. [code]
- So in Construct, put the shapes on a layer with the *Normal* blend mode.
  Put each glow on its own soft round sprite with the *Additive* blend
  mode, and tween only the glow's *Opacity*. The glow lifts the pixels
  under it off the palette. [observed in a probe project, r506.3 preview, 2026-10-30:
  in frames 1, 2 and 5, 7,500 to 8,800 of the 43,264 px around the burst
  left the palette with the two glows shown, and none with them hidden]
- Keep the shapes themselves *Normal*. An additive shape adds to the
  background, so its pixels leave the palette wherever it is drawn.
  [inferred]
- End a hit's glow faster than its debris. The glow of an impact falls as
  `exp(-t / 0.05)`, so to a twentieth in 9 frames. The glow of a muzzle
  flash falls as `exp(-t / 0.03)`, in 5 frames. An explosion adds a white
  glow of 0.08 s and a warm glow of 0.7 s, whose strength falls with the
  square of its remaining life. [code, derived]
- To fade a glow as `exp(-t / τ)`, tween its *Opacity* to 0 with the ease
  *Out Exponential* over `10 × τ × ln 2` seconds, 0.35 s for the impact.
  The tween then follows the curve. [observed in a probe project, r506.3 preview, 2026-10-30:
  the two glows, tweened from 90 and from 70 over 0.3466 s, stayed
  within 0.9 opacity points of `90 × exp(-t / 0.05)` and
  `70 × exp(-t / 0.05)` in about 100 samples of each of six impacts]
- So the muzzle flash's glow, with τ of 0.03, takes 0.21 s. [derived]

## Key frames for the burst

- Draw the brightest shape of a burst as one or two separate frames, not
  as one shape tweened. An impact runs in three steps:
  1. Frame 1: an 8-point star with a white core.
  2. Frame 2: the star 1.25 times longer, 0.55 times as thick and one ramp
     colour darker.
  3. From frame 3: the four longest spikes leave as crescent shards until
     0.13 s, and a ring opens from 8 to 20 art px over 0.2 s with an
     ease-out cubic.

  [code]
- A muzzle flash is two frames only, the second at 0.6 of the first's
  length. Its lobes take a new random spread for every shot. An
  explosion's flash lasts 0.06 s, 4 frames, and shrinks by a fifth.
  [code, derived]
- This agrees with "The area's first frame" in
  [vfx-timing.md](vfx-timing.md): the burst covers its area on its first
  frame. [derived]
- The impact's rise-to-fall ratio is 0 to 0.17, below the impact row's
  1.0 to 2.0 in [vfx-timing.md](vfx-timing.md). It rises in 0 or 1
  frames, holds its peak for 2 to 4, falls to half in 6 to 8 and to a
  twentieth in 5 to 8 more. That page's "The four parts of one effect"
  predicts a ratio under 1.0 for an effect without a sweep layer.
  [observed in a probe project, r506.3 preview, 2026-10-30: `measure_timing.py` on
  six impacts, recorded at a time scale of 0.1 and resampled to 60 fps of
  game time]
- In Construct, make the burst a Sprite whose animation holds those
  frames at speed 60 with *Loop* off, and destroy it in *On finished*.
  The impact's burst has 11 frames, because the effect draws nothing from
  0.2 s on. In a preview that ticks at 143 Hz, frame k first shows at
  `(k - 1) / 60` s, and the burst is gone after its 11th frame.
  [observed in a probe project, r506.3 preview, 2026-10-30: frame k first showed 0 to
  0.3 frames after `(k - 1) / 60` s, within the recording's sampling
  step, and the burst was gone 11.0 to 11.2 frames after its creation, in
  six impacts]

## Behind and in front of the character

- Draw each effect in two passes, one behind the character and one in
  front. Behind: smoke, dust, scorch marks, stains, afterimages and the far
  half of a floor ring. In front: the flash, sparks, shards, chips, fire,
  rocks and the near half of the ring. [code]
- Draw a floor shockwave as an ellipse 0.16 times as tall as it is wide,
  split into halves, so it rings the character's feet. [code]
- In Construct, put an effects layer under the characters' layer and one
  over it. Make the floor ring two half-ellipse sprites, one on each.
  [inferred]

## Particles

- Draw a spark as a streak behind its head along its velocity. The
  streak is min(9, 1 + 0.011 × speed) art px long, so a fast spark is a
  line and a slow one a dot. [code]
- A spark falls at 0.45 of a gravity of 1900 px/s². It loses 2.2 times
  its speed per second. It bounces off the ground at 0.45 of its fall
  speed. [code]
- A spark lives 0.05 to 0.15 s at a muzzle, 0.1 to 0.3 s at an impact,
  0.12 to 0.35 s off a slash and 0.18 to 0.7 s in an explosion. [code]
- In Construct, give a spark Sprite the Bullet behavior with *Set gravity*
  855, and keep the Bullet's *Set angle* property on, so the streak
  points along its motion. Every tick, set its width to the streak length
  and its speed to `Bullet.Speed * (1 - 2.2 * dt)`. The spark then moves
  as the code moves it. [observed in a probe project, r506.3 preview, 2026-10-30: over
  the first 85 ms, while all 18 sparks of an impact were alive, each
  spark's speed stayed within 1.2 px/s and its position within 1.4 px of
  the code's update run from the same starting velocity, in six impacts;
  its *Angle* equalled `Bullet.AngleOfMotion` on every recorded frame
  after its first]
- Set a new spark's angle, width and colour in the event that creates it,
  not only in the *Every tick* event. Without them its first frame shows
  the white image at angle 0. A created instance is not picked by another
  event until its top-level event ends, as
  [how-events-work.md](../primitives/events/how-events-work.md) says, and
  the Bullet first turns it on the next tick. [observed in a probe project, r506.3 preview, 2026-10-30:
  with the *Every tick* event and the spawn in one group, a frame
  0.1 ms after an impact's creation showed its 18 sparks white, 2 px wide
  and at angle 0; with the three actions added to the spawn, no recorded
  frame did]
- A rotated sprite is drawn on the screen's pixels, not on the art grid.
  At 2 layout px per art px, a spark's streak has edges inside an art px,
  while the burst's frames stay on the grid. [observed in a probe project, r506.3 preview, 2026-10-30:
  under the *High* fullscreen quality, 16 to 128 cells of 2 × 2
  screen px, one art px each, held two colours in each screenshot, all of
  them on sparks]
- The *Low* fullscreen quality renders at the viewport's size and then
  stretches the result. *Optimize for pixel art* turns it on. [manual:
  project-primitives/projects.md "Fullscreen quality",
  interface/dialogs/new-project.md "Optimize for pixel art"]
- So to keep a rotated streak on the grid, draw the game at 1 layout px
  per art px with the *Low* fullscreen quality, and halve this page's
  positions and speeds. [inferred]
- Spawn the next particle where one ends. In an explosion:
  - 45 to 60 % of the fire bits leave smoke where they end.
  - A burning brand trails fire and lights a short blaze where it lands.
  - A rock that lands faster than 200 px/s throws dust.

  In Construct, create the next particle in *On destroyed* of the first.
  [code, inferred]
- Colour the chips of a hit from the struck surface, in three shades:
  1.25, 1 and 0.7 times its colour. [code]

## The six effects

The counts are at size 1. Each effect also passes a shake strength to the
game, on a scale that the game sets, so only the ratios between effects
carry over.

- Slash, shake 0.12:
  - The head sweeps the arc in 0.06 s with an ease-out exponential, so it
    covers 97 % of the arc in 2 frames.
  - The arc holds 0.06 s. Then the tail follows in 0.24 s, while the
    width falls to 45 %.
  - An inner echo at 0.79 of the radius starts 1 frame later and one ramp
    colour darker.
  - At the end of the sweep, 10 sparks leave within 0.5 rad of the arc's
    direction, and 16 shavings leave the arc. A star glints at the tip
    for 0.22 s.
  - The effect ends at 0.5 s.
- Impact, shake 0.03:
  - The star shows on frames 1 and 2, the shards until 0.13 s and the
    ring until 0.2 s.
  - A ricochet adds a streak at 1500 px/s for 0.16 s, and a scorch on the
    surface that cools in 0.9 s.
- Muzzle flash, no shake:
  - The flash is two frames. Then 7 sparks leave within 0.32 rad of the
    barrel, and a curl of smoke rises.
  - The casing leaves up and back. It bounces until it falls slower than
    160 px/s, glints 0.06 s at each bounce, and stays 3.6 to 4.6 s.
  - The gun kicks back 1.6 px.
- Explosion, shake 0.6:
  - A flash of 0.06 s, two rings of 0.34 s and 0.22 s, and a glow of
    0.7 s.
  - 72 sparks, embers that live up to 3.2 s, thrown earth and rocks, and
    a floor ring of 0.5 s.
  - A scorch that cools through the fire ramp to soot.
  - The blast pushes the particles near it outward.
- Blood, shake 0.25:
  - Strands grow in 0.045 s and break by 0.09 s. Mist lives 0.35 to
    0.6 s.
  - Drops land as stains that dry darker and fade after 6 s.
  - Drips fall from the wound at about 0.47, 0.9 and 1.45 s.
  - The effect asks the game for a hurt flash of 0.12 s and a knockback
    of 520 px/s.
- Dash, shake 0.25 at the stop:
  - 0.12 s passes before the move. The move takes 0.2 s with an ease-out
    of power 1.6.
  - An afterimage appears every 44 px. It is made from the character's
    own pixels, mapped to the ramp by brightness. It stays solid for 45 %
    of its 0.4 s, then dithers out.
  - At the stop, the character skids from 700 px/s at 4600 px/s², with
    dust and sparks.

[code]

- Keep the shakes in this order when you set them in [feel.md](feel.md),
  "Hit feedback". An impact shakes a quarter as much as a slash. A hurt
  and a dash's stop shake about twice a slash, and an explosion five
  times a slash. [code, derived]
- Scale an effect's size sublinearly. An explosion's size factor `S`
  scales its radius by `S`, its force and the counts that follow the force
  by `S^0.8`, and its smoke by `√S`. So a large blast has more and larger
  bits, but not in proportion. [code]

## Running the source in Construct

- Each file steps by `dt` and draws into 32-bit pixel arrays. So port it
  with `dt`, not with the per-frame step of
  [porting-web-effects.md](porting-web-effects.md), "Frame steps". [code]
- A script can hand pixels to a Drawing Canvas with
  `loadImagePixelData(imageData)`, which takes an `ImageData`
  [script API: IDrawingCanvasInstance]. One canvas for the back pass, one
  for the front pass and one with the *Additive* blend mode for the light
  can show a file's pixels after a conversion to `ImageData`. The canvases
  then upload their pixels every tick, so read
  [plugins/drawingcanvas.md](../plugins/drawingcanvas.md) for the cost.
  [inferred]
