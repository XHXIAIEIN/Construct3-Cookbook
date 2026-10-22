# Construct3-Cookbook

**English** | [中文](README_CN.md)

Construct3-Cookbook is the companion guide collection for [Construct3-Agent-Skills](https://github.com/XHXIAIEIN/Construct3-Agent-Skills). AI agents consult it before they write [Construct 3](https://editor.construct.net/) event sheets. The guides cover runtime pitfalls of the event system, practices for designing events, implementation recipes, and conventions for editing project files by hand.

## Installation

### Clone with the setup script

Construct3-Agent-Skills includes a setup script that clones this repository together with the other repositories the skill reads. Run it from your Construct3-Agent-Skills clone:

```bash
python scripts/bootstrap.py
```

The script clones each missing repository into the folder that contains Construct3-Agent-Skills and leaves existing clones unchanged. You can run the script again at any time to add a missing clone.

### Clone manually

To clone this repository without the setup script, clone it into a folder named `Construct3-Cookbook` next to your Construct3-Agent-Skills or Construct3-RAG clone. The skill finds a clone in this location without further configuration.

```bash
git clone --depth 1 https://github.com/XHXIAIEIN/Construct3-Cookbook <parent-folder>/Construct3-Cookbook
```

Replace `<parent-folder>` with the folder that contains your Construct3-Agent-Skills clone.

### Use a custom location

To keep the clone in another folder, point the skill to it with one of the methods below. The skill checks them in order of priority and uses the first folder that contains `guides/pitfalls.md`.

| Priority | Method | Example |
|----------|--------|---------|
| 1 | The `--cookbook` option of `search_guides.py` | `--cookbook D:/GitHub/Construct3-Cookbook` |
| 2 | The `CONSTRUCT3_COOKBOOK` environment variable | `CONSTRUCT3_COOKBOOK=D:/GitHub/Construct3-Cookbook` |
| 3 | A line in the game project's `AGENTS.md` or `CLAUDE.md` | `- Construct3-Cookbook: D:/GitHub/Construct3-Cookbook` |
| 4 | The default location | A `Construct3-Cookbook` folder next to the Construct3-RAG or Construct3-Agent-Skills clone |

The skill's `install.py` writes the line for method 3 into the Construct 3 block of the game project's `AGENTS.md`.

> [!NOTE]
> If `search_guides.py` or `check_project.py` cannot find a clone, it prints the `git clone` command to run and completes the rest of its work.

### Update the guides

Pull the latest changes in your clone:

```bash
git -C <parent-folder>/Construct3-Cookbook pull
```

## Repository structure

| Path | Contents |
|------|----------|
| [`guides/pitfalls.md`](guides/pitfalls.md) | The index of all pitfalls. It has one group per page, with a one-line conclusion for each pitfall and a note on when to read the page. |
| `guides/plugins/`, `guides/behaviors/` | Pitfalls of a single plugin or behavior. Each page is named after the addon's Construct ID, for example `plugins/system.md` or `behaviors/tween.md`. |
| `guides/behavior-category/`, `guides/plugin-category/` | Pitfalls that arise when choosing between several objects for the same goal, for example `behavior-category/movements.md`. |
| `guides/primitives/` | Pitfalls of the event engine and the runtime that belong to no single addon. Page paths follow the Construct 3 manual, for example `primitives/events/how-events-work.md`. |
| [`guides/design/`](guides/design/thinking.md) | Event design guidance: `thinking.md` covers planning events before you write them, `style.md` covers how the official examples organise, name and comment event sheets, and `native-first.json` lists superseded addons with their built-in replacements. |
| [`guides/recipes/`](guides/recipes/feel.md) | Implementation recipes for game feel, attack feel, effect timing, menus, progress bars, scripted sequences and dialogue, sound, and layered depth under a 3D camera, with a worked slot grid example. |
| [`guides/project-files/`](guides/project-files/hand-editing.md) | Conventions for editing the JSON in `eventSheets/`, `layouts/` and `objectTypes/` by hand, and the default event sheets, layers and visual style of a new project. |
| [`docs/decisions/`](docs/decisions/README.md) | The decision records: why the guides are laid out, named and indexed as they are, with the evidence and the options weighed. |
| [`scripts/check.py`](scripts/check.py) | The validation script that CI runs. |

## Contributing

A pitfall is a runtime behaviour of the event system that changes which events an agent should write. Each entry states the behaviour, its consequence and its source. See [AGENTS.md](AGENTS.md) for page naming, entry placement and the required format.

### Run the checks

Before you open a pull request, run the validation script from the repository root:

```bash
python scripts/check.py
```

The script verifies that:

- Every relative link and heading anchor resolves.
- Every decision record has its line in `docs/decisions/README.md`, newest first, and every line has a record.
- Every pitfall page has one group in `guides/pitfalls.md`, with one conclusion line per entry, and every entry ends with a source.
- Every page name is an addon ID from Construct3-RAG, a category key from its c3-lang data, or a page of the Construct 3 manual.
- Every ID in a page's `addons:` line is a plugin, a behavior or an ACE in the Construct3-RAG schemas.

The last two checks read the Construct3-RAG and Construct3-Manual clones next to this repository. When the script runs in a git worktree, it looks next to the main working tree instead. If a clone is missing, the script skips the checks that need it and prints the command that clones it.

CI runs the same script, with both clones present, on every pull request and on every push to `main`.

## License

Construct3-Cookbook is released under the [MIT License](LICENSE).
