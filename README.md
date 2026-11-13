# 生理基础模型 · 思想年谱

一个纯静态的可视化页面，按时间梳理 2019–2026 年“生理基础模型”方向的**思想演进**：不是论文列表，而是每一步解决了什么问题、和前作是什么关系（继承 / 转向 / 分岔 / 并行 / 落地 / 奠基 / 检验 / 呼应 / 接入），这些问题如何连成脉络，以及各家公司如何把数据变成模型和产品。年谱收录 113 项（论文 55、开源 18、产品 33、宣布 / 收购 / 在建 6、研究队列 1），来自 40 家机构，由 149 条关系连成 9 条脉络；另有 204 项检索到但未上年谱的工作（含第五版从年谱移出的 60 项及其配套链接）列在页面底部“全部来源”，各附原因。

**第五版做了减法**：样本量小、支撑不足（只有题目、海报、招聘或 workshop 短文）、与更强条目重复、或偏离可穿戴主线的条目都移出年谱，转入“全部来源”的“第五版从年谱移出”分组；标准与完整清单见 `RESEARCH.md` 第 3 节。

- **起点**：苹果 ICLR 2024 论文 *Large-scale Training of Foundation Models for Wearable Biosignals*（arXiv 2023-12，ICLR 2024）。之前的 2019–2023 年作为“前奏”可折叠。
- **四条纲**（泳道）：生理信号基础模型 · 生理参数基础模型 · 生理世界模型 · Agent。
- **四个视图**：年谱（四列时间轴）· 脉络（9 条思想线，每条写明问题 → 做法 → 改变 → 解锁 → 未决）· 公司（数据资产 → 模型 → 产品与 Agent）· 问题（5 个核心问题 × 5 个时期）。
- **公司**：苹果、谷歌（含 Fitbit）、三星、Oura、WHOOP、OPPO、华为为主线；Meta、Garmin、Dexcom、雅培、Withings、Ultrahuman、iRhythm、小米（仅公开论文）以及 OpenAI、Anthropic、微软、Amazon 等通用 AI 公司作为参照；FDA 的指南与授权作为监管背景；另有约 35 家高校与研究机构。
- 数据截至 2026-11-13。所有条目的来源、核实过程和存疑项见 [RESEARCH.md](RESEARCH.md)。

## 怎么读

| 操作 | 效果 |
|---|---|
| 顶部“年谱 / 脉络 / 公司 / 问题” | 切换视图；URL 会变成 `#view=threads` 等，可直接分享 |
| 鼠标悬停节点或条目标签 | 显示紧凑卡片：问题 / 做法 / 意义（含编者解读），承接自哪些条目、被哪些条目承接（按关系类型计数）；年谱中同时画出关系线（超过 6 条时，后续关系变淡、不加文字） |
| 点击节点或条目标签 | 新标签页打开原始来源（论文、官方博客、新闻稿或监管文件） |
| 触屏 | 轻点一次弹出底部卡片（含“打开原文”与关闭按钮），点空白处关闭 |
| 筛选（仅年谱视图）：纲 / 机构 / 类型 | 只看某几条泳道、某几类机构、某类条目；窄屏下收进“筛选”按钮 |
| 脉络下拉框 | 在年谱中高亮一条思想线，其余淡出；URL 变成 `#thread=<id>` |
| “显示前奏” | 显示 / 隐藏 2019–2023 年的前史 |
| 页面底部“全部来源” | 年谱条目的全部链接，以及未上年谱的工作（按原因分组）；顶部输入框可按标题、机构、原因筛选 |

节点形状：实心圆 = 论文；带环圆 = 开源模型（权重或代码公开）；菱形 = 产品；虚线空心 = 宣布或在建；大环加“起点” = 起点论文。

宽度不足 860px 时，年谱切换为单列列表（按时期和年份分组，时期要点可折叠，点条目展开摘要）；脉络、公司、问题视图改为单列排版。

## 本地预览

页面通过 `fetch` 读取 `data/*.json`，需要本地 HTTP 服务（直接双击 `index.html` 会提示错误）：

```bash
cd physio-fm-history
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000/
```

## 目录

```
index.html            页面骨架与导言
css/style.css         样式（系统中文字体栈，少量颜色）
js/app.js             渲染：四个视图、泳道布局、关系线、卡片、筛选、移动端列表与底部卡片
data/meta.json        纲、类型、关系、机构与分组、时期、脉络、公司卡、问题矩阵、主叙事
data/entries.json     全部条目
data/sources-extra.json  检索到但未上年谱的工作（分组、原因），由 research/build_sources_extra.py 生成
scripts/validate.py   结构与引用校验（含脱敏检查）
scripts/check_links.py  逐个 curl 检查链接状态
research/             核实用的脚本、研究笔记、迁移脚本（不影响页面）；RESEARCH.head.md 为 RESEARCH.md 的手写部分
scripts/gen_research_index.py  由 RESEARCH.head.md + entries.json 生成 RESEARCH.md
.nojekyll             让 GitHub Pages 原样发布
```

无构建步骤，任何静态托管（含 GitHub Pages）都可直接发布仓库根目录。

## 增改条目

在 `data/entries.json` 的 `entries` 数组中添加对象：

```jsonc
{
  "id": "唯一短 id",
  "date": "2026-07-09",            // YYYY-MM-DD 或 YYYY-MM，决定纵向位置
  "dateShort": "2026.07 / ICML'26", // 可选，节点上显示
  "dateLabel": "arXiv 2026-05；ICML 2026", // 卡片上显示，请区分预印本、会议录用、期刊、产品发布
  "track": "signal | param | world | agent",
  "org": "meta.json 中 orgs 的键",
  "orgNote": "可选，合作方说明",
  "type": "paper | open | product | announce | cohort",
  "era": "e0..e4",                 // 时期，见 meta.json eras
  "prelude": true,                 // 仅前奏条目
  "start": true,                   // 仅起点条目
  "title": "原始标题",
  "short": "节点上的中文短名",
  "url": "主链接（必须是 https、亲自打开过的一手来源）",
  "sources": [{"label": "arXiv", "url": "https://..."}],
  "q": "它要回答的问题", "how": "做了什么", "shift": "意义（编者解读须标明）",
  "links": [{"from": "更早条目的 id", "type": "继承|转向|分岔|并行|落地|奠基|检验|呼应|接入", "note": "一句话说明"}]
}
```

`era` 必须与日期一致（e0 < 2023-12 ≤ e1 < 2024-06 ≤ e2 < 2025-07 ≤ e3 < 2026-01 ≤ e4），校验脚本会检查。

新增脉络时，在 `data/meta.json` 的 `threads` 里加入：

```jsonc
{"id": "…", "name": "…", "question": "一句话问题", "problem": "…", "approach": "…",
 "changed": "…", "unlocked": "…", "open": "仍未解决", "desc": "同 question",
 "steps": [{"id": "条目 id（按日期排序）", "role": "它在这条线里的作用"}]}
```

公司卡在 `companies`（`data` / `model` / `product` 各含 `text` 与 `ids`），问题矩阵在 `questions`（每个问题对每个时期一格，格内 `ids` 必须属于该时期）。改完后运行：

```bash
python3 scripts/validate.py      # 结构、引用、时间顺序、时期、并行跨度、脱敏检查
python3 scripts/gen_research_index.py  # 重新生成 RESEARCH.md
python3 scripts/check_links.py   # 链接状态；404 必须替换，403 多为站点反爬
```

**JSON 是唯一数据源。** 首次生成 JSON 的 `build_entries.py` / `build_meta.py` 已移到 `research/archive/` 并停用（不要再运行，会覆盖修改）。`research/migrate_v2.py`、`migrate_v2_meta.py`、`migrate_v3.py`、`migrate_v4.py`、`migrate_v5.py` 依次记录了第二至五版的增改（`migrate_v4.py` 的外部输入缓存为 `research/v4_*.json`）。第五版做减法后 `meta.json` 带 `dataVersion: 5`，v2–v4 会自动跳过（否则会把移出的条目加回来）；`migrate_v5.py` 本身幂等，移出条目缓存在 `research/v5_removed.json`。`research/build_sources_extra.py` 重新生成 `data/sources-extra.json`（需要工作区里的检索结果文件，缺失时跳过对应部分）。以后直接编辑 JSON 即可。

## 原则

- 每条信息都来自实际打开过的一手来源（论文页、官方博客、新闻稿、产品页）；无法核实的不上页面，写进 RESEARCH.md。
- 区分预印本日期、会议录用、期刊发表与产品发布。
- 只写已公开的论文、产品和博客，不推测任何公司的内部进展。
