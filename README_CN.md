# Construct3-Cookbook

[English](README.md) | **中文**

Construct3-Cookbook 是一套参考指引，供编写 [Construct 3](https://editor.construct.net/) 事件表的 AI agent 使用。指引涵盖事件系统的运行时陷阱、事件设计方法、实现示例，以及手动编辑工程文件的规范。

[Construct3-Agent-Skills](https://github.com/XHXIAIEIN/Construct3-Agent-Skills) 中的 `construct3-agent-plugin` skill 会读取这些指引。该 skill 在本仓库的本地克隆中搜索，并为每条结果注明来源页面。

## 安装

### 前提条件

- Git
- Construct3-Agent-Skills 或 Construct3-RAG 的克隆

### 克隆仓库

将本仓库克隆到名为 `Construct3-Cookbook` 的文件夹，并与 Construct3-Agent-Skills 或 Construct3-RAG 的克隆放在同一目录下。放在此位置时，skill 无需额外配置即可找到它。

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
| `guides/plugins/`、`guides/behaviors/` | 单个插件或行为的陷阱。页面以该 addon 的 Construct ID 命名，例如 `plugins/system.md`、`behaviors/tween.md`。 |
| `guides/behavior-category/`、`guides/plugin-category/` | 为同一目标在多个对象之间选择时出现的陷阱，例如 `behavior-category/movements.md`。 |
| `guides/primitives/` | 不属于任何单个 addon 的事件引擎和运行时陷阱。页面路径沿用 Construct 3 手册，例如 `primitives/events/how-events-work.md`。 |
| [`guides/design/`](guides/design/thinking.md) | 事件设计指引：`thinking.md` 介绍编写事件之前如何规划，`style.md` 介绍官方示例如何组织、命名和注释事件表，`native-first.json` 列出已被取代的 addon 及其内置替代方案。 |
| [`guides/recipes/`](guides/recipes/feel.md) | 实现示例，涵盖手感、打击感、菜单、进度条、脚本化序列与对话、声音、3D 相机下的分层纵深，并附一个完整的格子案例。 |
| [`guides/project-files/`](guides/project-files/hand-editing.md) | 手动编辑 `eventSheets/`、`layouts/`、`objectTypes/` 中 JSON 的规范，以及新工程默认的事件表、图层和视觉风格。 |
| [`scripts/check.py`](scripts/check.py) | CI 运行的校验脚本。 |

## 贡献

陷阱是指事件系统的某种运行时行为，它会影响 agent 应该写出怎样的事件。每条条目都需要写明行为、后果和来源。页面命名、条目位置和格式要求见 [AGENTS.md](AGENTS.md)。

### 运行检查

提交 pull request 之前，在仓库根目录运行校验脚本：

```bash
python scripts/check.py
```

该脚本会检查以下内容：

- 每个相对链接和标题锚点都能解析。
- 每个陷阱页面在 `guides/pitfalls.md` 中都有一组，每条条目对应一行结论，并且每条条目都以来源结尾。
- 每个页面名都是 Construct3-RAG 中的 addon ID、其 c3-lang 数据中的分类键，或 Construct 3 手册中的页面。
- 页面 `addons:` 行中的每个 ID 都是 Construct3-RAG schema 中的插件、行为或 ACE。

后两项检查会读取与本仓库同级的 Construct3-RAG 和 Construct3-Manual 克隆。在 git worktree 中运行时，脚本会改为在主工作树的同级目录中查找。如果缺少某个克隆，脚本会跳过依赖它的检查，并打印克隆它的命令。

CI 在每个 pull request 和每次推送到 `main` 时，都会在两个克隆齐备的环境中运行同一脚本。

## 许可证

Construct3-Cookbook 基于 [MIT 许可证](LICENSE) 发布。
