# Construct3-Cookbook

**English** | [中文](README_CN.md)

Construct3-Cookbook holds the guides that an AI agent reads before it writes [Construct 3](https://editor.construct.net/) event sheets: the pitfalls of events with their sources, how to design events, recipes, and how to hand-edit project files.

The `construct3-agent-plugin` skill of [Construct3-Agent-Skills](https://github.com/XHXIAIEIN/Construct3-Agent-Skills) searches the guides in a local clone of this repository, and its output names the page that each result comes from.

## Set it up

Clone this repository into a folder named `Construct3-Cookbook`, beside your clone of Construct3-Agent-Skills or Construct3-RAG:

```bash
git clone --depth 1 https://github.com/XHXIAIEIN/Construct3-Cookbook <folder that holds Construct3-Agent-Skills>/Construct3-Cookbook
```

The skill's scripts look for the clone in this order. If your clone is in another folder, name that folder with one of the first three:

1. The `--cookbook <folder>` option of `search_guides.py`.
2. The environment variable `CONSTRUCT3_COOKBOOK`.
3. A line in the game project's `AGENTS.md` or `CLAUDE.md`:

   ```markdown
   - Construct3-Cookbook: D:/GitHub/Construct3-Cookbook
   ```

4. A `Construct3-Cookbook` folder beside the Construct3-RAG or Construct3-Agent-Skills clone.

The skill's `install.py` writes the line of step 3 into the Construct 3 block of the project's `AGENTS.md`. If `search_guides.py` or `check_project.py` finds no clone, it prints the `git clone` command and still does the rest of its work.

To update the guides, run `git pull` in the clone.

## What is here

| Path | What it holds |
|------|---------------|
| [`guides/pitfalls.md`](guides/pitfalls.md) | The index of the pitfalls. It has a group per page and one conclusion per pitfall, and each group says when to open its page |
| `guides/plugins/`, `guides/behaviors/` | The pitfalls of one plugin or behavior, on a page named by its Construct id, such as `plugins/system.md` or `behaviors/tween.md`. Each entry holds its cases and its source |
| `guides/behavior-category/`, `guides/plugin-category/` | The pitfalls of a choice between objects for one goal, such as `behavior-category/movements.md` |
| `guides/primitives/` | The pitfalls of the event engine and the runtime world, on the manual's page names, such as `primitives/events/how-events-work.md` |
| [`guides/design/`](guides/design/thinking.md) | `thinking.md`: how to design events before you write them. `style.md`: how the official examples organise, name and comment a sheet. `native-first.json`: the superseded addons and the built-in feature that replaces each |
| [`guides/recipes/`](guides/recipes/feel.md) | Recipes for game feel, attack feel, menus, progress bars, scripted sequences and dialogue, sound and flat layers in depth under a 3D camera, and a worked slot grid |
| [`guides/project-files/`](guides/project-files/hand-editing.md) | How to edit the JSON of `eventSheets/`, `layouts/` and `objectTypes/` by hand, and the sheets, layers and look of a new project |

## Contribute

A pitfall is a runtime behaviour of events that changes which events an agent writes. Each entry states the fact, its consequence and its source. [AGENTS.md](AGENTS.md) says how a page is named and where an entry goes.

Before you open a pull request, run `python scripts/check.py`. It checks the links, the index against its pages and the names of the pages. For the names, it reads the Construct3-RAG and Construct3-Manual clones beside this repository. If a clone is missing, it skips that part and prints the command that clones it. CI runs the same check, with both clones, on every pull request and on every push to `main`.

## Licence

[MIT](LICENSE).
