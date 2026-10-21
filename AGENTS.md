# Construct3-Cookbook for AI Agents

This repository holds the guides an agent reads before it writes Construct 3
event sheets. The `construct3-agent-plugin` skill of
[Construct3-Agent-Skills](https://github.com/XHXIAIEIN/Construct3-Agent-Skills)
reads them from a clone of this repository; `README.md` says how it finds the
clone.

| Path | What it holds |
|------|---------------|
| `guides/pitfalls.md` | The index of the pitfalls: one conclusion line per entry, a group per page, and "Adding an entry" |
| `guides/plugins/{id}.md`, `guides/behaviors/{id}.md`, `guides/effects/{id}.md` | The pitfalls of one plugin, behavior or effect |
| `guides/{behavior,plugin,effect}-category/{id}.md` | The pitfalls of choosing between objects for one goal |
| `guides/primitives/` | The pitfalls of the event engine and the runtime world that belong to no add-on, on the manual's page names |
| `guides/design/thinking.md`, `guides/design/style.md` | How to design events before writing them, and how the official examples organise, name and comment a sheet |
| `guides/recipes/` | Recipes for feel, menus, sequences and dialogue, sound, progress bars, layers in depth |
| `guides/project-files/` | Hand-editing project JSON, and a new project's sheets, layers and look |
| `scripts/check.py` | The check CI runs: links, the index against its pages, and the names of the pages |

The skill's scripts recognise a clone by `guides/pitfalls.md`, search the
pitfall pages and cite them by these paths. Moving or renaming one is a
change to Construct3-Agent-Skills as well.

## Naming

A page's path comes from three sources only, never a noun of our own:

1. **Construct3-RAG ids.** `plugins/{id}.md`, `behaviors/{id}.md` and
   `effects/{id}.md` take the id exactly as `data/c3-schemas/_index.json` of
   Construct3-RAG writes it, lowercase: `tween`, `eightdir`, `spritefont2`,
   `arr`, `system`, and `_common` for what every object shares.
2. **c3-lang category ids.** A page that chooses between objects for one
   goal is `behavior-category/{id}.md`, `plugin-category/{id}.md` or
   `effect-category/{id}.md`, with the id a key of `text.model.<kind>` in
   Construct3-RAG's `data/c3-lang/en-US.json`: `movements`, `input`,
   `data-and-storage`. A choice with no matching category goes on the page
   of the first object it would go wrong in, and the other objects' pages
   link to it.
3. **Manual page names.** What belongs to no add-on goes under
   `primitives/`, which mirrors the manual's `project-primitives/`:
   `primitives/events/how-events-work.md`, `primitives/objects/containers.md`,
   `primitives/layers.md`.

A file exists only when it holds an entry. Which add-on belongs to which
category is not in the schemas, so a category page is placed by hand.

Words in the text follow the manual: instance, object type, family,
container, hierarchy, sub-event, top-level event, tick, global layer,
template, custom action, image point, time scale. Where the manual spells a
word two ways, take the more frequent one (sub-event, time scale; `timescale`
only as the expression). An ACE or an object is named by its schema
`display-text` and its c3-lang name: *Set animation*, Sprite Font, 9-patch,
8 Direction, Drag & Drop.

## Where an entry goes

- An entry about what one ACE does goes on the page of the schema that
  holds the ACE. System ACEs go to `plugins/system.md`, the ACEs every
  object shares to `plugins/_common.md`. Check the schema with
  `lookup_ace.py` of the skill, which prints the add-on that holds an ACE.
- An entry about how the event engine treats a whole class of things
  (picking, triggers, Else, sub-event order, scope, functions), or about the
  runtime world with no ACE (coordinates, angles, global layers), goes under
  `primitives/`, on the manual page that covers it.
- An entry that chooses between objects for one goal goes on the category
  page.
- An entry has one home. The other pages it concerns link to it.

## Add a pitfall

A pitfall is a runtime behaviour of events that changes which events an
agent writes. A lesson about the project file format, the editor, the
preview or the look goes where "Adding an entry" in `guides/pitfalls.md`
says.

1. Write the entry on its page: the fact, its consequence and its source
   in brackets at the end, such as `[manual: <page>]`, an official example
   id, a schema file or `[observed in a game project, <date>]`. Manual
   wording outranks an observation, which outranks intuition.
2. Add its conclusion as one line to the page's group in
   `guides/pitfalls.md`, in the same place in the order. A conclusion keeps
   the fix, not only the prohibition.
3. A new page starts with the title and the line back to the index that the
   other pages have, and gets a group in the index that says when to read it.

## Before you finish

```bash
python scripts/check.py
git diff --check
```

`check.py` reads the ids from a Construct3-RAG clone and the manual's pages
from a Construct3-Manual clone beside this one; without a clone it skips that
part and prints the command that clones it.

The guides, `AGENTS.md` and the scripts are English. `README.md` and
`README_CN.md` hold the same content; `README.md` names no Chinese text
besides its link to `README_CN.md`. A commit message names an issue of
another repository in words or as a URL in backticks, never as
`owner/repo#N` or `#N`.
