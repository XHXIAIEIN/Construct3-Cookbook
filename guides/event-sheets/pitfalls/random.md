# Event Sheet Pitfalls: Random

Sources and the rule for adding an entry are in the index,
[pitfalls/README.md](README.md).

- Advanced Random has one number sequence, and `Random`, `Weighted`,
  `WeightedByName` and *Create permutation table* all take numbers from
  it. A weighted draw takes one number. A permutation table of length n,
  where n is 2 or more, takes n numbers for its shuffle when it is
  created, and *Shuffle permutation table* takes n numbers again. *Create
  probability table* (also from JSON), *Add probability entry* and *Remove
  probability entry* take no numbers. So two kinds of draws that share the
  sequence shift each other: one more card drawn changes every enemy after
  it. *Update seed* with a string starts the sequence again from the start
  of that seed. So the same string gives the same numbers, weighted draws
  and permutation every time. To make each kind of draw reproducible on
  its own, set the seed before each draw. Build the seed from the run's
  seed, the use of the draw and a counter, as in
  `GameSeed & ":card:" & CardsDrawn`, and save the counter with the run.
  A script that sets the same seeds and makes the same draws in the same
  order gets the same numbers as the game, so such a run can be
  reproduced offline. `advanced_random.py` of the `construct3-agent-plugin`
  skill computes these numbers as the plugin does, for a seed, a
  probability table or a permutation table. A Construct update can change
  the plugin's algorithm, and with it every number after a seed. So after
  an update, run `advanced_random.py --check` before you trust the offline
  numbers. It runs the plugin's code with node, from the project's export
  or, with `--preview`, from the editor's preview, and compares every
  value.
  [manual: plugin-reference/advanced-random.md, "Seed" and "Update seed";
  runtime code, `plugins/AdvancedRandom` in an r505 export's
  `c3runtime.js`: `_UpdateSeed` hashes the string and re-initialises the
  generator; observed in a game project, r505 editor, 2026-10-07: a re-set seed
  repeated `Random`, `WeightedByName` and the permutation, a draw from a
  probability table took one number, and two runs of one seed with
  different buying times dealt the same cards and enemies; c3runtime.js
  `plugins/AdvancedRandom` and `lib/misc/probability.js`, r504 Web export
  and r505 editor preview, 2026-10-07: `_CreatePermutationTable` and
  `_ShufflePermutationTable` shuffle with one draw per entry, and
  `advanced_random.py --check` found 1068 values over six seeds the same]
- If *Replace system random* is off, `random()`, `choose()` and *Pick
  random instance* use the system random, which no seed controls. If the
  seed must reproduce a draw, use Advanced Random for it. An integer below
  `n` is `floor(AdvancedRandom.Random * n)`. A random instance among the
  picked ones is *Pick nth instance* with
  `floor(AdvancedRandom.Random * Slot.PickedCount)`. *Pick nth instance*
  counts in the picked instances in creation order, so a layout's
  instances come in the same order on every run. If only some draws are
  part of the run, leave *Replace system random* off. Then battle rolls
  and visual jitter do not consume the run's numbers.
  [manual: plugin-reference/advanced-random.md, "Replace system random";
  plugins/system.json, condition `pick-nth-instance`; observed in a game
  project, r505 editor, 2026-10-07]
