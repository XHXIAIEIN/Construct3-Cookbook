# The Pitfalls Are an Index of Conclusion Lines over Their Pages

Moved from Construct3-Agent-Skills at commit 46bf73f, where its history stays.

Date: 2026-09-29, revised 2026-10-21 and 2026-10-24

## Problem

The pitfalls file, now `guides/pitfalls.md`, had grown to 599 lines, about
39 KB, 72 entries in 13 groups. The README loaded it as part of the system
prompt and `guides/design/thinking.md` sends the agent to it before writing
events, so every task paid for all 72 entries while one used two or three
groups.

A table of links is not enough: the file holds facts that intuition gets
wrong, so the agent does not know which one it needs. It has to see that
each pitfall exists without opening anything.

Once split, the index kept growing, by about 30 entries between 2026-09-20
and 2026-09-29. The instructions sent every lesson a preview taught to the
pitfalls, so the index also collected how a project file is written, what
the editor's preview starts from, how a script drives a preview, and how art
should be painted. None of those changes the events an agent writes, and
each one costs every task a line.

## Options

1. One file. Every task reads 39 KB, and the file grows with every preview
   that teaches something.
2. An index of links to topic files. Small, but the agent has to guess
   which topic hides the fact it does not know it is missing.
3. An index that states every pitfall's conclusion in one line, grouped
   under a line that says when to open the group's topic file, which holds
   the entries with their cases and sources.

## Evidence

Three tasks, each hinging on a pitfall outside the inline groups (a global
kept across *Restart layout*, a 44 pt line in a 46 px Text box, *Wait 0*
after *Create object*), one Haiku run per task on the single file and one on
the index. Every run on the index opened the topic file its task needed,
from the when-to-read line, and every run in both arms avoided the pitfall.
The runs on the index read about 7 % fewer tokens.

Picking and Triggers and Else were then tried as topic files too, on three
tasks hinging on them (a family's container, a tween finished inside a
function, *Else* per instance). No run opened either topic file: "when the
events pick" and "when they use a trigger" hold for every sheet, and the
agent took the conclusion line as the whole fact. On the tween task the line
kept the prohibition and lost the fix the full entry gives, and the run built
a sequence that destroys the gem before its tween ends. Tokens did not move.
Runs and grading: `.local/docs/evidence/pitfalls-split-2026-09-28/` and
`pitfalls-split-2026-09-29/`.

By 2026-09-30 the index was 19.5 KB again, 8 KB of it the two inline groups,
whose entries carry long sources and observations. The two groups became
topic files a second time, with a change that answers the failure above:
each conclusion line keeps the fix and not only the prohibition.

By 2026-10-24 the index was 42 KB, past the mark below, so the measurement
that the mark asks for was run: Audio, Timeline controller, Touch and Tween
reduced to their when-to-read lines (34.7 KB) against the full index, three
Haiku runs per task and arm. On four tasks that name
their addon, every run in the reduced arm opened the page its task needed,
and all 24 runs avoided the pitfall. On four tasks that only show what
happens on screen (a coin chime, a finger on a bomb, a fade, a hop), the
chime, finger and fade tasks were right in every run of both arms. The hop
task split them. Every run built the hop from a value tween, not from a
timeline. No reduced run opened the Tween page, and all three restarted
the hop's tag while it still played, so a hit enemy hopped twice. All
three full runs stopped the tag first, two of them from the conclusion
lines alone. An agent that picks an addon as a means to another end does
not think of the addon's group as something to read. Runs and grading:
`.local/docs/evidence/pitfalls-addon-lines-2026-10-24/`.

## Decision

Option 3. `guides/pitfalls.md` keeps its opening rules. Each group is a
`###` heading, a when-to-read line linking its page under `guides/`, and
one conclusion line per entry in the page's order. A page is what owns its
entries ([guides-layout.md](guides-layout.md)): an addon's id
(`guides/plugins/system.md`, `guides/behaviors/tween.md`), a c3-lang
category key (`guides/behavior-category/movements.md`) or a page of the
manual's `project-primitives/`
(`guides/primitives/events/how-events-work.md`), so a group is smaller
than a topic of this repository's own was: 45 groups where there were 18.

The groups stand in two sections. Under Topics, a group keeps its
conclusion lines: the primitives, the categories, and every addon that an
agent picks as a means to another end, such as System, Sprite, Tween,
Timer, Array, Dictionary, JSON or Bullet. Under Feature pages, a group is a
heading and its when-to-read line only: an addon that an agent uses only
when the task names or shows what it does, such as Audio for a sound,
Touch for a finger, Local Storage for a save or Platform for a platformer.
So the index is 32 KB, and a feature page costs a task only when the
task uses its addon.
Picking is now `primitives/events/how-events-work.md` and
`primitives/objects/containers.md`, and Triggers and Else is
`primitives/events/conditions.md`, besides the entries that went to an
addon's page; these are pages too, with groups in the index like the rest. A conclusion keeps the fix: "a tween's *On
finished* is a top-level event of its own that calls the next function",
not only "no trigger inside a function".

A pitfall is a runtime behaviour of events that changes which events an
agent writes: without the line, the agent would write them wrong. Other
lessons have their own homes, named in the index's "Adding an entry" and in
every place that routes a lesson (this repository's `AGENTS.md`, and in
Construct3-Agent-Skills the root `AGENTS.md`, the `construct3-agent-plugin`
skill's `SKILL.md`, `generating-a-project.md` and `checker-rules.md`):

| Lesson | Home |
|--------|------|
| How a project file is written | `guides/project-files/hand-editing.md`, or a checker rule of the skill when a script can test it |
| What the editor, the preview or a script driving them does | the skill's `plugin/skills/construct3-agent-plugin/references/` in Construct3-Agent-Skills, `editor-and-preview.md` for the preview |
| Which cases to play to check a change, and how to reach and read them | the skill's `references/verifying-a-change.md` in Construct3-Agent-Skills |
| How the game looks, its art and colours | `guides/project-files/new-project.md`, or the look documents in the root `AGENTS.md` of Construct3-Agent-Skills |

By that test, where the preview starts and how a script drags in it went to
`editor-and-preview.md`, and the Local Storage key that a rewritten
`project.c3proj` must keep went to `guides/project-files/hand-editing.md`;
the group they left was *Storage and export*. How a WebM Opus file decodes
went to `guides/recipes/sound.md`, the seam of a far-stretched 9-patch to
`guides/recipes/progress-bars.md`, and the renderer that a third-party
effect forces to `guides/project-files/new-project.md`. A sprite drawn
facing right stays: given art that faces up, the agent writes every *Set
angle* wrong without it. An entry the checker also enforces stays too, since
the guides serve as a system prompt where no checker runs.

A new entry goes onto its page with its source, and its conclusion into the
index if its group is under Topics. `scripts/check.py` fails when a page is
not linked from the index, when a Topics group's conclusion lines and the
page's entries differ in number, when a Feature pages group has a
conclusion line, or when an entry has no source.

## Re-evaluate when

- The index passes about 35 KB: first move out what fails the scope
  test, then move to Feature pages a group whose addon only a named or
  shown feature brings into a task, then shorten conclusion lines. The
  sizes behind the mark are in `.local/docs/evidence/prompt-cut-2026-10-15/`.
- An agent breaks an entry of a Feature pages group without opening its
  page, because it picked the addon as a means, as the hop runs picked
  Tween: move the group back to Topics with its conclusion lines. Audio
  and Touch were measured on tasks that only show their feature, and
  Timeline controller only on tasks that name it. The other Feature pages
  groups were placed by judgement.
- An agent writes a sheet that breaks an entry of How events work,
  Containers or Conditions whose fix its conclusion line states: these
  pages are read by nearly every sheet and are not opened, so bring the
  entry back in full and cut elsewhere. Nine runs on the conclusion lines
  that keep the fix (three tasks, three runs each, Haiku 4.5, 2026-09-30)
  broke none: eight opened a topic file, all three tween runs wrote the
  tween's *On finished* as its own top-level event, and all three family
  runs picked through the type
  (`.local/docs/evidence/pitfalls-fix-lines-2026-09-30/`). The line does not
  replace the page: with the Triggers and Else file, now
  `guides/primitives/events/conditions.md`, deleted, three tween runs gave
  one top-level *On finished*, one *Wait* route with format errors and one
  trigger nested in the function.
- An eval shows an agent writing a pitfall's topic without opening its page:
  reword that group's when-to-read line first.
- An agent repeats a mistake that a moved lesson describes, because it did
  not read the lesson's home: bring the lesson back, or point to it from
  where that agent does read.
