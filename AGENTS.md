# Construct3-Cookbook for AI Agents

This repository holds the guides that an agent reads before it writes
Construct 3 event sheets. The `construct3-agent-plugin` skill of
[Construct3-Agent-Skills](https://github.com/XHXIAIEIN/Construct3-Agent-Skills)
reads them from a clone, and `README.md` says how the skill finds that
clone.

| Path | What it holds |
|------|---------------|
| `guides/pitfalls.md` | The index of the pitfalls: one conclusion line per entry, a group per page, and the section "Adding an entry" |
| `guides/plugins/{id}.md`, `guides/behaviors/{id}.md`, `guides/effects/{id}.md` | The pitfalls of one plugin, behavior or effect |
| `guides/{behavior,plugin,effect}-category/{id}.md` | The pitfalls of a choice between objects for one goal |
| `guides/primitives/` | The pitfalls of the event engine and the runtime world that belong to no add-on, on the manual's page names |
| `guides/design/thinking.md`, `guides/design/style.md` | How to design events before you write them, and how the official examples organise, name and comment a sheet |
| `guides/recipes/` | Recipes for feel, menus, sequences and dialogue, sound, progress bars and layers in depth |
| `guides/project-files/` | How to hand-edit project JSON, and the sheets, layers and look of a new project |
| `scripts/check.py` | The check that CI runs on the links, on the index against its pages and on the names of the pages |

Keep these paths stable. The skill's scripts recognise a clone by
`guides/pitfalls.md`, search the pitfall pages and cite them by these
paths. So if you move or rename one of them, change
Construct3-Agent-Skills to match.

## Naming

Take the path of a page from one of these three sources only, never from
a noun of your own:

1. **Construct3-RAG ids.** `plugins/{id}.md`, `behaviors/{id}.md` and
   `effects/{id}.md` use the id exactly as `data/c3-schemas/_index.json` of
   Construct3-RAG writes it, in lowercase: `tween`, `eightdir`,
   `spritefont2`, `arr`, `system`. What every object shares goes on
   `_common`.
2. **c3-lang category ids.** A page about a choice between objects for one
   goal is `behavior-category/{id}.md`, `plugin-category/{id}.md` or
   `effect-category/{id}.md`. Its id is a key of `text.model.<kind>` in
   Construct3-RAG's `data/c3-lang/en-US.json`: `movements`, `input`,
   `data-and-storage`. If no category matches the choice, put it on the
   page of the first object that it would go wrong in, and link to it from
   the pages of the other objects.
3. **Manual page names.** What belongs to no add-on goes under
   `primitives/`, which mirrors the manual's `project-primitives/`:
   `primitives/events/how-events-work.md`,
   `primitives/objects/containers.md`, `primitives/layers.md`.

Create a file only when it holds an entry. The schemas do not say which
add-on belongs to which category, so place a category page by hand.

Use the manual's words in the text: instance, object type, family,
container, hierarchy, sub-event, top-level event, tick, global layer,
template, custom action, image point, time scale. If the manual spells a
word two ways, use the more frequent one: sub-event and time scale, with
`timescale` only as the expression. Name an ACE or an object by its schema
`display-text` and its c3-lang name: *Set animation*, Sprite Font,
9-patch, 8 Direction, Drag & Drop.

## Where an entry goes

- If an entry is about what one ACE does, put it on the page of the schema
  that holds the ACE. System ACEs go on `plugins/system.md`, and the ACEs
  that every object shares go on `plugins/_common.md`. To find the schema,
  run the skill's `lookup_ace.py`, which prints the add-on that holds an
  ACE.
- If an entry is about how the event engine treats a whole class of things
  (picking, triggers, Else, sub-event order, scope, functions), or about
  the runtime world with no ACE (coordinates, angles, global layers), put
  it under `primitives/`, on the manual page that covers it.
- If an entry is about a choice between objects for one goal, put it on
  the category page.
- Give each entry one page. Link to it from the other pages that it
  concerns.

## Add a pitfall

A pitfall is a runtime behaviour of events that changes which events an
agent writes. If a lesson is about the project file format, the editor,
the preview or the look, put it where "Adding an entry" in
`guides/pitfalls.md` says.

1. Write the entry on its page. State the fact and its consequence, and
   end the entry with its source in brackets, such as `[manual: <page>]`,
   an official example id, a schema file or
   `[observed in a game project, <date>]`.
2. Add the conclusion of the entry as one line to the page's group in
   `guides/pitfalls.md`, at the same position as the entry on the page.
   Keep the fix in the conclusion, not only the prohibition.
3. If you create a page, start it with the title and the line back to the
   index that the other pages have. Then add a group to the index that
   says when to read the page.

If sources disagree, manual wording outranks an observation, and an
observation outranks intuition.

## Releases

The entries describe the current stable release. To find the current
Stable and Beta releases, read `https://editor.construct.net/versions.json`.
The `version` in Construct3-RAG's `data/c3-schemas/_index.json` names the
stable release whose data the clone holds. To read the runtime code of a
release, fetch `https://editor.construct.net/<dir>/<path>`. `<dir>` writes a
patch release with a dash, such as `r506-3` for r506.3, and `offline.json`
in that folder lists every `<path>`, such as
`preview/timelines/timelineManager.js`.

- If a stable release fixes a pitfall, delete the entry, or rewrite it to
  the behaviour that remains. Leave out the report and the release that
  fixed it, because the reader acts on the current behaviour only.
- If only a beta fixes it, keep the entry, and name the beta in its source.

## Before you finish

Run these checks from the root of the repository:

```bash
python scripts/check.py
git diff --check
```

`check.py` reads the ids from a Construct3-RAG clone and the manual's
pages from a Construct3-Manual clone beside this one. If a clone is
missing, the check skips that part and prints the command that clones it.

## Language and commit messages

- Write the guides, `AGENTS.md` and the scripts in English.
- Keep the same content in `README.md` and `README_CN.md`. In
  `README.md`, write no Chinese text other than the link to
  `README_CN.md`.
- In a commit message, name an issue of another repository in words or
  as a URL in backticks. Do not write `owner/repo#N` or `#N`, because
  GitHub then adds the commit permanently to the timeline of that issue.
