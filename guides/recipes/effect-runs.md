# A run of effects

One effect has four parts and a ratio ([vfx-timing.md](vfx-timing.md)).
A fight is a run of them: several effects, close together, in one frame.
This page is about arranging that run — how long each effect stays, where
it sits, and what an empty beat does. Read it after
[vfx-timing.md](vfx-timing.md), when the events spawn more than one effect
and the screen has to keep reading.

The rules below come from building one thirty-frame effect into a series
of runs and watching each back, not from the reels that the counts come
from. Each rule ends with the kind of its evidence:

- `derived`: computed from the counts of [vfx-timing.md](vfx-timing.md).
- `inferred`: a reading of how a run plays, so a starting point to tune.
- `observed`: seen in one built project, so a fact about the engine rather
  than about the run.

## Give the effects different lengths

- Write the length of every effect of the run down before the events, as
  beats or frames. A run whose effects each last one beat is a metronome:
  the eye learns the spacing in three hits and stops watching. A run of
  eight effects is better with lengths such as 2 · 1 · 3 · 1 · 1 · 2 · 1 ·
  1 than with eight equal ones. [inferred]
- Let the effect that carries the most information stay longest. A shape
  the player has not seen needs about a second to read; a repeat of one
  they have seen needs a quarter of that. [inferred]
- An effect that outlives its four parts holds, it does not stretch. Play
  the rise and the peak, keep the shape at its peak value, then take it
  away over the last 10 to 15 frames. Spreading the four parts over a
  longer time turns an impact into a fade. [derived]
- Decide at each join whether it is a cut or a seam. An effect whose tail
  ends on the frame the next effect starts gives a seam; one that ends
  three or four frames early gives a cut. Both read, but a run that mixes
  them at random reads as a timing mistake. [inferred]

## Leave a beat empty

- Put an empty beat after every three or four hits. Without one the run is
  a wall of light and the eye takes the whole thing as one event, however
  well each effect is built. [inferred]
- An empty beat is not an empty screen. Keep one small thing moving — a
  background layer, a light, the player's idle — so the game still reads
  as running while nothing is hit. [inferred]
- The empty beat is where the last effect's tail is still on screen. Leave
  the tail alone: cutting it to make the frame clean removes the thing the
  gap was for. [derived]

## Compose the frame, not the centre

- One focal shape per frame. A burst arranged symmetrically about the
  centre reads as decoration, because nothing in the frame says where to
  look. Move the effect off centre and the eye finds it at once.
  [inferred]
- Either let the shape run past an edge or keep a full margin inside it. A
  shape that stops a little inside an edge reads as a mistake, and one
  that stops a little past it reads as a crop. [inferred]
- Shapes of one kind read as a pattern when they are equal and as a
  composition when they are not. Vary one dimension — length, width,
  spacing — and leave the others equal. [inferred]
- Keep the area the player must watch clear. The effect is the loudest
  thing on screen, so an effect that covers the place the player is
  looking turns a hit into a blind frame. [inferred]

## Timing and motion are two choices

- The four counts say when the effect is bright, not what moves. Choose
  the motion separately: a sweep across the frame, a stretch on one axis,
  a rotation, a collapse. A run in which every effect grows from its own
  centre looks like one effect played eight times. [inferred]
- Drive a travel from the effect's elapsed time, not from its brightness.
  A sweep or a slide that is scaled by the brightness stops when the
  effect dims, which reads as a stutter; one scaled by the elapsed frames
  keeps going while the effect fades. [derived]
- Drive a deformation from the brightness: a squash, a stretch or a
  skew that peaks with the effect and returns to rest as it dims is what
  makes the hit land on the body it hit. [inferred]
- Give the debris its own position, not only its own life. Two layers at
  the same point hide each other, so the handover that
  [vfx-timing.md](vfx-timing.md) asks for cannot be seen. [derived]

## Building it in Construct

- Keep the lengths of a run in one place, as a list of frames or beats
  that the events read, in the same spirit as the counts of one effect:
  a change of tempo then changes one list. [inferred]
- Advance the run's own schedule at the top of the block, before the
  actions that wait. A *Wait* delays the rest of its block, so a threshold
  added after one is added late by the length of the effect
  ([pitfalls: System](../plugins/system.md)). [observed]
- For a run that holds a shape between hits, run one Tween to the peak and
  leave it there, then a second Tween for the removal. A single Tween that
  reaches its end value and stops keeps the shape at that value, which is
  the hold. [inferred]
