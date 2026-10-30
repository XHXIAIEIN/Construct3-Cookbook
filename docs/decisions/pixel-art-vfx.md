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
- The Construct builds are `inferred`, because no probe project runs them.
- The source is not copied into this repository. The page cites each
  effect's page, from which the file can be downloaded.

## Re-evaluate when

- A probe project builds one of the effects in Construct, with frames and
  a separate additive glow, and records it with `measure_timing.py`. Its
  observations then replace the `inferred` lines they test.
- Sprite Fusion changes the effects' numbers, or a second pixel-art source
  disagrees with them.
