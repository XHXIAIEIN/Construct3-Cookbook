# Construct3-Cookbook for AI Agents

This repository holds the guides an agent reads before it writes Construct 3
event sheets. The `construct3-agent-plugin` skill of
[Construct3-Agent-Skills](https://github.com/XHXIAIEIN/Construct3-Agent-Skills)
reads them from a clone of this repository; `README.md` says how it finds the
clone.

| Path | What it holds |
|------|---------------|
| `guides/event-sheets/design/thinking.md` | How to design events before writing them |
| `guides/event-sheets/design/style.md` | How the official examples organise, name and comment a sheet |
| `guides/event-sheets/pitfalls/README.md` | The index of the pitfalls: one conclusion line per entry, grouped by topic, and "Adding an entry" |
| `guides/event-sheets/pitfalls/*.md` | One topic file per group, each entry with its cases and its source |
| `guides/event-sheets/recipes/` | Recipes for feel, menus, sequences and dialogue, sound, progress bars, layers in depth |
| `guides/event-sheets/project-files/` | Hand-editing project JSON, and a new project's sheets, layers and look |
| `scripts/check.py` | The check CI runs: links, and the index against its topic files |

The skill's scripts look for `guides/event-sheets/pitfalls/README.md` to
recognise a clone, and cite files by these paths. Moving or renaming one
is a change to Construct3-Agent-Skills as well.

## Add a pitfall

A pitfall is a runtime behaviour of events that changes which events an
agent writes. A lesson about the project file format, the editor, the
preview or the look goes where "Adding an entry" in
`guides/event-sheets/pitfalls/README.md` says.

1. Write the entry into the topic file of its group: the fact, its
   consequence and its source in brackets at the end, such as
   `[manual: <page>]`, an official example id, a schema file or
   `[observed in a game project, <date>]`. Manual wording outranks an
   observation, which outranks intuition.
2. Add its conclusion as one line to the group in the index, in the same
   place in the order. A conclusion keeps the fix, not only the
   prohibition.
3. A fact that fits no group gets a topic file of its own and a group in
   the index that says when to read it.

## Before you finish

```bash
python scripts/check.py
git diff --check
```

The guides, `AGENTS.md` and the scripts are English. `README.md` and
`README_CN.md` hold the same content; `README.md` names no Chinese text
besides its link to `README_CN.md`. A commit message names an issue of
another repository in words or as a URL in backticks, never as
`owner/repo#N` or `#N`.
