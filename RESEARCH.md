# RESEARCH · 研究笔记与核实记录

核实日期：2026-11-13（Asia/Shanghai）。本文件记录起点如何确定、主叙事、每条条目的来源与核实方式，以及**没有上页面**的条目和原因。

## 1. 核实方法

- **arXiv 条目**：逐个调用 arXiv API（`export.arxiv.org/api/query?id_list=…`）读取标题、作者、v1 日期、comment / journal_ref 与摘要；页面中的数字（人数、小时数、任务数、指标）均取自摘要或正文，脚本见 `research/arx.py`，原始输出见 `research/abstracts.jsonl`。
- **期刊 / 会议 DOI**：经 Crossref API（`research/cr.py`）或 doi.org handle API、PubMed esummary、medRxiv API 核对标题、刊名与出版日期（第二版补录时 Crossref 限流，改用后三者），例如 NEJM 10.1056/NEJMoa1901183（2019-11-14）、npj Digit. Med. 10.1038/s41746-024-01062-3（2024-04-12）、KDD 2026 AnyPPG 10.1145/3770855.3818911（2026-08-08）。
- **公司博客 / 新闻稿 / 产品页**：用 curl 抓取文本后检索关键句；客户端渲染或对 curl 返回 403 的页面（WHOOP、OpenAI、部分 Oura 页面）改用浏览器式抓取读取全文。
- **链接状态**：`scripts/check_links.py` 对全部链接逐一 curl（第四版，2026-11-13，数量见 check_links 输出）。结果：**无 404**。以下为非 2xx 但页面本身存在（站点对脚本反爬或 DOI 跳转限制）：
  - DOI 跳转：NEJM 10.1056/NEJMoa1901183（500）、JAMIA Open ECG-FM、NEJM AI ECGFounder、ACM Pulse-PPG / AnyPPG（403）、medRxiv HuBERT-ECG（500）。均经 doi.org handle API 确认 DOI 已注册并指向出版方页面。
  - WHOOP 新闻稿（403）、OpenAI HealthBench 与 ChatGPT Health（403）：浏览器式抓取已读全文。
  - Meta sEMG 博客（400）：浏览器式抓取已读全文（2025-07-23，数千名参与者、公开 300 多人 100 多小时数据）。
- **日期口径**：`dateLabel` 区分“arXiv 首版日期”“会议录用 / 会议年份”“期刊在线日期”“产品发布 / 测试 / 宣布日期”。纵轴位置用最早公开日期（通常是 arXiv v1 或发布日）。

## 2. 起点的确定

用户要求“起点是 ICLR 苹果那篇论文”。核对苹果在 ICLR 上与可穿戴生理信号相关的工作：

| 候选 | 时间 / 形式 | 结论 |
|---|---|---|
| **Large-scale Training of Foundation Models for Wearable Biosignals** | arXiv 2312.05409（v1 2023-12-08，v2 2024-03-06 注明 “Camera ready version for ICLR 2024”）；OpenReview pC3WJHf51j，ICLR 2024 poster；ICLR 会议录已收录 | **选为起点** |
| RelCon（运动基础模型） | ICLR 2025 | 更晚，且是对起点的延伸 |
| Frequency-Aware MAE（bioFAME） | arXiv 2023-09-12；2024 年 ICLR workshop | workshop，非主会；第四版作为起点之前的苹果方法论文上页面 |
| Subject-Aware Contrastive Learning | 2021 | 更早，作为前奏 |

选定理由：它是苹果第一篇在 ICLR 主会、明确以“基础模型”为框架处理消费级可穿戴 PPG/ECG 的论文；作者自述为首个在消费级可穿戴设备大规模采集的 PPG/ECG 上训练的基础模型（AHMS 约 14.1 万人、约 3 年数据）。后续苹果的加速度蒸馏、WBM、高血压提醒、符号结构等工作都可追溯到它。

作者：Salar Abbaspourazad, Oussama Elachqar, Andrew C. Miller, Saba Emrani, Udhyakumar Nallasamy, Ian Shapiro（Apple）。

## 3. 结构：四个视图与它们回答的问题

第二版（2026-11-13）把页面从“一张时间轴”扩成四个互相引用的视图，全部由 `data/meta.json` 驱动：

| 视图 | 数据 | 回答的问题 |
|---|---|---|
| 年谱 | `entries` + `eras` | 什么时候、谁、做了什么；与前作是什么关系 |
| 脉络 | `threads`（9 条，每条含 problem / approach / changed / unlocked / open 与逐步 role） | 一个问题如何被一代代改写 |
| 公司 | `companies`（9 张卡：数据资产 → 模型 → 产品与 Agent + 编者判断） | 各家把数据变成产品的路径差在哪里 |
| 问题 | `questions`（5 个核心问题 × 5 个时期） | 同一问题在不同时期的答案；每个时期的整体立场 |

九条脉络（第五版由 13 条合并而来）：数据从哪里来；监督从哪里来（同一个人，或更贵的模态；原“以人为锚”“跨模态脚手架”“预训练目标”合并）；建在哪一层；开放、外推与检验（原“开放与检验”“配方外推”合并）；从表征到动力学（世界模型）；健康年龄；语言接口；Agent 与入口（原“Agent 的闭环”“谁拥有入口”合并）；落地（监管级功能从专门模型到基础模型特征）。

五个核心问题：监督信号从哪里来；建模放在哪一层；模型回答什么问题；谁来解释、谁来行动；数据与模型是否公开、能否被检验。

关系类型定义：继承（沿用核心做法并推进）、转向（保留问题，换对象或范式）、分岔（从同一思路分出新方向）、并行（同期独立的相近思路，校验脚本对相隔超过约 14 个月的“并行”报警）、落地（研究进入产品或服务）、奠基（提供数据、队列或通道，而非方法；第二版新增）；第三版新增：检验（后作系统评测或批评前作）、呼应（思路相近但无直接继承，编者解读）、接入（前作被后作当作组件调用）。关系、脉络、公司判断与问题矩阵都是本项目的**解读**，除注明“官方称”“论文称”外，并非原作者自述。

主叙事（页面底部）共七段：起点如何改写问题；向上、横向、向外三个扩张方向；开放之后的检验（PPG-Bench、ECG 尺度律）；落地的两种节奏（苹果 vs OPPO，Meta 两个月量产）；Agent 先行、接地在后，以及通用 AI 公司入场；世界模型的形成与批评；各家位置（编者判断）。

## 3.1 收录标准

一项工作上页面，需要同时满足：

1. **有一手来源**：论文页 / DOI、官方博客、新闻稿、监管文件或产品页，且已实际打开读取；仅有媒体转述的不收。
2. **在某条脉络里有位置**：它提出、推进、反驳或落地了某个问题；能写出“问题 / 做法 / 意义”三句话，且至少能和一条已有条目建立有理由的关系，或作为某条脉络的一步。
3. **与可穿戴或生理信号直接相关**：通用时序模型（TimesFM、Chronos、MIRA）和疾病轨迹模型（Delphi-2M）作为参照收录，因为生理世界模型以它们为基线或对照。
4. **公司条目只写公开信息**：论文、产品、新闻稿、招聘页；不推测任何公司的内部进展。

## 3.2 第二版新增（47 项）

前奏补源头：CLOCS、华为心脏研究、BIOT、谷歌“LLM 是少样本健康学习者”、谷歌收购 Fitbit。
2024：HeAR、SiamQuality、SleepFM、苹果 Vitals、AMIE、ECG-FM、ECGFounder、HuBERT-ECG、SensorLLM、CGM-LSM、CBraMod、Oura × Dexcom、苹果睡眠呼吸暂停提醒。
2025：谷歌脉搏丢失检测、GPT-PPG、HealthBench、Workout Buddy、CSFM、三星收购 Xealth、Meta Neural Band、WHOOP Advanced Labs、OPPO AI 健康管家、Oura AHA 2025 海报。
2026：Claude 健康连接器、Ultrahuman Jade、微软 Copilot Health、AC-JEPA、WavesFM、ECG-WM、ECG 尺度律、OpenMHC、WEQA、StepFM、PWM、Sensori、PulseLM、SleepFM-2、PPG-LM、传感器—语言—行动模型、PPG-Bench、Rethinking World Models、Oura 个性化计划。

第一版中几处跨度达数年的“并行”关系被删除或改为更准确的类型（例如 ChatGPT Health 与 WHOOP Coach 改为“转向”，三星就寝建议、OPPO 2024 高血压研究去掉牵强的并行线）。

## 3.3 第三、四版（2026-11-13 下午）

**第三版：逻辑与事实复核。** 按逻辑审阅与事实核查两份报告逐条核对后修改：SensorWM 不再写“四条纲第一次闭合”（输入是周级指标，信号纲没有进入；反事实来自观察数据），数字按 arXiv 2611.08568 摘要与谷歌博客重写；PPG-Bench 的 35.3% 与 83.8% 按原文口径重写；9 条牵强关系降级为“呼应”或删除；牛津加速度模型移到 2022-06（arXiv 首版）、Meta 肌电移到 2024-02（bioRxiv）；新增“数据从哪里来”“预训练目标”“健康年龄”三条脉络；7 个孤立节点补上有理由的关系；11 处事实修正（日期、单位、数字）。脚本：`research/migrate_v3.py`。

**第四版：补漏合并。** 输入五份只读检索结果（补漏候选 20 项、公司检索 128 项、学术检索 1,218 项、深读 21 项、会议/期刊补扫 527 项），逐条打开一手来源抽查后合并，条目由 111 增至 172，未上年谱的 114 项列入第 6 节。脚本 `research/migrate_v4.py`（依次在 v2、v3 之后运行）与 `research/build_sources_extra.py`：

- 补漏候选采纳 15 项（Google Health app、Health Guardian、谷歌 Nature 高血压筛查、GlucoFM、FDA 健康功能指南、Oura Health Radar、ChatGPT Health 全面推送、亚马逊健康 AI、MAI-DxO、OpenTSLM、sleep2vec、杜比 PPG、Aether 尺度律、SOTER、苹果语音模型迁移）；第 16、20 名作为已有条目的补充来源；第 17–19 名（低置信）列入第 6 节。日期按最早公开修正：GlucoFM 取 arXiv 2026-05-29（博客 2026-08-26），MAI-DxO 取 arXiv 2025-06-27，苹果语音模型迁移取 arXiv 2025-08-29。
- 公司检索新增 10 项：Oura 心血管年龄、三星睡眠呼吸暂停（FDA De Novo）与 LVSD、三星 Galaxy AI 手表、Withings AI 连接器、微软波形推理立场论文、Amazon Halo（2020 上市、2023 停止）、首个非处方 CGM、雅培 × 谷歌、谷歌生物标志物多 Agent；另把 17 个“附为来源”的链接挂到对应条目。
- 学术检索新增 16 项：NeuroLM、REVE、GPTCoach、HeartLang、OPERA、OSF、HEARTS、Inertia-1、DeepMind 活动识别尺度律、“超越静态编码器”立场论文、Organ-Agents、苹果 PpgAge 衰老时钟、HeartBEiT、PULSE、Sonata、HealthJev，均核对了 arXiv/DOI 页面、首版日期与作者单位。
- 深读新增 13 篇苹果论文（2020 ECG 表征与去噪 → 2026 EMBridge）与 SleepFounder；另有 7 条与补漏候选重叠的条目（苹果语音模型迁移、sleep2vec、GlucoFM、杜比 PPG、SOTER、Aether、OpenTSLM）以深读版本替换。
- 会议/期刊补扫新增 6 项：IMWUT 2024“从分类到临床洞见”、IMWUT 2025 GLOSS、npj Digital Medicine 2026“杭好梦”睡眠 Agent、medRxiv 代谢健康 Agent、HealthFlux 全模态健康世界模型、BioLT 流式生理建模（均经 Crossref、medRxiv API 或期刊页面核对）；SensorWM 的世界模型部分在 2026-10-02 先以 NeurIPS 2026 workshop 论文公开，作为补充来源写入（条目日期仍取 arXiv 2026-11-05，因为两者题目与范围不同）。OpenReview 上的 PhysioJEPA、PATCHCODE、睡眠 next-token 预训练因页面需人机验证、未能亲自核对，列入第 6 节观察名单。其中指向更晚条目的关系被反转方向，跨度超过约 14 个月的“并行”改为“呼应”。

**第五版：做减法（2026-11-13 傍晚）。** 目标是逻辑清晰：每条留在年谱上的条目都要在某条脉络里承担一步，并有一手来源支撑。条目由 172 减到 112，收尾时按同一标准升格 1 项（SleepJEPA），最终 113 项；脉络由 13 条合并为 9 条，关系由 263 条减到 149 条。脚本 `research/migrate_v5.py`（被移出条目缓存在 `research/v5_removed.json`；数据标记 `dataVersion: 5` 后，v2–v4 脚本自动跳过，不会把移出的条目加回来）。

移出标准（满足任一项且不是某条脉络必需的一步）：

1. **样本量小**：几十人或模拟用户的研究，结论不足以代表一个方向；
2. **支撑不足**：只有题目、海报、招聘或新闻稿而无技术材料；workshop 短文；不改变脉络走向的单篇方法；
3. **重复**：与更强的已收条目思路相同（同一配方换一个模态或数据集，或同一产品的后续推送）；
4. **偏离主线**：与可穿戴生理信号无直接关系的通用医疗 AI、医疗 Agent 或已停产设备。

保留：起点论文；各家公司有官方来源的关键产品；每条脉络的转折点。移出的 60 项全部转入“全部来源”最前面的分组“第五版从年谱移出”，每条注明类别与原因，连同其补充来源（共 90 个链接）。关系方面：删去指向移出条目的边；“呼应”只保留 10 条承载论点的；跨度超过 200 天的“并行”删除；再补上有依据的主线关系（如谷歌 Nature 高血压筛查 ↔ 苹果高血压提醒、健康年龄链、睡眠与血糖链），保证没有孤立节点、每个条目都在至少一条脉络中。时期要点、主叙事、公司卡与问题矩阵按新条目集重写，结论先行。会议/期刊补扫的最终结果（推荐 16 项，其中高优先 8 项；仅列表 531 项）按更严格的标准处理：只升格 SleepJEPA（medRxiv 2026-04-03，西奈山伊坎医学院；经 medRxiv API 核对摘要：55,518 次居家睡眠研究、422,035 小时，在独立队列上复现、各结局优于 SleepFM），因为它为“监督从哪里来”提供了 JEPA 潜空间预测在大规模睡眠数据上的证据；斯坦福等的健康世界模型 HealthFlux（medRxiv 2026-09-21）不含可穿戴信号，仍列在“第五版从年谱移出”；睡眠 next-token 预训练（ICML 2026 workshop，作者单位未核实）、睡眠公平性、PSG 大模型、AcceleRest 等列入观察名单。SensorWM 的 NeurIPS 2026 CWM workshop 论文（OpenReview 8SH3daIGHz，Lee & Heydari，谷歌，2026-10-02 发布，已录用）作为 sensorwm 的补充来源，注明它在潜空间建模周级指标、不重建原始信号；AMIE 的 Nature Medicine 2026 心内科论文（10.1038/s41591-025-04190-9，2026-02-06）挂在已移出的 AMIE 条目下。

移出清单：

- **样本量小（4 项）**：PhysioMTL：为每个人学 HRV 昼夜节律，并能做反事实（苹果，2022-03-19）——小规模 HRV 研究，与后来的个体基线产品没有公开承接；GPTCoach：按动机访谈做运动教练的 LLM（斯坦福大学，2024-05-09）——16 名参与者的实验室研究；教练方法论由后来的 PHA、Fitbit 教练承接；Sonata：小数据下的 IMU 潜空间世界模型（TimeTrace Labs × 牛津大学，2026-04-20）——739 人、19 万窗口的小规模预训练；预训练目标的对照意义由 AC-JEPA 等代表；HealthJev：会积累经验的长期健康 Agent（复旦大学 等，2026-07-15）——20 名模拟用户、90 天的模拟基准，非真实可穿戴数据。
- **支撑不足（19 项）**：手表单导联心电的逐拍表示与结构化去噪（苹果，2020-11-30）——统计模型而非预训练；与主线没有可证的承接；Latent Temporal Flows：AHMS 多变量时序的潜空间生成预测（苹果，2022-10-14）——苹果动力学前史已由 2020 血糖与 2022 运动心率两篇代表；MAEEG：苹果在 EEG 上的掩码重建预训练（2022）（苹果，2022-10-27）——workshop 论文；掩码一支由 LaBraM、LSM 代表；三星：Galaxy AI 进入手表（Energy Score）（三星，2024-05-29）——Energy Score 等综合分，官方未说明模型，与基础模型主线无关；跨模态重建与模态丢弃：多模态生理基础模型怎么预训练（苹果，2024-10-21）——workshop 论文；跨模态机制的证据由正式发表的工作代表；语音基础模型的特征可直接用于可穿戴信号（苹果，2025-08-29）——workshop 论文；跨域复用的观察，未有后续；CPEP：用手部姿态教肌电，实现零样本手势识别（苹果，2025-09-04）——workshop 论文；同一工作的主会版本 EMBridge 已收录；Oura：用大规模基础模型检测心血管病（Oura，2025-11）——只有会议海报题目，摘要未能核实；PARS：预测两段 EEG 的相对时移来预训练（苹果，2025-11-14）——workshop 论文，未改变主线；Ultrahuman Jade：会触发测量的 Agent（Ultrahuman，2026-02-27）——产品介绍较少，未说明模型；立场：可穿戴基础模型应超越静态编码器（剑桥大学，2026-03-20）——立场论文；“走向动力学”的论证由实际的世界模型条目承担；不同模态的健康模型收敛到相近表征（苹果，2026-05-08）——表征收敛的分析性工作，暂无后续；微软立场论文：可核验的生理波形推理（微软，2026-06-19）——立场论文，没有模型或数据；PWM：以事件为条件的人体状态转移（Fullive-AI × 北京大学，2026-08-15）——小团队预印本，与 NormWear-2、HealthFormer 思路重复且证据更弱；代谢健康 Agent：用工具计算，避免编造指标（Pheno.AI × MBZUAI，2026-08-17）——预印本中的示例对比，非系统评测；谷歌：从可穿戴数据筛选候选生物标志物的多 Agent 系统（谷歌，2026-08-21）——研究博客介绍的工具，未有评测论文；传感器—语言—行动模型（UCLA，2026-10-06）——单篇预印本，“感知—语言—行动”统一的说法缺少后续验证；WHOOP 组建 Foundation AI 团队（WHOOP，2026-10-29）——只有招聘页与访谈，没有论文或产品；BioLT：把窗口级生理模型变成小时级流式模型（牛津大学，2026-11-09）——2026-11 新预印本，尚无可评估的影响。
- **重复（27 项）**：HeartBEiT：850 万份心电的掩码图像预训练（西奈山伊坎医学院，2023-06-06）——临床心电预训练由 ECG-FM、ECGFounder 代表；MotionPrint：一个端侧运动模型，戴在哪、什么设备都能用（苹果，2024-02-06）——设备与佩戴位置异构问题由 Device Passport 承接；本条只是数据集与端侧模型，未进入任何脉络；Chronos：把时序当语言来学（Amazon，2024-03-12）——通用时序基线由 TimesFM 代表；SiamQuality：把差质量 PPG 变成监督（埃默里大学 等，2024-04-26）——PPG 自监督由 PaPaGei、Pulse-PPG 代表；从分类到临床洞见：LLM 推理行为健康感知数据（华盛顿大学 等，2024-05-13）——与 Health-LLM 同期同题；OPERA：开放的呼吸声基础模型与基准（剑桥大学，2024-06-23）——呼吸声基础模型由 HeAR 代表；NeuroLM：把 EEG 当作外语交给 LLM（上海交通大学，2024-08-27）——EEG—语言对齐；“信号 + 语言”由 SensorLM、OpenTSLM 代表；HuBERT-ECG：三种规模的自监督心电模型（布雷西亚大学，2024-11-18）——与 ECG-FM、ECGFounder 同类；CBraMod：按空间与时间分解的 EEG 模型（浙江大学，2024-12-10）——EEG 基础模型由 LaBraM 代表；HeartLang：把心搏当词、节律当句（北京大学，2025-02-15）——心电表征同类工作；GPT-PPG：生成式 PPG 基础模型（埃默里大学 等，2025-03-11）——PPG 开源模型由 PaPaGei、Pulse-PPG 代表；Garmin Active Intelligence（Garmin，2025-03-27）——“AI 解释层进订阅”由 WHOOP、Oura、Dexcom 代表；GLOSS：多 LLM 协作解读被动感知数据（东北大学（美国）× RMIT，2025-09-03）——与 PHIA 同题（LLM 解读个人传感数据）；SleepFounder：只用心肺信号的“零负担”睡眠基础模型（北京大学，2025-09-09）——睡眠方向由 SleepFM、SleepFM-2、sleep2vec 代表；REVE：25,000 人、任意电极布局的 EEG 模型（IMT Atlantique × 蒙特利尔大学，2025-10-24）——EEG 基础模型由 LaBraM 代表；小波多尺度掩码重建的 PPG 模型（三星，2026-01-18）——三星多尺度思路由 HiMAE 代表；PulseLM：PPG—文本问答数据集（新加坡管理大学，2026-02-10）——PPG—文本方向由 HiPPT 代表；OSF：睡眠基础模型的预训练与尺度（UCLA，2026-02-27）——尺度律证据由 LSM、心电尺度律与 Aether 代表；用 ECG 与呼吸指标挑选对比样本的稳健 PPG 模型（杜比实验室 × 佐治亚理工，2026-06-05）——“用贵模态定义监督”由 AnyPPG、xMAE 代表；WEQA：按问题调度模型的可穿戴问答 Agent（剑桥大学，2026-06-16）——Agent 调度模型的思路由 PHA 代表；Inertia-1：1,820 万小时加速度的开放研究（UCLA，2026-07-07）——加速度预训练由牛津模型与 Sensori 代表；Health in ChatGPT：从独立空间到全对话可调用（OpenAI，2026-07-23）——已并入 ChatGPT Health 条目的补充来源；雅培 × 谷歌：Lingo 血糖数据进入 Google Health Coach（Abbott（雅培），2026-08-11）——可穿戴 + CGM 合作由 Oura × Dexcom 代表；作为 Google Health app 的补充来源；DNA-PPG：形态与生理语义的双邻域对齐（小米，2026-08-15）——“参数语义引导 PPG”与 AnyPPG、OPPO 心脏年龄的思路重复；SOTER：频段专家 + 神经 CDE 的连续时间生理生成模型（复旦大学 等，2026-09-15）——连续时间生成模型，与 NormWear-2 等重复，且以临床波形为主；PPG-LM：片段、事件、就诊三层文本对齐（埃默里大学 等，2026-09-27）——PPG—文本方向由 HiPPT 代表；MS-ECG-FM：多源临床报告对齐的 ECG 模型（苹果，2026-10-06）——报告对齐心电由 CSFM 代表。
- **偏离主线（10 项）**：Amazon Halo：通用科技公司进入可穿戴，三年后退出（Amazon，2020-08-27）——设备已停产，未涉及模型；AMIE：会问诊的对话 Agent（谷歌，2024-01-11）——临床问诊 Agent，不读可穿戴数据；HealthBench：262 名医生写的健康对话评测（OpenAI，2025-05-13）——通用健康对话评测，不涉及生理数据；MIRA：医疗时序预测基础模型（微软，2025-06-09）——ICU/EHR 时序，非可穿戴；MAI-DxO：模拟医生小组的诊断编排器（微软，2025-06-27）——基于病例的诊断编排，不涉及可穿戴；Organ-Agents：多 LLM Agent 模拟器官系统（天津大学 等，2025-08-20）——ICU 病人数据上的 LLM 模拟，不涉及可穿戴；让 LLM 做声音与运动传感器的晚融合（苹果，2025-09-12）——任务是活动识别而非健康，只是语言接口线的旁证；Amazon Health AI：读病历、约诊、续方的 Agent（Amazon，2026-01-21）——基于病历与诊所服务，不读可穿戴数据；“杭好梦”：已规模部署的睡眠健康专家 Agent（浙江大学，2026-02-09）——医院睡眠专科 Agent，不以可穿戴数据为主；HealthFlux：全模态的人体健康世界模型（斯坦福大学，2026-09-21）——UK Biobank 病历、化验与影像，不含可穿戴信号。

## 3.4 来源索引的范围与方法

“全部来源”= 年谱条目（含每条的补充来源）+ 第 6 节的未上年谱条目。第 6 节包含：公司检索中没有上年谱的全部条目（每条附原因与检索备注）、学术检索中人工挑选的“推荐”与“观察名单”里没有上年谱的条目、补漏候选的低置信项。

学术检索另有约 1,147 项由规则自动判为“仅列表”的论文，没有逐篇列出。检索方法：arXiv 站内摘要检索 34 组查询（每组最多 600 条，按提交时间倒序）；Semantic Scholar 与 OpenAlex 上起点论文 arXiv 2312.05409 的全部施引文献（155 + 103），以及 LSM、PaPaGei、SensorLM、PHIA、WBM、NormWear 的施引文献；Semantic Scholar 批量关键词检索 30 组（2019–2026，只保留标题同时含“模态词 + 方法词”的条目）；Hugging Face 模型库关键词检索 17 组（15 个模型，多为已收条目的权重发布）；OpenReview 关键词检索 14 组（只保留已录用或已发表的条目）。会议/期刊补扫另有 531 项“仅列表”的论文没有逐篇列出，覆盖 KDD/CHI/IMWUT 2024–2026、ML4H 2024–2025、CHIL 2024–2026、NeurIPS 2025 与 ICLR 2026 主会及 workshop、Nature Medicine / npj Digital Medicine / Nature Communications 2025–2026、medRxiv/bioRxiv 2025–2026。方法：PMLR 论文集全量目录（CHIL、ML4H 共 264 篇）按标题过滤后人工过目；KDD 官网录用列表；OpenReview 检索 77 个检索词（只保留已录用或已发表的条目，剔除投稿中、撤稿与拒稿）；OpenAlex 按来源检索。即便如此，ACM DL 与 bioRxiv/medRxiv 也没有全量逐篇浏览，仍可能有标题不含关键词的工作遗漏。

## 4. 存疑、未上页面与需要说明的条目

| 内容 | 处理 | 原因 |
|---|---|---|
| 苹果高血压提醒与 ICLR 2024 论文的关系 | 页面写“同一队列、同一自监督范式”，注明官方未点名论文 | 官方验证 PDF 只写“在 AHMS 无标签数据上自监督训练的深度网络”，未引用论文；网上有二手说法称是 ICLR 模型，未采信 |
| 苹果 AI 健康教练（传闻代号等） | 未上页面 | 仅有媒体报道（如 9to5Mac 2026-02-05 称计划收缩），无官方来源 |
| Meta Muse 接入 Apple Health | 未上页面 | 无法在 Meta 一手页面确认 |
| Oura “Large Physiology Models” 招聘 | 未上页面 | 招聘信息不能说明成果 |
| Oura AHA 2025 心血管基础模型海报 | 第五版移出年谱，列入“全部来源” | Oura 官方页面只列出海报题目，摘要全文未能打开，支撑不足 |
| Oura 2026-06 PPG 研究博客（高血压算法等） | 未上页面（可选补充） | 一手来源已核实，但与“基础模型”关系不明，为控制条目数暂未收录 |
| WHOOP Foundation AI | 第五版移出年谱，列入“全部来源”；公司卡只作一句说明 | 证据为官方招聘页（Ashby）与 CEO 访谈；访谈只读了节目简介，未逐字核对；LinkedIn 上 Foundation AI 副总裁的帖子按活动 ID 推算为 2026-01-07，未用作链接 |
| 华为 WATCH 6 发布日 | 写“2026-09（据发布会报道）” | 官方产品页无日期；日期来自新浪、IT之家报道 |
| 华为基础模型 | 未上页面 | 未找到可核实的华为可穿戴生理基础模型论文 |
| OPPO Watch X3 中文产品页 | 未使用 | 链接 404；改用 OPPO 新闻稿与英文发布稿 |
| AnyPPG 的单位 | 标为北京大学 | 有搜索摘要称其为 OPPO 工作；arXiv 作者单位只有北大，不采信 |
| DNA-PPG | 第五版移出年谱，列入“全部来源” | 与已收 PPG 模型思路重复 |
| SensorWM 的 “2.28M person-weeks” | 页面写“超过 220 万人周” | arXiv 摘要为 “over 2.2 million”；博客数值略有不同，取保守值 |
| PWM（Fullive-AI × 北京大学，arXiv 2608.15309） | 第五版移出年谱，列入“全部来源” | 作者单位与摘要已核对；世界模型一支由 SensorWM、ECG 世界模型等代表，本条支撑不足 |
| PPG-Bench（Mannas AI，arXiv 2610.13435） | 上页面 | 第二版已核对；另一篇 PPG 评测（arXiv 2610.33788）未核对，未收录 |
| Chronos / TimesFM / MIRA | 只保留 TimesFM（作为基线参照）；Chronos、MIRA 第五版移出 | 非生理专用；Chronos 仍在 Aether 条目中作为基线提及 |
| TimesFM 开源状态 | 标为“论文” | 摘要未提权重开放，不在页面声称开源 |
| Delphi-2M | 上页面（世界模型纲，学术参照） | 对象是病历事件而非可穿戴信号，页面已注明 |
| 苹果 bioFAME、跨模态表征、CPEP、EMBridge、语音基础模型迁移、LLM 后期融合等 14 篇 | 第四版上页面；第五版只保留 bioFAME、EMBridge、Device Passport、PPG 混合建模、心血管模拟等进入脉络的几篇，其余移入“全部来源” | 深读核对了 arXiv v1 日期、作者单位与摘要数字；补齐苹果 2020–2026 年的方法线，也修正了“苹果动力学停在 2022 年”的说法（2023 年心血管模拟推断、2025 年 PPG 混合建模） |
| OPPO AI 健康管家的发布日期 | 写“2025-07（WAIC 2025）” | OPPO 官方新闻稿未提及该功能；以新华网 2025-07-29 报道为主链接，只写到月 |
| 华为 BP 随访智能体、vivo / 荣耀的健康大模型功能 | 未上页面 | 只有媒体报道，未找到一手页面 |
| Polar、Garmin 健康功能 | 未上年谱（Garmin Active Intelligence 第五版移出），列入第 6 节 | 未见与基础模型或 LLM 相关的一手材料；Withings AI 连接器第四版已上页面 |
| iRhythm 后续模型 | 只收 2019 Nature Medicine 论文；第三代 Zio AI（2026）列入第 6 节 | 公司称训练于大量 ECG，但未公开为基础模型 |
| 苹果 Sleep Score、AirPods 心率 | 未上页面 | 官方未说明使用基础模型 |
| MOMENT、FemWear、CardioState-JEPA、BCG 基础模型等 | 未上年谱，列入第 6 节与页面“全部来源” | 一手来源存在，但与已收条目思路重复，为控制密度未收；MOMENT 在 PPG-Bench 条目中作为基线提及；Inertia-1 第四版上页面、第五版移出 |
| 苹果高血压提醒“第一个以自监督基础模型为特征的获许可功能” | 页面写“编者所见首例” | 未做穷尽检索，不作绝对断言；FDA 510(k) K250507（2025-09-11）已核实 |
| 并行关系的时间跨度 | 校验脚本对相隔超过约 14 个月的“并行”报警；第五版删掉了跨度超过 200 天的原有“并行” | 防止把不同时期的工作误标为“同期” |

## 5. 条目索引（由 data/entries.json 自动生成）

每条列出：日期口径、机构、主链接、补充链接、与前作的关系。核实方式见第 1 节。


### 前奏 · 2019–2023.11 · 单任务落地，几处先声

- **单导联动态心电的心律失常分类** `p-hannun2019` — 生理信号基础模型 · 论文 · iRhythm × 斯坦福 · Nature Medicine 2019-01  
  原题：Cardiologist-level arrhythmia detection and classification in ambulatory electrocardiograms using a deep neural network  
  主链接：<https://doi.org/10.1038/s41591-018-0268-3>  
  改变：确立了“一个任务、一套标注、一个模型”的范式。它的成功也暴露了瓶颈：每个新任务都需要昂贵的专家标注。
- **华为心脏研究：手环/手表 PPG 房颤筛查** `huawei-heart` — 生理信号基础模型 · 论文 · 华为（与解放军总医院等合作） · JACC 在线 2019-09-02（刊期 2019-11）  
  原题：Mobile Photoplethysmographic Technology to Detect Atrial Fibrillation (Huawei Heart Study)  
  主链接：<https://doi.org/10.1016/j.jacc.2019.08.019>；PubMed：<https://pubmed.ncbi.nlm.nih.gov/31487545/>  
  改变：与 Apple Heart Study 同年发表，说明中国厂商同样有人群规模的远程研究能力。华为后来把“研究 App + 医院合作”做成长期平台，这是它最主要的数据资产（编者解读）。
- **Apple Heart and Movement Study 启动** `p-ahms2019` — 生理参数基础模型 · 研究队列/数据集 · 苹果（与布莱根妇女医院、美国心脏协会合作） · 研究启动 2019-09  
  原题：Apple Heart and Movement Study（Apple Research App 三项研究之一）  
  主链接：<https://www.apple.com/newsroom/2019/09/apple-announces-three-groundbreaking-health-studies/>  
  改变：它本身不是模型，但后来苹果的 PPG/ECG、加速度和行为基础模型都在这个队列上训练。先有长期、知情同意的数据，才有后面的基础模型。
- **谷歌收购 Fitbit：买下数据入口** `fitbit-acq` — 生理参数基础模型 · 宣布/收购/在建 · 谷歌 · 宣布 2019-11-01；完成 2021-01-14  
  原题：Google to acquire Fitbit（2021-01-14 完成）  
  主链接：<https://blog.google/products/hardware/agreement-with-fitbit/>；2021-01-14 完成收购：<https://blog.google/products/devices-services/fitbit-acquisition/>  
  改变：它本身不是模型。但谷歌博客写明，LSM 的数据来自佩戴 Fitbit Sense 2 或 Pixel Watch 2 并同意用于研发的用户，SensorFM 覆盖 20 多款 Fitbit 与 Pixel Watch 设备；Fitbit App 也成了健康教练的落地入口。谷歌的数据资产靠收购获得，苹果的靠自建研究队列，路径不同（编者解读）。
- **Apple Heart Study：手表房颤提醒** `p-ahs2019` — 生理信号基础模型 · 论文 · 苹果（与斯坦福合作） · NEJM 2019-11  
  原题：Large-Scale Assessment of a Smartwatch to Identify Atrial Fibrillation (Apple Heart Study)  
  主链接：<https://doi.org/10.1056/NEJMoa1901183>  
  关系：并行「华为心脏研究：手环/手表 PPG 房颤筛查」— 同年、同一问题：消费级 PPG 的人群级房颤筛查  
  改变：证明了消费级手表 PPG 可以在人群规模上做健康筛查，也说明苹果已经具备开展大型远程研究的能力，这是后来预训练数据的来源。
- **CLOCS：跨时间、导联与病人的心电对比学习** `clocs` — 生理信号基础模型 · 论文 · 牛津大学 · arXiv 2020-05；ICML 2021  
  原题：CLOCS: Contrastive Learning of Cardiac Signals Across Space, Time, and Patients  
  主链接：<https://arxiv.org/abs/2005.13249>  
  改变：较早把“同一个病人”当作对比学习的正样本来源，并指出学到的表征天然带有病人特异性，可用来度量病人相似度。后来“以人为锚”的思路在这里已有雏形（编者归类）。
- **被试感知的生物信号对比学习** `p-cheng2021` — 生理信号基础模型 · 论文 · 苹果 · arXiv 2020-06-30（2007.04871）  
  原题：Subject-Aware Contrastive Learning for Biosignals  
  主链接：<https://machinelearning.apple.com/research/subject-aware-contrastive-learning>  
  改变：苹果内部较早地把“被试”作为对比学习的组织单位。ICLR 2024 把它反转并放大：在大规模数据上，同一参与者的两段信号互为正样本。
- **胰岛素–血糖动力学：机理模型 + 序列模型** `p-miller2020` — 生理世界模型 · 论文 · 苹果 · MLHC 2020（苹果页面 2020-08）  
  原题：Learning Insulin-Glucose Dynamics in the Wild  
  主链接：<https://machinelearning.apple.com/research/learning-insulin-glucose-dynamics-in-the-wild>  
  改变：早期的“生理世界模型”思路：不是纯黑箱预测，而是让学习去调节一个有结构的动力学系统。论文发现约束更少的 LSTM 反而给不出可靠、合理的长时预测。
- **用心率监督加速度：自由生活数据的自监督** `p-spathis2021` — 生理信号基础模型 · 论文 · 剑桥大学 · arXiv 2020-11；ACM CHIL 2021  
  原题：Self-supervised transfer learning of physiological representations from free-living wearable data  
  主链接：<https://arxiv.org/abs/2011.12121>  
  改变：把“生理耦合关系本身就是监督”这一想法带进可穿戴领域，也是苹果 ICLR 2024 论文引用的自由生活自监督先例。
- **70 万人日加速度的自监督预训练** `oxford-ssl` — 生理信号基础模型 · 开源模型/数据 · 牛津大学 · arXiv 2022-06-06；npj Digital Medicine 2024-04  
  原题：Self-supervised learning for human activity recognition using 700,000 person-days of wearable data  
  主链接：<https://doi.org/10.1038/s41746-024-01062-3>；arXiv 2206.02909：<https://arxiv.org/abs/2206.02909>  
  改变：在加速度上较早独立证明“大规模无标签 → 跨数据集、跨设备泛化”（预印本 2022-06，早于苹果 ICLR 2024），与苹果的 PPG/ECG 工作是并行的两条腿。2026 年同一团队的 Sensori 把目标从识别动作推进到全表型疾病风险（编者解读）。
- **运动心率响应的个体化建模** `p-nazaret2022` — 生理世界模型 · 论文 · 苹果 · NeurIPS 2022 TS4H workshop  
  原题：Modeling Heart Rate Response to Exercise with Wearable Data  
  主链接：<https://machinelearning.apple.com/research/modeling-heart-rate>  
  关系：继承「胰岛素–血糖动力学：机理模型 + 序列模型」— 同一作者线（Andrew C. Miller），从血糖动力学转到运动心率动力学  
  改变：和胰岛素–血糖工作一脉相承：建模的是“输入→生理反应”的个体动力学，而不是静态分类。这正是后来以行为为动作的世界模型所需要的形态。
- **BIOT：把异构生物信号变成统一“句子”** `biot` — 生理信号基础模型 · 开源模型/数据 · UIUC · arXiv 2023-05（附代码与预训练模型）  
  原题：BIOT: Cross-data Biosignal Learning in the Wild  
  主链接：<https://arxiv.org/abs/2305.10351>；GitHub：<https://github.com/ycq091044/BIOT>  
  改变：给出“先统一分词，再跨数据集预训练”的配方。EEG 大模型沿着这条路走下去；它要解决的通道异构问题，后来在可穿戴设备的跨布局迁移中再次出现（编者解读）。
- **LLM 是少样本健康学习者** `google-fewshot` — Agent · 论文 · 谷歌 · arXiv 2023-05  
  原题：Large Language Models are Few-Shot Health Learners  
  主链接：<https://arxiv.org/abs/2305.15525>  
  改变：最早把“让语言模型直接读传感器数值”作为研究问题提出，是谷歌“语言 × 可穿戴”研究线的起点。半年后的 Health-LLM（McDuff 同为作者）把它系统化（编者解读）。
- **心血管模拟器 + 机器学习：从脉搏波反推生理参数** `apple-hybrid-cv` — 生理世界模型 · 论文 · 苹果 · arXiv 2023-07-26（SBI）；NeurIPS 2023 两个研讨会  
  原题：Simulation-based Inference for Cardiovascular Models / Hybrid Model Learning for Cardiovascular Biomarkers Inference  
  主链接：<https://arxiv.org/abs/2307.13918>；Apple ML Research：SBI：<https://machinelearning.apple.com/research/simulation-based-inference>；Apple ML Research：Hybrid Model Learning：<https://machinelearning.apple.com/research/hybrid-model-learning>；OpenReview：Hybrid Model Learning（NeurIPS 2023 DGM4H）：<https://openreview.net/forum?id=RP12BvHTnt>  
  关系：继承「胰岛素–血糖动力学：机理模型 + 序列模型」— 同为机理模型与学习结合；Andrew C. Miller 是两篇共同作者（编者解读）  
  改变：苹果 2023 年后的“机理 + 学习”线由此开始：不靠大规模标签，而是用生理模拟器提供监督与可解释的参数。这条线延续到 2025 年的 PPG 混合建模和 2026 年的 PPG 光学组织推断，说明苹果并非在 2022 年后完全停止动力学/机理方向的公开工作。
- **bioFAME：在频域做掩码预训练，任意模态组合可用** `biofame` — 生理信号基础模型 · 论文 · 苹果 · arXiv 2023-09-12；扩展版为 ICLR 2024 TS4H 研讨会论文  
  原题：Frequency-Aware Masked Autoencoders for Multimodal Pretraining on Biosignals (bioFAME)  
  主链接：<https://arxiv.org/abs/2309.05927>；Apple ML Research：<https://machinelearning.apple.com/research/frequency-aware-masked-autoencoders>；GitHub：apple/ml-famae：<https://github.com/apple/ml-famae>  
  关系：并行「BIOT：把异构生物信号变成统一“句子”」— 同年都在解决异构通道、任意模态组合的跨数据集预训练（编者解读）  
  改变：和起点论文几乎同期，苹果另一组把问题定义为“架构能否不挑模态、不挑长度”。预训练数据是公开的 SleepEDF，不是 AHMS 大规模数据；它和 2024 年的跨模态研究构成苹果“多模态生物信号架构”这一支。
- **WHOOP Coach：GPT-4 驱动的教练** `p-whoopcoach` — Agent · 产品 · WHOOP · 产品上线 2023-09-26  
  原题：WHOOP Coach Powered by OpenAI（GPT-4）  
  主链接：<https://www.whoop.com/us/en/press-center/whoop-unveils-the-new-whoop-coach-powered-by-openai/>  
  改变：Agent 线实际上比基础模型线更早出现。但此时的 LLM 只读汇总指标，背后没有生理基础模型；这个缺口到 2025–2026 年才由谷歌（SensorFM 接入 Agent）等开始补上，WHOOP 自己则到 2026 年才组建基础模型团队（编者解读）。
- **TimesFM：通用时序预测基础模型** `p-timesfm` — 生理世界模型 · 论文 · 谷歌 · arXiv 2023-10  
  原题：A decoder-only foundation model for time-series forecasting (TimesFM)  
  主链接：<https://arxiv.org/abs/2310.10688>  
  改变：它不是生理模型，却是生理世界模型的对照基线：2026 年谷歌的 SensorWM 明确与 TimesFM 比较，并报告更好的生理轨迹预测。

### 起点 · 2023.12–2024.05 · 不靠标签，以人为锚

- **可穿戴生物信号基础模型的大规模训练** `apple-iclr24` **【起点】** — 生理信号基础模型 · 论文 · 苹果 · arXiv 2023-12-08；ICLR 2024 录用（OpenReview 2024-01-16）  
  原题：Large-scale Training of Foundation Models for Wearable Biosignals  
  主链接：<https://openreview.net/forum?id=pC3WJHf51j>；arXiv：<https://arxiv.org/abs/2312.05409>；ICLR 会议录：<https://proceedings.iclr.cc/paper_files/paper/2024/hash/0d99a8c048befb6dd6e17d7684adacac-Abstract-Conference.html>；Apple ML Research：<https://machinelearning.apple.com/research/large-scale-training>  
  关系：继承「被试感知的生物信号对比学习」— 以被试为单位组织对比学习，在大数据上改为参与者级正样本；继承「用心率监督加速度：自由生活数据的自监督」— 沿用自由生活数据的自监督思路，规模提高两个数量级；奠基「Apple Heart and Movement Study 启动」— 约 14 万名 AHMS 参与者的手表 PPG/ECG 是预训练数据；转向「单导联动态心电的心律失常分类」— 从单任务监督转向无标签预训练；呼应「70 万人日加速度的自监督预训练」— 同一判断先在加速度上成立：大规模无标签预训练可跨数据集泛化；并行「bioFAME：在频域做掩码预训练，任意模态组合可用」— 同一时期、同一公司：一个在大规模私有数据上做对比学习，一个在公开数据上做多模态掩码架构；继承「CLOCS：跨时间、导联与病人的心电对比学习」— 同样用“同一个人”的不同片段构造正样本，从临床心电搬到消费级手表（编者解读）  
  改变：作者称这是首个用消费级可穿戴设备大规模采集的 PPG/ECG 训练的基础模型。它把问题从“为每个病训练一个分类器”改成“先学一个人的通用生理表征”，嵌入中已编码人口学与健康状态。
- **Health-LLM：让 LLM 直接读可穿戴指标** `health-llm` — Agent · 论文 · MIT（含谷歌作者） · arXiv 2024-01  
  原题：Health-LLM: Large Language Models for Health Prediction via Wearable Sensor Data  
  主链接：<https://arxiv.org/abs/2401.06866>  
  关系：继承「LLM 是少样本健康学习者」— 同一问题的系统化评测（McDuff 同为作者）  
  改变：把“指标 + 上下文 → 语言模型推断”作为研究问题提出，并发现健康知识上下文的作用最大。这是谷歌 PH-LLM 之前的学术铺垫。
- **LaBraM：EEG 的通用大模型** `labram` — 生理信号基础模型 · 论文 · 上海交通大学 · ICLR 2024 录用（OpenReview 2024-01-16）；arXiv 2024-05  
  原题：Large Brain Model for Learning Generic Representations with Tremendous EEG Data in BCI (LaBraM)  
  主链接：<https://arxiv.org/abs/2405.18765>  
  关系：继承「BIOT：把异构生物信号变成统一“句子”」— 同样把多源 EEG 切成通道片段做跨数据集预训练，改用神经分词器与掩码预测（编者解读）  
  改变：说明“通用表征”的思路在脑电这类多通道、异构格式的信号上同样可行，并引入分词与掩码重建这条和对比学习不同的技术路线。
- **三星睡眠呼吸暂停功能：FDA De Novo 授权** `samsung-sleepapnea` — 生理信号基础模型 · 产品 · 三星 · FDA De Novo DEN230041（2024-02）  
  原题：Samsung Health Monitor sleep apnea feature (FDA De Novo DEN230041)  
  主链接：<https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPMN/denovo.cfm?knumber=DEN230041>  
  改变：同类功能的首个监管路径由三星打开，苹果同年 9 月的睡眠呼吸暂停提醒随后获 510(k) 许可。两者都是专门模型，不是基础模型（编者解读）。
- **Meta 腕部 sEMG 的通用神经运动接口** `meta-emg` — 生理信号基础模型 · 开源模型/数据 · Meta · bioRxiv 2024-02-28；Nature 2025-07-23  
  原题：A generic non-invasive neuromotor interface for human-computer interaction  
  主链接：<https://doi.org/10.1038/s41586-025-09255-w>；Meta 博客：<https://www.meta.com/blog/reality-labs-surface-emg-research-nature-publication-ar-glasses-orion/>；代码：<https://github.com/facebookresearch/generic-neuromotor-interface>；bioRxiv 预印本：<https://www.biorxiv.org/content/10.1101/2024.02.23.581779v1>；emg2qwerty / emg2pose 数据集（2024-12）：<https://ai.meta.com/blog/open-sourcing-surface-electromyography-datasets-neurips-2024/>  
  关系：并行「可穿戴生物信号基础模型的大规模训练」— 同期：“足够多的人换来跨人泛化”，但 Meta 用的是数千人的大规模监督，不是自监督  
  改变：这里的生理信号用于“意图”而非健康，但它在 EMG 上证明了同一判断：足够多的人就能换来免校准的通用模型。苹果随后也发表了 EMG 方向的跨模态工作。
- **HeAR：咳嗽与呼吸声的基础模型** `hear` — 生理信号基础模型 · 开源模型/数据 · 谷歌 · arXiv 2024-03；后作为 HAI-DEF 开放模型发布  
  原题：HeAR – Health Acoustic Representations  
  主链接：<https://arxiv.org/abs/2403.02522>；谷歌博客 2024-08：<https://blog.google/innovation-and-ai/technology/health/ai-model-cough-disease-detection/>；HAI-DEF 模型页：<https://developers.google.com/health-ai-developer-foundations/hear>  
  关系：并行「可穿戴生物信号基础模型的大规模训练」— 同期在声学模态上的大规模自监督  
  改变：把“自监督 + 线性探针”的配方复制到声音这一模态。生理基础模型的边界从光学和电信号扩展到声学（编者解读）。
- **首个非处方 CGM 获 FDA 许可** `stelo-otc` — 生理参数基础模型 · 宣布/收购/在建 · Dexcom · FDA 新闻稿 2024-03-05  
  原题：FDA Clears First Over-the-Counter Continuous Glucose Monitor (Dexcom Stelo)  
  主链接：<https://www.fda.gov/news-events/press-announcements/fda-clears-first-over-counter-continuous-glucose-monitor>  
  改变：为血糖数据进入消费可穿戴与基础模型打开了数据来源：随后有 Oura × Dexcom、CGM-LSM、GlucoFM（编者解读）。
- **Oura 心血管年龄：PPG 估计的血管年龄** `oura-cvage` — 生理参数基础模型 · 产品 · Oura · 发布 2024-05-10  
  原题：ŌURA Announces Two New Heart Health Features: Cardiovascular Age and Cardio Capacity  
  主链接：<https://ouraring.com/blog/heart-health-at-oura/>  
  关系：转向「可穿戴生物信号基础模型的大规模训练」— 把 PPG 的生理信息直接做成“年龄差”指标（编者解读）  
  改变：“年龄差”作为产品指标在戒指上出现，比 WHOOP Age 早一年；它是 PPG 形态特征的产物，官方未说明使用基础模型（编者解读）。
- **SleepFM：多导睡眠图的多模态基础模型** `sleepfm` — 生理信号基础模型 · 开源模型/数据 · 斯坦福大学 · arXiv 2024-05；扩展版 Nature Medicine 2026-01-06  
  原题：SleepFM: Multi-modal Representation Learning for Sleep Across Brain Activity, ECG and Respiratory Signals  
  主链接：<https://arxiv.org/abs/2405.17766>；Nature Medicine 2026：<https://doi.org/10.1038/s41591-025-04133-4>；GitHub：<https://github.com/rthapa84/sleepfm-codebase>  
  改变：把跨模态对比从两两配对推广到“留一模态”，并把睡眠模型的目标从分期推到疾病预测（编者解读）。

### 第二章 · 2024.06–2025.06 · 扩张：层级、模态、开放与语言

- **PH-LLM：面向睡眠与健身教练的 Gemini 微调** `ph-llm` — Agent · 论文 · 谷歌 · arXiv 2024-06；Nature Medicine 2025-08  
  原题：A personal health large language model for sleep and fitness coaching (PH-LLM)  
  主链接：<https://doi.org/10.1038/s41591-025-03888-0>；arXiv：<https://arxiv.org/abs/2406.06474>；谷歌研究博客：Advancing personal health and wellness insights with AI：<https://research.google/blog/advancing-personal-health-and-wellness-insights-with-ai/>  
  关系：继承「Health-LLM：让 LLM 直接读可穿戴指标」— 从评测转为微调专用模型  
  改变：把“读指标的 LLM”从提示工程推进到领域微调与专家对照评测，并尝试用多模态编码直接接入传感器数据。
- **PHIA：用代码与检索分析个人数据的 Agent** `phia` — Agent · 论文 · 谷歌 · arXiv 2024-06；Nature Communications 2026-01  
  原题：Transforming wearable data into personal health insights using large language model agents (PHIA)  
  主链接：<https://doi.org/10.1038/s41467-025-67922-y>；arXiv：<https://arxiv.org/abs/2406.06464>  
  关系：转向「Health-LLM：让 LLM 直接读可穿戴指标」— 不再把数字塞进提示，而是交给代码工具  
  改变：从“让模型记住怎么读数”转向“让模型写代码去算”，即 Agent 范式。之后的 PHA 把它作为数据科学子智能体。
- **Vitals：夜间个人基线与异常提示** `apple-vitals` — 生理参数基础模型 · 产品 · 苹果 · WWDC 2024 公布（watchOS 11）  
  原题：Vitals app（watchOS 11）  
  主链接：<https://www.apple.com/newsroom/2024/06/watchos-11-brings-powerful-health-and-fitness-insights/>  
  关系：奠基「Apple Heart and Movement Study 启动」— 官方称算法基于 AHMS 真实世界数据开发  
  改变：AHMS 第一次明确支撑参数层的个体基线产品。思路与 ICLR 2024 一致：先知道这个人平常什么样（编者解读）。
- **Oura Advisor：从 Labs 测试到全面上线** `oura-advisor` — Agent · 产品 · Oura · Oura Labs 测试 2024-07；全面上线 2025-03-31  
  原题：Oura Advisor（AI 个人健康助手）  
  主链接：<https://ouraring.com/blog/oura-advisor/>；2024-07 Labs 公告：<https://ouraring.com/blog/made-for-members-july-2024/>  
  改变：戒指厂商的 Agent 路线：先上产品、再积累对话与反馈。后续的女性健康专用模型和收购 Counsel Health 都建立在这个入口上。
- **手表 PPG 高血压风险筛查** `oppo-embc2024` — 生理信号基础模型 · 论文 · OPPO · IEEE EMBC 2024（会议录 2024-07）  
  原题：Continuous Blood Pressure Monitoring and Hypertension Risk Screening Using Smart Watch  
  主链接：<https://doi.org/10.1109/embc53108.2024.10782190>；相关 arXiv（2024-11）：<https://arxiv.org/abs/2411.11863>  
  改变：单任务模型先行落地。OPPO 官方称该研究 2024-07 在 EMBC 发布，风险评估模型 ROC-AUC 超过 0.8，此后成为手表上的高血压风险评估。
- **ECG-FM：开源权重的心电基础模型** `ecg-fm` — 生理信号基础模型 · 开源模型/数据 · 多伦多大学健康网络（UHN） · arXiv 2024-08；JAMIA Open 2025-10  
  原题：ECG-FM: An Open Electrocardiogram Foundation Model  
  主链接：<https://arxiv.org/abs/2408.05178>；JAMIA Open：<https://doi.org/10.1093/jamiaopen/ooaf122>；GitHub：<https://github.com/bowang-lab/ECG-FM>  
  改变：ECG 一侧的开放基线。临床 ECG 的数据量远大于可穿戴，这类模型后来成为“ECG 教 PPG”路线的老师来源（编者解读）。
- **GluFormer：连续血糖的生成式基础模型** `gluformer` — 生理世界模型 · 论文 · 魏茨曼研究所 × NVIDIA · arXiv 2024-08；Nature 2026-01-14  
  原题：A foundation model for continuous glucose monitoring data (GluFormer)  
  主链接：<https://doi.org/10.1038/s41586-025-09925-9>；arXiv：<https://arxiv.org/abs/2408.11876>；NVIDIA Research：<https://research.nvidia.com/labs/par/publication/cgm_foundation_model_nature/>  
  关系：转向「胰岛素–血糖动力学：机理模型 + 序列模型」— 同为血糖动力学，从机理混合模型转为纯生成式预训练  
  改变：参数层（血糖）第一次出现生成式基础模型：用“预测下一个读数”学习血糖动力学。论文称其表征对糖尿病和心血管死亡风险的分层优于 HbA1c。注意它是无动作条件的生成式预训练，干预推演要到 2026 年的 HealthFormer。
- **华为玄玑感知系统** `huawei-trusense` — 生理参数基础模型 · 产品 · 华为 · 发布 2024-08-28  
  原题：华为玄玑感知系统（HUAWEI TruSense System）  
  主链接：<https://www.huawei.com/cn/news/2024/8/wearable-healthandfitness-trusense-system>  
  改变：代表“参数层”的工程路线：先把指标测准、测全，形成稳定的参数底座。华为尚未公开可核实的生理基础模型论文，见研究笔记。
- **睡眠呼吸暂停提醒：加速度 + 30 天汇总** `apple-sleepapnea` — 生理信号基础模型 · 产品 · 苹果 · 发布 2024-09-09（随后获 FDA 许可）  
  原题：Sleep apnea notifications（Breathing Disturbances，Apple Watch）  
  主链接：<https://www.apple.com/newsroom/2024/09/apple-introduces-groundbreaking-health-features/>；验证文件：<https://www.apple.com/health/pdf/sleep-apnea/Sleep_Apnea_Notifications_on_Apple_Watch_September_2024.pdf>；FDA 510(k) K240929：<https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K240929>  
  关系：并行「三星睡眠呼吸暂停功能：FDA De Novo 授权」— 同年先后获 FDA 授权的手表睡眠呼吸暂停功能  
  改变：苹果此时的监管级功能仍是专门模型：单一传感器、单一病种、长窗口汇总。一年后的高血压提醒保留了“30 天汇总 + 提醒”的形态，但把特征提取换成了自监督基础模型（编者对比）。
- **ECGFounder：千万级专家标注心电** `ecgfounder` — 生理信号基础模型 · 开源模型/数据 · 北京大学（训练数据为 Harvard-Emory ECG Database） · arXiv 2024-10；NEJM AI 2025-09  
  原题：An Electrocardiogram Foundation Model Built on over 10 Million Recordings (ECGFounder)  
  主链接：<https://doi.org/10.1056/aix2500913>；arXiv：<https://arxiv.org/abs/2410.04133>；GitHub：<https://github.com/PKUDigitalHealth/ECGFounder>  
  关系：继承「单导联动态心电的心律失常分类」— 同样依赖大规模专家标注，从单任务扩展到 150 类的通用模型  
  改变：与自监督路线不同，它用大规模专家标注训练“有监督的基础模型”，并把单导联（可穿戴形态）当作一等公民。同一北大团队随后做出 ECG 引导的 AnyPPG（编者据代码仓库归属判断）。
- **SensorLLM：运动传感器与 LLM 对齐** `sensorllm` — 生理信号基础模型 · 开源模型/数据 · 新南威尔士大学 · arXiv 2024-10；EMNLP 2025  
  原题：SensorLLM: Aligning Large Language Models with Motion Sensors for Human Activity Recognition  
  主链接：<https://arxiv.org/abs/2410.10624>；GitHub：<https://github.com/zechenli03/SensorLLM>  
  关系：转向「Health-LLM：让 LLM 直接读可穿戴指标」— 从把数值写进提示词，改为先对齐表征  
  改变：“传感器—语言对齐”的早期学术版本，比谷歌 SensorLM 早约 8 个月；两者都用自动生成的文字描述代替人工标注（编者对比）。
- **LSM：分钟级可穿戴数据的尺度律** `lsm` — 生理参数基础模型 · 论文 · 谷歌 · arXiv 2024-10；ICLR 2025  
  原题：Scaling Wearable Foundation Models (LSM)  
  主链接：<https://research.google/blog/scaling-wearable-foundation-models/>；arXiv：<https://arxiv.org/abs/2410.13638>；ICLR 会议录：<https://proceedings.iclr.cc/paper_files/paper/2025/hash/94b25992757a549470c8f8dfe73d8df6-Abstract-Conference.html>  
  关系：转向「可穿戴生物信号基础模型的大规模训练」— 从原始波形转到分钟级指标，从对比学习转到掩码重建；呼应「TimesFM：通用时序预测基础模型」— 同为时序基础模型；LSM 是掩码重建的表征模型，不是 TimesFM 式零样本预测的特化；奠基「谷歌收购 Fitbit：买下数据入口」— 预训练数据来自经同意的 Fitbit / Pixel Watch 用户  
  改变：两个转向：建模对象从原始波形上移到分钟级参数；目标从判别式对比改为掩码重建，模型因此能补全缺失、外推短程。掩码重建不含动作或干预，它为后来的预测任务铺路，但本身不是世界模型（编者解读）。
- **PULSE：教多模态大模型读心电图图像** `pulse-ecg` — Agent · 开源模型/数据 · 俄亥俄州立大学 等 · arXiv 2024-10；npj Digital Medicine 2026  
  原题：Teach Multimodal LLMs to Comprehend Electrocardiographic Images (PULSE)  
  主链接：<https://arxiv.org/abs/2410.19008>  
  关系：分岔「ECGFounder：千万级专家标注心电」— 同为心电通用模型，PULSE 走图像 + 语言  
  改变：语言接口的另一入口：不从原始波形，而从“图像化的心电”接入大模型（编者解读）。
- **PaPaGei：首个开源 PPG 基础模型** `papagei` — 生理信号基础模型 · 开源模型/数据 · 诺基亚贝尔实验室（与达特茅斯学院合作） · arXiv 2024-10；ICLR 2025  
  原题：PaPaGei: Open Foundation Models for Optical Physiological Signals  
  主链接：<https://arxiv.org/abs/2410.20542>  
  关系：分岔「可穿戴生物信号基础模型的大规模训练」— 同一问题，从闭源私有数据转向开源与公开数据；并行「ECG-FM：开源权重的心电基础模型」— 同期开放权重的心血管信号模型（PPG 与 ECG）  
  改变：把苹果闭源的范式变成社区可用的公共基础设施，也让“PPG 形态学先验”成为后续工作的参照。
- **Oura × Dexcom：把血糖接进戒指** `oura-dexcom` — 生理参数基础模型 · 宣布/收购/在建 · Oura（与 Dexcom 合作，Dexcom 投资 7,500 万美元） · 宣布 2024-11-19；随后 Oura App 上线 Stelo 血糖集成（美国）  
  原题：Dexcom and ŌURA Announce Strategic Partnership  
  主链接：<https://investors.dexcom.com/news/news-details/2024/Dexcom-and-URA-Announce-Strategic-Partnership/default.aspx>；Oura 代谢健康博客：<https://ouraring.com/blog/introducing-metabolic-health/>  
  关系：奠基「首个非处方 CGM 获 FDA 许可」— 非处方 CGM 提供数据来源  
  改变：设备公司用合作补齐自己没有的传感模态，数据资产从“单设备”变成“多源拼合”。WHOOP（化验）、Ultrahuman（血检 + CGM）后来走了同一条路（编者解读）。
- **RelCon：相对对比学习的运动基础模型** `apple-relcon` — 生理信号基础模型 · 论文 · 苹果（与 UIUC 合作） · arXiv 2024-11；ICLR 2025  
  原题：RelCon: Relative Contrastive Learning for a Motion Foundation Model for Wearable Data  
  主链接：<https://machinelearning.apple.com/research/relative-contrastive-learning>；arXiv：<https://arxiv.org/abs/2411.18822>  
  关系：继承「可穿戴生物信号基础模型的大规模训练」— 同样以个体为锚，正负样本改为相对相似度  
  改变：把“以人为锚”的对比学习改为“相对”的对比学习；同一思路随后被 Pulse-PPG 用到 PPG 上。
- **NormWear：多传感器通用可穿戴模型** `normwear` — 生理信号基础模型 · 开源模型/数据 · 加州大学圣迭戈分校 · arXiv 2024-12（附代码）  
  原题：Toward Foundation Model for Multivariate Wearable Sensing of Physiological Signals (NormWear)  
  主链接：<https://arxiv.org/abs/2412.09758>  
  关系：并行「PaPaGei：首个开源 PPG 基础模型」— 同为开放的学术模型，目标从单模态 PPG 扩到多传感器  
  改变：把问题从“某个信号”改成“任意传感器组合”。同一团队 2026 年在此基础上做世界模型 NormWear-2。
- **CGM-LSM：160 万条血糖记录的自回归模型** `cgm-lsm` — 生理世界模型 · 论文 · 约翰斯·霍普金斯 × Welldoc · arXiv 2024-12  
  原题：A Large Sensor Foundation Model Pretrained on Continuous Glucose Monitor Data for Diabetes Management (CGM-LSM)  
  主链接：<https://arxiv.org/abs/2412.09727>  
  关系：并行「GluFormer：连续血糖的生成式基础模型」— 同期的 CGM 生成式预训练  
  改变：与 GluFormer 同期，把“预测下一个 token”用到血糖上。生成式时序模型成为代谢方向世界模型的第一步（编者解读）。
- **把 PPG 表征蒸馏进加速度** `apple-accel` — 生理信号基础模型 · 论文 · 苹果 · arXiv 2024-12  
  原题：Wearable Accelerometer Foundation Models for Health via Knowledge Distillation  
  主链接：<https://machinelearning.apple.com/research/wearable-accelerometer-foundation-models>；arXiv：<https://arxiv.org/abs/2412.11276>  
  关系：继承「可穿戴生物信号基础模型的大规模训练」— 以 ICLR 2024 的 PPG 编码器为教师；继承「用心率监督加速度：自由生活数据的自监督」— 同为生理模态监督加速度，改为表征蒸馏  
  改变：基础模型第一次被用来“迁移传感器”：贵模态在训练期当老师，便宜模态在推理期单独工作。论文报告心率、HRV 预测比直接在加速度上训练的模型好 23%–49%。
- **Dexcom Stelo：生成式 AI 周报** `dexcom-genai` — Agent · 产品 · Dexcom · 发布 2024-12-17  
  原题：Dexcom Launches the First Generative AI Platform in Glucose Biosensing  
  主链接：<https://investors.dexcom.com/news/news-details/2024/Dexcom-Launches-the-First-Generative-AI-Platform-in-Glucose-Biosensing/default.aspx>  
  关系：奠基「首个非处方 CGM 获 FDA 许可」— 非处方 CGM 提供数据来源；并行「Oura × Dexcom：把血糖接进戒指」— 同期，Dexcom 一边与 Oura 互通数据，一边在 Stelo 上做生成式 AI  
  改变：生物传感器厂商把 LLM 当作参数数据的解释层，这和 WHOOP、Oura 的路线一致，只是对象换成了血糖。
- **Pulse-PPG：只用野外数据训练的开源 PPG 模型** `pulse-ppg` — 生理信号基础模型 · 开源模型/数据 · 孟菲斯大学 × UIUC · arXiv 2025-02；IMWUT 2025-09  
  原题：Pulse-PPG: An Open-Source Field-Trained PPG Foundation Model for Wearable Applications across Lab and Field Settings  
  主链接：<https://doi.org/10.1145/3749494>；arXiv：<https://arxiv.org/abs/2502.01108>  
  关系：继承「RelCon：相对对比学习的运动基础模型」— 直接沿用 RelCon 的相对对比学习（Maxwell A. Xu 为两篇共同作者）；分岔「PaPaGei：首个开源 PPG 基础模型」— 同为开源，数据来源从临床转向野外  
  改变：反直觉的结论：在许多任务上，野外数据预训练优于临床数据预训练。数据的“真实变异性”被当作一种资源。
- **可穿戴活动识别的尺度律（DeepMind）** `har-scaling` — 生理信号基础模型 · 论文 · 谷歌（Google DeepMind） · arXiv 2025-02  
  原题：Scaling laws in wearable human activity recognition  
  主链接：<https://arxiv.org/abs/2502.03364>  
  关系：检验「可穿戴生物信号基础模型的大规模训练」— 从尺度律角度检验“以人为锚”：人的多样性比单人数据量更重要（编者解读）  
  改变：“人的多样性比单人数据量更重要”，从尺度律角度支持了“以人为锚”的直觉（编者解读）。
- **Pixel Watch 3：脉搏丢失检测** `google-lop` — 生理信号基础模型 · 产品 · 谷歌 · Nature 2025-02-26；Pixel Watch 3 功能  
  原题：Automated loss of pulse detection on a consumer smartwatch（Pixel Watch 3）  
  主链接：<https://doi.org/10.1038/s41586-025-08810-9>；谷歌博客 2025-03-20：<https://research.google/blog/loss-of-pulse-detection-on-the-google-pixel-watch-3/>；FDA 许可（谷歌 2025-02-26）：<https://blog.google/feed/pixel-watch-3-loss-of-pulse-detection-fda/>；谷歌博客 2024-08-13：Pixel Watch 3 introduces Loss of Pulse Detection：<https://blog.google/products-and-platforms/devices/pixel/pixel-watch-3-loss-of-pulse-detection/>  
  改变：单任务路线的高峰：数据靠巧妙的实验设计而非大规模预训练获得，强调可审计的多级门控与极低误报。今天的监管级与安全功能，大多仍由这类专门模型完成（编者解读）。
- **可穿戴 + 常规血检预测胰岛素抵抗** `ir-wearme` — 生理参数基础模型 · 论文 · 谷歌 · arXiv 2025-04；Nature 2026-03-16  
  原题：Insulin resistance prediction from wearables and routine blood biomarkers (WEAR-ME)  
  主链接：<https://doi.org/10.1038/s41586-026-10179-2>；arXiv：<https://arxiv.org/abs/2505.03784>；谷歌博客：<https://research.google/blog/insulin-resistance-prediction-from-wearables-and-routine-blood-biomarkers/>  
  关系：并行「LSM：分钟级可穿戴数据的尺度律」— 同属谷歌的参数层，从表征学习走向具体代谢终点；奠基「谷歌收购 Fitbit：买下数据入口」— Fitbit 设备与用户提供研究数据  
  改变：参数层开始和化验数据融合，问题从“可穿戴能测什么”转为“可穿戴加少量化验能补全什么”。谷歌称这项工作是 Fitbit 健康教练的研究基础之一。
- **WHOOP Age 与血压洞察** `whoop-5` — 生理参数基础模型 · 产品 · WHOOP · 发布 2025-05-08  
  原题：WHOOP 5.0 / MG：Healthspan（WHOOP Age）与血压洞察  
  主链接：<https://www.whoop.com/us/en/press-center/whoop-unveils-5.0-MG/>；FDA 2026-06-17 致函：对修改后的血压洞察不再执法：<https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/whoop-inc-709755-06172026>；FDA 警告信 2025-07-14（Blood Pressure Insights）：<https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/whoop-inc-709755-07142025>；MedTech Dive 2026-06-23：FDA 撤回对 WHOOP 的警告信：<https://www.medtechdive.com/news/fda-drops-whoop-warning-letter-over-blood-pressure-feature/823652/>  
  关系：继承「Oura 心血管年龄：PPG 估计的血管年龄」— “年龄差”类指标从单项（心血管）扩展到综合（编者解读）  
  改变：参数层的产品形态从“单项分数”走向“生理年龄”这类综合指标。2026 年苹果在健康 App 中推出 Health Age，谷歌在研究中提出可教练健康年龄（CHA），OPPO 发表手表心脏年龄（编者对比）。
- **LSM-2：把缺失当作信息** `lsm2` — 生理参数基础模型 · 论文 · 谷歌 · arXiv 2025-06；博客 2025-07-22  
  原题：LSM-2: Learning from Incomplete Wearable Sensor Data  
  主链接：<https://research.google/blog/lsm-2-learning-from-incomplete-wearable-sensor-data/>；arXiv：<https://arxiv.org/abs/2506.05321>  
  关系：继承「LSM：分钟级可穿戴数据的尺度律」— LSM-1 的直接后继  
  改变：缺失从“噪声”变成“模型的一部分”。模型能在传感器失效时保持性能，也能生成缺失段，这为之后的 SensorFM 和世界模型打下基础。
- **Workout Buddy：运动中的生成式语音教练** `apple-workout-buddy` — Agent · 产品 · 苹果 · WWDC 2025 公布（watchOS 26）  
  原题：Workout Buddy with Apple Intelligence  
  主链接：<https://www.apple.com/newsroom/2025/06/watchos-26-delivers-more-personalized-ways-to-stay-active-and-connected/>  
  改变：苹果第一个生成式“教练”只做运动场景、只讲事实型数据，体现它在 Agent 上的克制：嵌入系统、窄场景、隐私优先（编者解读）。
- **SensorLM：传感器与语言对齐** `sensorlm` — 生理参数基础模型 · 论文 · 谷歌 · arXiv 2025-06；博客 2025-07-28  
  原题：SensorLM: Learning the Language of Wearable Sensors  
  主链接：<https://research.google/blog/sensorlm-learning-the-language-of-wearable-sensors/>；arXiv：<https://arxiv.org/abs/2506.09108>  
  关系：继承「LSM：分钟级可穿戴数据的尺度律」— 同一数据与团队，加入语言对齐；分岔「PH-LLM：面向睡眠与健身教练的 Gemini 微调」— 从“LLM 读数字”转为“传感器与文本共享表征”  
  改变：参数层表征有了语言接口，支持零样本识别、检索和传感器描述，为 Agent 直接“看”数据而不只是读摘要铺路。
- **三星就寝建议：睡眠压力 × 昼夜节律** `samsung-oneui8` — 生理世界模型 · 产品 · 三星 · 公布 2025-06-16（One UI 8 Watch，测试计划）  
  原题：One UI 8 Watch：Bedtime Guidance、Vascular Load、Antioxidant Index  
  主链接：<https://news.samsung.com/global/new-features-on-one-ui-8-watch-help-users-build-healthier-habits>  
  关系：呼应「胰岛素–血糖动力学：机理模型 + 序列模型」— 机理式的个体前瞻推演进入产品：睡眠压力 × 昼夜节律（编者解读）  
  改变：产品中的“小型世界模型”：用经典的睡眠压力与昼夜节律思路做前瞻推演，而不是只回顾昨晚。它是机理式的，不是大规模学习式的。
- **CSFM：170 万人的心脏多模态模型** `csfm` — 生理信号基础模型 · 论文 · 牛津大学 · arXiv 2025-06  
  原题：Sensing Cardiac Health Across Scenarios and Devices: A Multi-Modal Foundation Model Pretrained on Heterogeneous Data from 1.7 Million Individuals (CSFM)  
  主链接：<https://arxiv.org/abs/2507.01045>  
  关系：并行「把 PPG 表征蒸馏进加速度」— 同为跨模态脚手架：苹果用 PPG 教加速度，CSFM 在临床大数据上让 ECG、PPG、文字共享表征  
  改变：“跨模态脚手架”的临床大数据版本：ECG、PPG 与文字在同一个模型里共享表征（编者解读）。
- **WBM：行为数据的基础模型** `wbm` — 生理参数基础模型 · 论文 · 苹果 · arXiv 2025-06-30；ICML 2025  
  原题：Beyond Sensor Data: Foundation Models of Behavioral Data from Wearables Improve Health Predictions (WBM)  
  主链接：<https://machinelearning.apple.com/research/beyond-sensor>；arXiv：<https://arxiv.org/abs/2507.00191>  
  关系：继承「可穿戴生物信号基础模型的大规模训练」— 同一队列；与 PPG 基础模型组合使用  
  改变：苹果在自家框架里回答了“表征该建在哪一层”：行为模型擅长睡眠等行为驱动任务，与原始 PPG 模型结合效果更好。两层互补，不必二选一。

### 第三章 · 2025.07–2025.12 · 分层与落地

- **OPPO AI 健康管家与健康档案** `oppo-healthagent` — Agent · 产品 · OPPO · WAIC 2025 发布（新华网 2025-07-29 报道）  
  原题：OPPO AI 健康档案与 AI 健康管家  
  主链接：<https://www.news.cn/tech/20250729/dd108772aaa44e7988ff06742e1c3cd7/c.html>  
  关系：继承「手表 PPG 高血压风险筛查」— 同一公司从单项 PPG 功能走到 Agent 层（编者解读）  
  改变：OPPO 的 Agent 层与 PPG 基础模型研究（心脏年龄、HiPPT）同年推进，但公开材料尚未说明两者如何衔接（编者解读）。
- **三星收购 Xealth：通往医院的管道** `samsung-xealth` — Agent · 宣布/收购/在建 · 三星 · 宣布 2025-07-08  
  原题：Samsung Electronics Acquires Xealth  
  主链接：<https://news.samsung.com/global/samsung-electronics-acquires-xealth-bridging-the-gap-between-wellness-and-medical-care>  
  改变：设备公司开始买下“通往临床的管道”。一年后三星 Health Assistant 写明将通过 Xealth 连接临床照护；Oura 收购 Counsel Health 是同一方向（编者解读）。
- **PHA：数据科学家、领域专家与教练的多智能体** `pha` — Agent · 论文 · 谷歌 · arXiv 2025-08；Nature 2026-10-21  
  原题：The anatomy of a personal health agent (PHA)  
  主链接：<https://doi.org/10.1038/s41586-026-11161-8>；arXiv：<https://arxiv.org/abs/2508.20148>；谷歌研究博客：The anatomy of a personal health agent：<https://research.google/blog/the-anatomy-of-a-personal-health-agent/>  
  关系：继承「PHIA：用代码与检索分析个人数据的 Agent」— PHIA 成为数据科学子智能体的前身；继承「PH-LLM：面向睡眠与健身教练的 Gemini 微调」— 领域知识与教练能力  
  改变：Agent 的结构从“一个会聊天的模型”变成“分工明确的团队”。2026 年谷歌把 SensorFM 定位为它的数据接地工具。
- **高血压提醒：自监督 PPG 特征上线** `apple-htn` — 生理信号基础模型 · 产品 · 苹果 · 发布 2025-09-09；验证文件 2025-09  
  原题：Hypertension Notifications（Apple Watch Series 11 / watchOS 26）  
  主链接：<https://www.apple.com/health/pdf/Hypertension_Notifications_Validation_Paper_September_2025.pdf>；Apple 新闻稿：<https://www.apple.com/newsroom/2025/09/apple-debuts-apple-watch-series-11-featuring-groundbreaking-health-insights/>；FDA 510(k) K250507（2025-09-11 许可）：<https://www.accessdata.fda.gov/cdrh_docs/pdf25/K250507.pdf>  
  关系：落地「可穿戴生物信号基础模型的大规模训练」— 同一队列、同一自监督范式的 PPG 特征提取器（官方未点名论文）；继承「睡眠呼吸暂停提醒：加速度 + 30 天汇总」— 沿用“长窗口汇总 + 风险提醒”的产品形态，特征提取换成自监督 PPG 模型（编者解读）  
  改变：这是该领域最清晰的“基础模型 → 获许可产品”路径之一：表征一次学好，具体病种只需线性头和少量标注。官方文件没有点名 ICLR 2024 论文，但数据来源与自监督范式一致。
- **Delphi-2M：疾病自然史的生成式模型** `delphi` — 生理世界模型 · 论文 · EMBL-EBI × DKFZ 等 · Nature 2025-09-17  
  原题：Learning the natural history of human disease with generative transformers (Delphi-2M)  
  主链接：<https://doi.org/10.1038/s41586-025-09529-3>  
  关系：呼应「GluFormer：连续血糖的生成式基础模型」— 同为生成式健康轨迹，对象不同（病历事件 vs 血糖）  
  改变：它建模的是病历事件而不是可穿戴信号，但给出了“健康轨迹生成模型”的范本。生理世界模型可以理解为把这种生成能力下沉到日常生理尺度。
- **Meta Neural Band：sEMG 腕带量产** `meta-neuralband` — 生理信号基础模型 · 产品 · Meta · 发布 2025-09-17（美国 2025-09-30 上市）  
  原题：Meta Ray-Ban Display with Meta Neural Band  
  主链接：<https://about.fb.com/news/2025/09/meta-ray-ban-display-ai-glasses-emg-wristband/>  
  关系：落地「Meta 腕部 sEMG 的通用神经运动接口」— 跨人泛化的 sEMG 解码进入量产腕带  
  改变：生理信号模型最干净的一次“研究 → 产品”：预印本 2024-02 公开，Nature 论文 2025-07 发表，约两个月后随量产腕带上市（产品研发显然并行进行）。用途是交互而不是健康（编者解读）。
- **WHOOP Advanced Labs：化验接入教练** `whoop-labs` — Agent · 产品 · WHOOP · 上线 2025-09-30（美国）；2025-11-12 化验单上传向全体会员开放  
  原题：WHOOP Advanced Labs  
  主链接：<https://www.whoop.com/us/en/press-center/whoop-launches-clinician-reviewed-advanced-labs/>；化验单上传 2025-11-12：<https://www.whoop.com/us/en/press-center/whoop-launches-advanced-labs-uploads-us/>  
  关系：继承「WHOOP Coach：GPT-4 驱动的教练」— 教练开始读化验结果  
  改变：Agent 的输入从可穿戴指标扩展到血液化验。“化验 + 连续监测”随后成为谷歌、Oura、Ultrahuman、微软等健康 Agent 的共同配置（编者解读）。
- **三星手表左心室收缩功能障碍（LVSD）检测** `samsung-lvsd` — 生理信号基础模型 · 产品 · 三星 · 三星新闻稿 2025-10（韩国 MFDS 批准）  
  原题：Samsung's LVSD detection on Galaxy Watch (with Medical AI)  
  主链接：<https://news.samsung.com/global/samsungs-breakthrough-wearable-technologies-driven-by-innovation-and-collaboration>  
  关系：继承「单导联动态心电的心律失常分类」— 把医院里的专门心电 AI 搬到手表单导联上  
  改变：监管级功能的另一种来源：不是自研基础模型，而是把医院里的临床 AI 模型搬到手表上（编者解读）。
- **OpenTSLM：把时序作为原生模态接入 LLM（开源）** `opentslm` — 生理信号基础模型 · 开源模型/数据 · 斯坦福大学（斯坦福、ETH 等合作） · arXiv 2025-10-02  
  原题：OpenTSLM: Time-Series Language Models for Reasoning over Multivariate Medical Text- and Time-Series Data  
  主链接：<https://arxiv.org/abs/2510.02410>；GitHub：<https://github.com/OpenTSLM/OpenTSLM>  
  关系：继承「SensorLLM：运动传感器与 LLM 对齐」— 同为传感器对齐 LLM，扩展到 ECG、睡眠和思维链推理；并行「SensorLM：传感器与语言对齐」— 同期的传感器—语言模型，一个开源、一个闭源  
  改变：“传感器 + 语言”这条线出现了开源、可复现的时序语言模型，作为 SensorLM 一类闭源工作的开放对照。
- **苹果 PpgAge：手腕 PPG 的衰老时钟** `apple-ppgage` — 生理信号基础模型 · 论文 · 苹果 · Nature Communications 2025-10-20  
  原题：A wearable-based aging clock associates with disease and behavior (PpgAge)  
  主链接：<https://www.nature.com/articles/s41467-025-64275-4>；DOI 10.1038/s41467-025-64275-4：<https://doi.org/10.1038/s41467-025-64275-4>  
  关系：继承「可穿戴生物信号基础模型的大规模训练」— 同一队列的手腕 PPG 与同一团队成员；呼应「Oura 心血管年龄：PPG 估计的血管年龄」— 同为从 PPG 推算的“年龄”指标  
  改变：健康年龄一线的学术源头之一：同一队列、同一 PPG 信号，从“表征”走到“年龄差”这一可解释指标。论文作者与起点论文团队有重叠（编者解读）。
- **Fitbit 个人健康教练公开预览** `fitbit-coach` — Agent · 产品 · 谷歌 · 公开预览 2025-10-28 起（美国 Android）  
  原题：Fitbit personal health coach（Gemini）公开预览  
  主链接：<https://blog.google/products-and-platforms/devices/fitbit/personal-health-coach-public-preview/>；2026-04 扩展到 37 国：<https://blog.google/products-and-platforms/devices/fitbit/fitbit-personal-health-coach-expansion/>；谷歌研究博客：How we are building the personal health coach：<https://research.google/blog/how-we-are-building-the-personal-health-coach/>；谷歌博客：Pixel Watch 4（宣布教练预览）：<https://blog.google/products-and-platforms/devices/pixel/pixel-watch-4/>  
  关系：落地「PHA：数据科学家、领域专家与教练的多智能体」— 多智能体研究进入消费产品  
  改变：谷歌把 PH-LLM、PHIA、PHA 这条研究线做成了产品。研究与产品之间有公开、明确的承接关系，这在各家中少见。
- **HiMAE：多分辨率表征，手表端亚毫秒推理** `himae` — 生理信号基础模型 · 论文 · 三星 · arXiv 2025-10；ICLR 2026  
  原题：HiMAE: Hierarchical Masked Autoencoders Discover Resolution-Specific Structure in Wearable Time Series  
  主链接：<https://research.samsung.com/research-papers/HiMAE-Hierarchical-Masked-Autoencoders-Discover-Resolution-Specific-Structure-in-Wearable-Time-Series>；arXiv：<https://arxiv.org/abs/2510.25785>；三星新闻 2026-08：<https://news.samsung.com/global/from-biosignals-to-health-insights-samsung-researchs-work-on-health-foundation-models>；三星新闻稿 2026-08-14（健康基础模型）：<https://samsungmobilepress.com/articles/samsung-research-biosignals-health-insights-foundation-models>；三星研究博客：The Resolution Hypothesis：<https://research.samsung.com/blog/The-Resolution-Hypothesis-Discovering-how-Time-Scale-Maps-to-Health-Outcomes>  
  关系：分岔「LSM：分钟级可穿戴数据的尺度律」— 把“建在哪一层”细化为“用哪个时间分辨率”  
  改变：三星的切入点是“小而准、能在端上跑”。它把“表征该用哪一层”从信号/参数之争，细化为时间分辨率的问题。
- **AnyPPG：ECG 引导的 PPG 与全表型筛查** `anyppg` — 生理信号基础模型 · 开源模型/数据 · 北京大学 · arXiv 2025-11；KDD 2026  
  原题：AnyPPG: An ECG-Guided PPG Foundation Model Trained on Over 100,000 Hours of Recordings for Holistic Health Profiling  
  主链接：<https://doi.org/10.1145/3770855.3818911>；arXiv：<https://arxiv.org/abs/2511.01747>；代码与权重：<https://github.com/PKUDigitalHealth/AnyPPG>  
  关系：继承「ECGFounder：千万级专家标注心电」— 同一北大团队，用 ECG 侧能力引导 PPG 表征  
  改变：把问题从“PPG 能测哪些心血管指标”扩大到“PPG 携带多少全身健康信息”：307 种表型 AUC≥0.70，其中 230 种是非循环系统疾病。
- **PPG 混合建模：用血流动力学模拟估计心输出量** `apple-ppg-hybrid` — 生理世界模型 · 论文 · 苹果 · ML4H 2025 · arXiv 2025-11-18  
  原题：Hybrid Modeling of Photoplethysmography for Non-Invasive Monitoring of Cardiovascular Parameters  
  主链接：<https://arxiv.org/abs/2511.14452>；Apple ML Research：<https://machinelearning.apple.com/research/photoplethysmography>；相关：Inferring Optical Tissue Properties from PPG using Hybrid Amortized Inference（arXiv 2025-10-02）：<https://arxiv.org/abs/2510.02073>  
  关系：继承「心血管模拟器 + 机器学习：从脉搏波反推生理参数」— 同一团队（Wehenkel、Behrmann、Miller、Sapiro）的心血管混合建模，从模拟研究走到 PPG；并行「AnyPPG：ECG 引导的 PPG 与全表型筛查」— 同一时期另一种让 PPG“知道更多”的做法：AnyPPG 用 ECG 当老师，本文用模拟器当老师（编者解读）  
  改变：苹果“机理 + 学习”线进入 PPG：模拟器提供标签，真实数据只用来跨越 PPG 与动脉压之间的差距。这条线还包括 2025-10 的 PPG 光学组织参数推断（PPGen + 混合摊销推断）。

### 第四章 · 2026.01–2026.11 · 动力学、闭环与自我检验

- **FDA 修订一般健康指南：无创可穿戴的血压估计可归入一般健康** `fda-wellness-2026` — 生理参数基础模型 · 宣布/收购/在建 · FDA（美国食药监局） · FDA 修订指南 2026-01-06  
  原题：FDA：General Wellness: Policy for Low Risk Devices（2026 修订版）  
  主链接：<https://www.fda.gov/media/90652/download>；Covington 解读：<https://www.cov.com/en/news-and-insights/insights/2026/01/fda-issues-revised-guidance-on-general-wellness-products>；FDA 对 WHOOP 的不执法函（2026-06-17）：<https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/whoop-inc-709755-06172026>  
  关系：转向「WHOOP Age 与血压洞察」— 2025 年对 WHOOP 血压洞察的警告信在 2026 年转为不执法；并行「高血压提醒：自监督 PPG 特征上线」— 苹果走 FDA 许可路径，与一般健康路径并存  
  改变：这是参数层产品形态的外部条件。2026 年 Google Health Guardian 的“血压趋势”、Oura 的 Blood Pressure Signals、WHOOP 的血压洞察都选择了“趋势 + 一般健康”的表述（三者与指南的因果关系为编者解读）。
- **ChatGPT Health：通用助手接入 Apple Health 与病历** `chatgpt-health` — Agent · 产品 · OpenAI · 发布 2026-01-07；2026-07 面向美国成人开放  
  原题：Introducing ChatGPT Health  
  主链接：<https://openai.com/index/introducing-chatgpt-health/>；OpenAI 2026-07-23：Health in ChatGPT（美国全面推送）：<https://openai.com/index/health-in-chatgpt/>  
  关系：转向「WHOOP Coach：GPT-4 驱动的教练」— 2023 年 OpenAI 为 WHOOP 提供模型；2026 年自己做面向用户的健康入口  
  改变：通用大模型公司直接站到了可穿戴 Agent 的位置上。可穿戴厂商的护城河，从“有没有 LLM”变成“有没有生理模型和连续数据”（编者解读）。
- **Claude 接入 Apple Health 与病历** `claude-health` — Agent · 产品 · Anthropic · 发布 2026-01-11（美国，测试版）  
  原题：Claude for Healthcare：personal health data integrations  
  主链接：<https://www.anthropic.com/news/healthcare-life-sciences>；Claude 帮助中心：与 iOS 健康数据集成：<https://support.claude.com/en/articles/11869619-use-claude-with-ios-apps>  
  关系：并行「ChatGPT Health：通用助手接入 Apple Health 与病历」— 同一周、同一形态  
  改变：与 ChatGPT Health 相隔四天发布。通用 AI 公司把“个人健康数据入口”做成标准连接器，设备公司的数据开始被别家的 Agent 读取（编者解读）。
- **sleep2vec：九种夜间模态任意子集可用的睡眠基础模型** `sleep2vec` — 生理信号基础模型 · 论文 · 五季医学 × 清华大学（第一单位五季医学，与清华大学、睡眠呼吸障碍北京市重点实验室合作） · arXiv 2026-02-14；ICLR 2026  
  原题：sleep2vec: Unified Cross-Modal Alignment for Heterogeneous Nocturnal Biosignals  
  主链接：<https://arxiv.org/abs/2602.13857>；ICLR 2026 论文集：<https://proceedings.iclr.cc/paper_files/paper/2026/hash/bbbd6d915cb90be21c1254a82d45cedd-Abstract-Conference.html>  
  关系：继承「SleepFM：多导睡眠图的多模态基础模型」— 沿用跨模态对比对齐，并在全部通道组合上直接对比 SleepFM  
  改变：睡眠模型从“固定通道组合”走向“任意子集可用”，直接对应只有心搏和呼吸的低负担设备；同时把“负样本里的混杂因素”显式写进对比目标。
- **Oura 女性健康专用 LLM** `oura-womens` — Agent · 产品 · Oura · Oura Labs 首发（TechCrunch 2026-02-24 报道）；官方博客 2026-04-08  
  原题：Oura：首个自研的女性健康大语言模型（Oura Advisor 内）  
  主链接：<https://ouraring.com/blog/womens-health-ai-model/>；TechCrunch 2026-02-24：<https://techcrunch.com/2026/02/24/oura-launches-a-proprietary-ai-model-focused-on-womens-health/>；Oura 博客 2026-03-02：Designing Trustworthy Health AI：<https://ouraring.com/blog/designing-trustworthy-health-ai/>  
  关系：继承「Oura Advisor：从 Labs 测试到全面上线」— 在 Advisor 中加入专用模型  
  改变：从“调用通用模型”走向“为特定生理人群定制模型”。Agent 层也开始分专科。
- **HEARTS：LLM 在健康时序上的推理基准** `hearts` — Agent · 开源模型/数据 · UCLA（与谷歌研究院合作） · arXiv 2026-02  
  原题：HEARTS: Benchmarking LLM Reasoning on Health Time Series  
  主链接：<https://arxiv.org/abs/2603.06638>  
  关系：检验「Health-LLM：让 LLM 直接读可穿戴指标」— 系统检验 LLM 读生理数据的能力；检验「OpenTSLM：把时序作为原生模态接入 LLM（开源）」— 时序原生 LLM 也在被测之列的路线  
  改变：结论直接：LLM 明显不如专门模型，且多步时间推理薄弱，“只靠扩大模型”不够。这为“Agent 调用基础模型”的架构提供了证据（编者解读）。
- **EMBridge：肌电与姿态的跨模态桥接（ICLR 2026）** `apple-embridge` — 生理信号基础模型 · 论文 · 苹果 · ICLR 2026（苹果页面 2026-03-03）  
  原题：EMBridge: Enhancing Gesture Generalization from EMG Signals through Cross-Modal Representation Learning  
  主链接：<https://openreview.net/forum?id=LqrWNdceum>；Apple ML Research：<https://machinelearning.apple.com/research/embridge>  
  关系：并行「Meta Neural Band：sEMG 腕带量产」— 同一时期肌电腕带进入量产产品，苹果仍停在研究阶段；转向「Meta 腕部 sEMG 的通用神经运动接口」— 肌电从“数千人监督”转向跨模态对齐与零样本手势（编者解读）  
  改变：苹果肌电线从研讨会论文进入主会；“软对比、对齐相对几何”与 RelCon 的相对对比思路相通。
- **微软 Copilot Health** `ms-copilot-health` — Agent · 产品 · 微软 · 发布 2026-03-12（美国，分阶段推出）  
  原题：Introducing Copilot Health  
  主链接：<https://microsoft.ai/news/introducing-copilot-health/>  
  关系：并行「ChatGPT Health：通用助手接入 Apple Health 与病历」— 同类的通用助手健康空间；并行「Claude 接入 Apple Health 与病历」— 同样经 HealthEx、Function 接入病历与化验  
  改变：到 2026 年一季度，通用 AI 公司的健康 Agent 已经长得差不多：读可穿戴、病历、化验三类数据，由医生把关。区别在于有没有自己的设备和生理模型（编者解读）。
- **Fitbit 教练接入病历** `fitbit-2026` — Agent · 产品 · 谷歌 · 发布 2026-03-17（The Check Up）  
  原题：Fitbit personal health coach：链接病历、新睡眠评分与代谢研究  
  主链接：<https://blog.google/products-and-platforms/devices/fitbit/fitbit-personal-health-coach-updates-2026/>  
  关系：继承「Fitbit 个人健康教练公开预览」— 同一产品的下一步；落地「可穿戴 + 常规血检预测胰岛素抵抗」— 官方称该研究支撑教练的代谢洞察  
  改变：Agent 的上下文从“设备数据”扩展到“设备数据 + 临床史”，并开始与医疗服务方合作（Included Health 研究）。
- **SleepJEPA：在潜空间预测整夜睡眠，估计 15 年疾病风险** `sleepjepa` — 生理信号基础模型 · 论文 · 西奈山伊坎医学院 · medRxiv 2026-04-03（v3）  
  原题：SleepJEPA: Learning the latent world of sleep with at-home sleep data to estimate disease risk  
  主链接：<https://doi.org/10.64898/2026.03.20.26348834>  
  关系：转向「SleepFM：多导睡眠图的多模态基础模型」— 同为睡眠多导基础模型；目标从“留一模态”对比换成 JEPA 潜空间预测，论文称各项结局优于 SleepFM  
  改变：预训练目标从对比与重建转向潜空间预测，并且直接以远期疾病风险检验表征（编者解读）。对象是居家多导睡眠而非消费级手表。
- **超越病人不变性：动作条件的心电动力学** `ac-jepa` — 生理世界模型 · 论文 · 米纳斯吉拉斯联邦大学 · arXiv 2026-04（附代码）  
  原题：Beyond Patient Invariance: Learning Cardiac Dynamics via Action-Conditioned JEPAs  
  主链接：<https://arxiv.org/abs/2604.22618>  
  关系：检验「CLOCS：跨时间、导联与病人的心电对比学习」— 直接批评“病人不变性”目标：它会抹掉短暂的病理变化；检验「可穿戴生物信号基础模型的大规模训练」— 同一批评适用于参与者级正样本（编者解读）；并行「SleepJEPA：在潜空间预测整夜睡眠，估计 15 年疾病风险」— 同月出现的 JEPA 潜空间预测：一个用于居家睡眠的疾病风险，一个用来反思“以人为锚”的不变性  
  改变：对“以人为锚”的直接反思：不变性擅长刻画稳定的个体特征，却会把变化本身当作噪声。这为“从表征转向动力学”给出了一个技术理由（编者解读）。
- **HealthFormer：生成式多模态生理轨迹与干预模拟** `healthformer` — 生理世界模型 · 论文 · 魏茨曼研究所 × NVIDIA（含 Pheno.AI、哥本哈根大学、MBZUAI） · arXiv 2026-04  
  原题：Simulating clinical interventions with a generative multimodal model of human physiology (HealthFormer)  
  主链接：<https://arxiv.org/abs/2604.27899>  
  关系：继承「GluFormer：连续血糖的生成式基础模型」— 同一团队，从单一 CGM 扩展到多领域联合生成  
  改变：从 GluFormer 的单一参数，扩展到多系统的联合生成，并明确提出“在电脑里模拟干预”。世界模型纲在这里有了清晰的形态。
- **xMAE：利用 ECG→PPG 时序关系的预训练** `xmae` — 生理信号基础模型 · 开源模型/数据 · 三星 · arXiv 2026-05；ICML 2026  
  原题：Physiology-Aware Masked Cross-Modal Reconstruction for Biosignal Representation Learning (xMAE)  
  主链接：<https://research.samsung.com/blog/Respecting-Underlying-Biosignal-Structure-Cross-Biosignal-Pretraining-for-Wearable-Health-AI>；arXiv：<https://arxiv.org/abs/2605.00973>；代码：<https://github.com/hzhou3/xMAE>；三星新闻稿 2026-08-14（健康基础模型）：<https://samsungmobilepress.com/articles/samsung-research-biosignals-health-insights-foundation-models>；三星新闻稿 2026-08-14：From Biosignals to Health Insights：<https://news.samsung.com/global/from-biosignals-to-health-insights-samsung-researchs-work-on-health-foundation-models>  
  关系：继承「AnyPPG：ECG 引导的 PPG 与全表型筛查」— 同为 ECG 当老师，加入方向性的时序约束  
  改变：跨模态脚手架开始尊重生理机制：不是简单对齐，而是学“谁先谁后”。论文报告在 19 项任务中的 15 项优于单模态与多模态基线。
- **Fitbit 应用升级为 Google Health；Gemini 教练结束预览** `google-health-app` — Agent · 产品 · 谷歌 · 发布 2026-05-07；Coach 正式版 2026-05-19 起推送  
  原题：Google Health app、Google Health Coach（正式版）与 Fitbit Air  
  主链接：<https://blog.google/products-and-platforms/products/google-health/google-health-fitbit/>；Google Health Coach 正式版：<https://blog.google/products-and-platforms/products/google-health/google-health-coach/>；雅培新闻稿 2026-08-11：Lingo 血糖数据进入 Google Health Coach：<https://abbott.mediaroom.com/2026-08-11-Abbott-and-Google-launch-first-of-its-kind-partnership-to-transform-everyday-health-through-glucose-insights-and-AI>  
  关系：继承「Fitbit 个人健康教练公开预览」— 2025-10 公开预览转为全球正式版；继承「Fitbit 教练接入病历」— 3 月的病历链接与睡眠更新并入新应用；落地「PHA：数据科学家、领域专家与教练的多智能体」— PHA 多智能体研究的产品化延续（编者解读，博客未点名 PHA）  
  改变：谷歌的 Agent 线从“Fitbit 里的实验功能”变成整个健康入口的主界面：品牌从 Fitbit 换成 Google Health，硬件反过来按“教练需要什么数据”来设计（博客原话：designed with the Google Health Coach in mind）。
- **WHOOP AI：记忆、主动关怀与医生** `whoop-2026` — Agent · 产品 · WHOOP · 发布 2026-05-08  
  原题：WHOOP：医生在线问诊、病历同步与 AI 记忆、主动关怀  
  主链接：<https://www.whoop.com/us/en/press-center/whoop-expands-health-platform-with-on-demand-clinician-access-and-new-ai-features/>；WHOOP：How WHOOP AI guidance turns your health data into personalized coaching：<https://www.whoop.com/us/en/thelocker/new-ai-guidance-from-whoop/>；WHOOP：2026 What’s New：<https://www.whoop.com/us/en/thelocker/2026-whats-new/>  
  关系：继承「WHOOP Coach：GPT-4 驱动的教练」— WHOOP Coach 的演进；奠基「WHOOP Advanced Labs：化验接入教练」— 化验与临床审核流程为医生问诊打下基础  
  改变：WHOOP 的 Agent 从“被动答疑”变成“有记忆、会主动、能转诊”，最早做 LLM 教练的公司开始把 Agent 接到医疗服务上。
- **WavesFM：多日原始波形的层级模型** `wavesfm` — 生理信号基础模型 · 论文 · 谷歌 · arXiv 2026-05  
  原题：WavesFM: Hierarchical Representation Learning for Longitudinal Wearable Sensor Waveforms  
  主链接：<https://arxiv.org/abs/2605.09173>  
  关系：转向「LSM-2：把缺失当作信息」— 从分钟级特征回到原始波形  
  改变：谷歌从分钟级指标回到原始波形，用层级结构保留多日动态，补上 LSM 系列放弃的波形细节。苹果从波形走向行为（WBM），谷歌从指标回到波形，两家在“两层兼得”上会合（编者解读）。
- **NormWear-2：信号级的生理世界模型** `normwear-wm` — 生理世界模型 · 论文 · 加州大学圣迭戈分校 · arXiv 2026-05  
  原题：Toward World Modeling of Physiological Signals with Chaos-Theoretic Balancing and Latent Dynamics (NormWear-2)  
  主链接：<https://arxiv.org/abs/2605.15465>  
  关系：继承「NormWear：多传感器通用可穿戴模型」— 同一团队，从表征模型到世界模型  
  改变：世界模型的思路落到原始信号层，而不只是分钟、天级参数，并且显式建模干预变量。
- **ECG-WM：给药后心电的世界模型** `ecg-wm` — 生理世界模型 · 论文 · 牛津大学（与清华大学、南方科技大学合作） · arXiv 2026-05  
  原题：ECG-WM: A Physiology-Informed ECG World Model for Clinical Intervention Simulation  
  主链接：<https://arxiv.org/abs/2605.17580>  
  关系：呼应「胰岛素–血糖动力学：机理模型 + 序列模型」— 同为机理先验约束学习到的动力学；无引用承接（编者解读）；并行「超越病人不变性：动作条件的心电动力学」— 同期的动作条件心电动力学  
  改变：世界模型落到单一器官信号上：动作是药物，状态是心电，机理先验用来抑制生成幻觉。思路上接近苹果 2020 年“机理模型 + 学习”的混合路线（编者解读）。
- **心电模型怎样随规模变好？** `ecg-scaling` — 生理信号基础模型 · 论文 · 乌普萨拉大学 · arXiv 2026-05  
  原题：How Do Electrocardiogram Models Scale?  
  主链接：<https://arxiv.org/abs/2605.17276>  
  关系：检验「LSM：分钟级可穿戴数据的尺度律」— 把“规模越大越好”放到临床心电上系统检验，并拆开架构与范式  
  改变：尺度律在心电上被系统检验，答案不是“越大越好”，而是范式与归纳偏置决定收益（编者解读）。
- **Health Radar：Oura 把夜间 PPG 做成血压与呼吸趋势** `oura-health-radar` — 生理参数基础模型 · 产品 · Oura · 发布 2026-05-28（随 Oura Ring 5）；2026-10 扩展到 30 多个市场  
  原题：Oura Health Radar：Blood Pressure Signals 与 Nighttime Breathing  
  主链接：<https://ouraring.com/blog/introducing-health-radar/>；WIRED：Oura Ring 5：<https://www.wired.com/story/oura-ring-5/>  
  关系：继承「Oura Advisor：从 Labs 测试到全面上线」— Advisor 成为提示后的承接入口；并行「FDA 修订一般健康指南：无创可穿戴的血压估计可归入一般健康」— 同样采用一般健康表述（编者解读）  
  改变：Oura 的路线从“读数 + Advisor 对话”推进到“背景监测 → 提示 → Advisor → 真人医生”的闭环；5 月的 Counsel 试点在 11 月变成收购。
- **GlucoFM：双流 CGM 基础模型，分开慢趋势与短时波动** `glucofm` — 生理世界模型 · 论文 · 谷歌（与新南威尔士大学合作） · arXiv 2026-05-29；谷歌研究博客 2026-08-26  
  原题：GlucoFM: A Dual-Stream Foundation Model for Continuous Glucose Monitoring  
  主链接：<https://arxiv.org/abs/2605.30865>；谷歌研究博客 2026-08-26：<https://research.google/blog/glucofm-foundation-model-for-continuous-glucose-monitoring/>；前作：CGM-JEPA（arXiv 2026-05-01）：<https://arxiv.org/abs/2605.00933>；arXiv 2605.30865：<https://arxiv.org/abs/2605.30865>  
  关系：转向「GluFormer：连续血糖的生成式基础模型」— 从自回归 token 预测转为双流潜空间预测，并直接对比  
  改变：血糖模型从“预测下一个读数”（GluFormer）转向 JEPA 式潜空间预测加显式的多时间尺度结构；同一团队 2026-05-01 先发表了 CGM-JEPA。
- **OpenMHC：十年 MyHeart Counts 数据开放** `openmhc` — 生理参数基础模型 · 开源模型/数据 · 斯坦福大学（与帝国理工等合作） · arXiv 2026-06（数据向合格研究者开放，代码与权重开源）  
  原题：OpenMHC: Accelerating the Science of Wearable Foundation Models  
  主链接：<https://arxiv.org/abs/2607.16235>；项目页：<https://myheartcounts.stanford.edu/openmhc>  
  关系：分岔「LSM：分钟级可穿戴数据的尺度律」— 把分钟级可穿戴基础模型的研究带到公开数据上；呼应「Apple Heart and Movement Study 启动」— 公开的长期心脏研究队列，对照苹果的私有队列（编者解读）  
  改变：参数层第一次有了接近企业规模的公开数据与可复现基线，直接回应“私有数据垄断”的问题（编者解读）。
- **Device Passport：跨设备布局迁移** `apple-passport` — 生理信号基础模型 · 论文 · 苹果 · ICML 2026（苹果页面 2026-07）  
  原题：Device Passport: Enabling Spatio-Temporal Pretrained Models to Generalize Across Input Layouts  
  主链接：<https://machinelearning.apple.com/research/device-passport-input-layouts>；arXiv 2607.00249：<https://arxiv.org/abs/2607.00249>  
  关系：继承「把 PPG 表征蒸馏进加速度」— 同一苹果可穿戴模型线；继承「BIOT：把异构生物信号变成统一“句子”」— 通道异构问题的设备版：同一模型适配不同传感器布局（编者解读）；继承「bioFAME：在频域做掩码预训练，任意模态组合可用」— 苹果内部延续：任意模态组合的生理信号预训练 → 跨设备、跨通道的表征  
  改变：“基础模型能否跨设备”从数据问题变成架构问题。对拥有多代硬件的厂商来说，这决定了一次预训练能用多久。
- **StepFM：只用步数的基础模型** `stepfm` — 生理参数基础模型 · 论文 · 香港理工 × 北航 × 中国科大 · arXiv 2026-07  
  原题：Physical activities enable scalable foundation modelling for broad-spectrum health prediction (StepFM)  
  主链接：<https://arxiv.org/abs/2607.06954>  
  关系：分岔「LSM：分钟级可穿戴数据的尺度律」— 分钟级路线的极简版本：只保留步数  
  改变：“层级上移”的极端情形：连心率都不用。它检验的是基础模型的收益来自信号细节，还是来自规模与时序结构（编者解读）。
- **SensorFM：500 万人、万亿分钟** `sensorfm` — 生理参数基础模型 · 论文 · 谷歌 · 谷歌博客 2026-07-09  
  原题：SensorFM: Towards a general intelligence and interface for wearable health data  
  主链接：<https://research.google/blog/sensorfm-towards-a-general-intelligence-and-interface-for-wearable-health-data/>；arXiv 2605.22759：<https://arxiv.org/abs/2605.22759>  
  关系：继承「LSM-2：把缺失当作信息」— 沿用 AIM，规模扩大约两个数量级；接入「PHA：数据科学家、领域专家与教练的多智能体」— 官方把 SensorFM 定位为个人健康 Agent 的数据接地工具  
  改变：参数纲规模最大的一次扩展：最大模型下游分类平均提升 9%（AUC），回归提升 21%。谷歌同时把它定位为个人健康 Agent 的接地工具，参数模型由此成为 Agent 的组件。
- **三星 Health Assistant 测试版** `samsung-ha` — Agent · 产品 · 三星 · 测试版 2026-07-21（美国）  
  原题：Samsung Health Assistant（Beta）  
  主链接：<https://www.samsungmobilepress.com/articles/health-assistant-beta-ai-powered-wellness>  
  关系：奠基「三星收购 Xealth：通往医院的管道」— 官方称将通过 Xealth 连接临床照护  
  改变：三星的研究（HiMAE、xMAE）和产品（Health Assistant）同年推进，但公开材料中尚未说明二者的直接接口。
- **手表 PPG 心脏年龄：ECG 引导的预训练** `oppo-heartage` — 生理信号基础模型 · 论文 · OPPO（与北京大学合作） · arXiv 2026-08  
  原题：Smartwatch Photoplethysmography-Derived Heart Age via ECG-Guided Cross-Modal Pretraining as a Digital Biomarker of Vascular Aging  
  主链接：<https://arxiv.org/abs/2608.01620>  
  关系：转向「手表 PPG 高血压风险筛查」— 从专门模型转向跨模态预训练；继承「AnyPPG：ECG 引导的 PPG 与全表型筛查」— 同一北大团队参与，ECG 引导 PPG；继承「可穿戴生物信号基础模型的大规模训练」— 以被试为锚的自监督；并行「苹果 PpgAge：手腕 PPG 的衰老时钟」— 同为从手表 PPG 推算可追踪的“年龄”  
  改变：OPPO 从单任务风险评估走向基础模型式预训练，并把输出定义为“心脏年龄”这类可长期追踪的生物标志物。
- **Health Guardian：谷歌把健康基础模型做成月度趋势功能** `google-health-guardian` — 生理参数基础模型 · 产品 · 谷歌 · Pixel Watch 5 发布 2026-08-12；2026-10-12 扩展到 Fitbit Air / Edge  
  原题：Health Guardian：血压趋势、胰岛素抵抗趋势、睡眠呼吸质量趋势（Pixel Watch 5）  
  主链接：<https://blog.google/products-and-platforms/devices/pixel/pixel-watch-5/>；Google Health 帮助中心：Health Guardian：<https://support.google.com/googlehealth/answer/18538590?hl=en>；2026-10-12 扩展到 Fitbit Air/Edge：<https://blog.google/products-and-platforms/products/google-health/fitbit-google-health-updates/>；谷歌博客：Health Guardian features on Pixel and Fitbit：<https://blog.google/products-and-platforms/products/google-health/pixel-watch-health-guardian/>  
  关系：落地「SensorFM：500 万人、万亿分钟」— 官方称基于健康基础模型；未点名具体是哪个模型，对应关系为编者解读；落地「可穿戴 + 常规血检预测胰岛素抵抗」— 胰岛素抵抗研究线进入产品；继承「Pixel Watch 3：脉搏丢失检测」— 同属 Health Guardian 安全功能系列；落地「FDA 修订一般健康指南：无创可穿戴的血压估计可归入一般健康」— 同上  
  改变：谷歌第一次在产品文案里直接说功能“建在健康基础模型上”：参数层表征（LSM → SensorFM）和胰岛素抵抗研究从论文走进月度报告；和苹果高血压通知相比，谷歌选择“趋势 + 一般健康”而不是“通知 + 医疗器械许可”。
- **Sensori：一天的腕部运动 → 全表型疾病** `sensori` — 生理信号基础模型 · 论文 · 牛津大学 · arXiv 2026-08  
  原题：Learning Human Health and Diseases from 24-hour Wrist Movement (Sensori)  
  主链接：<https://arxiv.org/abs/2608.29494>  
  关系：继承「70 万人日加速度的自监督预训练」— 同一机构的加速度预训练路线，从活动识别转向疾病预测  
  改变：牛津大数据研究所从 2024 年的活动识别预训练，走到“一天的运动 → 全表型疾病风险”，加速度模型的目标从识别动作变成刻画健康（编者解读）。
- **华为 WATCH 6：AI 健康洞察** `huawei-watch6` — Agent · 产品 · 华为 · 全球发布 2026-09-02（慕尼黑）；中国发布 2026-09-07（据报道）  
  原题：HUAWEI WATCH 6：腕上小艺与 AI 健康洞察  
  主链接：<https://consumer.huawei.com/cn/wearables/watch-6/>  
  关系：继承「华为玄玑感知系统」— 在感知系统之上加入大模型解释层  
  改变：中国厂商的 Agent 形态：大模型助手加大规模健康研究，指标层与解释层在同一块表上合一。底层生理模型尚无公开论文可核。
- **SleepFM-2：200 万小时睡眠迁移到腕部** `sleepfm2` — 生理信号基础模型 · 论文 · 斯坦福大学 · arXiv 2026-09  
  原题：Learning transferable human physiology from two million hours of sleep with SleepFM-2  
  主链接：<https://arxiv.org/abs/2609.06849>  
  关系：继承「SleepFM：多导睡眠图的多模态基础模型」— 同一斯坦福团队，规模扩大约 20 倍并迁移到可穿戴  
  改变：睡眠模型反过来服务可穿戴：临床信号上学到的表征迁移到腕部 PPG 和加速度，是“贵模态教便宜模态”的另一种形态（编者解读）。
- **苹果健康 App：以 Apple Intelligence 为核心** `apple-health-app` — Agent · 产品 · 苹果 · 发布 2026-09-09；iOS 27.3 测试版 2026-11-03  
  原题：Redesigned Health app with Apple Intelligence（Insights、For You、Longevity / Health Age、Readiness）  
  主链接：<https://www.apple.com/newsroom/2026/09/apple-advances-health-and-fitness-capabilities-using-apple-intelligence/>；2026-11-03 语言扩展（含简体中文）：<https://www.apple.com/newsroom/2026/11/redesigned-health-app-expands-language-support/>  
  关系：继承「Workout Buddy：运动中的生成式语音教练」— 从运动场景的生成式提示扩展到整个健康 App；继承「Vitals：夜间个人基线与异常提示」— 夜间个人基线与 AHMS 开发的评分逻辑延续到 Readiness；呼应「WHOOP Age 与血压洞察」— “生理年龄”类综合指标进入两家产品  
  改变：苹果没有推出独立的 AI 教练，而是把 Apple Intelligence 放进健康 App 的核心。它的 Agent 形态是“嵌在系统里的解释与建议”。
- **Withings AI 连接器：把体重、血压数据开放给通用助手** `withings-mcp` — Agent · 产品 · Withings · 2026-10 向 Withings+ 会员推出  
  原题：Withings AI Connector for Claude, ChatGPT, Vibe and Grok  
  主链接：<https://static.withings.com/content/v2/app/mcp/en/index.html>  
  关系：接入「Claude 接入 Apple Health 与病历」— 通用助手通过连接器读取设备数据  
  改变：与 Oura、WHOOP 自研 Agent 相反，Withings 选择做通用助手的数据源：设备公司在“入口”之争中的另一种站位（编者解读）。
- **Aether：生理波形基础模型的算力最优尺度律** `aether-scaling` — 生理信号基础模型 · 论文 · 北卡罗来纳大学教堂山分校 × Foci Labs（与 Foci Labs 合作） · arXiv 2026-10-05  
  原题：Training and Scaling Compute-Optimal Physiological Waveform Foundation Models（Aether）  
  主链接：<https://arxiv.org/abs/2610.05649>  
  关系：继承「LSM：分钟级可穿戴数据的尺度律」— 论文引用 LSM 的尺度律分析，迁移到原始生理波形；并行「心电模型怎样随规模变好？」— 同期的心电尺度研究；检验「NormWear-2：信号级的生理世界模型」— NormWear 1/2 是被比较的基线  
  改变：尺度律问题从可穿戴分钟级数据（LSM）和心电延伸到多通道临床波形，并第一次把“标注病人数”作为显式资源。数据是 ICU 数据，不是可穿戴数据；3,630 万小时含重复。
- **OPPO：65 万人参与的手表血压研究** `oppo-bp2026` — 生理信号基础模型 · 产品 · OPPO · 发布 2026-10-08（Watch X3 于 2026-03 发布）  
  原题：《OPPO 血压健康研究年度报告 2026》与 Watch X3 的高血压风险评估  
  主链接：<https://www.oppo.com/cn/newsroom/stories/518/>；报告 PDF：<https://www.oppo.com/content/dam/oppo_com/cn/mkt/newsroom/stories/518/OPPO_Blood_Pressure_Health_Research_Report_2026.pdf>  
  关系：落地「手表 PPG 高血压风险筛查」— EMBC 2024 模型进入大规模研究与产品  
  改变：与苹果同期的平行路线：苹果靠基础模型加线性头，OPPO 靠专门模型加大规模研究，最后都落到手表的高血压提醒上。
- **PPG-Bench：公平比较下的开源 PPG 模型** `ppg-bench` — 生理信号基础模型 · 开源模型/数据 · Mannas AI · arXiv 2026-10（开源基准）  
  原题：PPG-Bench: A Unified Benchmark for PPG Foundation Models  
  主链接：<https://arxiv.org/abs/2610.13435>  
  关系：检验「PaPaGei：首个开源 PPG 基础模型」— 在统一口径下重新评测已发布的开源 PPG 模型；检验「Pulse-PPG：只用野外数据训练的开源 PPG 模型」— Pulse-PPG 是 5 个被测模型之一；检验「AnyPPG：ECG 引导的 PPG 与全表型筛查」— AnyPPG 是 5 个被测模型之一  
  改变：作者的结论是：当前公开的 PPG 基础模型还不能宣称学到了通用、可迁移的表征。这与企业在私有大数据上的强结果形成张力，提示数据规模与评测口径仍是关键未知数（编者解读）。
- **HiPPT：按证据范围对齐的 PPG–文本表征** `hippt` — 生理信号基础模型 · 论文 · OPPO（与东南大学、深圳技术大学、北京大学合作） · arXiv 2026-10  
  原题：HiPPT: Physiology-Grounded Wearable PPG Representation Learning via Multi-Scope Text Alignment  
  主链接：<https://arxiv.org/abs/2610.14489>  
  关系：继承「SensorLM：传感器与语言对齐」— 传感器–语言对齐，从分钟级指标下沉到 PPG 波形；继承「手表 PPG 心脏年龄：ECG 引导的预训练」— 同一厂商的 PPG 表征线  
  改变：把语言当作“分层监督”而不只是接口，并支持年龄组、性别、BMI 的零样本画像。手表厂商的私有大数据开始与语言对齐结合。
- **反思生物信号世界模型：预测 ≠ 干预** `rethink-wm` — 生理世界模型 · 论文 · 格里菲斯大学（与 UCLA、埃默里大学合作） · arXiv 2026-10  
  原题：Rethinking World Models for Biosignals  
  主链接：<https://arxiv.org/abs/2610.17510>  
  关系：检验「NormWear-2：信号级的生理世界模型」— 用“真实动作 + 因果证据”两条要求检视已有生物信号世界模型（编者解读）；检验「ECG-WM：给药后心电的世界模型」— 同上  
  改变：世界模型一年之内从概念走到被批判性检查，门槛从“预测得准”抬高到“因果上站得住”（编者解读）。
- **Oura Advisor 个性化计划：小步实验** `oura-plans` — Agent · 产品 · Oura · 2026-11-03 起逐步推出（英文）；官方博客 2026-11-10  
  原题：Personalized plans with Oura Advisor  
  主链接：<https://ouraring.com/blog/personalized-plans-with-oura-advisor/>；Oura 帮助中心：<https://support.ouraring.com/hc/en-us/articles/39512345699219-Oura-Advisor>  
  关系：继承「Oura Advisor：从 Labs 测试到全面上线」— 同一 Advisor，从问答扩展到计划与打卡  
  改变：Agent 从“解释过去”变成“小步实验”：计划、打卡、看数据变化，形成可度量的行为闭环。谷歌 SensorWM 用模拟推演未来，Oura 用真实打卡检验结果（编者对比）。
- **SensorWM：以行为为动作的可穿戴世界模型** `sensorwm` — 生理世界模型 · 论文 · 谷歌 · arXiv 2026-11-05；谷歌研究博客 2026-11-11；世界模型部分先以 NeurIPS 2026 workshop 论文在 OpenReview 公开（2026-10-02，两位谷歌作者）  
  原题：Personalized health coaching via coachable health age and counterfactual wearable trajectories (SensorWM)  
  主链接：<https://research.google/blog/using-wearables-to-enable-cardiovascular-kidney-metabolic-ckm-risk-profiling-for-personalized-coaching/>；arXiv：<https://arxiv.org/abs/2611.08568>；配套研究：CKM 健康年龄（arXiv 2603.27787）：<https://arxiv.org/abs/2603.27787>；NeurIPS 2026 世界模型（CWM）workshop 论文，已录用：Developing World Models from Wearable Sensors（Lee & Heydari，谷歌；OpenReview 2026-10-02 发布）；在潜空间建模周级可穿戴指标，不重建原始信号：<https://openreview.net/forum?id=8SH3daIGHz>  
  关系：继承「SensorFM：500 万人、万亿分钟」— 同一谷歌可穿戴研究线；论文未说明是否以 SensorFM 为编码器（编者解读）；奠基「可穿戴 + 常规血检预测胰岛素抵抗」— 健康年龄与 CKM 扩展在 WEAR-ME 研究中验证；呼应「运动心率响应的个体化建模」— 苹果 2022 年的个体“运动→心率”响应模型，是动作条件生理模型的早期形态；两者无引用承接（编者解读）；接入「PHA：数据科学家、领域专家与教练的多智能体」— 世界模型的推演交给语言模型教练 Agent 生成计划；转向「TimesFM：通用时序预测基础模型」— 从通用预测改为以动作为条件；呼应「WHOOP Age 与血压洞察」— “生理年龄”从展示用的综合分数，变成可以优化的目标；并行「HealthFormer：生成式多模态生理轨迹与干预模拟」— 都以干预为条件模拟个体轨迹；HealthFormer 用深度表型与营养试验，SensorWM 用可穿戴行为；并行「Oura Advisor 个性化计划：小步实验」— 同一周：Oura 用真实打卡检验计划，谷歌用反事实模拟挑选计划  
  改变：参数层表征、动作条件的动力学、一个可改变的目标（CHA）和语言模型 Agent，第一次在同一个公开系统里串起来（编者所见）；信号纲没有进入，因为输入是周级指标而非波形。盲评中，持证生活方式教练在 71.4% 的配对里更偏好基于反事实推演的计划，医生判定 99.2% 的这类计划符合安全标准。局限同样清楚：反事实来自观察数据训练的模型，评测的是计划质量而非健康结局；《Rethinking World Models》要求的干预效应验证尚未完成（编者解读）。
- **AI-PPG-ACC-HTN：免校准腕表高血压筛查（Nature）** `google-htn-nature` — 生理信号基础模型 · 论文 · 谷歌 · Nature 2026-11-05；谷歌研究博客同日  
  原题：Opportunistically Detecting Signs of Hypertension on a Consumer Smartwatch（AI-PPG-ACC-HTN）  
  主链接：<https://www.nature.com/articles/s41586-026-11336-3>；谷歌研究博客：<https://research.google/blog/detecting-signs-of-hypertension-using-wearable-sensors/>  
  关系：继承「可穿戴生物信号基础模型的大规模训练」— 同一受试者片段做正样本的对比预训练；奠基「Health Guardian：谷歌把健康基础模型做成月度趋势功能」— 博客称该研究为血压趋势功能提供了依据；并行「高血压提醒：自监督 PPG 特征上线」— 同为自监督 PPG 表征 + 少量标注的高血压筛查；苹果走 FDA 许可的提醒，谷歌发表 Nature 论文  
  改变：苹果 2023 年“以人为锚”的自监督配方，在谷歌这里以 Nature 论文和金标准前瞻验证的形式用到高血压上；博客说这项研究“帮助形成了 Google Health 应用里 Health Guardian 的血压趋势功能”，同时强调它本身是探索性研究，不代表现有或将来的产品能力。
- **Oura 收购 Counsel Health** `oura-counsel` — Agent · 宣布/收购/在建 · Oura · 宣布收购 2026-11-10（预计年底前完成）  
  原题：Oura to acquire Counsel Health（AI 原生初级保健）  
  主链接：<https://www.counselhealth.com/newsroom/oura-to-acquire-counsel-health-advancing-vision-for-more-connected-personalized-healthcare>；Oura 博客：<https://ouraring.com/blog/>  
  关系：继承「Oura Advisor：从 Labs 测试到全面上线」— 从健康助手延伸到医疗服务；并行「WHOOP AI：记忆、主动关怀与医生」— 同年 WHOOP 也引入医生问诊  
  改变：可穿戴 Agent 的终点被重新定义为医疗照护：从“解释我的数据”到“基于我的数据接受诊疗”。

## 6. 相关但未上年谱的工作（204 项）

来自公司与学术两轮检索；链接均经 scripts/check_links.py 检查可访问。按不上年谱的原因分组。页面底部“全部来源”中同样列出。


### 第五版从年谱移出（样本量小 / 支撑不足 / 重复 / 偏离主线）（91）

- **Introducing Amazon Halo and Amazon Halo Band（2023 年停止支持）** — Amazon · 2020-08-27 · <https://press.aboutamazon.com/2020/8/introducing-amazon-halo-and-amazon-halo-band-a-new-service-that-helps-customers-improve-their-health-and-wellness>  
  原因：【偏离主线】设备已停产，未涉及模型。原摘要：Amazon Halo：通用科技公司进入可穿戴，三年后退出
- **Amazon 2023-04-26：Our decision to wind down Amazon Halo** — Amazon · 2020-08-27 · <https://www.aboutamazon.com/news/company-news/amazon-halo-discontinued>  
  原因：【偏离主线】“Introducing Amazon Halo and Amazon Halo Band（2023 年停止支持）”的配套来源
- **Representing and Denoising Wearable ECG Recordings** — 苹果 · 2020-11-30 · <https://arxiv.org/abs/2012.00110>  
  原因：【支撑不足】统计模型而非预训练；与主线没有可证的承接。原摘要：手表单导联心电的逐拍表示与结构化去噪
- **Apple ML Research** — 苹果 · 2020-11-30 · <https://machinelearning.apple.com/research/wearable-ecg-recordings>  
  原因：【支撑不足】“Representing and Denoising Wearable ECG Recordings”的配套来源
- **PhysioMTL: Personalizing Physiological Patterns using Optimal Transport Multi-Task Regression** — 苹果 · 2022-03-19 · <https://arxiv.org/abs/2203.12595>  
  原因：【样本量小】小规模 HRV 研究，与后来的个体基线产品没有公开承接。原摘要：PhysioMTL：为每个人学 HRV 昼夜节律，并能做反事实
- **Apple ML Research（与 CMU、UIUC、密歇根大学合作）** — 苹果 · 2022-03-19 · <https://machinelearning.apple.com/research/physiomtl>  
  原因：【样本量小】“PhysioMTL: Personalizing Physiological Patterns using Optimal Transport Multi-Task Regression”的配套来源
- **Latent Temporal Flows for Multivariate Analysis of Wearables Data** — 苹果 · 2022-10-14 · <https://arxiv.org/abs/2210.07475>  
  原因：【支撑不足】苹果动力学前史已由 2020 血糖与 2022 运动心率两篇代表。原摘要：Latent Temporal Flows：AHMS 多变量时序的潜空间生成预测
- **Apple ML Research** — 苹果 · 2022-10-14 · <https://machinelearning.apple.com/research/latent-temporal-flows>  
  原因：【支撑不足】“Latent Temporal Flows for Multivariate Analysis of Wearables Data”的配套来源
- **MAEEG: Masked Auto-encoder for EEG Representation Learning** — 苹果 · 2022-10-27 · <https://arxiv.org/abs/2211.02625>  
  原因：【支撑不足】workshop 论文；掩码一支由 LaBraM、LSM 代表。原摘要：MAEEG：苹果在 EEG 上的掩码重建预训练（2022）
- **Apple ML Research** — 苹果 · 2022-10-27 · <https://machinelearning.apple.com/research/masked-auto-encoder>  
  原因：【支撑不足】“MAEEG: Masked Auto-encoder for EEG Representation Learning”的配套来源
- **A foundational vision transformer improves diagnostic performance for electrocardiograms (HeartBEiT)** — 西奈山伊坎医学院 · 2023-06-06 · <https://doi.org/10.1038/s41746-023-00840-9>  
  原因：【重复】临床心电预训练由 ECG-FM、ECGFounder 代表。原摘要：HeartBEiT：850 万份心电的掩码图像预训练
- **Towards Conversational Diagnostic AI (AMIE)** — 谷歌 · 2024-01-11 · <https://arxiv.org/abs/2401.05654>  
  原因：【偏离主线】临床问诊 Agent，不读可穿戴数据。原摘要：AMIE：会问诊的对话 Agent
- **Nature Medicine 2026-02-06：A large language model for complex cardiology care（AMIE 扩展到心内科复杂病例，斯坦福 × 谷歌）** — 谷歌 · 2024-01-11 · <https://doi.org/10.1038/s41591-025-04190-9>  
  原因：【偏离主线】“Towards Conversational Diagnostic AI (AMIE)”的配套来源
- **MotionPrint: Ready-to-Use, Device-Agnostic, and Location-Invariant Motion Activity Models（arXiv 题为 Advancing Location-Invariant and Device-Agnostic Motion Activity Recognition on Wearable Devices）** — 苹果 · 2024-02-06 · <https://arxiv.org/abs/2402.03714>  
  原因：【重复】设备与佩戴位置异构问题由 Device Passport 承接；本条只是数据集与端侧模型，未进入任何脉络。原摘要：MotionPrint：一个端侧运动模型，戴在哪、什么设备都能用
- **Apple ML Research** — 苹果 · 2024-02-06 · <https://machinelearning.apple.com/research/motionprint>  
  原因：【重复】“MotionPrint: Ready-to-Use, Device-Agnostic, and Location-Invariant Motion Activity Models（arXiv 题为 Advancing Location-Invariant and Device-Agnostic Motion Activity Recognition on Wearable Devices）”的配套来源
- **Chronos: Learning the Language of Time Series** — Amazon · 2024-03-12 · <https://arxiv.org/abs/2403.07815>  
  原因：【重复】通用时序基线由 TimesFM 代表。原摘要：Chronos：把时序当语言来学
- **SiamQuality: a ConvNet-based foundation model for photoplethysmography signals** — 埃默里大学 等 · 2024-04-26 · <https://doi.org/10.1088/1361-6579/ad6747>  
  原因：【重复】PPG 自监督由 PaPaGei、Pulse-PPG 代表。原摘要：SiamQuality：把差质量 PPG 变成监督
- **arXiv** — 埃默里大学 等 · 2024-04-26 · <https://arxiv.org/abs/2404.17667>  
  原因：【重复】“SiamQuality: a ConvNet-based foundation model for photoplethysmography signals”的配套来源
- **GPTCoach: Towards LLM-Based Physical Activity Coaching** — 斯坦福大学 · 2024-05-09 · <https://arxiv.org/abs/2405.06061>  
  原因：【样本量小】16 名参与者的实验室研究；教练方法论由后来的 PHA、Fitbit 教练承接。原摘要：GPTCoach：按动机访谈做运动教练的 LLM
- **From Classification to Clinical Insights: Towards Analyzing and Reasoning About Mobile and Behavioral Health Data With Large Language Models** — 华盛顿大学 等 · 2024-05-13 · <https://doi.org/10.1145/3659604>  
  原因：【重复】与 Health-LLM 同期同题。原摘要：从分类到临床洞见：LLM 推理行为健康感知数据
- **Galaxy AI Is Coming to New Galaxy Watch for More Motivational Health** — 三星 · 2024-05-29 · <https://news.samsung.com/global/galaxy-ai-is-coming-to-new-galaxy-watch-for-more-motivational-health>  
  原因：【支撑不足】Energy Score 等综合分，官方未说明模型，与基础模型主线无关。原摘要：三星：Galaxy AI 进入手表（Energy Score）
- **Towards Open Respiratory Acoustic Foundation Models: Pretraining and Benchmarking (OPERA)** — 剑桥大学 · 2024-06-23 · <https://arxiv.org/abs/2406.16148>  
  原因：【重复】呼吸声基础模型由 HeAR 代表。原摘要：OPERA：开放的呼吸声基础模型与基准
- **NeuroLM: A Universal Multi-task Foundation Model for Bridging the Gap between Language and EEG Signals** — 上海交通大学 · 2024-08-27 · <https://arxiv.org/abs/2409.00101>  
  原因：【重复】EEG—语言对齐；“信号 + 语言”由 SensorLM、OpenTSLM 代表。原摘要：NeuroLM：把 EEG 当作外语交给 LLM
- **Promoting Cross-Modal Representations to Improve Multimodal Foundation Models for Physiological Signals** — 苹果 · 2024-10-21 · <https://arxiv.org/abs/2410.16424>  
  原因：【支撑不足】workshop 论文；跨模态机制的证据由正式发表的工作代表。原摘要：跨模态重建与模态丢弃：多模态生理基础模型怎么预训练
- **Apple ML Research** — 苹果 · 2024-10-21 · <https://machinelearning.apple.com/research/modal-representations>  
  原因：【支撑不足】“Promoting Cross-Modal Representations to Improve Multimodal Foundation Models for Physiological Signals”的配套来源
- **HuBERT-ECG: a self-supervised foundation model for broad and scalable cardiac applications** — 布雷西亚大学 · 2024-11-18 · <https://doi.org/10.1101/2024.11.14.24317328>  
  原因：【重复】与 ECG-FM、ECGFounder 同类。原摘要：HuBERT-ECG：三种规模的自监督心电模型
- **CBraMod: A Criss-Cross Brain Foundation Model for EEG Decoding** — 浙江大学 · 2024-12-10 · <https://arxiv.org/abs/2412.07236>  
  原因：【重复】EEG 基础模型由 LaBraM 代表。原摘要：CBraMod：按空间与时间分解的 EEG 模型
- **GitHub** — 浙江大学 · 2024-12-10 · <https://github.com/wjq-learning/CBraMod>  
  原因：【重复】“CBraMod: A Criss-Cross Brain Foundation Model for EEG Decoding”的配套来源
- **Reading Your Heart: Learning ECG Words and Sentences via Pre-training ECG Language Model** — 北京大学 · 2025-02-15 · <https://arxiv.org/abs/2502.10707>  
  原因：【重复】心电表征同类工作。原摘要：HeartLang：把心搏当词、节律当句
- **GPT-PPG: A GPT-based Foundation Model for Photoplethysmography Signals** — 埃默里大学 等 · 2025-03-11 · <https://doi.org/10.1088/1361-6579/add988>  
  原因：【重复】PPG 开源模型由 PaPaGei、Pulse-PPG 代表。原摘要：GPT-PPG：生成式 PPG 基础模型
- **arXiv** — 埃默里大学 等 · 2025-03-11 · <https://arxiv.org/abs/2503.08015>  
  原因：【重复】“GPT-PPG: A GPT-based Foundation Model for Photoplethysmography Signals”的配套来源
- **Garmin Connect+ · Active Intelligence** — Garmin · 2025-03-27 · <https://www.garmin.com/en-US/newsroom/press-release/wearables-health/elevate-your-health-and-fitness-goals-with-garmin-connect/>  
  原因：【重复】“AI 解释层进订阅”由 WHOOP、Oura、Dexcom 代表。原摘要：Garmin Active Intelligence
- **HealthBench: Evaluating Large Language Models Towards Improved Human Health** — OpenAI · 2025-05-13 · <https://arxiv.org/abs/2505.08775>  
  原因：【偏离主线】通用健康对话评测，不涉及生理数据。原摘要：HealthBench：262 名医生写的健康对话评测
- **OpenAI 博客** — OpenAI · 2025-05-13 · <https://openai.com/index/healthbench/>  
  原因：【偏离主线】“HealthBench: Evaluating Large Language Models Towards Improved Human Health”的配套来源
- **MIRA: Medical Time Series Foundation Model for Real-World Health Data** — 微软 · 2025-06-09 · <https://www.microsoft.com/en-us/research/publication/mira-medical-time-series-foundation-model-for-real-world-health-data/>  
  原因：【偏离主线】ICU/EHR 时序，非可穿戴。原摘要：MIRA：医疗时序预测基础模型
- **arXiv** — 微软 · 2025-06-09 · <https://arxiv.org/abs/2506.07584>  
  原因：【偏离主线】“MIRA: Medical Time Series Foundation Model for Real-World Health Data”的配套来源
- **代码** — 微软 · 2025-06-09 · <https://github.com/microsoft/MIRA>  
  原因：【偏离主线】“MIRA: Medical Time Series Foundation Model for Real-World Health Data”的配套来源
- **Sequential Diagnosis with Language Models（MAI-DxO / SDBench）** — 微软 · 2025-06-27 · <https://microsoft.ai/news/the-path-to-medical-superintelligence/>  
  原因：【偏离主线】基于病例的诊断编排，不涉及可穿戴。原摘要：MAI-DxO：模拟医生小组的诊断编排器
- **arXiv** — 微软 · 2025-06-27 · <https://arxiv.org/abs/2506.22405>  
  原因：【偏离主线】“Sequential Diagnosis with Language Models（MAI-DxO / SDBench）”的配套来源
- **Organ-Agents: Virtual Human Physiology Simulator via LLMs** — 天津大学 等 · 2025-08-20 · <https://arxiv.org/abs/2508.14357>  
  原因：【偏离主线】ICU 病人数据上的 LLM 模拟，不涉及可穿戴。原摘要：Organ-Agents：多 LLM Agent 模拟器官系统
- **Speech Foundation Models Generalize to Time Series Tasks from Wearable Sensor Data** — 苹果 · 2025-08-29 · <https://arxiv.org/abs/2509.00221>  
  原因：【支撑不足】workshop 论文；跨域复用的观察，未有后续。原摘要：语音基础模型的特征可直接用于可穿戴信号
- **Apple ML Research（页面 2025-11）** — 苹果 · 2025-08-29 · <https://machinelearning.apple.com/research/speech-foundation>  
  原因：【支撑不足】“Speech Foundation Models Generalize to Time Series Tasks from Wearable Sensor Data”的配套来源
- **GLOSS: Group of LLMs for Open-ended Sensemaking of Passive Sensing Data for Health and Wellbeing** — 东北大学（美国）× RMIT · 2025-09-03 · <https://doi.org/10.1145/3749474>  
  原因：【重复】与 PHIA 同题（LLM 解读个人传感数据）。原摘要：GLOSS：多 LLM 协作解读被动感知数据
- **CPEP: Contrastive Pose-EMG Pre-training Enhances Gesture Generalization on EMG Signals** — 苹果 · 2025-09-04 · <https://arxiv.org/abs/2509.04699>  
  原因：【支撑不足】workshop 论文；同一工作的主会版本 EMBridge 已收录。原摘要：CPEP：用手部姿态教肌电，实现零样本手势识别
- **Apple ML Research** — 苹果 · 2025-09-04 · <https://machinelearning.apple.com/research/cpep-contrastive>  
  原因：【支撑不足】“CPEP: Contrastive Pose-EMG Pre-training Enhances Gesture Generalization on EMG Signals”的配套来源
- **A Zero-Burden Sleep Foundation Model Built on Cardiorespiratory Signals（SleepFounder；v1 题为 A Low-Burden Sleep Foundation Model Built on Respiratory and Heartbeat Signals from 780,000+ Hours…）** — 北京大学 · 2025-09-09 · <https://www.medrxiv.org/content/10.1101/2025.09.06.25335216v3>  
  原因：【重复】睡眠方向由 SleepFM、SleepFM-2、sleep2vec 代表。原摘要：SleepFounder：只用心肺信号的“零负担”睡眠基础模型
- **medRxiv API（各版本日期与摘要）** — 北京大学 · 2025-09-09 · <https://api.medrxiv.org/details/medrxiv/10.1101/2025.09.06.25335216>  
  原因：【重复】“A Zero-Burden Sleep Foundation Model Built on Cardiorespiratory Signals（SleepFounder；v1 题为 A Low-Burden Sleep Foundation Model Built on Respiratory and Heartbeat Signals from 780,000+ Hours…）”的配套来源
- **DOI 10.1101/2025.09.06.25335216** — 北京大学 · 2025-09-09 · <https://doi.org/10.1101/2025.09.06.25335216>  
  原因：【重复】“A Zero-Burden Sleep Foundation Model Built on Cardiorespiratory Signals（SleepFounder；v1 题为 A Low-Burden Sleep Foundation Model Built on Respiratory and Heartbeat Signals from 780,000+ Hours…）”的配套来源
- **Using LLMs for Late Multimodal Sensor Fusion for Activity Recognition** — 苹果 · 2025-09-12 · <https://arxiv.org/abs/2509.10729>  
  原因：【偏离主线】任务是活动识别而非健康，只是语言接口线的旁证。原摘要：让 LLM 做声音与运动传感器的晚融合
- **Apple ML Research** — 苹果 · 2025-09-12 · <https://machinelearning.apple.com/research/multimodal-sensor-fusion>  
  原因：【偏离主线】“Using LLMs for Late Multimodal Sensor Fusion for Activity Recognition”的配套来源
- **REVE: A Foundation Model for EEG -- Adapting to Any Setup with Large-Scale Pretraining on 25,000 Subjects** — IMT Atlantique × 蒙特利尔大学 · 2025-10-24 · <https://arxiv.org/abs/2510.21585>  
  原因：【重复】EEG 基础模型由 LaBraM 代表。原摘要：REVE：25,000 人、任意电极布局的 EEG 模型
- **Using Oura data for cardiovascular disease detection with a large-scale foundation model** — Oura · 2025-11 · <https://resources.ouraring.com/oura-aha-scientific-sessions-2026>  
  原因：【支撑不足】只有会议海报题目，摘要未能核实。原摘要：Oura：用大规模基础模型检测心血管病
- **Learning the Relative Composition of EEG Signals Using Pairwise Relative Shift Pretraining (PARS)** — 苹果 · 2025-11-14 · <https://arxiv.org/abs/2511.11940>  
  原因：【支撑不足】workshop 论文，未改变主线。原摘要：PARS：预测两段 EEG 的相对时移来预训练
- **Apple ML Research** — 苹果 · 2025-11-14 · <https://machinelearning.apple.com/research/relative-composition-eeg>  
  原因：【支撑不足】“Learning the Relative Composition of EEG Signals Using Pairwise Relative Shift Pretraining (PARS)”的配套来源
- **前作：Label-Efficient Sleep Staging Using Transformers Pre-trained with Position Prediction（IEEE AIMHC 2024，arXiv 2024-03-29）** — 苹果 · 2025-11-14 · <https://arxiv.org/abs/2404.15308>  
  原因：【支撑不足】“Learning the Relative Composition of EEG Signals Using Pairwise Relative Shift Pretraining (PARS)”的配套来源
- **Wavelet-Driven Masked Multiscale Reconstruction for PPG Foundation Models (MMR)** — 三星 · 2026-01-18 · <https://arxiv.org/abs/2601.12215>  
  原因：【重复】三星多尺度思路由 HiMAE 代表。原摘要：小波多尺度掩码重建的 PPG 模型
- **Amazon One Medical Health AI（agentic 健康助手）** — Amazon · 2026-01-21 · <https://www.aboutamazon.com/news/retail/one-medical-ai-health-assistant>  
  原因：【偏离主线】基于病历与诊所服务，不读可穿戴数据。原摘要：Amazon Health AI：读病历、约诊、续方的 Agent
- **2026-03-10 扩展到 Amazon.com** — Amazon · 2026-01-21 · <https://www.aboutamazon.com/news/retail/amazon-health-ai-agent-one-medical>  
  原因：【偏离主线】“Amazon One Medical Health AI（agentic 健康助手）”的配套来源
- **CNBC（Bedrock 模型）** — Amazon · 2026-01-21 · <https://www.cnbc.com/2026/01/21/amazon-ai-health-care-one-medical-members.html>  
  原因：【偏离主线】“Amazon One Medical Health AI（agentic 健康助手）”的配套来源
- **Toward integrated sleep health: multimodal AI in Hang Hao Meng agent** — 浙江大学 · 2026-02-09 · <https://doi.org/10.1038/s41746-026-02432-9>  
  原因：【偏离主线】医院睡眠专科 Agent，不以可穿戴数据为主。原摘要：“杭好梦”：已规模部署的睡眠健康专家 Agent
- **PulseLM: A Foundation Dataset and Benchmark for PPG-Text Learning** — 新加坡管理大学 · 2026-02-10 · <https://arxiv.org/abs/2603.03331>  
  原因：【重复】PPG—文本方向由 HiPPT 代表。原摘要：PulseLM：PPG—文本问答数据集
- **Hugging Face 数据集** — 新加坡管理大学 · 2026-02-10 · <https://huggingface.co/datasets/Manhph2211/PulseLM>  
  原因：【重复】“PulseLM: A Foundation Dataset and Benchmark for PPG-Text Learning”的配套来源
- **Jade by Ultrahuman（real-time biointelligence AI）** — Ultrahuman · 2026-02-27 · <https://cyborg.ultrahuman.com/press-releases/ultrahuman-unveils-ring-pro-with-category-defining-15-day-battery-and-jade-worlds-first-real-time-biointelligence-ai>  
  原因：【支撑不足】产品介绍较少，未说明模型。原摘要：Ultrahuman Jade：会触发测量的 Agent
- **OSF: On Pre-training and Scaling of Sleep Foundation Models** — UCLA · 2026-02-27 · <https://arxiv.org/abs/2603.00190>  
  原因：【重复】尺度律证据由 LSM、心电尺度律与 Aether 代表。原摘要：OSF：睡眠基础模型的预训练与尺度
- **Wearable Foundation Models Should Go Beyond Static Encoders** — 剑桥大学 · 2026-03-20 · <https://arxiv.org/abs/2603.19564>  
  原因：【支撑不足】立场论文；“走向动力学”的论证由实际的世界模型条目承担。原摘要：立场：可穿戴基础模型应超越静态编码器
- **Sonata: A Hybrid World Model for Inertial Kinematics under Clinical Data Scarcity** — TimeTrace Labs × 牛津大学 · 2026-04-20 · <https://arxiv.org/abs/2604.18058>  
  原因：【样本量小】739 人、19 万窗口的小规模预训练；预训练目标的对照意义由 AC-JEPA 等代表。原摘要：Sonata：小数据下的 IMU 潜空间世界模型
- **Emergent Symbolic Structure in Health Foundation Models: Extraction, Alignment, and Cross-Modal Transfer** — 苹果 · 2026-05-08 · <https://machinelearning.apple.com/research/health-foundation-models>  
  原因：【支撑不足】表征收敛的分析性工作，暂无后续。原摘要：不同模态的健康模型收敛到相近表征
- **arXiv** — 苹果 · 2026-05-08 · <https://arxiv.org/abs/2605.07407>  
  原因：【支撑不足】“Emergent Symbolic Structure in Health Foundation Models: Extraction, Alignment, and Cross-Modal Transfer”的配套来源
- **A robust PPG foundation model using multimodal physiological supervision** — 杜比实验室 × 佐治亚理工 · 2026-06-05 · <https://arxiv.org/abs/2606.07365>  
  原因：【重复】“用贵模态定义监督”由 AnyPPG、xMAE 代表。原摘要：用 ECG 与呼吸指标挑选对比样本的稳健 PPG 模型
- **ICML 2026 poster** — 杜比实验室 × 佐治亚理工 · 2026-06-05 · <https://icml.cc/virtual/2026/poster/64846>  
  原因：【重复】“A robust PPG foundation model using multimodal physiological supervision”的配套来源
- **WEQA: Wearable hEalth Question Answering with Query-Adaptive Agentic Reasoning** — 剑桥大学 · 2026-06-16 · <https://arxiv.org/abs/2606.18147>  
  原因：【重复】Agent 调度模型的思路由 PHA 代表。原摘要：WEQA：按问题调度模型的可穿戴问答 Agent
- **Position: Beyond Prediction: Toward Verifiable Physiological Waveform Reasoning with Foundation Models and Agentic LLMs** — 微软 · 2026-06-19 · <https://www.microsoft.com/en-us/research/publication/position-beyond-prediction-toward-verifiable-physiological-waveform-reasoning-with-foundation-models-and-agentic-llms/>  
  原因：【支撑不足】立场论文，没有模型或数据。原摘要：微软立场论文：可核验的生理波形推理
- **Inertia-1: An Open Exploration of Wearable Motion Foundation Models** — UCLA · 2026-07-07 · <https://arxiv.org/abs/2607.06617>  
  原因：【重复】加速度预训练由牛津模型与 Sensori 代表。原摘要：Inertia-1：1,820 万小时加速度的开放研究
- **A Self-Evolving Agent for Longitudinal Personal Health Management (HealthJev)** — 复旦大学 等 · 2026-07-15 · <https://arxiv.org/abs/2607.13940>  
  原因：【样本量小】20 名模拟用户、90 天的模拟基准，非真实可穿戴数据。原摘要：HealthJev：会积累经验的长期健康 Agent
- **MacRumors 报道** — OpenAI · 2026-07-23 · <https://www.macrumors.com/2026/07/23/chatgpt-apple-health-integration/>  
  原因：【重复】“Launching Health in ChatGPT（Apple Health 与病历接入，美国全量）”的配套来源
- **Physiological World Models for Human State Transitions** — Fullive-AI × 北京大学 · 2026-08-15 · <https://arxiv.org/abs/2608.15309>  
  原因：【支撑不足】小团队预印本，与 NormWear-2、HealthFormer 思路重复且证据更弱。原摘要：PWM：以事件为条件的人体状态转移
- **DNA-PPG: A Foundation Model for Photoplethysmography via Dual Neighborhood Alignment** — 小米 · 2026-08-15 · <https://ijcai.org/proceedings/2026/0777.pdf>  
  原因：【重复】“参数语义引导 PPG”与 AnyPPG、OPPO 心脏年龄的思路重复。原摘要：DNA-PPG：形态与生理语义的双邻域对齐
- **代码与权重** — 小米 · 2026-08-15 · <https://github.com/yyzyyz001/DNA-PPG>  
  原因：【重复】“DNA-PPG: A Foundation Model for Photoplethysmography via Dual Neighborhood Alignment”的配套来源
- **Grounding Health AI: Architecture and Evaluation of a Domain-Expert Metabolic Health Agent** — Pheno.AI × MBZUAI · 2026-08-17 · <https://doi.org/10.64898/2026.08.11.26359946>  
  原因：【支撑不足】预印本中的示例对比，非系统评测。原摘要：代谢健康 Agent：用工具计算，避免编造指标
- **An AI tool for prioritizing candidate biomarkers from wearable sensor data (Biomarker Discovery Framework)** — 谷歌 · 2026-08-21 · <https://research.google/blog/an-ai-tool-for-prioritizing-candidate-biomarkers-from-wearable-sensor-data/>  
  原因：【支撑不足】研究博客介绍的工具，未有评测论文。原摘要：谷歌：从可穿戴数据筛选候选生物标志物的多 Agent 系统
- **SOTER: A Generative Time-Series Foundation Model for Wearable Human Physiological Signals** — 复旦大学 等 · 2026-09-15 · <https://arxiv.org/abs/2609.16804>  
  原因：【重复】连续时间生成模型，与 NormWear-2 等重复，且以临床波形为主。原摘要：SOTER：频段专家 + 神经 CDE 的连续时间生理生成模型
- **GitHub：SII-fkchen/SOTER** — 复旦大学 等 · 2026-09-15 · <https://github.com/SII-fkchen/SOTER>  
  原因：【重复】“SOTER: A Generative Time-Series Foundation Model for Wearable Human Physiological Signals”的配套来源
- **Hugging Face Papers** — 复旦大学 等 · 2026-09-15 · <https://huggingface.co/papers/2609.16804>  
  原因：【重复】“SOTER: A Generative Time-Series Foundation Model for Wearable Human Physiological Signals”的配套来源
- **A world model simulates the latent dynamics of human health (HealthFlux)** — 斯坦福大学 · 2026-09-21 · <https://doi.org/10.64898/2026.09.19.26363460>  
  原因：【偏离主线】UK Biobank 病历、化验与影像，不含可穿戴信号。原摘要：HealthFlux：全模态的人体健康世界模型
- **PPG-LM: A Photoplethysmography–Language Model with Multi-Level Clinical Alignment** — 埃默里大学 等 · 2026-09-27 · <https://arxiv.org/abs/2609.33516>  
  原因：【重复】PPG—文本方向由 HiPPT 代表。原摘要：PPG-LM：片段、事件、就诊三层文本对齐
- **Sensor-Language-Action Models (OpenSLA)** — UCLA · 2026-10-06 · <https://arxiv.org/abs/2610.08244>  
  原因：【支撑不足】单篇预印本，“感知—语言—行动”统一的说法缺少后续验证。原摘要：传感器—语言—行动模型
- **项目页** — UCLA · 2026-10-06 · <https://yang-ai-lab.github.io/OpenSLA>  
  原因：【支撑不足】“Sensor-Language-Action Models (OpenSLA)”的配套来源
- **MS-ECG-FM: Towards a More Universal Electrocardiogram Foundation Model for Health Monitoring using Multi-source Contrastive Learning** — 苹果 · 2026-10-06 · <https://arxiv.org/abs/2610.07662>  
  原因：【重复】报告对齐心电由 CSFM 代表。原摘要：MS-ECG-FM：多源临床报告对齐的 ECG 模型
- **WHOOP Foundation AI：多模态基础模型团队** — WHOOP · 2026-10-29 · <https://jobs.ashbyhq.com/whoop/aac41dfe-9ddb-4194-a81e-95f339aa86c7>  
  原因：【支撑不足】只有招聘页与访谈，没有论文或产品。原摘要：WHOOP 组建 Foundation AI 团队
- **All-In 访谈（2026-10-29）** — WHOOP · 2026-10-29 · <https://podcasts.apple.com/us/podcast/whoop-ceo-will-ahmed-50b-hours-of-health-data-a/id1502871393?i=1000798784337>  
  原因：【支撑不足】“WHOOP Foundation AI：多模态基础模型团队”的配套来源
- **BioLT: Streaming Biosignal Modeling** — 牛津大学 · 2026-11-09 · <https://doi.org/10.64898/2026.11.06.26367429>  
  原因：【支撑不足】2026-11 新预印本，尚无可评估的影响。原摘要：BioLT：把窗口级生理模型变成小时级流式模型

### 与已收条目思路重复（控制密度）（18）

- **Google shares 4 updates on generative AI in healthcare (Fitbit Personal Health LLM announced)** — 谷歌 · 2024-03-19 · <https://blog.google/innovation-and-ai/technology/health/google-generative-ai-healthcare/>  
  原因：已核对存在；与已收条目思路相近，本版为控制密度未单列。检索备注：first public announcement of PH-LLM productization path
- **FDA clears Eko Low Ejection Fraction AI (ELEFT)** — Eko · 2024-04-02 · <https://www.ekohealth.com/blogs/newsroom/fda-clears-low-ejection-fraction-ai>  
  原因：已核对存在；与已收条目思路相近，本版为控制密度未单列。检索备注：Eko missing; multimodal ECG+PCG AI clearance
- **FDA qualifies Apple AFib History as Medical Device Development Tool (MDDT)** — 苹果 · 2024-05 · <https://www.fda.gov/media/178230/download>  
  原因：已核对存在；与已收条目思路相近，本版为控制密度未单列。检索备注：marks wearable signal becoming accepted clinical endpoint
- **AliveCor dual FDA clearance: KAI 12L AI (35 determinations) + Kardia 12L** — AliveCor · 2024-06-25 · <https://alivecor.com/press/press_release/alivecor-launches-kardia-12l-a-first-of-its-kind-ai-powered-12-lead-ecg-system>  
  原因：已核对存在；与已收条目思路相近，本版为控制密度未单列。检索备注：AliveCor missing; major AI ECG clearance
- **A step towards making heart health screening accessible for billions with PPG signals** — 谷歌 · 2024-07-25 · <https://research.google/blog/a-step-towards-making-heart-health-screening-accessible-for-billions-with-ppg-signals/>  
  原因：已核对存在；与已收条目思路相近，本版为控制密度未单列。检索备注：Google PPG representation for CVD risk; fills 2024 gap
- **From diagnosis to treatment: Advancing AMIE for longitudinal disease management** — 谷歌 · 2025-03-06 · <https://research.google/blog/from-diagnosis-to-treatment-advancing-amie-for-longitudinal-disease-management/>  
  原因：临床诊断对话 Agent 支线，与可穿戴主线关系较远。检索备注：clinical agent line; add only if AMIE thread expanded
- **AMIE gains vision: multimodal diagnostic dialogue** — 谷歌 · 2025-05-01 · <https://research.google/blog/amie-gains-vision-a-research-ai-agent-for-multi-modal-diagnostic-dialogue/>  
  原因：临床诊断对话 Agent 支线，与可穿戴主线关系较远。检索备注：clinical agent line
- **Withings Intelligence (AI health assistant, beta)** — Withings · 2025-06-10 · <https://media.withings.com/press/press-releases/Withings-Intelligence/Withings_Intelligence-EN.pdf>  
  原因：已核对存在；与已收条目思路相近，本版为控制密度未单列。检索备注：European device maker’s LLM layer; missing company
- **Enabling physician-centered oversight for AMIE** — 谷歌 · 2025-08-12 · <https://research.google/blog/enabling-physician-centered-oversight-for-amie/>  
  原因：临床诊断对话 Agent 支线，与可穿戴主线关系较远。检索备注：clinical agent line
- **Hypertension Notification Feature 510(k) K250507** — 苹果 · 2025-09-11 · <https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K250507>  
  原因：已核对存在；与已收条目思路相近，本版为控制密度未单列。检索备注：attach as source to existing Hypertension Notifications entry
- **Towards better health conversations: “wayfinding” AI agent based on Gemini** — 谷歌 · 2025-09-25 · <https://research.google/blog/towards-better-health-conversations-research-insights-on-a-wayfinding-ai-agent-based-on-gemini/>  
  原因：已核对存在；与已收条目思路相近，本版为控制密度未单列。检索备注：health-agent dialogue design; relevant to agent thread
- **TinyMyo: a Tiny Foundation Model for Flexible EMG Signal Processing at the Edge** — 学术 · 2025-12-05 · <https://arxiv.org/abs/2512.15729>  
  原因：检索推荐；本版核对后未单列（与已收条目重复或作者单位未核实）。TinyMyo：面向边缘的 EMG FM（IEEE TBME），站内 EMG 只有 Meta 一条，可补学术侧 EMG FM
- **Abbott Libre Assist (generative AI meal glucose prediction)** — 雅培 · 2026-01-05 · <https://abbott.mediaroom.com/2026-01-05-Abbotts-new-Libre-Assist-app-feature-tackles-a-top-need-for-people-living-with-diabetes-in-the-moment-food-decisions>  
  原因：已核对存在；与已收条目思路相近，本版为控制密度未单列。检索备注：Abbott has no entry; first GenAI feature
- **Next-Gen Galaxy Watch Features for AI-Powered Everyday Health Companion** — 三星 · 2026-06-04 · <https://news.samsung.com/global/samsung-introduces-next-gen-galaxy-watch-features-for-ai-powered-everyday-health-companion>  
  原因：已核对存在；与已收条目思路相近，本版为控制密度未单列。检索备注：Samsung 2026 product step before Health Assistant beta
- **SymptomAI: Towards a conversational AI agent for everyday symptom assessment** — 谷歌 · 2026-07-22 · <https://research.google/blog/symptomai-towards-a-conversational-ai-agent-for-everyday-symptom-assessment/>  
  原因：已核对存在；与已收条目思路相近，本版为控制密度未单列。检索备注：consumer health agent research 2026
- **iRhythm third-generation Zio AI algorithm FDA clearance (Q2 2026 results)** — iRhythm · 2026-08-06 · <https://investors.irhythmtech.com/news/news-details/2026/iRhythm-Holdings-Announces-Second-Quarter-2026-Financial-Results/>  
  原因：已核对存在；与已收条目思路相近，本版为控制密度未单列。检索备注：continuation of 2019 iRhythm/Stanford line
- **Advancing AMIE towards expert-level audio-visual clinical consultations** — 谷歌 · 2026-08-11 · <https://research.google/blog/advancing-amie-towards-expert-level-audio-visual-clinical-consultations/>  
  原因：临床诊断对话 Agent 支线，与可穿戴主线关系较远。检索备注：clinical agent line
- **DiabAgent: Toward Agentic Physiological Control** — 学术 · 2026-11-07 · <https://arxiv.org/abs/2611.03601>  
  原因：检索推荐；本版核对后未单列（与已收条目重复或作者单位未核实）。DiabAgent：面向“智能体式生理控制”（2026-11 最新），世界模型+Agent 闭环的最新学术节点

### 相关工作，未单列（观察名单）（38）

- **LLaSA: A Sensor-Aware LLM for Natural Language Reasoning of Human Activity from IMU Data** — 学术 · 2024-06-20 · <https://arxiv.org/abs/2406.14498>  
  原因：相关但非里程碑
- **PhysioLLM: Supporting Personalized Health Insights with Wearables and Large Language Models** — 学术 · 2024-06-27 · <https://arxiv.org/abs/2406.19283>  
  原因：相关但非里程碑
- **ECG-Chat: A Large ECG-Language Model for Cardiac Disease Diagnosis** — 学术 · 2024-08-16 · <https://arxiv.org/abs/2408.08849>  
  原因：ECG-Chat，ECG-LLM 线，PULSE 已代表
- **A Foundation Model for Wearable Movement Data in Mental Health Research** — 学术 · 2024-11-22 · <https://arxiv.org/abs/2411.15240>  
  原因：相关但非里程碑
- **ECG-Byte: A Tokenizer for End-to-End Generative Electrocardiogram Language Modeling** — 学术 · 2024-12-18 · <https://arxiv.org/abs/2412.14373>  
  原因：相关但非里程碑
- **Sleepless Nights, Sugary Days: Creating Synthetic Users with Health Conditions for Realistic Coaching Agent Interactions** — 学术 · 2025-02-18 · <https://arxiv.org/abs/2502.13135>  
  原因：相关但非里程碑
- **Exploring Personalized Health Support through Data-Driven, Theory-Guided LLMs: A Case Study in Sleep Health** — 学术 · 2025-02-19 · <https://arxiv.org/abs/2502.13920>  
  原因：相关但非里程碑
- **A foundation model for sleep-based risk stratification and clinical outcomes** — 学术 · 2025-04-10 · <https://doi.org/10.1038/s41467-026-75326-9>  
  原因：相关但非里程碑
- **LLM4HAR: Generalizable On-device Human Activity Recognition with Pretrained LLMs** — Rutgers, The State University of New Jersey、Jingdong (China) · 2025-08-03 · <https://doi.org/10.1145/3711896.3737226>  
  原因：会议/期刊补扫推荐；本版未单列（严格说不是基础模型，或与已收条目重复）。KDD 2025（Rutgers/京东/北大/港科广/UTD）：用预训练 LLM 做端侧 HAR 泛化，有工业（京东）背景，补 KDD 侧“LLM 吃传感器”节点
- **Towards Customizable Foundation Models for Human Activity Recognition with Wearable Devices** — 学术 · 2025-08-30 · <https://doi.org/10.1145/3749479>  
  原因：相关但非里程碑
- **MASTER: A Multi-modal Foundation Model for Human Activity Recognition** — State Key Laboratory of Network and Switching Technology, Beijing University of Posts and Telecommunications, Beijing, China · 2025-09-03 · <https://doi.org/10.1145/3749511>  
  原因：会议/期刊补扫推荐；本版未单列（严格说不是基础模型，或与已收条目重复）。IMWUT 2025（北邮）：明确以“多模态基础模型”定位的 HAR 模型，补 IMU/行为层的 FM 节点（站内 IMU 线偏薄）
- **A Low-Burden Sleep Foundation Model Built on Respiratory and Heartbeat Signals from 780,000+ Hours of Multi-Ethnic Sleep Recordings（SleepFounder）** — tsinghua · 2025-09-06 · <https://www.medrxiv.org/content/10.1101/2025.09.06.25335216v1>  
  原因：补漏检索低置信候选：中（medRxiv 页面对 curl 返回 403，搜索结果确认存在；作者单位依据 sleep2vec 的引用推断为清华、五季医学团队，需要打开原文核实）
- **HealthSLM-Bench: Benchmarking Small Language Models for Mobile and Wearable Healthcare Monitoring** — 学术 · 2025-09-08 · <https://arxiv.org/abs/2509.07260>  
  原因：基准/评测类，列表即可
- **PhysioJEPA: Joint Embedding Representations of Physiological Signals for Real Time Risk Estimation in the Intensive Care Unit** — 学术 · 2025-09-23 · <https://openreview.net/forum?id=JHMLr8zRuZ>  
  原因：OpenReview 页面对脚本需人机验证，未能亲自核对摘要，暂列观察名单。ML4H 2025 + NeurIPS 2025 BrainBodyFM：JEPA 目标用于多生理信号，是“预训练目标从重建到预测”的代表（ICU 场景）
- **Advancing sleep health equity through deep learning on large-scale nocturnal respiratory signals** — Nanjing University of Science and Technology、Air Force Medical University · 2025-10-22 · <https://doi.org/10.1038/s41467-025-64340-y>  
  原因：会议/期刊补扫推荐；本版未单列（严格说不是基础模型，或与已收条目重复）。Nature Communications 2025-10（南京理工/空军军医大学等）：15,785 夜呼吸信号训练的远程睡眠监测框架，中国学术侧大规模呼吸信号工作；严格说非 FM，可作睡眠线补充
- **Stanford Sleep Bench: Evaluating Polysomnography Pre-training Methods for Sleep Foundation Models** — 学术 · 2025-12-10 · <https://arxiv.org/abs/2512.09591>  
  原因：基准/评测类，列表即可
- **An EMG Foundation Model for Neural Decoding** — 学术 · 2025-12-19 · <https://doi.org/10.64898/2025.12.17.694831>  
  原因：相关但非里程碑
- **LifeAgentBench: A Multi-dimensional Benchmark and Agent for Personal Health Assistants in Digital Health** — 学术 · 2026 · <https://arxiv.org/abs/2601.13880>  
  原因：基准/评测类，列表即可
- **A unified time-frequency foundation model for sleep decoding** — 学术 · 2026-01-13 · <https://doi.org/10.1038/s41467-025-67970-4>  
  原因：相关但非里程碑
- **AcceleRest: A Physiology-Aware Masked Autoencoder for Wrist Accelerometer-based Sleep Staging and Apnea Evaluation** — Technical University of Denmark、Copenhagen University Hospital · 2026-01-30 · <https://doi.org/10.64898/2026.01.28.26345056>  
  原因：会议/期刊补扫推荐；本版未单列（严格说不是基础模型，或与已收条目重复）。medRxiv 2026-01（DTU/哥本哈根大学医院/Stanford）：腕部加速度计的生理感知 MAE，做睡眠分期与呼吸暂停评估——连接 IMU 预训练与苹果/三星睡眠呼吸暂停功能
- **SleepMaMi: A Universal Sleep Foundation Model for Integrating Macro- and Micro-structures** — 学术 · 2026-02-07 · <https://arxiv.org/abs/2602.07628>  
  原因：相关但非里程碑
- **Learning Transferable Sensor Models via Language-Informed Pretraining** — 学术 · 2026-03-12 · <https://arxiv.org/abs/2603.11950>  
  原因：相关但非里程碑
- **PATCHCODE: Discrete Latent Predictive Learning for EEG Foundation Model** — 学术 · 2026-04-30 · <https://openreview.net/forum?id=NWcZ5vualM>  
  原因：OpenReview 页面对脚本需人机验证，未能亲自核对摘要，暂列观察名单。ICML 2026：EEG FM 从掩码重建转向离散潜变量预测（JEPA 式）目标，可与 PhysioJEPA 一起作为“预训练目标演进”的 EEG 证据
- **Next-Token Prediction Enables Scalable Learning of Sleep Physiology** — 学术 · 2026-05-25 · <https://openreview.net/forum?id=QVavRSyjmj>  
  原因：OpenReview 页面对脚本需人机验证，未能亲自核对摘要，暂列观察名单。预训练目标演进的直接证据：把多模态睡眠生理改用自回归 next-token 目标并讨论扩展性（FMSD@ICML 2026 workshop）。正好补逻辑审查提出的“预训练目标演进”脉络
- **VitalAgent: A Tool-Augmented Agent for Reactive and Proactive Physiological Monitoring over Wearable Health Data** — 学术 · 2026-05-28 · <https://arxiv.org/abs/2605.29483>  
  原因：相关但非里程碑
- **BCG-FM: A Foundation Model for Ambient Cardiac Health Sensing** — 学术 · 2026-06-05 · <https://arxiv.org/abs/2606.07692>  
  原因：相关但非里程碑
- **RubricsTree: Scalable and Evolving Open-Ended Evaluation of Personal Health Agents across Health Memory and Medical Skills** — 学术 · 2026-06-16 · <https://arxiv.org/abs/2606.18203>  
  原因：相关但非里程碑
- **IMU2Video: World Model-Enabled Video Generation from IMU sensors** — 学术 · 2026-06-20 · <https://doi.org/10.1145/3812836.3814749>  
  原因：相关但非里程碑
- **A foundation model of wearable pulse oximetry reveals physiological signatures of health and cardiometabolic risk** — 学术 · 2026-07-02 · <https://doi.org/10.64898/2026.07.01.26356992>  
  原因：相关但非里程碑
- **MorphologyFM: A Foundation Model for Morphology-Aware Representation Learning from ECG and Pulse Oximetry Waveforms** — 学术 · 2026-07-03 · <https://arxiv.org/abs/2607.09749>  
  原因：相关但非里程碑
- **Zero-Shot Heart Rate Variability Forecasting from Consumer Wearables Using Time Series Foundation Models** — 学术 · 2026-07-22 · <https://arxiv.org/abs/2607.20027>  
  原因：相关但非里程碑
- **Dual foundation models for accelerometry predict future health** — 学术 · 2026-07-27 · <https://doi.org/10.64898/2026.07.24.26358894>  
  原因：相关但非里程碑
- **FemWear: A Parameter-Efficient Wearable Foundation Model for Women's Health** — 学术 · 2026-08-08 · <https://arxiv.org/abs/2608.08244>  
  原因：相关但非里程碑
- **LiteEMG-FM: An Efficient and Deployable Foundation Model for Robust EMG Sensing** — 学术 · 2026-10-01 · <https://arxiv.org/abs/2610.02497>  
  原因：相关但非里程碑
- **LifeLong Digital Twin: A Unified Modeling Paradigm and Agent Harness for Event-Driven Lifelong Health State Trajectories** — pku · 2026-10-04 · <https://arxiv.org/abs/2610.05566>  
  原因：补漏检索低置信候选：中（北大与 VITA-Med Group；为技术报告）
- **A Unified Flexible Large Polysomnography Model for Sleep Staging and Downstream Clinical Screening** — Affiliated Mental Health Center & Hangzhou Seventh People's Hospital, School of Brain Science and Brain Medicine, and Liangzhu Laboratory, Zhejiang Un · 2026-10-27 · <https://doi.org/10.1101/2024.12.11.24318815>  
  原因：会议/期刊补扫推荐；本版未单列（严格说不是基础模型，或与已收条目重复）。medRxiv 2026-10-27（通讯单位 杭州市第七人民医院/浙大附属精神卫生中心）：统一、灵活的大型 PSG 模型做睡眠分期与临床筛查，和同院的“杭好眠”Agent 构成中国睡眠线从模型到 Agent 的一组证据
- **The Athlete as a Scientist of One: Agentic Bayesian Experimental Design for Individualized Physiology from Consumer Wearables** — 学术 · 2026-10-29 · <https://arxiv.org/abs/2610.40370>  
  原因：相关但非里程碑
- **A Cardiorespiratory Foundation Model Pretrained on Ten Physiological Signals for Perioperative and Critical Care** — 学术 · 2026-11-10 · <https://arxiv.org/abs/2611.15004>  
  原因：相关但非里程碑

### 与主线关系较弱：单一任务、非可穿戴或 workshop 短文（26）

- **Developing Measures of Cognitive Impairment in the Real World from Consumer-Grade Multimodal Sensor Streams** — 苹果 · 2019 · <https://machinelearning.apple.com/research/developing-measures-of-cognitive-impairment-in-the-real-world-from-consumer-grade-multimodal-sensor-streams>  
  原因：与主线关系较弱。检索备注：early multimodal sensing study; could be prelude
- **Modeling Patterns of Smartphone Usage and their Relationship to Cognitive Health** — 苹果 · 2019-11 · <https://machinelearning.apple.com/research/modeling-patterns-of-smartphone-usage-and-their-relationship-to-cognitive-health>  
  原因：单一任务模型、观察性研究或方法学工作，不是基础模型主线。检索备注：behavioral data precursor, not wearable physiology FM
- **App Usage Predicts Cognitive Ability in Older Adults** — 苹果 · 2019-12 · <https://machinelearning.apple.com/research/app-usage-predicts-cognitive-ability>  
  原因：单一任务模型、观察性研究或方法学工作，不是基础模型主线。检索备注：behavioral precursor; marginal
- **Contactless Sleep Sensing in Nest Hub** — 谷歌 · 2021-03-16 · <https://research.google/blog/contactless-sleep-sensing-in-nest-hub/>  
  原因：非可穿戴传感（床头设备、雷达、手机摄像头等）。检索备注：non-wearable sensing precursor
- **Estimating Respiratory Rate From Breath Audio Obtained Through Wearable Microphones** — 苹果 · 2021-08 · <https://machinelearning.apple.com/research/estimating-respiratory-rate>  
  原因：单一任务模型、观察性研究或方法学工作，不是基础模型主线。检索备注：task-specific model
- **Enhanced Sleep Sensing in Nest Hub** — 谷歌 · 2021-11-09 · <https://research.google/blog/enhanced-sleep-sensing-in-nest-hub/>  
  原因：非可穿戴传感（床头设备、雷达、手机摄像头等）。检索备注：non-wearable
- **Fusion-Id: A Photoplethysmography and Motion Sensor Fusion Biometric Authenticator With Few-Shot on-Boarding** — 苹果 · 2022-10 · <https://machinelearning.apple.com/research/photoplethysmography-motion-sensor-fusion>  
  原因：身份识别类工作，不属于健康建模。检索备注：biometrics, not health
- **A Large-Scale Observational Study of the Causal Effects of a Behavioral Health Nudge** — 苹果 · 2022-11 · <https://machinelearning.apple.com/research/large-scale-observational>  
  原因：单一任务模型、观察性研究或方法学工作，不是基础模型主线。检索备注：behavior/causal; relevant only to agent-intervention thread
- **Considerations for Distribution Shift Robustness in Health** — 苹果 · 2023-05 · <https://machinelearning.apple.com/research/considerations-distribution-shift>  
  原因：单一任务模型、观察性研究或方法学工作，不是基础模型主线。检索备注：methodological
- **The first step is the hardest: Pitfalls of Representing and Tokenizing Temporal Data for Large Language Models** — 学术 · 2023-09-12 · <https://arxiv.org/abs/2309.06236>  
  原因：引用锚点论文但非生理 FM/世界模型/Agent 主题
- **Slower Respiration Rate is Associated with Higher Self-reported Well-being After Wellness Training** — 苹果 · 2023-10 · <https://machinelearning.apple.com/research/slower-respiration-rate>  
  原因：单一任务模型、观察性研究或方法学工作，不是基础模型主线。检索备注：observational study
- **Audioplethysmography for cardiac monitoring with hearable devices** — 谷歌 · 2023-10-27 · <https://research.google/blog/audioplethysmography-for-cardiac-monitoring-with-hearable-devices/>  
  原因：单一任务模型、观察性研究或方法学工作，不是基础模型主线。检索备注：sensing modality, not FM
- **Neuro-GPT: Towards A Foundation Model for EEG** — 学术 · 2023-11-07 · <https://arxiv.org/abs/2311.03764>  
  原因：早期 EEG FM（Neuro-GPT），EEG 非可穿戴主线，列表即可
- **Moonwalk: Advancing Gait-Based User Recognition on Wearable Devices with Metric Learning** — 苹果 · 2024-03 · <https://machinelearning.apple.com/research/moonwalk>  
  原因：身份识别类工作，不属于健康建模。检索备注：biometrics
- **Evaluating Large Language Models as Virtual Annotators for Time-Series Physical Sensing Data** — 学术 · 2024-03-02 · <https://arxiv.org/abs/2403.01133>  
  原因：引用锚点论文但非生理 FM/世界模型/Agent 主题
- **Model-Driven Heart Rate Estimation and Heart Murmur Detection Based on Phonocardiogram** — 苹果 · 2024-08 · <https://machinelearning.apple.com/research/model-driven-heart>  
  原因：单一任务模型、观察性研究或方法学工作，不是基础模型主线。检索备注：auscultation task
- **What does electrodermal sensing reveal? Insights from the Pixel Watch & Fitbit Sense 2** — 谷歌 · 2024-10-24 · <https://research.google/blog/what-does-electrodermal-sensing-reveal-insights-from-the-pixel-watch-fitbit-sense-2/>  
  原因：与主线关系较弱。检索备注：modality study
- **Leveraging Periodicity for Robustness with Multi-modal Mood Pattern Models** — 苹果 · 2024-12 · <https://machinelearning.apple.com/research/leveraging-periodicity>  
  原因：单一任务模型、观察性研究或方法学工作，不是基础模型主线。检索备注：mental-health task
- **Polar launches Polar Loop (screen-free)** — Polar · 2025 · <https://www.polar.com/en/media-room/polar-launches-polar-loop-first-screen-free-subscription-free-wearable>  
  原因：与主线关系较弱。检索备注：no AI/FM item found for Polar
- **vivo WATCH 5 – BlueLM-powered AI sports coach; BP risk** — vivo · 2025 · <https://www.vivo.com.cn/vivo/vivowatch5/>  
  原因：与主线关系较弱。检索备注：LLM coach feature; no FM paper found
- **TAU: Temporal Attentive U-Net for PPG Peak Detection (Huawei authors)** — 华为 · 2025-03 · <https://arxiv.org/abs/2503.10733>  
  原因：单一任务模型、观察性研究或方法学工作，不是基础模型主线。检索备注：task model, not FM
- **Measuring heart rate with consumer ultra-wideband radar** — 谷歌 · 2025-07-17 · <https://research.google/blog/measuring-heart-rate-with-consumer-ultra-wideband-radar/>  
  原因：非可穿戴传感（床头设备、雷达、手机摄像头等）。检索备注：non-wearable sensing
- **Inferring Optical Tissue Properties from Photoplethysmography using Hybrid Amortized Inference** — 苹果 · 2026-01 · <https://machinelearning.apple.com/research/inferring-optical-tissue>  
  原因：单一任务模型、观察性研究或方法学工作，不是基础模型主线。检索备注：methodological physiology modelling
- **Unlocking health insights: Estimating advanced walking metrics with smartwatches** — 谷歌 · 2026-01-15 · <https://research.google/blog/unlocking-health-insights-estimating-advanced-walking-metrics-with-smartwatches/>  
  原因：单一任务模型、观察性研究或方法学工作，不是基础模型主线。检索备注：task model
- **Towards passive heart health monitoring via smartphone camera** — 谷歌 · 2026-06-04 · <https://research.google/blog/towards-passive-heart-health-monitoring-via-smartphone-camera/>  
  原因：非可穿戴传感（床头设备、雷达、手机摄像头等）。检索备注：non-wearable
- **Verily Health at HLTH USA 2026** — Verily · 2026-11-12 · <https://www.businesswire.com/news/home/20261112805911/en/Verily-Health-Brings-Its-Vision-for-Secure-Healthcare-Intelligence-to-HLTH-USA-2026>  
  原因：与主线关系较弱。检索备注：no public Verily wearable FM found

### 仅有媒体报道或信息不足（11）

- **Fitbit Labs launches with Gemini Insights Explorer** — 谷歌 · 2024-10-08 · <https://9to5google.com/2024/10/08/fitbit-labs-testing/>  
  原因：仅有媒体报道、招聘或演讲信息，缺少一手技术材料。检索备注：first shipped LLM-over-wearable-data feature from Google; secondary source (no primary blog found in sweep)
- **华为运动健康 2025 长城会：血压健康助手智能体 (with PLA General Hospital)** — 华为 · 2025 · <https://www.163.com/dy/article/KCG72SDP05566WT8.html>  
  原因：仅有媒体报道、招聘或演讲信息，缺少一手技术材料。检索备注：secondary media; no primary Huawei page found
- **Fitbit Labs testing Medical record navigator, Symptom Checker, Unusual trends** — 谷歌 · 2025-05-12 · <https://9to5google.com/2025/05/12/fitbit-labs-medical-records/>  
  原因：仅有媒体报道、招聘或演讲信息，缺少一手技术材料。检索备注：secondary source
- **HUAWEI WATCH 5 – first HarmonyOS AI watch with Pangu + DeepSeek models** — 华为 · 2025-06 · <https://www.ithome.com/0/858/008.htm>  
  原因：仅有媒体报道、招聘或演讲信息，缺少一手技术材料。检索备注：precedes existing WATCH 6 entry; secondary (IT之家)
- **荣耀手表5 Ultra：YOYO 接入 DeepSeek、运动健康智能体** — 荣耀 · 2025-07 · <https://www.ithome.com/0/865/371.htm>  
  原因：仅有媒体报道、招聘或演讲信息，缺少一手技术材料。检索备注：secondary; LLM assistant only
- **可穿戴运动健康技术的科学挑战与vivo产品实践 (CNCC)** — vivo · 2025-10-22 · <https://www.ccf.org.cn/Media_list/cncc/2025-10-22/850167.shtml>  
  原因：仅有媒体报道、招聘或演讲信息，缺少一手技术材料。检索备注：talk only
- **OPPO at CNCC 2025: AI health assistant** — OPPO · 2025-10-24 · <https://finance.sina.com.cn/tech/roll/2025-10-24/doc-infuyvpi5951832.shtml>  
  原因：仅有媒体报道、招聘或演讲信息，缺少一手技术材料。检索备注：secondary
- **荣耀手表6 Pro：心脏停搏监测、全天候血压、CGM 联动** — 荣耀 · 2026 · <https://www.ithome.com/1/008/432.htm>  
  原因：仅有媒体报道、招聘或演讲信息，缺少一手技术材料。检索备注：secondary
- **OpenAI acquires Torch (medical records)** — OpenAI · 2026-01-12 · <https://techcrunch.com/2026/01/12/openai-buys-tiny-health-records-startup-torch-for-reportedly-100m/>  
  原因：仅有媒体报道、招聘或演讲信息，缺少一手技术材料。检索备注：entry-point/data-layer move; secondary source
- **Apple reportedly scales back AI health coach (Project Mulberry)** — 苹果 · 2026-02-05 · <https://9to5mac.com/2026/02/05/apple-reportedly-scales-back-plans-for-ai-powered-health-coach/>  
  原因：仅有媒体报道、招聘或演讲信息，缺少一手技术材料。检索备注：secondary/rumor; useful only as context
- **Oura Health Foundation Models team opening** — Oura · 2026-09-22 · <https://www.linkedin.com/feed/update/urn:li:activity:7507971794746654720>  
  原因：仅有媒体报道、招聘或演讲信息，缺少一手技术材料。检索备注：hiring signal only; LinkedIn

### 背景、监管与配套资料（20）

- **AFib History feature 510(k) K213971** — 苹果 · 2022-06 · <https://www.accessdata.fda.gov/cdrh_docs/pdf21/K213971.pdf>  
  原因：监管背景资料。检索备注：regulatory milestone; context for later MDDT
- **Galaxy Watch Sleep Apnea feature De Novo DEN230041** — 三星 · 2024-02-06 · <https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPMN/denovo.cfm?knumber=DEN230041&start_search=1>  
  原因：监管背景资料。检索备注：first-of-kind regulatory milestone in sleep apnea notifications
- **Label-Efficient Sleep Staging Using Transformers Pre-trained with Position Prediction** — 苹果 · 2024-04 · <https://machinelearning.apple.com/research/label-efficient-sleep-staging>  
  原因：增量功能、硬件发布或已收条目的补充材料。检索备注：task-level SSL; optional
- **Pre-Trained Foundation Model Representations to Uncover Breathing Patterns in Speech** — 苹果 · 2024-07 · <https://machinelearning.apple.com/research/pretrained-foundation-model>  
  原因：增量功能、硬件发布或已收条目的补充材料。检索备注：audio-health; optional
- **Large Language Models for Wearable Sensor-Based Human Activity Recognition, Health Monitoring, and Behavioral Modeling: A Survey of Early Trends, Datasets, and Challenges** — 学术 · 2024-07-09 · <https://arxiv.org/abs/2407.07196>  
  原因：综述/立场类，作参考文献来源，不单列条目
- **Abbott Lingo OTC CGM available in U.S.** — 雅培 · 2024-09-05 · <https://abbott.mediaroom.com/2024-09-05-Abbotts-Lingo-TM-Continuous-Glucose-Monitor-for-Health-and-Wellness-Now-Available-in-the-U-S>  
  原因：增量功能、硬件发布或已收条目的补充材料。检索备注：context
- **A Systematic Review on Foundation Models for Electrocardiogram Analysis: Initial Strides and Expansive Horizons** — 学术 · 2024-10-24 · <https://arxiv.org/abs/2410.19877>  
  原因：综述/立场类，作参考文献来源，不单列条目
- **OPPO Watch X2 (blood pressure research, 60s health check)** — OPPO · 2025-02 · <https://www.oppo.com/en/newsroom/press/oppo-unveils-oppo-watch-x-2/>  
  原因：增量功能、硬件发布或已收条目的补充材料。检索备注：hardware context
- **WHOOP ECG Heart Screener 510(k) K243236** — WHOOP · 2025-04-04 · <https://www.accessdata.fda.gov/cdrh_docs/pdf24/K243236.pdf>  
  原因：监管背景资料。检索备注：regulatory context for WHOOP MG
- **Foundation Model Hidden Representations for Heart Rate Estimation from Auscultation** — 苹果 · 2025-05 · <https://machinelearning.apple.com/research/heart-rate-estimation>  
  原因：增量功能、硬件发布或已收条目的补充材料。检索备注：audio FM transfer; optional
- **Assessing the Feasibility of Large-Scale Digital Sensing for Depression and Anxiety: The Digital Mental Health Study** — 苹果 · 2025-12 · <https://machinelearning.apple.com/research/digital-mental-health>  
  原因：增量功能、硬件发布或已收条目的补充材料。检索备注：study result; optional data-asset context
- **Garmin announces nutrition tracking in Garmin Connect (AI food logging, Connect+)** — Garmin · 2026-01-05 · <https://www.garmin.com/en-US/newsroom/press-release/sports-fitness/stay-on-top-of-nutrition-goals-in-garmin-connect/>  
  原因：增量功能、硬件发布或已收条目的补充材料。检索备注：incremental to Connect+ entry
- **KAI 12L new determinations, total 39** — AliveCor · 2026-01-13 · <https://alivecor.com/press/press_release/alivecor-announces-fda-clearance-new-cardiac-determinations-kardia-12l-ecg-system>  
  原因：增量功能、硬件发布或已收条目的补充材料。检索备注：incremental
- **Stelo adds enhanced Smart Meal Logging** — Dexcom · 2026-02-04 · <https://investors.dexcom.com/news/news-details/2026/Stelo-Adds-Enhanced-Smart-Meal-Logging-Features-as-Dexcom-Continues-to-Transform-Personal-Glucose-Management/default.aspx>  
  原因：增量功能、硬件发布或已收条目的补充材料。检索备注：incremental to Dec 2024 GenAI entry
- **How New FDA Guidance Unlocks Innovation at Oura** — Oura · 2026-02-10 · <https://ouraring.com/blog/new-fda-guidance/>  
  原因：监管背景资料。检索备注：regulatory context
- **Foundation Models Defining A New Era In Sensor-based Human Activity Recognition: A Survey And Outlook** — 学术 · 2026-04-03 · <https://arxiv.org/abs/2604.02711>  
  原因：综述/立场类，作参考文献来源，不单列条目
- **Galaxy Watch Ultra2 and Watch9: Your Health Companion on the Wrist** — 三星 · 2026-07-22 · <https://news.samsung.com/global/samsung-galaxy-watch-ultra2-and-watch9-your-health-companion-on-the-wrist>  
  原因：增量功能、硬件发布或已收条目的补充材料。检索备注：hardware launch; optional
- **Review of open foundation models and datasets for ECG and PPG waveforms** — 学术 · 2026-08-07 · <https://doi.org/10.1038/s41746-026-03101-7>  
  原因：综述/立场类，作参考文献来源，不单列条目
- **Apple Watch Series 12 with all-new Health Sensing System** — 苹果 · 2026-09-09 · <https://www.apple.com/newsroom/2026/09/introducing-apple-watch-series-12-with-the-all-new-health-sensing-system/>  
  原因：增量功能、硬件发布或已收条目的补充材料。检索备注：hardware/data-asset change paired with Apple Intelligence Health app (existing 2026-09-09 entry)
- **FDA-cleared advanced AI | Zio ECG monitors** — iRhythm · — · <https://www.irhythmtech.com/us/en/solutions-services/fda-cleared-ai>  
  原因：增量功能、硬件发布或已收条目的补充材料。检索备注：supporting source
