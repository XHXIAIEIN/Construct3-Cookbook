# Construct3-Cookbook for AI Agents

This repository holds the guides that an AI agent reads before it writes Construct 3 event sheets: the pitfalls of the event system, how to design events, how the official examples write them, and recipes. The `construct3-agent-plugin` skill of [Construct3-Agent-Skills](https://github.com/XHXIAIEIN/Construct3-Agent-Skills) reads them from a local clone, and `README.md` says how the skill finds that clone.

This file says where an entry goes, what its page is named, how to write it, and which checks to run before you finish.

## Repository layout

| Path | Contents |
|------|----------|
| `guides/pitfalls.md` | The index of all pitfalls: one group per page, with one conclusion line per entry for the groups under Topics and none for the groups under Feature pages, and the section "Adding an entry" |
| `guides/plugins/{id}.md`, `guides/behaviors/{id}.md`, `guides/effects/{id}.md` | The pitfalls of one plugin, behavior or effect |
| `guides/{behavior,plugin,effect}-category/{id}.md` | The pitfalls of a choice between several objects for the same goal |
| `guides/primitives/` | The pitfalls of the event engine and the runtime that belong to no single addon, at paths that follow the manual |
| `guides/design/` | `thinking.md`, how to design events before you write them; `style.md`, how the official examples organise, name and comment event sheets; `native-first.json`, which maps each superseded addon to the row of the "Native first" table in `thinking.md` that replaces it |
| `guides/recipes/` | Recipes for game feel, menus, sequences and dialogue, sound, progress bars and layered depth |
| `guides/project-files/` | The conventions for hand-editing project JSON, and the defaults of a new project |
| `docs/decisions/` | The records of how the guides are laid out, named and indexed, with their evidence, options and trade-offs, listed in `docs/decisions/README.md` |
| `scripts/check.py` | The validation that CI runs on links, on the index against its pages, on sources and their releases, on page names and on the index of the records |
| `scripts/test_check.py` | The cases that `check.py` must refuse or accept, which CI also runs |

Keep these paths stable, because the skill depends on them. Its scripts recognise a clone by `guides/pitfalls.md`, search and cite the pitfall pages by path, and read `guides/design/native-first.json`. If you move or rename one of these files, update Construct3-Agent-Skills at the same time, because its `test_cookbook_paths.py` fails on a path that this repository no longer has.

## Naming

Derive every page path from one of the three sources below. The skill's lookup finds an addon's page by the addon's ID, and `check.py` rejects any other name, so a name of your own is never correct.

1. **Construct3-RAG IDs.** A page under `plugins/`, `behaviors/` or `effects/` takes the addon ID exactly as `data/c3-schemas/_index.json` of Construct3-RAG writes it, in lowercase: `tween`, `eightdir`, `spritefont2`, `arr`, `system`. The ACEs that every object type shares go on `plugins/_common.md`.
2. **c3-lang category IDs.** A page about a choice between objects for one goal is `behavior-category/{id}.md`, `plugin-category/{id}.md` or `effect-category/{id}.md`. The ID is a key of `text.model.<kind>` in `data/c3-lang/en-US.json` of Construct3-RAG, such as `movements`, `input` or `data-and-storage`. If no category fits the choice, put the entry on the page of the first object where it goes wrong, and link to it from the pages of the other objects.
3. **Manual page names.** A topic that belongs to no addon goes under `primitives/`, which mirrors the manual's `project-primitives/` folder: `primitives/events/how-events-work.md`, `primitives/objects/containers.md`, `primitives/layers.md`.

Create a page only when it holds at least one entry. The schemas do not record which addon belongs to which category, so choose the category page by hand.

### Terminology

Use the manual's terms: instance, object type, family, container, hierarchy, sub-event, top-level event, tick, global layer, template, custom action, image point and time scale. Where the manual spells a term two ways, use the more frequent spelling, such as "sub-event" and "time scale". Write `timescale` only for the expression.

Name an ACE or an object by its schema `display-text` and its c3-lang name, such as *Set animation*, Sprite Font, 9-patch, 8 Direction or Drag & Drop.

## Placing an entry

Each entry lives on exactly one page, and every other page that it concerns links to it. Choose the page by the subject of the entry:

| Subject | Page |
|---------|------|
| The behaviour of one ACE | The page of the schema that holds the ACE. System ACEs go on `plugins/system.md`, and the ACEs that every object type shares go on `plugins/_common.md`. To find which addon holds an ACE, run the skill's `lookup_ace.py` |
| A class of event behaviour, such as picking, triggers, Else, sub-event order, scope or functions, or a part of the runtime that has no ACE, such as coordinates, angles or global layers | The `primitives/` page for the manual page that covers it |
| A choice between objects for one goal | The category page |

### The `addons:` line

When `lookup_ace.py` prints an ACE that has a matching page, it ends its output with a `pitfalls:` line that lists the pages to read before writing that ACE. The script finds the page named by the addon's ID by itself. It finds a category page or a `primitives/` page only through the `addons:` line between the `---` fences at the top of that page.

If a category page or a `primitives/` page holds an entry about an addon or one of its ACEs, add the ID to the page's `addons:` line. Write `eightdir` for the whole addon, or `system/else` for one ACE. `check.py` fails on an ID that the schemas do not have.

## Adding a pitfall

A pitfall is a runtime behaviour of the event system that changes which events an agent should write. A lesson about the project file format, the editor, the preview or the visual style is not a pitfall, and the section "Adding an entry" in `guides/pitfalls.md` says where it goes.

To add a pitfall:

1. Write the entry on its page. State the behaviour and its consequence, and end the entry with its source in brackets: `[manual: <page>]`, an official example ID, a schema file, or `[observed in a game project, <release> preview, <date>]`. An observation names the release it ran on, or the browser and its version when it ran outside Construct. `check.py` fails on an observation that names neither and is dated after 2026-10-30.
2. If the page's group in `guides/pitfalls.md` is under Topics, add the entry's conclusion to the group as one line, at the same position as the entry on its page. Include the fix in the line, not only the prohibition, because an agent reads the index before it decides whether to open the page. A group under Feature pages takes no line.
3. If you created the page, start it with the title and the link back to the index that the other pages use. Then add a group to the index that says when to read the page. Put the group under Topics or under Feature pages by the rule in "Adding an entry" in `guides/pitfalls.md`. The evidence for the rule is in `docs/decisions/pitfalls-index-and-topics.md`.

If sources disagree, the manual's wording takes precedence over an observation, and an observation takes precedence over intuition.

## Construct 3 releases

An entry describes the behaviour of the current stable release of Construct 3. To check a release, read these sources:

| To find | Read |
|---------|------|
| The current Stable and Beta releases | `https://editor.construct.net/versions.json` |
| The stable release that the Construct3-RAG data comes from | The `version` field in `data/c3-schemas/_index.json` of the Construct3-RAG clone |
| The runtime code of a release | `https://editor.construct.net/<dir>/<path>`. `<dir>` writes a patch release with a dash (`r506-3` for r506.3), and `offline.json` in that folder lists every `<path>`, such as `preview/timelines/timelineManager.js` |

To find the entries to check again, run `python scripts/check.py --releases`. It lists the observations that name no release, and the sources whose newest observed release is older than the release of the Construct3-RAG data. Neither list fails the check, because each entry needs a probe by hand. The reasons are in `docs/decisions/observed-releases.md`.

If a stable release fixes a pitfall, delete the entry, or rewrite it to describe the behaviour that remains. Do not mention the bug report or the release that fixed it, because the reader acts only on the current behaviour. If only a beta release fixes it, keep the entry and name the beta in its source.

## Recording a decision

If a choice about how the guides are laid out, named or written has a visible effect, record its evidence, options and trade-offs in `docs/decisions/`. Add its line to `docs/decisions/README.md` in the same change, because `check.py` compares that index with the records. The README states the form of a record.

A record about the skill's scripts, the plugin or the checker belongs to Construct3-Agent-Skills. Link to it from here instead of copying it, because two copies drift apart.

## Validation

Before you finish, run these commands from the repository root:

```bash
python scripts/check.py
python -m unittest discover -s scripts
git diff --check
```

`scripts/test_check.py` holds the cases that `check.py` must refuse or accept. If you change what `check.py` refuses or accepts, add a case for that input to `scripts/test_check.py`.

`check.py` reads the addon IDs from a Construct3-RAG clone and the manual pages from a Construct3-Manual clone beside this repository. In a git worktree, it looks beside the main working tree instead. If a clone is missing, the script skips the checks that need it and prints the command that clones it.

## Language and commit messages

- Write the guides, `AGENTS.md` and the scripts in English.
- Keep `README.md` and `README_CN.md` in sync. `README.md` contains no Chinese text other than the link to `README_CN.md`.
- In a commit message, name an issue of another repository in words or by its full URL in backticks. Do not write `owner/repo#N` or `#N`, because GitHub then adds the commit to that issue's timeline permanently.
