# Construct3-Cookbook

[English](README.md) | **中文**

Construct3-Cookbook 收的是 AI agent 写 [Construct 3](https://editor.construct.net/) 事件表之前要读的东西：怎么先把交互想清楚、带出处的运行时陷阱、官方示例的写法，以及手感、菜单、对话和工程文件的做法。

[`construct3-agent-plugin`](https://github.com/XHXIAIEIN/Construct3-Agent-Skills) skill 从这个仓库的克隆里读这些指引。它们单独放在这里、不放进插件，是为了让新的陷阱条目 `git pull` 一下就能拿到，不用等插件发版。

## 里面有什么

| 文件夹 | 内容 |
|--------|------|
| [`guides/event-sheets/design/`](guides/event-sheets/design/thinking.md) | `thinking.md` 讲写事件之前怎么设计；`style.md` 讲官方示例怎么组织、命名和注释一张事件表 |
| [`guides/event-sheets/pitfalls/`](guides/event-sheets/pitfalls/README.md) | 事件的运行时行为里和程序员直觉不一样的地方。`README.md` 是索引，每条陷阱一句结论；各专题文件写着具体情况和出处 |
| [`guides/event-sheets/recipes/`](guides/event-sheets/recipes/feel.md) | 手感、打击感、菜单、进度条、脚本化序列和对话、声音、3D 相机下的平面分层，以及一个完整的格子案例 |
| [`guides/event-sheets/project-files/`](guides/event-sheets/project-files/hand-editing.md) | 手改 `eventSheets/`、`layouts/`、`objectTypes/` 的 JSON，以及新工程的事件表、图层和外观 |

## 配合 skill 使用

克隆到 Construct3-Agent-Skills 或 Construct3-RAG 的克隆旁边，文件夹名用 `Construct3-Cookbook`：

```bash
git clone --depth 1 https://github.com/XHXIAIEIN/Construct3-Cookbook <放 Construct3-Agent-Skills 的文件夹>/Construct3-Cookbook
```

这样 skill 的脚本会自己找到它。克隆放在别处时，用下面任一方式指给脚本，脚本按这个顺序找：

1. `search_guides.py` 的 `--cookbook <文件夹>`；
2. 环境变量 `CONSTRUCT3_COOKBOOK`；
3. 游戏项目 `AGENTS.md` 或 `CLAUDE.md` 里的一行：

   ```markdown
   - Construct3-Cookbook: D:/GitHub/Construct3-Cookbook
   ```

skill 的 `install.py` 会把这一行写进项目的 Construct 3 块。没有克隆时，`search_guides.py` 和 `check_project.py` 会打印 `git clone` 命令，其余工作照常进行。

想拿到新的陷阱条目，在克隆里跑 `git pull`。

## 贡献

一条陷阱是事件的一种运行时行为，它会改变 agent 写出的事件，并且要带出处。条目放在哪、需要写什么，见 [AGENTS.md](AGENTS.md)。提 pull request 之前跑一下 `python scripts/check.py`，CI 也会跑。

## 许可证

[MIT](LICENSE)。
