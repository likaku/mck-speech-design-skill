<p align="center">
  <h1 align="center">🎙️ McKinsey Speech Design Skill</h1>
  <p align="center">
    <strong>一个让 AI 帮你写演讲稿、自动填入 PPT 备注的 CodeBuddy Skill</strong>
  </p>
  <p align="center">
    告别逐页写备注的痛苦 · 每页 PPT 节省 15 分钟 · 30 页 PPT 省下一整个下午
  </p>
</p>

<p align="center">
  <a href="#-快速开始">快速开始</a> •
  <a href="#-它能做什么">功能</a> •
  <a href="#-为什么做这个">故事</a> •
  <a href="#-加入社群">社群</a>
</p>

---

## 💡 为什么做这个

我们每个人可能都经历过这样的场景：

> 明天要给客户做一场 30 页 PPT 的演讲。PPT 已经做好了，但是——**演讲稿还没写**。
>
> 于是你开始一页一页地想：这页讲什么？怎么开头？怎么过渡到下一页？数据怎么解读？最后怎么收？
>
> 写完之后，还要把演讲稿**手动粘贴到每页 PPT 的备注栏**里。
>
> 一页大概花 15 分钟：构思措辞、组织逻辑、写过渡句、调整语气……30 页下来，**至少半天时间就没了**。

这个 Skill 就是为了解决这个问题。

**它能帮你做到：**

| 传统方式 | 用了这个 Skill |
|---------|--------------|
| 手动逐页写演讲稿 | AI 根据你的角色、听众、目标，自动生成全套演讲稿 |
| 手动复制粘贴到 PPT 备注 | 一键注入所有 PPT 的 Speaker Notes（<1 秒完成） |
| 演讲稿只有 Word 版 | 同时输出 PPT（备注版）+ Word（完整参考版）|
| 每页 ~15 分钟 | 全程 AI 协作，**30 页 PPT 从半天缩短到十几分钟** |

**简单算一笔账：**

```
📊 30 页 PPT × 15 分钟/页 = 450 分钟 = 7.5 小时

用这个 Skill：
  · AI 生成演讲稿：约 10-15 分钟（含对话调整）
  · 注入 PPT 备注：< 1 秒
  · 导出 Word 文档：< 1 秒
  
  总计：约 15 分钟 → 节省 7+ 小时 🎉
```

## 🚀 它能做什么

### 完整的 4 阶段工作流

```
📋 Stage 1: Briefing          →  了解你的角色、听众、场景、目标
🏗️ Stage 2: Architecture      →  金字塔原理 + SCR 框架设计演讲结构
✍️ Stage 3: Drafting           →  逐页生成完整演讲稿（含过渡句）
💉 Stage 4: PPTX Injection    →  自动写入 PPT 备注 + 导出 Word
```

### 核心能力一览

| 能力 | 说明 |
|------|------|
| 🎭 **角色适配** | 根据演讲者身份（CEO / 总监 / 产品经理）自动调整语气和用词 |
| 👥 **听众感知** | 分析听众背景（技术 / 业务 / 高管），调整内容深度 |
| 🏛️ **金字塔原理** | McKinsey Pyramid Principle — 结论先行、MECE 分组、SCR 开场 |
| 📐 **4 种演讲模式** | Executive Briefing / Keynote / Pitch / Workshop，自动匹配 |
| ⏱️ **时间管控** | 按每分钟 130-150 字精确分配每页时间 |
| 🔄 **过渡句设计** | 每个章节间自动生成自然过渡，不会有突兀的跳转 |
| ❓ **自问自答技巧** | 在演讲中插入听众可能的疑问并回答，增强互动感 |
| 🌐 **多语言支持** | 中文 / 英文 / 其他语言，根据实际演讲语言生成 |
| 💉 **PPT 注入** | 全内存操作，20 页 PPT < 1 秒完成注入 |
| 📄 **Word 导出** | 演讲稿自动转为格式化 Word 文档（含时间表、Q&A 准备、备忘） |

### 两份交付物

1. **📊 PPT 文件**（带 Speaker Notes）— 演示时看，只含 Script + Transition，简洁可扫
2. **📄 Word 文档**（完整参考版）— 准备时看，含时间表、Q&A 准备、关键数据备忘、语调提醒

## 📦 安装

### 方式一：在 CodeBuddy 中安装（推荐）

1. 打开 CodeBuddy
2. 将整个 `mck-speech-design-skill` 文件夹放入你项目的 `.codebuddy/skills/` 目录下
3. 开始使用！

```
your-project/
├── .codebuddy/
│   └── skills/
│       └── mck-speech-design-skill/   ← 放这里
│           ├── SKILL.md
│           ├── scripts/
│           ├── references/
│           └── examples/
└── ...
```

### 方式二：直接下载 ZIP

从 [Releases](../../releases) 页面下载最新版 ZIP，解压到 `.codebuddy/skills/` 下。

### 依赖

注入 PPT 和导出 Word 需要 Python 环境：

```bash
pip install python-docx
```

> `inject_notes.py` 仅使用 Python 标准库（`zipfile`, `xml.etree`），无需额外依赖。

## 🎯 快速开始

### 最简用法

在 CodeBuddy 中直接说：

> "我有一份 30 页的 PPT，明天要给客户做汇报，帮我写一份演讲稿并填入 PPT 备注"

Skill 会自动触发，开始询问你的角色、听众、目标等信息，然后生成演讲稿并注入 PPT。

### 进阶用法

你也可以提供更多上下文以获得更精准的演讲稿：

> "我是 XX 公司的技术总监，明天要给客户 CIO 做一场 20 分钟的 AI 战略汇报。这是我的 PPT（附件），听众之前对 AI 有一定了解但持观望态度，我的目标是让他们同意启动一个试点项目。语言用中文，语气要专业但不要太正式。"

### 触发关键词

以下关键词会自动激活这个 Skill：

`speech` · `keynote` · `talking points` · `presentation script` · `speaking notes` · `演讲稿` · `发言稿` · `汇报脚本` · `讲稿` · `备注` · `speaker notes`

## 📁 项目结构

```
mck-speech-design-skill/
├── SKILL.md                              # Skill 核心定义（工作流 + 规范）
├── scripts/
│   ├── inject_notes.py                   # PPT Speaker Notes 注入脚本
│   └── speech_to_docx.py                # MD → Word 格式化导出脚本
├── references/
│   ├── context-gathering-checklist.md    # Briefing 阶段信息收集清单
│   ├── speech-structure-patterns.md      # 4 种演讲结构模式 + 金字塔原理
│   └── tone-and-style-guide.md          # 语调与风格指南
├── examples/
│   ├── notes_example.json               # 示例 Notes JSON
│   └── speech_example.md                # 示例演讲稿
└── README.md
```

## ⚙️ 脚本说明

### inject_notes.py — PPT 备注注入

```bash
python scripts/inject_notes.py <原始.pptx> <notes.json> [输出.pptx]
```

- **全内存操作**：不解压文件到磁盘，直接在内存中修改 ZIP → 速度极快
- **自动处理**：自动创建 notesSlide、notesMaster、Content_Types 注册
- **安全**：不修改原文件，输出到新文件

### speech_to_docx.py — 演讲稿 Word 导出

```bash
python scripts/speech_to_docx.py <speech.md> [输出.docx]
```

- 解析演讲稿 Markdown 结构
- 输出格式化 Word 文档：标题、时间表、分节脚本、Q&A、备忘
- 支持中英文

## 🤝 加入社群

如果这个 Skill 帮到了你，请帮忙 **点个 ⭐ Star**！你的支持是持续更新的最大动力。

有问题、建议或想交流使用心得？欢迎加入我们的社群：

### 💬 微信群

扫码加入微信交流群：

<!-- 👇 在这里替换为你的微信群二维码图片 -->
<p align="center">
  <img src="assets/wechat-qr.png" alt="微信群二维码" width="200" />
</p>

> 如果二维码过期，请添加微信号 `YOUR_WECHAT_ID` 备注「Speech Skill」拉你入群。

### 🎮 Discord

加入 Discord 社区，获取最新更新、提交 Bug 和参与讨论：

<!-- 👇 在这里替换为你的 Discord 邀请链接 -->
**👉 [点击加入 Discord 社区](https://discord.gg/YOUR_INVITE_LINK)**

---

## 📋 Changelog

### v1.3 (2026-03-12)
- 🚀 `inject_notes.py` 重写：全内存 ZIP 操作，注入速度从数秒降至 < 1 秒
- ✂️ PPT Notes 精简：只注入 Script + Transition，去掉冗余内容
- 📄 新增 `speech_to_docx.py`：自动导出格式化 Word 文档
- 📦 双文件交付：PPT（演示用）+ Word（准备用）

### v1.0
- 🎙️ 完整 4 阶段工作流：Briefing → Architecture → Drafting → PPTX Injection
- 🏛️ McKinsey Pyramid Principle + SCR 框架
- 📐 4 种演讲模式匹配
- 💉 PPT Speaker Notes 自动注入

## 📄 License

[MIT](LICENSE) © 2026
