# Sound

This file says which sounds play, when, how loud, and how to make and
check placeholder files. Read it before you add sounds or music. Also read
it when a user says that the game is too loud or too busy, or that every
sound is the same. It adds to the Audio plugin's runtime facts in
[pitfalls: Audio](../pitfalls/audio.md). The rules come from a game
project with automatic combat, drag-and-drop merging and three music
stems. An r504 preview and an offline mix verified them, 2026-09-30 to
2026-10-02. Treat the numbers as starting points to tune.

## One entry for every sound

If the game has more than a few sounds, the events that make things
happen name the moment, not the file: `cue("merge", X, tier, 0)`. One
sheet decides what each moment plays, when, how often and where in the
stereo field. Then a change of sounds, or of a rule, changes that sheet
only. In the source project, the replacement of every sound and rule
changed the sound sheet throughout and about 130 lines of the four
gameplay sheets.

- If every moment plays its own file at once, the entry needs no map.
  Name the files after the moments and play them with Audio
  *Play (by name)*, as the official examples do.
- Moments can follow different rules: at once, on the grid, at most once
  in a gap, or one reward per cell. If they do, the entry is a function
  `cue(name, x, a, b)`. It runs *Call mapped function* on map `"cue"`
  with the string `name`, forwarding from index 0. Each rule is one
  function with the same four parameters. Because the function reads
  `name`, it serves every moment that is mapped to it: one function for
  the immediate sounds, one for the gated ones, one per rewarded moment.
  In *On start of layout*, group the *Map function to string* actions by
  the function that they map to. Each group then lists the moments that
  share a rule.
- Map the default to a function that plays nothing. Then gameplay can
  call a moment before its sound exists, and the sound can arrive later
  with no change to gameplay. The default function takes the whole
  parameter list ([pitfalls: Functions](../pitfalls/functions.md)), the
  same four parameters.
- Write the meaning of `a` and `b` for each moment in one table of the
  project's sound document. Each moment uses them differently: as a
  level, a weapon kind, a count or a switch.

[example: function-maps; observed in a game project, r504, 2026-10-04 to
2026-10-07: 37 moments, 20 rule functions and a silent default; the sound
system replaced on 2026-10-05]

## Three roles

Every sound is a reward, an impact or a music stem. A reward is a pitched
sound: a merge chord, a kill chord, a level-clear arpeggio. An impact is
unpitched: hit, land, pick up, button. A music stem is one layer of the
music. The role decides the rule:

- Play one reward at a time. A global holds the time, priority and one-off
  tag of the last scheduled reward. A later reward for the same 16th-note
  cell replaces the scheduled one if the later reward has higher priority
  and the scheduled one has not started. *Stop* on its tag cancels a
  scheduled instance. Otherwise, the later reward moves to the next cell,
  at most a beat, or it is dropped.
- Play one impact per cell. If a crit comes for a cell with a hit
  scheduled, drop the hit. While a kill holds the cell, drop both.
- A sound on the grid that is not an impact (an enemy appearing, the first
  landing of a stage) holds its cell too. Hits, crits and auto-merges skip
  that cell, because otherwise two files start on one sample and their
  peaks add. Claim the cell when its time is first known, as the stage is
  laid out. Do not wait for the frame that the sound plays, because
  impacts are queued for their cell before that frame.
- Music stems duck only for the Key tier ("Tiers and loudness"). Duck them
  through a gain effect on the music tags, not with *Set volume*, because
  the stems' fades use *Set volume*. Merge overlapping ducks into one
  release, with the deeper depth and the later release, because *Set
  effect parameter* cancels the ramp that is still running. Hits never
  duck the music, because ducking at five hits a second makes the music pulse.

## Immediate or on the grid

- Answer the player's input in the same frame: pick up, drop, a button, an
  error, the first kill of a streak. These sounds are unpitched, or they
  use only the notes that every chord of the progression allows.
- Schedule what happens by itself on the grid: automatic attacks,
  auto-merges, held-button spawns, the chord after a merge, stem fades on
  the bar. A 16th at 100 BPM is 0.15 s. This is too short for the player
  to feel a delayed attack, but long enough to hear as rhythm.
- The grid is integer steps from `Audio.CurrentTime` minus the stored
  start of the music. A scheduled time is
  `start + ceil((now + lead - start) / step) * step`, with a lead of
  0.03 s. Never use `%` on float seconds; count integer steps as this
  formula does ([pitfalls: Audio](../pitfalls/audio.md)). Before the music
  starts, a sound scheduled for a time in the past plays at once, so grid
  sounds become immediate.
- Move what a sound marks to its cell: the damage, the squash and the
  floating number land on the same cell as the hit. The attack timer only
  records the due cell. The charge-up pose stays at full until that cell,
  so the body does not stand up before it lunges.
- A hit stop at time scale 0.1 does not delay a scheduled sound, because
  the audio clock ignores the time scale. A timeline with *Use system
  timescale* on slows with the time scale
  ([pitfalls: Timeline](../pitfalls/timeline.md)).

## Tiers and loudness

Measure every file the same way: K-weighted (ITU-R BS.1770), above 150 Hz
only, the loudest 400 ms (3 s for music). The reference M is the music
with every stem on, set at −30 LUFS in the game.

| Tier | Sounds | Over M | Rule |
|------|--------|--------|------|
| Key | kill, the rare merge tiers, level clear, stage start, an error | +8 to +14 dB | never skipped, immediate, ducks the music |
| Action | merges, crit, pick up, land, equip, a switch | 0 to +9 dB | one per cell or per 8th; the automatic version of an action 3 dB under the player's |
| Repeat | hit, hover, held spawn, auto-merge | −7 to +1 dB | each repeat within its window 1 dB under the last, to a floor; an attack rate above 4 a second lowers impacts by 10·log10(rate / 4) dB |

- A Repeat sound that starts within 0.25 s after a Key sound plays 3 dB
  lower, set at *Play*. This keeps the foreground clear and leaves the
  playing instances unchanged.
- A dialogue voice is a Repeat sound: one short file per speaker, played
  once per character shown ([scripted-sequences.md](scripted-sequences.md),
  "Dialogue"). Play it on one tag per speaker: *Stop* the tag, then
  *Play*, so that a fast line plays one voice at a time. Skip it on a
  space and while the player skips the line, because a voice at every
  character of a skipped line sounds like a buzz. [a studied project,
  2026-10-06]
- The mix has no master limiter, so peaks add. File ceilings leave room:
  −3 dBFS for effects, −12 dBFS for music. The stereo panner mixes the far
  channel into the near one. This raises an attack by 1.3, 2.3 and 3.2 dB
  at ±10, ±20 and ±30. So keep the loudest sounds within ±10, and keep
  them off each other's cell.
- Do not retune pitched sounds at random. For variation, use three to five
  variants and a random gain of −1.5 to 0 dB. Play the variants from a
  shuffled list, so that no variant plays twice in a row. Retune by whole
  semitones (`rate = 2^(n/12)`), per play, on a one-off tag. An unpitched
  impact may also take a random rate ([attack-feel.md](attack-feel.md),
  "Sounds of an attack").
- Pitched sounds follow the current chord. A scheduled chord reads the
  chord of its cell and retunes to it. An immediate sound uses only the
  notes that every chord of the progression allows
  ("Immediate or on the grid"). A scale that climbs with the level is the
  cheapest success sound in games. The game gives it a different root
  each time.

## Bands

- Phone speakers reproduce nothing below 150 Hz. Put a low layer only on
  rare accents. End it on one note (A1 55 Hz in the game) with its 2nd and
  3rd harmonics, so that phones still play the drop. Keep the low layer
  out of the compressor, so that the compressor does not lift its tail.
  Give frequent sounds no low layer, because the low band belongs to the
  bass stem, which is high-passed at 70 Hz.
- Sustain nothing above 5 kHz. Band-limit baked reverb to 250 Hz to
  5 kHz, so that the tails carry no highs. A low-pass on the music between
  1 and 5 kHz, ramped by progress, is the cheapest way to make the music
  show progress. Its Q is in dB: use −3 for a flat knee.
- The melody shares a band with the merge chords. So the melody starts
  notes only on the first two beats of a bar, and it ducks 4 dB under a
  chord.

## Making placeholder files

- Use four layers per sound: an attack (a burst of filtered noise or a
  thump), a body (a harmonic timbre), a low layer for rare accents, and
  one room that all sounds share. Bake the reverb in, with a dry-to-wet
  ratio set by how often the sound plays: about 28 dB for hits, 11 to
  18 dB for rare chords and 12 dB for music. The most frequent sound is
  then the driest.
- The timbre follows the art. For a round, soft look, use bars with
  harmonic partials only (1 and about 4 for a soft mallet, 1 and 2 for a
  damped thud), sine bubbles that glide up a few semitones in 30 ms, and
  triangle pads. Leave out bell partials (2.76, 5.40 and 8.93 of the
  fundamental, the sound of metal: Fletcher and Rossing, *The Physics of
  Musical Instruments*), clicks above 1.5 kHz and attacks under 3 ms. For
  a hard look, invert these choices.
- Normalise each file to its tier's loudness, and limit the peak to the
  ceiling. Then encode the file as WebM Opus (ffmpeg `libopus`): 96 kbps
  stereo for effects and the stereo stem, 64 kbps mono for the rest. If a
  file is encoded to an exact length, Chrome decodes it with the
  encoder's pre-skip removed. At 48 kHz the decoded file has that length,
  and at 44.1 kHz it has one sample less. Music that is rescheduled on
  the grid, as the next item describes, does not depend on that length.
  [observed with a test page, Chrome 155, 2026-09-30]
- Make each music file one pass plus the reverb tail. Reschedule it on
  the grid for each pass instead of looping it, so that a stem can join
  on a bar.
  Render each note on its own and add it at an integer sample. Process
  the whole stem only linearly (high-pass, reverb), so that a rescheduled
  pass equals continuous playing. A seam test overlays two passes offset
  by one and requires the difference under −60 dB of the peak.
- The generator writes the pitched layers of each file (frequency, start,
  time to −12 dB) to a JSON next to the WAVs. The offline check reads
  this JSON.

## Memory for several songs

Once a file in the Sounds folder loads, the runtime holds it decoded, as
32-bit samples at the audio context's rate. One second of sound takes
the rate × 4 bytes × the channels. In mono at 48 kHz, the rate of the
measured Edge preview, this is 192 KB. An 18 s mono stem takes about
3.5 MB, so several songs of several stems each, all preloaded, take tens
of MB. A file in the Music folder streams instead, but it cannot be
scheduled on the grid ([pitfalls: Audio](../pitfalls/audio.md)). To hold
only the effects and the songs in use:

1. Turn the project property *Preload sounds* off.
2. *Preload* the effects and the stems of the current song at the start.
3. Start the music in an event that tests *Preloads complete*, as the
   scheduled-play entry of the Audio pitfalls describes.
4. *Preload* the next song a stage or more before it plays, so that its
   decode is complete when it starts.
5. *Unload audio* the old song only in *On fade ended* of its last fade,
   because an unload stops every instance still playing the file.

To list what is decoded at a moment in a preview, see "Reading one value"
in
[reading-the-runtime.md](https://github.com/XHXIAIEIN/Construct3-Agent-Skills/blob/main/plugin/skills/construct3-agent-plugin/references/reading-the-runtime.md).
[manual: plugin-reference/audio.md "Preloading sounds", "Categorise audio
files correctly"; Web Audio spec, AudioBuffer: 32-bit linear PCM;
pitfalls/audio.md, the unload entry; observed in Edge 155, 2026-10-02: a
64 kb/s mono stem decoded to 1 channel of 998,400 samples; observed in a
minimal project, r504 preview in Edge, 2026-10-05: a mono file of the
Sounds folder decoded to one channel at 48 kHz]

## Checking

- Offline mix. It proves that the mix follows the rules, and a
  person judges the WAVs by ear.
  1. Copy the sheet's sound functions (grid, gates, reward claim, streak,
     duck) into a script.
  2. Drive them with fixed-seed scenarios: a minute of play, a quiet board,
     a full board, a boss, the first touch.
  3. Mix the WAVs and assert these limits:
     - peak ≤ −1 dBFS;
     - any 3 s short-term loudness ≤ −18 LUFS;
     - each class's grid delay ≤ step + lead;
     - every pitched play a whole number of semitones and inside every
       chord it overlaps;
     - one reward per cell;
     - a kill's 400 ms at least 6 dB over the 400 ms before it;
     - impacts no more than one per cell.
- Preview. The browser runs with `--mute-audio`. To hear or measure a
  sound, record it inside the page; see
  [editor-and-preview.md](https://github.com/XHXIAIEIN/Construct3-Agent-Skills/blob/main/plugin/skills/construct3-agent-plugin/references/editor-and-preview.md).
  A debug global that logs the beat at each pass shows that the grid keeps
  time: at pass n the beat read `32n − 1.67` within a frame over 62 s.
- On the device. Each item is a row in the project's own risk table, with
  a pass mark and what to change when it fails:
  - *Use worker* set to *No*, for sample-accurate scheduling
  - `Audio.OutputLatency`, read and recorded
  - resume after five seconds in the background
  - the first touch before the audio clock runs
  - the loudness on the speaker and in headphones

[manual: plugin-reference/audio.md "Schedule next play", "Autoplay
restrictions", "Tags"; pitfalls/audio.md; observed in a game project, r504
preview and an offline mix of 73 assertions, 2026-09-30 to 2026-10-01]
