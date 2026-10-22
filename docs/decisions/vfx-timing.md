# Effect Timing Counts Read from Recorded Frames

Date: 2026-10-22
Schema: Construct 3 r495.2

## Problem

An agent that writes a hit effect must choose how many frames its rise
takes, how long it holds, and how long it falls. The guides gave it one
length for the whole effect, "2 to 8 one-shot layers that end within 0.2
to 0.5 s" (`attack-feel.md`, "Hit effects and damage numbers"), and
nothing about the division inside that length. Left to divide it by feel,
an agent usually gives the rise and the fall one length, and the effect
reads as a sprite that blinks rather than as a hit that lands.

Published effect reels show a clear division, and the reels are neither a
game's data files nor a probe of this repository. The guides' source kinds
(`data`, `documented`, `derived`, `inferred`) had no room for a number
read from rendered frames, so the division had nowhere to go.

## Evidence

Seven published effect reels were decoded frame by frame: 4,468 frames at
60 fps, so 16.7 ms a frame, from 2.4 s to 27.9 s each, at 1280×720 after
the platform's transcode. Each frame was measured for mean brightness
(Rec. 709), frame to frame difference, brightness-weighted radius about
the centre, the count of bright specks, and the dominant hue of its
saturated pixels. A second pass differenced each frame against a
per-pixel median plate and measured the largest connected region: its
area, bounding box, principal axes and axis angle.

One reel repeats a single effect five times on a still background, which
gives the only clean sample of a repeat:

| Peak to peak | 1766.7 | 1733.3 | 1766.7 | 1766.7 | ms |
|--------------|--------|--------|--------|--------|----|
| In frames | 106 | 104 | 106 | 106 | |

Four of the seven reels open on a white title card. A measure over the
whole clip took the cut from the card to the effect for the effect's peak
and reported a brightness change of +595 % and +1017 %, which no effect in
the sample shows. The counts below start after the cut. This is the one
place where the frames alone mislead, and the reason the page tells the
reader to drop the card.

The division, from the one repeated effect and confirmed across the other
six:

| Part | Frames | Share |
|------|--------|-------|
| Rise, to the brightest frame | 6 to 8 | 23 % |
| Peak, within 8 % of the gain | 2 to 3 | 7 % |
| Fall, from the peak to half the gain | 5 to 6 | 17 % |
| Tail, from half to a twentieth | 4 to 6 | 13 % |
| Ember, under a twentieth | 10 to 12 | 40 % |

The share is the part's median count over the median 30-frame effect,
rounded to whole percents, so the column sums to 100. The first four parts
cover 60 % of the effect; the ember is the longest single part and carries
almost no brightness. A first pass took the whole decay for the fall and
reported 18 to 20 frames for it, which is in fact the four parts together.

Two further counts separate the kinds of effect, and the sample holds
nothing between them:

| Rise : fall | Effects |
|-------------|---------|
| 1.00, 1.17, 1.33, 1.40, 1.60 | an impact: a slash, a blow, a spark burst |
| 4.43, 5.40 | a charge or an ambient field |

The covered area of one effect grew 5.7 times over 8 frames, and its
first frame took 43 % of that growth. Near the end of the same effect the
short axis of the covered shape closed 44 % in one frame while the long
axis moved 9 %, and the count of bright specks reached its highest at
that moment.

The limits of the evidence:

- The reels are someone else's work at a resolution and bitrate the
  platform chose, so edges are softened and a count of specks is not a
  count of particles.
- The measurement sees the composited result. It cannot read the engine's
  curves, so a count is what the viewer saw, not what the author set.
- Seven reels, one repeated effect. A count that appears once is a target,
  not a range.
- An effect over a busy scene cannot be measured this way. One reel shows
  an effect over a whole game screen; the scene's own brightness moved the
  measure by 1 %, and the half-gain point of one effect landed at ratios
  from 3.8 to 7.0 depending on where the scene sat. Those numbers are not
  in the tables, and the page tells the reader to record the effect alone.

## Options

1. **Keep the single length.** An agent divides 0.2 to 0.5 s by feel, and
   most of its effects keep the blink shape the guides already produce.
2. **Give a division from intuition.** The guides would carry a shape with
   no source, which is what `borrowed-numbers.md` refuses for other
   numbers.
3. **Measure published frames, and add a rule only where the measurement
   supports it.** Chosen.

## Decision

- A new page, `guides/recipes/vfx-timing.md`, holds the division and the
  counts. It defines a fifth source kind, `frames`: a number read from the
  decoded frames of a published video, which is weaker than `data` and
  unlike `measured`, a probe of this repository played in a preview.
- `attack-feel.md` keeps its length and gains one line that sends the
  reader to the new page for the division inside it, so the two pages do
  not state the same numbers twice.
- The four parts and their shares go in as the default. The rise is the
  part that changes the look most, so its count is the one to tune.
- The rise to fall ratio goes in as two rows, an impact and a charge, with
  no row between them, because the sample has none. An effect that falls
  between the rows is not an error; it is a shape the sample does not
  cover.
- The area rule, the two-layer handover, the closing radius and the hue
  set go in as rules about shape, not as numbers for a checker. The
  source is not this project's, so no checker warns on it.
- No number from the reels enters the generator template. The template's
  effects stay as they are until a game built from it is recorded and
  measured the same way.
- The measure that produced the counts is a script of the skill,
  `measure_timing.py`, run by the plugin's `/measure-timing` row. It reads
  a recording of this project's effect the same way, so a game's own
  numbers can be put beside the reels'. It keeps to the standard library
  and needs ffmpeg, as `check_sounds.py` does.

## Re-evaluate when

- A game built from the template is recorded and measured, and its rise
  and fall differ from the four parts here: the template's numbers then
  take precedence, because they are this project's.
- A reel repeats an effect more than five times, or a second reel repeats
  one: the ratio's two rows gain a boundary, or move.
- A 30 fps project is measured: a count in frames holds across frame
  rates, but the encoder's blur at 30 fps may move the peak by a frame.
- A reel shows an effect whose rise to fall ratio falls between 2.0 and
  4.4: the gap in the two rows is then a real shape and not a limit of
  the sample.
