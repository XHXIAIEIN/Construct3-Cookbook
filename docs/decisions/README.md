# Decision Records

This folder holds the decision records of the guides: the evidence, the
options and the trade-offs behind how the guides are laid out, named and
written. The records about the skill's scripts, the plugin and the checker
stay in [Construct3-Agent-Skills](https://github.com/XHXIAIEIN/Construct3-Agent-Skills/tree/main/docs/decisions),
which this repository links rather than copies. A record goes with what it
decides.

A record answers why the current design is what it is. It carries a `Date`
line, then `Problem`, `Evidence` when it is not in the problem, `Options`,
`Decision`, and `Re-evaluate when`.

- A record states what holds now. When a decision changes, rewrite the
  record; do not append a dated update. A record whose subject is gone is deleted, and the commit that
  deletes it says why.
- A record moved here from Construct3-Agent-Skills says so under its title,
  with the commit it left from. Its history stays in that repository.
- Evidence is the finding that settles the choice, in a sentence or a small
  table, not the log of the runs behind it. A path under
  `.local/docs/evidence/` names the runs in the maintainer's
  Construct3-Agent-Skills clone, which are not published.
- A finding from someone's game project is stated generically: no project,
  object or variable names.

A new record gets a line below, in the same change that adds it: its own
title, its file and the date of its `Date:` line, newest first, and records
of one date by file name. `scripts/check.py` fails when a record has no
line, a line has no record, or the order differs, and prints the expected
lines.

- [Observations Name the Release They Were Made On](observed-releases.md) — 2026-10-30
- [Pixel-Art Effects Read from an Open Source Effect Library](pixel-art-vfx.md) — 2026-10-30
- [Effect Timing Counts Read from Recorded Frames](vfx-timing.md) — 2026-10-22
- [The Guides Are Named by Construct's Own Ids, Categories and Manual Pages](guides-layout.md) — 2026-10-21
- [Design and Style Prompts Keep What Every Task Reads](prompt-references-by-task.md) — 2026-09-30
- [The Pitfalls Are an Index of Conclusion Lines over Their Pages](pitfalls-index-and-topics.md) — 2026-09-29
