# Construct3-Cookbook for AI Agents

This repository holds the guides that an agent reads before it writes
Construct 3 event sheets. The `construct3-agent-plugin` skill of
[Construct3-Agent-Skills](https://github.com/XHXIAIEIN/Construct3-Agent-Skills)
reads them from a clone, and `README.md` says how the skill finds that
clone.

| Path | What it holds |
|------|---------------|
| `guides/pitfalls.md` | The index of the pitfalls: a group per page, one conclusion line per entry, and the section "Adding an entry" |
| `guides/plugins/{id}.md`, `guides/behaviors/{id}.md`, `guides/effects/{id}.md` | The pitfalls of one plugin, behavior or effect |
| `guides/{behavior,plugin,effect}-category/{id}.md` | The pitfalls of a choice between objects for one goal |
| `guides/primitives/` | The pitfalls of the event engine and the runtime world that belong to no addon, on the manual's page names |
| `guides/design/` | `thinking.md`: how to design events before you write them. `style.md`: how the official examples organise, name and comment a sheet. `native-first.json`: the superseded addons, each with the row of the "Native first" table in `thinking.md` that replaces it |
| `guides/recipes/` | Recipes for feel, menus, sequences and dialogue, sound, progress bars and layers in depth |
| `guides/project-files/` | How to hand-edit project JSON, and the sheets, layers and look of a new project |
| `scripts/check.py` | The check that CI runs on the links, on the index against its pages and on the names of the pages |

Keep these paths stable, because the skill's scripts depend on them. They
recognise a clone by `guides/pitfalls.md`, search the pitfall pages, cite
them by path and read `guides/design/native-first.json`. If you move or
rename one of these files, change Construct3-Agent-Skills to match.

## Naming

Take the path of a page from one of these three sources only. The
skill's lookup finds an addon's page by its id, and `check.py` fails on
any other name.

1. **Construct3-RAG ids.** `plugins/{id}.md`, `behaviors/{id}.md` and
   `effects/{id}.md` use the id exactly as `data/c3-schemas/_index.json` of
   Construct3-RAG writes it, in lowercase: `tween`, `eightdir`,
   `spritefont2`, `arr`, `system`. The ACEs that every object type shares
   go on `plugins/_common.md`.
2. **c3-lang category ids.** A page about a choice between objects for one
   goal is `behavior-category/{id}.md`, `plugin-category/{id}.md` or
   `effect-category/{id}.md`. Its id is a key of `text.model.<kind>` in
   Construct3-RAG's `data/c3-lang/en-US.json`: `movements`, `input`,
   `data-and-storage`. If no category matches the choice, put the entry on
   the page of the first object that it would go wrong in, and link to it
   from the pages of the other objects.
3. **Manual page names.** What belongs to no addon goes under
   `primitives/`, which mirrors the manual's `project-primitives/`:
   `primitives/events/how-events-work.md`,
   `primitives/objects/containers.md`, `primitives/layers.md`.

Create a page only when it holds an entry. The schemas do not say which
addon belongs to which category, so choose the category page by hand.

Use the manual's words in the text: instance, object type, family,
container, hierarchy, sub-event, top-level event, tick, global layer,
template, custom action, image point, time scale. If the manual spells a
word two ways, use the more frequent one: sub-event and time scale, with
`timescale` only as the expression. Name an ACE or an object by its schema
`display-text` and its c3-lang name: *Set animation*, Sprite Font,
9-patch, 8 Direction, Drag & Drop.

## Where an entry goes

Give each entry one page, and link to it from the other pages that it
concerns. Choose the page by what the entry is about:

- **One ACE.** Put the entry on the page of the schema that holds the ACE.
  System ACEs go on `plugins/system.md`, and the ACEs that every object
  type shares go on `plugins/_common.md`. To find the schema, run the
  skill's `lookup_ace.py`, which prints the addon that holds an ACE.
- **A whole class of event behaviour or the runtime world.** Picking,
  triggers, Else, sub-event order, scope and functions, and the parts of
  the runtime world that have no ACE (coordinates, angles, global layers),
  go under `primitives/`, on the manual page that covers them.
- **A choice between objects for one goal.** Put the entry on the category
  page.

When a page matches, `lookup_ace.py` ends a printed ACE with a
`pitfalls:` line that lists the pages to read before an agent writes the
ACE. It finds the page that the addon's id
names by itself. It finds a category page or a `primitives/` page only
through the `addons:` line between the `---` fences at the top of that
page. So if such a page holds an entry about an addon or one of its ACEs,
add the addon id to its `addons:` line: `eightdir` for the whole addon,
or `system/else` for one ACE. `check.py` fails on an id that the schemas
do not hold.

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
   Write the fix into the conclusion, not only the prohibition, because
   an agent reads the index before it decides to open the page.
3. If you create a page, start it with the title and the line back to the
   index that the other pages have. Then add a group to the index that
   says when to read the page.

If sources disagree, manual wording outranks an observation, and an
observation outranks intuition.

## Releases

The entries describe the current stable release of Construct 3.

- To find the current Stable and Beta releases, read
  `https://editor.construct.net/versions.json`.
- To find the stable release whose data the Construct3-RAG clone holds,
  read the `version` in its `data/c3-schemas/_index.json`.
- To read the runtime code of a release, fetch
  `https://editor.construct.net/<dir>/<path>`. `<dir>` writes a patch
  release with a dash, such as `r506-3` for r506.3. `offline.json` in that
  folder lists every `<path>`, such as
  `preview/timelines/timelineManager.js`.

If a stable release fixes a pitfall, delete the entry, or rewrite it to
the behaviour that remains. Leave out the report and the release that
fixed it, because the reader acts on the current behaviour only. If only
a beta fixes it, keep the entry, and name the beta in its source.

## Before you finish

Run these checks from the root of the repository:

```bash
python scripts/check.py
git diff --check
```

`check.py` reads the ids from a Construct3-RAG clone and the manual's
pages from a Construct3-Manual clone beside this repository. If a clone
is missing, the check skips that part and prints the command that clones
it.

## Language and commit messages

- Write the guides, `AGENTS.md` and the scripts in English.
- Keep the same content in `README.md` and `README_CN.md`. In
  `README.md`, write no Chinese text other than the link to
  `README_CN.md`.
- In a commit message, name an issue of another repository in words or
  as a URL in backticks. Do not write `owner/repo#N` or `#N`, because
  GitHub then adds the commit permanently to the timeline of that issue.
