# Construct3-Cookbook for AI Agents

This repository contains the guides that AI agents read before they write Construct 3 event sheets. The `construct3-agent-plugin` skill in [Construct3-Agent-Skills](https://github.com/XHXIAIEIN/Construct3-Agent-Skills) reads them from a local clone. `README.md` describes how the skill locates that clone.

This file describes how to name, place and add entries, and which checks to run before you finish.

## Repository layout

| Path | Contents |
|------|----------|
| `guides/pitfalls.md` | The index of all pitfalls: one group per page, one conclusion line per entry, and the section "Adding an entry" |
| `guides/plugins/{id}.md`, `guides/behaviors/{id}.md`, `guides/effects/{id}.md` | Pitfalls of a single plugin, behavior or effect |
| `guides/{behavior,plugin,effect}-category/{id}.md` | Pitfalls of a choice between several objects for the same goal |
| `guides/primitives/` | Pitfalls of the event engine and the runtime that belong to no single addon, at paths that follow the manual |
| `guides/design/` | `thinking.md` (how to design events before writing them), `style.md` (how the official examples organise, name and comment event sheets) and `native-first.json` (superseded addons, each mapped to the row of the "Native first" table in `thinking.md` that replaces it) |
| `guides/recipes/` | Recipes for game feel, menus, sequences and dialogue, sound, progress bars and layered depth |
| `guides/project-files/` | Conventions for hand-editing project JSON, and the defaults of a new project |
| `docs/decisions/` | The decision records of the guides' layout, naming and index, with their evidence, options and trade-offs, listed in `docs/decisions/README.md` |
| `scripts/check.py` | The validation script that CI runs on links, on the index against its pages, on page names and on the index of the decision records |

Keep these paths stable. The skill's scripts recognise a clone by `guides/pitfalls.md`, search and cite the pitfall pages by path, and read `guides/design/native-first.json`. If you move or rename any of these files, update Construct3-Agent-Skills in the same change.

## Page naming

Derive every page path from one of the three sources below, and never from a name of your own. The skill's lookup finds an addon's page by its ID, and `check.py` rejects any other name.

1. **Construct3-RAG IDs.** Pages under `plugins/`, `behaviors/` and `effects/` use the addon ID exactly as it appears in `data/c3-schemas/_index.json` of Construct3-RAG, in lowercase, for example `tween`, `eightdir`, `spritefont2`, `arr` or `system`. ACEs that every object type shares go on `plugins/_common.md`.
2. **c3-lang category IDs.** A page about a choice between objects for one goal is named `behavior-category/{id}.md`, `plugin-category/{id}.md` or `effect-category/{id}.md`. The ID is a key of `text.model.<kind>` in `data/c3-lang/en-US.json` of Construct3-RAG, for example `movements`, `input` or `data-and-storage`. If no category fits the choice, put the entry on the page of the first object where it would go wrong, and link to it from the pages of the other objects.
3. **Manual page names.** Topics that belong to no addon go under `primitives/`, which mirrors the manual's `project-primitives/` folder, for example `primitives/events/how-events-work.md`, `primitives/objects/containers.md` or `primitives/layers.md`.

Create a page only when it holds at least one entry. The schemas do not record which addon belongs to which category, so choose the category page by hand.

### Terminology

Use the manual's terms: instance, object type, family, container, hierarchy, sub-event, top-level event, tick, global layer, template, custom action, image point and time scale. Where the manual uses two spellings, use the more frequent one, for example "sub-event" and "time scale", and write `timescale` only for the expression.

Refer to an ACE or an object by its schema `display-text` and its c3-lang name, for example *Set animation*, Sprite Font, 9-patch, 8 Direction or Drag & Drop.

## Placing an entry

Each entry lives on exactly one page. Link to it from any other page it concerns. Choose the page by the subject of the entry:

| Subject | Page |
|---------|------|
| The behaviour of one ACE | The page of the schema that holds the ACE. System ACEs go on `plugins/system.md`, and ACEs shared by every object type go on `plugins/_common.md`. Run the skill's `lookup_ace.py` to find which addon holds an ACE. |
| A class of event behaviour, such as picking, triggers, Else, sub-event order, scope or functions, or a part of the runtime with no ACE, such as coordinates, angles or global layers | The `primitives/` page for the manual page that covers it |
| A choice between objects for one goal | The category page |

### The `addons:` line

When `lookup_ace.py` prints an ACE and a matching page exists, it ends the output with a `pitfalls:` line that lists the pages to read before writing that ACE. The script finds the page named by the addon's ID on its own. It finds a category page or a `primitives/` page only through the `addons:` line between the `---` fences at the top of that page.

If a category page or a `primitives/` page holds an entry about an addon or one of its ACEs, add the ID to the page's `addons:` line. Write `eightdir` for the whole addon, or `system/else` for a single ACE. `check.py` fails if an ID is not in the schemas.

## Recording a decision

If a choice about how the guides are laid out, named or written has a visible effect, record its evidence, options and trade-offs in `docs/decisions/`, and add its line to `docs/decisions/README.md` in the same change. That README states the form of a record. A record about the skill's scripts, the plugin or the checker belongs to Construct3-Agent-Skills; link it from here rather than copying it.

## Adding a pitfall

A pitfall is a runtime behaviour of the event system that changes which events an agent should write. Lessons about the project file format, the editor, the preview or the visual style belong elsewhere; the section "Adding an entry" in `guides/pitfalls.md` lists where.

To add a pitfall:

1. Write the entry on its page. State the behaviour and its consequence, and end the entry with its source in brackets, for example `[manual: <page>]`, an official example ID, a schema file or `[observed in a game project, <date>]`.
2. Add the entry's conclusion as one line to the page's group in `guides/pitfalls.md`, at the same position as the entry on its page. Include the fix in the conclusion, not only the prohibition, because an agent reads the index before it decides whether to open the page.
3. If you created the page, start it with the title and the link back to the index that other pages use, and add a group to the index that says when to read the page.

When sources disagree, the manual's wording takes precedence over an observation, and an observation takes precedence over intuition.

## Construct 3 releases

Entries describe the behaviour of the current stable release of Construct 3. Use these sources to check a release:

| To find | Read |
|---------|------|
| The current Stable and Beta releases | `https://editor.construct.net/versions.json` |
| The stable release that the Construct3-RAG data comes from | The `version` field in `data/c3-schemas/_index.json` of the Construct3-RAG clone |
| The runtime code of a release | `https://editor.construct.net/<dir>/<path>`, where `<dir>` writes a patch release with a dash (`r506-3` for r506.3) and `offline.json` in that folder lists every `<path>`, for example `preview/timelines/timelineManager.js` |

If a stable release fixes a pitfall, delete the entry or rewrite it to describe the behaviour that remains. Do not mention the bug report or the release that fixed it, because the reader acts only on the current behaviour. If only a beta release fixes it, keep the entry and name the beta in its source.

## Validation

Before you finish, run these commands from the repository root:

```bash
python scripts/check.py
git diff --check
```

`check.py` reads addon IDs from a Construct3-RAG clone and manual pages from a Construct3-Manual clone next to this repository. When it runs in a git worktree, it looks next to the main working tree instead. If a clone is missing, the script skips the checks that need it and prints the command that clones it.

## Language and commit messages

- Write the guides, `AGENTS.md` and the scripts in English.
- Keep `README.md` and `README_CN.md` in sync. `README.md` contains no Chinese text other than the link to `README_CN.md`.
- In a commit message, refer to an issue in another repository in words or by its full URL in backticks. Do not write `owner/repo#N` or `#N`, because GitHub then adds the commit permanently to that issue's timeline.
