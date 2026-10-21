# Scripted sequences

This page shows how an attack pattern, a cutscene or a line of dialogue
runs from a data file. A designer then edits the file, and the events stay
the same. Read it before you write a boss fight with scripted attacks, a
cutscene of several cues, or dialogue with pauses, colours and a voice.
Design first with [design/thinking.md](../design/thinking.md). This page
expands its row "a sequence scripted in data" and its smell "a cue list or
dialogue markup read with `mid`". The mechanisms come from the official
examples that each section names, and from a studied project read on
2026-10-06. A mechanism from that project is marked `studied`.

## A cue list

A sequence is a project file with one row per cue: the delay since the cue
before it, the cue's name, then its parameters. Write the delay as seconds
since the previous row, so that you can move or insert a row and the other
rows keep their numbers. The block shows only the form of a row.

```
0,ShowBanner,title
0.5,SpawnWave,left,3
0,SpawnWave,right,3
2,PlayLine,intro_2
```

- **Load once.** When the sequence starts, run AJAX *Request project
  file*, *Wait for previous actions*, then CSV *Parse CSV* from
  `AJAX.LastData` into an Array, all in that one block
  ([design/thinking.md](../design/thinking.md), "Level data, loot
  tables"). The Array then holds one row per cue on its Y axis, and
  `Array.At(0, row)` is the delay. When the file loads, store the row
  index of each row that only names a label in a Dictionary, so a jump
  finds the label without a search. [manual: plugin-reference/csv.md
  "Parse CSV"; studied; observed in a minimal project, 2026-10-06: four
  rows parsed to a width of 2 and a height of 4]
- **Step with an accumulated clock.** While the sequence runs, one number,
  `clock`, gains `dt` each tick. A *While* with the conditions `running`,
  `row < Array.Height` and `clock ≥ float(Array.At(0, row))` runs every
  cue that is due. Each pass subtracts the row's delay from the clock,
  dispatches the cue and adds 1 to the row. Several cues with delay 0 fire
  in one tick, in file order. A cue is never more than a tick late,
  because the clock keeps the time that the tick overshot. A Timer per cue
  loses that remainder each time it restarts. [studied; observed in a
  minimal project, 2026-10-06: two rows with delay 0 fired in the first
  tick in file order, and a row with delay 0.5 fired 0.506 s after them]
- **Cap the steps.** Count the steps in one tick. If the count passes a
  bound, such as 1000, stop the sequence with a message. A jump back to a
  label with no delay on the way never advances the clock, so without the
  cap it hangs the tick and shows no error. [studied]
- **Keep the file a cue list.** If the file holds variables, arithmetic,
  random choices or jumps, the sheet becomes an interpreter, and each
  opcode that you add is an event that no tool checks. If a pattern needs
  a loop or a random choice, write it as a function with parameters. Then
  call that function from one row that gives its numbers. The file then
  holds only what a designer changes: when, which cue, with which numbers.
  [studied]
- **Music in step.** If the attack pattern must stay on the music through
  a pause, let one clock lead. Each tick, if `abs(Audio.PlaybackTime(tag) -
  clock)` passes a frame, *Seek to* the clock. Then a pause of the
  sequence also holds the music's place. [studied; the audio clock's own
  rules are in [pitfalls: Audio](../pitfalls/audio.md)]

## Dispatching a cue by its name

The cue's name is a string from the file, and a function map calls a
function by a string.

1. At the start, run *Map function to string* once per cue name. Then *Map
   default function* to a function that reports an unknown cue with its
   row.
2. The step calls an intermediate function, `Cue(name, a, b, c, d)`, with
   the row's fields as typed parameters.
3. Inside it, *Call mapped function* with `name` forwards the parameters
   from index 1. Each cue function then declares only the parameters that
   it uses, in the order that the file gives them.

If the cue is a query, `Functions.CallMapped(map, name, ...)` returns a
value. If a project has cue names in the hundreds, it can dispatch from a
script block instead, with `runtime.callFunction(name, ...params)`. The
deprecated Function plugin's *Call function* by name has the same form.
To migrate it, replace it with a map ([pitfalls:
Functions](../pitfalls/functions.md)). [manual:
project-primitives/events/functions.md "Function maps"; example:
function-maps, events 7 to 10; data/c3-ts-defs/preview/interfaces/IRuntime.d.ts
`callFunction`]

## A cue that waits for a motion

A cue such as "resize the arena, then go on" starts a tween and must hold
the sequence until the tween ends.

1. In the cue function, start the tween and store the name of the cue to
   resume with. Then set `running` to 0.
2. Make the tween's *On finished* a top-level event of its own ([pitfalls:
   Triggers and Else](../pitfalls/triggers-and-else.md)). It reads the
   stored name, clears it, and calls that cue through the map, which sets
   `running` back to 1.
3. If a motion has several tweens, such as one per edge of a box, keep a
   progress latch per tween and set it to 1 in that tween's *On finished*.
   Resume when every latch is 1. Because the resume clears the stored
   name, it runs once, whichever tween ends last ([feel.md](feel.md), "An
   arena box").

[studied]

## Dialogue

The baseline is the Text or Sprite Font object's own *Typewriter text*. It
shows the line over a duration. *Is running typewriter text* is true while
the line still types, *On typewriter text finished* fires when it ends,
and *Finish typewriter* is the skip. If the line needs no pause and no
voice, use it. [plugins/text.json and plugins/spritefont2.json
`typewriter-text`]

- **Pauses, a voice, a speed that changes.** Use one Text or Sprite Font
  object and a count of shown characters. A regular Timer runs at the
  interval per character. In *On timer*, add 1 to the count,
  *Set text* to `left(line,
  count)`, and play the voice ([sound.md](sound.md), "A dialogue voice").
  If a pause mark is at the count, restart the Timer with the pause's
  length: *Start timer* on the same tag does this. To skip, set the count
  to `len(line)` and stop the Timer. [manual: behavior-reference/timer.md
  "Start timer"; studied]
- **Parse the markup once per line.** When a line such as `<color red>Hi<pause
  3> there` starts, split it into the plain text and a second Array as
  long as the text. At each index, that Array holds the tag that applies
  there. The typing event then reads one index per character. If the tag
  Array holds a tag at the count, one *Compare* per tag kind applies it,
  and `tokenat(tag, i, " ")` gives the tag's parts. Reading the raw line
  with `mid` one character at a time, every tick, inside a *While*, is the
  smell row of the design guide. Write a colour in a tag as three numbers,
  such as `<color 255 0 0>`, and read them into `rgbEx255`. Or write it as
  a name that a Dictionary maps to a hex string for `HexColor`. Then no
  event decodes hex by hand. [studied]
- **Glyphs that move.** Only if a glyph shakes or waves on its own, make
  each glyph an instance: one Sprite Font instance per character, with its
  own Sine or Tween. Make it a child of the line's object with *Add
  child*, so it follows the line and is destroyed with it. Its X is the
  sum of `CharacterWidth` of the characters before it. The hierarchy is
  the link to the line, so the glyph stores no UID of the line
  ([design/thinking.md](../design/thinking.md), rule 1). [studied]
- **Arguments in a line.** Build the line with
  `StringSub("{0} takes {1} damage", name, n)`
  ([design/style.md](../design/style.md), "UI text"), so a translator
  can reorder the arguments by moving `{0}` and `{1}`. [manual:
  system-reference/system-expressions.md "StringSub"]

## Localisation

The Internationalization plugin holds the strings: one JSON file per
language with a `locale` key and a `strings` object. Load each file with
the plugin's *Load from JSON*, with the string from `AJAX.LastData`. Then
*Set locale* and read `Lookup(path)`, where a dot steps into a nested
object. The plugin also formats numbers and plurals for the locale.

The examples use a simpler form: an Array project file with one column per
language and one row per string. When the language changes, the events
read it as `Strings.At(language, index)`. A hand-written JSON with one
root per language also works. Read it through a lookup function that
returns the key when *Has key* fails. Then a missing translation shows its
key on screen, where a tester sees it. If a key in that JSON holds a dot,
escape the dot in the path ([pitfalls:
Expressions](../pitfalls/expressions.md)); keys without dots need none.
For a font per language, use a Sprite Font per language, with its widths
in *Spacing data* ([pitfalls: Rendering](../pitfalls/rendering.md)).
[manual: plugin-reference/internationalization.md "The translation file",
"Looking up localized strings"; examples: internationalization,
languages-from-json events 2 to 5; studied]
