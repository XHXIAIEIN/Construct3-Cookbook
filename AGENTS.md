# Construct3-Cookbook for AI Agents

This repository holds the guides that an agent reads before it writes
Construct 3 event sheets. The `construct3-agent-plugin` skill of
[Construct3-Agent-Skills](https://github.com/XHXIAIEIN/Construct3-Agent-Skills)
reads them from a clone, and `README.md` says how the skill finds that
clone.

| Path | What it holds |
|------|---------------|
| `guides/event-sheets/design/thinking.md` | How to design events before you write them |
| `guides/event-sheets/design/style.md` | How the official examples organise, name and comment a sheet |
| `guides/event-sheets/pitfalls/README.md` | The index of the pitfalls: one conclusion line per entry, grouped by topic, and the section "Adding an entry" |
| `guides/event-sheets/pitfalls/*.md` | One topic file per group, each entry with its cases and its source |
| `guides/event-sheets/recipes/` | Recipes for feel, menus, sequences and dialogue, sound, progress bars and layers in depth |
| `guides/event-sheets/project-files/` | How to hand-edit project JSON, and the sheets, layers and look of a new project |
| `scripts/check.py` | The check that CI runs on the links and on the index against its topic files |

Keep these paths stable. The skill's scripts recognise a clone by the file
`guides/event-sheets/pitfalls/README.md` and cite the guides by these
paths. So if you move or rename one of them, change
Construct3-Agent-Skills to match.

## Add a pitfall

A pitfall is a runtime behaviour of events that changes which events an
agent writes. If a lesson is about the project file format, the editor,
the preview or the look, put it where "Adding an entry" in
`guides/event-sheets/pitfalls/README.md` says.

1. Write the entry into the topic file of its group. State the fact and
   its consequence, and end the entry with its source in brackets, such
   as `[manual: <page>]`, an official example id, a schema file or
   `[observed in a game project, <date>]`.
2. Add the conclusion of the entry as one line to its group in the
   index, at the same position as the entry in the topic file. Keep the
   fix in the conclusion, not only the prohibition.
3. If a fact fits no group, give it a topic file of its own. Then add a
   group to the index that says when to read that file.

If sources disagree, manual wording outranks an observation, and an
observation outranks intuition.

## Before you finish

Run these checks from the root of the repository:

```bash
python scripts/check.py
git diff --check
```

`check.py` reports a broken link or anchor, a group whose conclusion
lines differ in number from the entries of its topic file, a topic file
that the index does not link, and an entry without a source.

## Language and commit messages

- Write the guides, `AGENTS.md` and the scripts in English.
- Keep the same content in `README.md` and `README_CN.md`. In
  `README.md`, write no Chinese text other than the link to
  `README_CN.md`.
- In a commit message, name an issue of another repository in words or
  as a URL in backticks. Do not write `owner/repo#N` or `#N`, because
  GitHub then adds the commit permanently to the timeline of that issue.
