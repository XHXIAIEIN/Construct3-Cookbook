# Design and Style Prompts Keep What Every Task Reads

Moved from Construct3-Agent-Skills at commit 46bf73f, where its history stays.

Date: 2026-09-30

## Problem

`guides/design/thinking.md` (20 492 bytes) and `guides/design/style.md`
(15 019 bytes) are read whole for every event design, and style.md again
before events go into a project. About a third of the two served one kind
of task: how a new project is laid out and how it looks (style.md
*Project*, thinking.md *Layout of the sheet*), the examples' feel recipes
(thinking.md *Feel*), and the slot-grid worked case. A task that adds one
interaction to an existing sheet paid for all of it.

## Evidence

The pitfalls split ([pitfalls-index-and-topics.md](pitfalls-index-and-topics.md))
showed that an agent opens a split-out file only when its read-when line
names a narrow feature the task visibly has. So a section moves only when
the task that needs it is visible from the start: generating a project, a
stated effect, a drag onto slots. Native first stays inline: which row
applies shows only while drafting.

Four tasks, two Haiku runs per task and arm, each run confined to its arm's
guides (a new game, one interaction added to an existing sheet, a design
that rests on Native first, a drag onto a slot grid). In the new arm, every
run that needed a moved file opened it from its read-when line, and the
answers scored the same as the old arm's against the guidance; the mistakes
that recurred (walking on *On key pressed*, a graphics sprite copied every
tick, a counter mirroring an instance count) came from rules that stayed
inline, in both arms. Tokens were 1 to 6 % lower in every cell, within the
spread of two runs. Runs and grading:
`.local/docs/evidence/prompt-trim-2026-09-29/`.

The mechanics behind a Native first row move the same way, and the row
keeps the built-ins and a link. With the menu row's navigation in
`guides/recipes/menus.md` and the stacked-items row cut to what the Timer
page, now `guides/behaviors/timer.md`, does not hold, Haiku runs scored the
same as runs on the guide before the cut. The tasks were a key-driven menu,
a stacked-shield design and the trigger-in-function task. Every menu run on
the cut guide opened `menus.md`, every shield run opened the Timer page, and
no run put a trigger inside a function. Runs and grading:
`.local/docs/evidence/prompt-cut-2026-10-15/`.

## Options

1. Keep both files whole. Every design task reads 35 KB.
2. Move each section whose reader is a visible kind of task to a file of
   its own, now under `guides/recipes/` and `guides/project-files/`,
   leaving a read-when line that names the task.
3. Also move Native first, the largest section. Its rows are needed while
   drafting, when the agent does not yet know it needs them; the pitfalls
   split showed that a line a task does not visibly trigger is not followed.

## Decision

Option 2.

| Moved | To | Read when |
|-------|----|-----------|
| style.md *Project*, thinking.md *Layout of the sheet* | `guides/project-files/new-project.md` | generating a project, or adding a layout, layer, event sheet, group or object type to one; how the game looks |
| thinking.md *Feel* | `guides/recipes/feel.md` | generating a game, or events for screen shake, hit stop, squash, hit flash, a choreographed sequence, a following camera or a fade between layouts |
| thinking.md's native slot-grid case | `guides/recipes/worked-case-slot-grid.md`, before the transcribed version | dragging pieces onto slots or a grid, or a draft that hit the smell table |

The sections moved word for word. Each source keeps its heading with the
read-when line, so step 3 of "Before proposing a structure" and the readers
in the skill and the root `AGENTS.md` of Construct3-Agent-Skills still find
them.

A Native first row names the built-in and what to write. A row whose
examples or mechanics need more than that links to the file that holds them
(`guides/recipes/progress-bars.md`, `guides/plugins/touch.md`, and
`guides/recipes/menus.md` for how a menu's cursor moves), so the table
grows by rows, not by what lies behind them.

## Re-evaluate when

- An agent generating a project, or adding a layer or object type, writes
  it without opening `new-project.md`: reword the read-when line, then bring
  the part it missed back inline.
- A task names one of the effects and the run skips `feel.md`: the same.
- `guides/design/thinking.md` passes about 28 KB, or `guides/design/style.md`
  15 KB: look for the next section whose reader is a visible kind of task.
  What keeps the guide above 20 KB is Native first, the smell table and the
  rules, which every design task reads while it drafts.
