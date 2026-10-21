# Construct3-Cookbook

**English** | [中文](README_CN.md)

Construct3-Cookbook holds the guides that an AI agent reads before it writes [Construct 3](https://editor.construct.net/) event sheets. They cover how to plan an interaction before writing its events, the runtime pitfalls with their sources and the style of the official examples. They also hold recipes for game feel, menus, dialogue and the project files.

The [`construct3-agent-plugin`](https://github.com/XHXIAIEIN/Construct3-Agent-Skills) skill reads these guides from a clone of this repository. The guides are kept here, apart from the plugin, so `git pull` brings you each pitfall added here, without a plugin release.

## What is here

| Folder | What it holds |
|--------|---------------|
| [`guides/event-sheets/design/`](guides/event-sheets/design/thinking.md) | `thinking.md`, how to design events before writing them; `style.md`, how the official examples organise, name and comment a sheet |
| [`guides/event-sheets/pitfalls/`](guides/event-sheets/pitfalls/README.md) | Runtime behaviour of events that differs from what a programmer expects. `README.md` is the index, with one conclusion per pitfall. Each topic file holds the cases and the sources |
| [`guides/event-sheets/recipes/`](guides/event-sheets/recipes/feel.md) | Game feel, attack feel, menus, progress bars, scripted sequences and dialogue, sound, flat layers in depth under a 3D camera, and a worked slot grid |
| [`guides/event-sheets/project-files/`](guides/event-sheets/project-files/hand-editing.md) | Editing `eventSheets/`, `layouts/` and `objectTypes/` JSON by hand, and the sheets, layers and look of a new project |

## Use it with the skill

Clone this repository into a folder named `Construct3-Cookbook`, beside your clone of Construct3-Agent-Skills or Construct3-RAG:

```bash
git clone --depth 1 https://github.com/XHXIAIEIN/Construct3-Cookbook <folder that holds Construct3-Agent-Skills>/Construct3-Cookbook
```

The skill's scripts look for the clone in this order. If your clone is in another place, name it with one of the first three:

1. `--cookbook <folder>` on `search_guides.py`;
2. the environment variable `CONSTRUCT3_COOKBOOK`;
3. a line in the game project's `AGENTS.md` or `CLAUDE.md`:

   ```markdown
   - Construct3-Cookbook: D:/GitHub/Construct3-Cookbook
   ```

4. a `Construct3-Cookbook` folder beside the Construct3-RAG or Construct3-Agent-Skills clone.

The skill's `install.py` writes that line into the Construct 3 block of the project's `AGENTS.md`. If `search_guides.py` and `check_project.py` find no clone, they print the `git clone` command and do the rest of their work.

To update the guides, run `git pull` in the clone.

## Contribute

A pitfall is a runtime behaviour of events that changes which events an agent writes. Each pitfall carries its source. [AGENTS.md](AGENTS.md) says where an entry goes and what it needs. Before you open a pull request, run `python scripts/check.py`. CI runs the same check.

## Licence

[MIT](LICENSE).
