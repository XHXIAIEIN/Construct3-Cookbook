# Construct3-Cookbook

[English](README.md) | **中文**

Construct3-Cookbook 是 [Construct3-Agent-Skills](https://github.com/XHXIAIEIN/Construct3-Agent-Skills) 的配套指引库，供 AI agent 在编写 [Construct 3](https://editor.construct.net/) 事件表之前查阅。指引涵盖事件系统的运行时陷阱、事件设计方法、实现示例，以及手动编辑工程文件的规范。

## 安装

### 使用安装脚本克隆

Construct3-Agent-Skills 自带一个安装脚本，会把本仓库和 skill 读取的其他仓库一起克隆下来。在 Construct3-Agent-Skills 的克隆中运行：

```bash
python scripts/bootstrap.py
```

脚本会把缺少的仓库克隆到存放 Construct3-Agent-Skills 的文件夹中，已有的克隆保持不变。脚本可以随时重新运行，以补上缺少的克隆。

### 手动克隆

如果不使用安装脚本，将本仓库克隆到名为 `Construct3-Cookbook` 的文件夹，并与 Construct3-Agent-Skills 或 Construct3-RAG 的克隆放在同一目录下。放在此位置时，skill 无需额外配置即可找到它。

```bash
git clone --depth 1 https://github.com/XHXIAIEIN/Construct3-Cookbook <parent-folder>/Construct3-Cookbook
```

将 `<parent-folder>` 替换为存放 Construct3-Agent-Skills 克隆的文件夹。

### 使用自定义位置

如果要把克隆放在其他文件夹，可以通过以下任一方式告诉 skill。skill 按优先级依次检查，并使用第一个包含 `guides/pitfalls.md` 的文件夹。

| 优先级 | 方式 | 示例 |
|--------|------|------|
| 1 | `search_guides.py` 的 `--cookbook` 选项 | `--cookbook D:/GitHub/Construct3-Cookbook` |
| 2 | 环境变量 `CONSTRUCT3_COOKBOOK` | `CONSTRUCT3_COOKBOOK=D:/GitHub/Construct3-Cookbook` |
| 3 | 游戏项目 `AGENTS.md` 或 `CLAUDE.md` 中的一行 | `- Construct3-Cookbook: D:/GitHub/Construct3-Cookbook` |
| 4 | 默认位置 | 与 Construct3-RAG 或 Construct3-Agent-Skills 克隆同级的 `Construct3-Cookbook` 文件夹 |

skill 的 `install.py` 会把方式 3 的那一行写入游戏项目 `AGENTS.md` 的 Construct 3 区块。

> [!NOTE]
> 如果 `search_guides.py` 或 `check_project.py` 找不到克隆，会打印需要执行的 `git clone` 命令，并照常完成其余工作。

### 更新指引

在克隆中拉取最新内容：

```bash
git -C <parent-folder>/Construct3-Cookbook pull
```

## 仓库结构

| 路径 | 内容 |
|------|------|
| [`guides/pitfalls.md`](guides/pitfalls.md) | 全部陷阱的索引。每个页面对应一组，每条陷阱一行结论，并说明何时需要阅读该页面。 |
| [`guides/symptoms.md`](guides/symptoms.md) | 按现象排查，例如点击没有反应：每个现象列出要按顺序检查的原因，并链接写有修正方法的页面。 |
| `guides/plugins/`、`guides/behaviors/` | 单个插件或行为的陷阱。页面以该 addon 的 Construct ID 命名，例如 `plugins/system.md`、`behaviors/tween.md`。 |
| `guides/behavior-category/`、`guides/plugin-category/` | 为同一目标在多个对象之间选择时出现的陷阱，例如 `behavior-category/movements.md`。 |
| `guides/primitives/` | 不属于任何单个 addon 的事件引擎和运行时陷阱。页面路径沿用 Construct 3 手册，例如 `primitives/events/how-events-work.md`。 |
| [`guides/design/`](guides/design/thinking.md) | 事件设计指引：`thinking.md` 介绍编写事件之前如何规划，`style.md` 介绍官方示例如何组织、命名和注释事件表，`native-first.json` 列出已被取代的 addon 及其内置替代方案。 |
| [`guides/recipes/`](guides/recipes/feel.md) | 实现示例，涵盖手感、打击感、特效时序、菜单、进度条、拖拽换位排序、脚本化序列与对话、声音、3D 相机下的分层纵深、移植网页或 WebGL 效果，并附一个完整的格子案例。 |
| [`guides/project-files/`](guides/project-files/hand-editing.md) | 手动编辑 `eventSheets/`、`layouts/`、`objectTypes/` 中 JSON 的规范，以及新工程默认的事件表、图层和视觉风格。 |
| [`docs/decisions/`](docs/decisions/README.md) | 决策记录：指引为什么这样分布、命名和建索引，以及依据和权衡过的方案。 |
| [`scripts/check.py`](scripts/check.py) | CI 运行的校验脚本。 |
| [`scripts/test_check.py`](scripts/test_check.py) | 校验脚本必须拒绝或接受的用例。 |

## 贡献

陷阱是指事件系统的某种运行时行为，它会影响 agent 应该写出怎样的事件。每条条目都需要写明行为、后果和来源。页面命名、条目位置和格式要求见 [AGENTS.md](AGENTS.md)。

### 运行检查

提交 pull request 之前，在仓库根目录运行校验脚本：

```bash
python scripts/check.py
python -m unittest discover -s scripts
```

该脚本会检查以下内容：

- 每个相对链接和标题锚点都能解析。
- 每份决策记录在 `docs/decisions/README.md` 中都有一行，按日期从新到旧排列，并且每一行都对应一份记录。
- 每个陷阱页面在 `guides/pitfalls.md` 中都有一组，每条条目对应一行结论，并且每条条目都以来源结尾。
- 来源中每条日期晚于 2026-10-30 的观察都写明它运行的 Construct 版本；在 Construct 之外运行的观察则写明浏览器及其版本。
- 每个页面名都是 Construct3-RAG 中的 addon ID、其 c3-lang 数据中的分类键，或 Construct 3 手册中的页面。
- 页面 `addons:` 行中的每个 ID 都是 Construct3-RAG schema 中的插件、行为或 ACE。

后两项检查会读取与本仓库同级的 Construct3-RAG 和 Construct3-Manual 克隆。在 git worktree 中运行时，脚本会改为在主工作树的同级目录中查找。如果缺少某个克隆，脚本会跳过依赖它的检查，并打印克隆它的命令。

脚本还会打印两个数字：其余观察（日期不晚于 2026-10-30 或没有日期）中有多少条没有写明版本，以及有多少个来源最近一次观察所用的版本早于 Construct3-RAG 数据的版本。`python scripts/check.py --releases` 会列出它们所在的文件和行。这两份清单都不会让检查失败，因为其中每条条目都需要手动重新验证。

CI 在每个 pull request 和每次推送到 `main` 时，都会在两个克隆齐备的环境中运行同一脚本及其测试。

## 许可证

Construct3-Cookbook 基于 [MIT 许可证](LICENSE) 发布。
