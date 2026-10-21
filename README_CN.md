# Construct3-Cookbook

[English](README.md) | **中文**

Construct3-Cookbook 收录 AI agent 写 [Construct 3](https://editor.construct.net/) 事件表之前要读的指引。[`construct3-agent-plugin`](https://github.com/XHXIAIEIN/Construct3-Agent-Skills) skill 从这个仓库的克隆里读取它们。指引和插件分开存放，所以在克隆里 `git pull` 就能拿到每条加进来的陷阱，不用等插件发版。

## 安装

把这个仓库克隆到名为 `Construct3-Cookbook` 的文件夹，放在你的 Construct3-Agent-Skills 或 Construct3-RAG 克隆旁边：

```bash
git clone --depth 1 https://github.com/XHXIAIEIN/Construct3-Cookbook <放 Construct3-Agent-Skills 的文件夹>/Construct3-Cookbook
```

skill 的脚本按下面的顺序找克隆。如果克隆放在别的文件夹，用前三种方式之一指明它：

1. `search_guides.py` 的 `--cookbook <文件夹>`；
2. 环境变量 `CONSTRUCT3_COOKBOOK`；
3. 游戏项目 `AGENTS.md` 或 `CLAUDE.md` 里的一行：

   ```markdown
   - Construct3-Cookbook: D:/GitHub/Construct3-Cookbook
   ```

4. 放在 Construct3-RAG 或 Construct3-Agent-Skills 克隆旁边的 `Construct3-Cookbook` 文件夹。

skill 的 `install.py` 把第 3 种方式的那一行写进项目 `AGENTS.md` 的 Construct 3 块。如果 `search_guides.py` 和 `check_project.py` 找不到克隆，它们会打印 `git clone` 命令，其余工作照常完成。

要更新指引，在克隆里运行 `git pull`。

## 里面有什么

| 文件夹 | 内容 |
|--------|------|
| [`guides/pitfalls.md`](guides/pitfalls.md) | 陷阱索引：事件的运行时行为里和程序员预期不一样的地方。每条陷阱一句结论，按页面分组 |
| `guides/plugins/`、`guides/behaviors/` | 某个插件或行为的陷阱，每个 Construct id 一页，比如 `plugins/system.md`、`behaviors/tween.md`。每条都写着具体情况和出处 |
| `guides/behavior-category/`、`guides/plugin-category/` | 为同一个目标在几个对象之间做选择时的陷阱，比如 `behavior-category/movements.md` |
| `guides/primitives/` | 事件引擎和运行时世界的陷阱，页面名沿用手册，比如 `primitives/events/how-events-work.md` |
| [`guides/design/`](guides/design/thinking.md) | `thinking.md`：写事件之前怎么设计。`style.md`：官方示例怎么组织、命名和注释一张事件表 |
| [`guides/recipes/`](guides/recipes/feel.md) | 手感、打击感、菜单、进度条、脚本化序列和对话、声音、3D 相机下的平面分层，以及一个完整的格子案例 |
| [`guides/project-files/`](guides/project-files/hand-editing.md) | 怎么手改 `eventSheets/`、`layouts/`、`objectTypes/` 的 JSON，以及新工程的事件表、图层和外观 |

## 贡献

一条陷阱是事件的一种运行时行为，它会改变 agent 写出的事件，并且每条都带出处。页面怎么命名、条目放在哪、需要写什么，见 [AGENTS.md](AGENTS.md)。提 pull request 之前，先运行 `python scripts/check.py`。CI 在每个 pull request 和每次推送到 `main` 时运行同一个检查。

## 许可证

[MIT](LICENSE)。
