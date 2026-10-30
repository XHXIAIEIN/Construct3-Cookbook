# Pixel-Art Effects Read from an Open Source Effect Library

Date: 2026-10-30

## Problem

The effect recipes, `vfx-timing.md` and `attack-feel.md`, build a hit
from Sprites that fade by tweening *Opacity* and add to the background
with the *Additive* blend mode. In a pixel-art game, both break the
palette: a half-opaque or additive pixel takes a colour that no ramp
holds, and the effect looks pasted on. No other guide says how a
pixel-art effect fades instead.

## Evidence

Sprite Fusion publishes its pixel-art effects as MIT TypeScript, one
file each, built for an agent to port. The six Combat files were read on
2026-10-30. Compared with the effect recipes:

| Topic | `vfx-timing.md` and `attack-feel.md` | The code |
|-------|-------------------|------------|
| Fade of a shape | Tween *Opacity* over 90 % of the life | Opaque pixels only; colour steps down a 6 to 9 colour ramp, a 4×4 Bayer dither removes pixels, the burst ends on a frame |
| Additive blend | On the solid shape | Only on a separate light buffer of soft glows |
| The burst | One sprite, full in 1 to 3 frames, then fading | Two hand-shaped frames, then new layers (shards, ring) |
| Depth | Not covered | A back pass and a front pass around the character; a floor ring split into halves |
| Sparks | Fly outwards for 0.3 to 0.45 s | Streaks whose length follows speed, with gravity, drag and a bounce |
| Area on the first frame | Most of it in two frames (from recorded reels) | The same: the slash covers 97 % of its arc in 2 frames |
| Shake per effect | Not covered | Strengths on a scale the game sets: 0.03 impact, 0.12 slash, 0.25 hurt and dash stop, 0.6 explosion |

The timing of the recorded reels and of the code agree where both
speak, so the new page adds to `vfx-timing.md` and does not replace it.

A probe project builds the impact in Construct as
`guides/recipes/pixel-art-vfx.md` describes: baked frames for the burst,
two soft glows with the *Additive* blend mode, and Bullet sparks. It ran
in an r506.3 preview on 2026-10-30. The recording ran at a time scale of
0.1 and was resampled to 60 fps of game time. Six impacts showed:

| Measure | Result |
|---------|--------|
| The 208 × 208 px around the burst, glow hidden | No colour outside the ramp, the backdrop and the target |
| The same, glow shown | 7,500 to 8,800 of 43,264 px outside them |
| Burst frames | Frame k first shown 0 to 0.3 frames after (k - 1) / 60 s; gone after frame 11 |
| Glow, *Out Exponential* tween over 0.3466 s | Within 0.9 opacity points of `90 × exp(-t / 0.05)` and `70 × exp(-t / 0.05)` |
| Sparks against the code's update | Speed within 1.2 px/s, position within 1.4 px, over the first 85 ms |
| `measure_timing.py` | Rise 0 to 1, peak 2 to 4, fall 6 to 8, tail 5 to 8 frames; ratio 0 to 0.17 |

The ratio falls under the impact row's 1.0 to 2.0, as `vfx-timing.md`
predicts for an effect without a sweep layer. The probe also showed two
traps. A spark's first frame showed the plain white image until the
event that creates it also set its look. A rotated streak left the 2 px
art grid.

## Options

1. **Keep the opacity recipes for every look.** A pixel-art game keeps
   effects that leave its palette.
2. **Rewrite `vfx-timing.md` for pixel art.** Its counts hold for any
   look, and the reels it comes from are not pixel art, so one page would
   mix two sources and two looks.
3. **A new recipe page for pixel art, linked from the two pages where
   their advice turns over.** Chosen.

## Decision

- `guides/recipes/pixel-art-vfx.md` holds the rules and the numbers of
  the six effects. It names a source kind, `code`: a number read from
  published source code. It states exactly what the effect draws, but not
  how a player reads it, so it ranks beside `frames` and below `data`.
- `vfx-timing.md` and `attack-feel.md` each gain one sentence at the rule
  that a pixel-art game reverses: the additive shape and the opacity fade.
- The page names a source kind `observed`, the probe project above. It
  marks the Construct builds that the probe ran. `inferred` marks the
  builds it did not reach: the layers behind and in front of the
  character, the particles spawned where others end, the canvases that a
  script fills with a file's pixels, and keeping a rotated streak on the
  grid.
- The source is not copied into this repository. The page cites each
  effect's page, from which the file can be downloaded.

## Re-evaluate when

- A probe project builds one of these: a back pass such as a floor ring
  or a stain, a chain of particles, or canvases filled by a script. Its
  observations then replace the `inferred` lines they test.
- A probe draws at 1 layout px per art px with the *Low* fullscreen
  quality. Its result decides whether a rotated streak stays on the art
  grid.
- Sprite Fusion changes the effects' numbers, or a second pixel-art source
  disagrees with them.
