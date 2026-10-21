# The Guides Are Named by Construct's Own Ids, Categories and Manual Pages

Date: 2026-10-21

## Problem

When the guides moved out of Construct3-Agent-Skills
(`guides-in-cookbook.md` there), they kept the layout they had in the
plugin: `guides/event-sheets/{design,pitfalls,recipes,project-files}`, the
pitfalls as an index, `pitfalls/README.md`, with one topic file per group
(Picking, Triggers and Else, Input, Rendering and 14 more). The topics were
this repository's own nouns. Nothing could check a topic's name, and an
entry about one ACE could sit under any of several topics: *Wait* under
Wait and time scale, *Create object* under Creating objects, *Restart
layout* under Restarting a layout, all of them System ACEs.

The skill's `lookup_ace.py` ends an ACE's entry with the pitfall pages to
read before writing it (`lookup-pointers.md` in Construct3-Agent-Skills).
With topic files it needed an `addons:` line in each file to map an addon to
its topics, and a topic renamed or split kept stale lines until someone
noticed.

A public repository takes entries from people who do not know those
topics. A contributor needs a rule that says where an entry goes, and a
check that refuses a page in the wrong place.

## Options

1. **One folder per use**, as moved: `guides/event-sheets/` with
   `design/`, `pitfalls/`, `recipes/` and `project-files/`, pitfalls in
   topic files. Dropped: the repository holds only event sheet guides, so
   `event-sheets/` named nothing, and the topic names stayed unverifiable.
2. **Pages by concept** (Picking, Input, Rendering) **or by addon id**
   (`plugins/sprite.md`, `behaviors/tween.md`). A concept page mixes the
   ACEs of many addons, and an agent at the lookup knows the addon's id,
   not the concept. An id is in Construct3-RAG's
   `data/c3-schemas/_index.json`, so a check can refuse a name that is not
   one, and the lookup finds the page from the id with no map. Chosen: ids,
   with the next two options for what an id cannot name.
3. **System folded into the concepts** (*Wait* under time, *Create object*
   under creating objects) **or its own page**, `plugins/system.md`.
   Folding keeps the concept pages that people would look for, but needs a
   hand map from each System ACE to a concept, which is the stale map of
   option 1 again. System is an id in the schemas like any other. Chosen:
   its own page, `plugins/system.md`, and the ACEs every object type shares
   on `plugins/_common.md`. It is the largest page, about 320 lines.
4. **A `solutions/` folder with tags of our own** for a choice between
   objects for one goal (which movement follows a target, Mouse or Touch),
   **or the c3-lang category ids**. Our own tags are unverifiable nouns
   again. The editor groups addons by category in its Add object dialog,
   and the keys are in `text.model.behavior-category`,
   `text.model.plugin-category` and `text.model.effect-category` of
   Construct3-RAG's `data/c3-lang/en-US.json` (`movements`, `input`,
   `data-and-storage`). Chosen: the category ids, as
   `behavior-category/{id}.md`, `plugin-category/{id}.md` and
   `effect-category/{id}.md`. A choice that fits no category goes on the
   page of the first object it would go wrong in, and the other objects'
   pages link to it.
5. **Page names of our own for the event engine** (`picking.md`,
   `triggers-and-else.md`) **or the manual's `project-primitives/` page
   names**. An entry about picking, triggers, *Else*, sub-event order,
   scope or functions, or about the runtime with no ACE (coordinates,
   angles, global layers), has no addon. The manual already has a page for
   each, the entries cite those pages as their source, and a
   Construct3-Manual clone lets a check refuse a path the manual lacks.
   Chosen: `primitives/` mirrors `project-primitives/`
   (`primitives/events/how-events-work.md`,
   `primitives/events/conditions.md`, `primitives/objects/containers.md`,
   `primitives/layers.md`). Picking split between how-events-work and
   containers, and Triggers and Else became conditions.
6. **Terms as each author writes them, or the manual's.** Chosen: the
   manual's terms (instance, object type, family, container, hierarchy,
   sub-event, top-level event, tick, global layer, template, custom action,
   image point, time scale), the more frequent spelling where the manual
   has two, and an ACE or an object by its schema `display-text` and its
   c3-lang name (*Set animation*, Sprite Font, 8 Direction). These are the
   words an agent reads in the lookup's output and the user sees in the
   editor, so a search for them finds the entry.

## Decision

Options 2 to 6 together. Under `guides/`, a pitfall lives on the page of
what owns it, and a page's path comes from one of three sources, never a
noun of this repository's own:

| Pages | Name from | Checked against |
|-------|-----------|-----------------|
| `plugins/{id}.md`, `behaviors/{id}.md`, `effects/{id}.md` | the addon id, lowercase | `data/c3-schemas/_index.json` of Construct3-RAG |
| `{behavior,plugin,effect}-category/{id}.md` | the c3-lang category key | `text.model.<kind>` of `data/c3-lang/en-US.json` |
| `primitives/...` | the manual's `project-primitives/...` path | the Construct3-Manual clone |

An entry about one ACE goes on the page of the schema that holds it. An
entry about a class of event behaviour, or the runtime with no ACE, goes on
the `primitives/` page that covers it. An entry that chooses between
objects goes on the category page. Each entry has one page, and the other
pages it concerns link to it. A page exists only when it holds an entry.

`design/`, `recipes/` and `project-files/` kept their pages and names and
moved up to `guides/`, so `guides/event-sheets/` is gone. The index is
`guides/pitfalls.md`, one group per page, and works as
[pitfalls-index-and-topics.md](pitfalls-index-and-topics.md) decided.

A page named by an id needs no `addons:` line: the lookup finds it from the
id. A category page or a `primitives/` page names the addons and ACEs it
covers in an `addons:` line, because its name does not say which.
`scripts/check.py` fails on a page name outside the three sources and on an
`addons:` id that the schemas do not hold, and skips each part whose clone
is missing.

What it costs:

- Which addon belongs to which category is not in Construct3-RAG: an
  addon's `category` field in the schemas is empty. So an entry goes on a
  category page by hand, and no check says the page is the right one.
- A topic that people looked for by name (Picking, Input) is now spread
  over several pages, and the index is the only place that lists them
  together.
- A pitfall that reads like a recipe (hit stop, a combo reset, stacked
  buffs, coyote jump, closing a popup) stays on its owner's page for now;
  moving such entries into `recipes/` waits.

## Re-evaluate when

- Construct3-RAG records each addon's category: check a category page's
  `addons:` line against it.
- The manual renames or removes a `project-primitives/` page:
  `scripts/check.py` fails, and the page follows the manual.
- A page holds mostly recipe-like entries, or an agent reads a recipe page
  and misses the pitfall on the owner's page: move those entries to
  `recipes/` and keep a conclusion line on the owner's page.
- An agent misses a pitfall because it looked for a concept the index no
  longer names: reword the group's when-to-read line before adding a
  concept page.
