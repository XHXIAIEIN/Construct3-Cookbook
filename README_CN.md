# Construct3-Cookbook

[English](README.md) | **中文**

Construct3-Cookbook 收录 AI agent 写 [Construct 3](https://editor.construct.net/) 事件表之前要读的指引：带出处的事件陷阱、事件的设计方法、做法示例，以及手改工程文件的方法。

[Construct3-Agent-Skills](https://github.com/XHXIAIEIN/Construct3-Agent-Skills) 的 `construct3-agent-plugin` skill 在这个仓库的本地克隆里搜索指引，输出里会注明每条结果出自哪一页。

## 安装

把这个仓库克隆到名为 `Construct3-Cookbook` 的文件夹，放在你的 Construct3-Agent-Skills 或 Construct3-RAG 克隆旁边：

```bash
git clone --depth 1 https://github.com/XHXIAIEIN/Construct3-Cookbook <放 Construct3-Agent-Skills 的文件夹>/Construct3-Cookbook
```

skill 的脚本按下面的顺序找克隆。如果克隆放在别的文件夹，用前三种方式之一指明它：

1. `search_guides.py` 的 `--cookbook <文件夹>` 选项。
2. 环境变量 `CONSTRUCT3_COOKBOOK`。
3. 游戏项目 `AGENTS.md` 或 `CLAUDE.md` 里的一行：

   ```markdown
   - Construct3-Cookbook: D:/GitHub/Construct3-Cookbook
   ```

4. Construct3-RAG 或 Construct3-Agent-Skills 克隆旁边的 `Construct3-Cookbook` 文件夹。

skill 的 `install.py` 把第 3 种方式的那一行写进项目 `AGENTS.md` 的 Construct 3 块。如果 `search_guides.py` 或 `check_project.py` 找不到克隆，它会打印 `git clone` 命令，其余工作照常完成。

要更新指引，在克隆里运行 `git pull`。

## 里面有什么

| 路径 | 内容 |
|------|------|
| [`guides/pitfalls.md`](guides/pitfalls.md) | 陷阱索引。每个页面一组，每条陷阱一句结论，每组写明什么时候打开它的页面 |
| `guides/plugins/`、`guides/behaviors/` | 某个插件或行为的陷阱，页面以它的 Construct id 命名，比如 `plugins/system.md`、`behaviors/tween.md`。每条都写着具体情况和出处 |
| `guides/behavior-category/`、`guides/plugin-category/` | 为同一个目标在几个对象之间做选择时的陷阱，比如 `behavior-category/movements.md` |
| `guides/primitives/` | 事件引擎和运行时世界的陷阱，页面名沿用手册，比如 `primitives/events/how-events-work.md` |
| [`guides/design/`](guides/design/thinking.md) | `thinking.md`：写事件之前怎么设计。`style.md`：官方示例怎么组织、命名和注释一张事件表。`native-first.json`：已被取代的 addon，以及取代每个 addon 的内置功能 |
| [`guides/recipes/`](guides/recipes/feel.md) | 手感、打击感、菜单、进度条、脚本化序列和对话、声音、3D 相机下的平面分层，以及一个完整的格子案例 |
| [`guides/project-files/`](guides/project-files/hand-editing.md) | 怎么手改 `eventSheets/`、`layouts/`、`objectTypes/` 的 JSON，以及新工程的事件表、图层和外观 |

## 贡献

一条陷阱是事件的一种运行时行为，它会改变 agent 写出的事件。每条都写明事实、后果和出处。页面怎么命名、条目放在哪，见 [AGENTS.md](AGENTS.md)。

提 pull request 之前，先运行 `python scripts/check.py`。它检查链接、索引和页面是否对应，以及页面的命名。检查命名时，它读取放在这个仓库旁边的 Construct3-RAG 和 Construct3-Manual 克隆。缺了某个克隆，它就跳过对应部分，并打印克隆它的命令。CI 带着这两个克隆，在每个 pull request 和每次推送到 `main` 时运行同一个检查。

## 许可证

[MIT](LICENSE)。
