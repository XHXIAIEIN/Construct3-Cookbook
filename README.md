# Construct3-Cookbook

**English** | [中文](README_CN.md)

Construct3-Cookbook holds what an AI agent reads before it writes [Construct 3](https://editor.construct.net/) event sheets: how to think an interaction through, the runtime pitfalls with their sources, the style of the official examples, and recipes for game feel, menus, dialogue and the project files.

The [`construct3-agent-plugin`](https://github.com/XHXIAIEIN/Construct3-Agent-Skills) skill reads these guides from a clone of this repository. They live here, apart from the plugin, so that a new pitfall reaches you with `git pull`, without a plugin release.

## What is here

| Folder | What it holds |
|--------|---------------|
| [`guides/pitfalls.md`](guides/pitfalls.md) | The index of the pitfalls: runtime behaviour of events that differs from what a programmer expects, one conclusion per pitfall, grouped by page |
| `guides/plugins/`, `guides/behaviors/` | The pitfalls of one plugin or behavior, a page per Construct id such as `plugins/system.md` or `behaviors/tween.md`, each entry with its cases and its source |
| `guides/behavior-category/`, `guides/plugin-category/` | The pitfalls of choosing between objects for one goal, such as `behavior-category/movements.md` |
| `guides/primitives/` | The pitfalls of the event engine and the runtime world, on the manual's page names, such as `primitives/events/how-events-work.md` |
| [`guides/design/`](guides/design/thinking.md) | `thinking.md`, how to design events before writing them; `style.md`, how the official examples organise, name and comment a sheet |
| [`guides/recipes/`](guides/recipes/feel.md) | Game feel, attack feel, menus, progress bars, scripted sequences and dialogue, sound, flat layers in depth under a 3D camera, and a worked slot grid |
| [`guides/project-files/`](guides/project-files/hand-editing.md) | Editing `eventSheets/`, `layouts/` and `objectTypes/` JSON by hand, and the sheets, layers and look of a new project |

## Use it with the skill

Clone it beside the clone of Construct3-Agent-Skills or Construct3-RAG, under the name `Construct3-Cookbook`:

```bash
git clone --depth 1 https://github.com/XHXIAIEIN/Construct3-Cookbook <folder that holds Construct3-Agent-Skills>/Construct3-Cookbook
```

The scripts look for the clone in this order, so a clone elsewhere is named by one of the first three:

1. `--cookbook <folder>` on `search_guides.py`;
2. the environment variable `CONSTRUCT3_COOKBOOK`;
3. a line in the game project's `AGENTS.md` or `CLAUDE.md`:

   ```markdown
   - Construct3-Cookbook: D:/GitHub/Construct3-Cookbook
   ```

4. a `Construct3-Cookbook` folder beside the Construct3-RAG or Construct3-Agent-Skills clone.

`install.py` of the skill writes that line into the project's block. Without a clone, `search_guides.py` and `check_project.py` print the `git clone` command and run the rest of their work.

To get new pitfalls, run `git pull` in the clone.

## Contribute

A pitfall is a runtime behaviour of events that changes which events an agent writes, with its source. [AGENTS.md](AGENTS.md) says how pages are named, where an entry goes and what it needs. Run `python scripts/check.py` before a pull request; CI runs it too.

## Licence

[MIT](LICENSE).
