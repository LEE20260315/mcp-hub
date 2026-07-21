---
name: obsidian
description: 读写 Obsidian 知识库笔记。当用户要查笔记、写笔记、搜索知识库、整理 Obsidian vault 时使用。知识库位于 C:/Users/MR.Dong/OneDrive/Obsidian Vault。
---

# Obsidian 知识库

## 知识库位置

```
C:/Users/MR.Dong/OneDrive/Obsidian Vault
```

用 bash 时路径写为：`~/OneDrive/Obsidian\ Vault` 或 `"C:/Users/MR.Dong/OneDrive/Obsidian Vault"`。

## 如何操作

Obsidian vault 本质就是一个**装满 Markdown 文件的文件夹**。pi 内置的 `read`、`write`、`bash` 工具即可完成所有操作，无需 MCP。

### 读取笔记

```bash
# 列出某个子目录
ls "C:/Users/MR.Dong/OneDrive/Obsidian Vault/交易笔记"
```

用 `read` 工具读具体笔记内容。

### 搜索笔记

```bash
# 按内容搜索（递归，忽略 .obsidian 配置目录）
rg -i "关键词" "C:/Users/MR.Dong/OneDrive/Obsidian Vault" -g '!.obsidian' -n
```

### 创建/更新笔记

用 `write` 工具写新文件，或用 `edit` 工具改已有笔记。

笔记建议放对应子目录，命名用中文即可：
- `交易笔记/` - 量化交易相关
- `他山之石/` - 参考资料
- `微信读书笔记/` - 读书笔记
- `Wiki/` - 知识库

### Obsidian 语法要点

- 双链：`[[笔记名]]`
- 标签：`#标签`
- 嵌入：`![[图片.png]]`
- frontmatter：文件顶部 `---` 包裹的 YAML

## 注意事项

- `.obsidian/` 目录是配置，不要乱改
- 改动会通过 OneDrive 自动同步
- 中文文件名注意用引号包裹
