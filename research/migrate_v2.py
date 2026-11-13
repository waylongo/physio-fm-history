#!/usr/bin/env python3
"""第二版数据增改（2026-11-13）。幂等：按 id 新增或覆盖条目、修改关系。
JSON（data/*.json）是唯一数据源；本脚本只是这次增改的记录，重复运行结果不变。"""
import json as _j, os as _o
if _j.load(open(_o.path.join(_o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))), 'data/meta.json'))).get('dataVersion', 0) >= 5:
    print('数据已是第五版（做过减法），历史迁移不再运行'); raise SystemExit(0)
import json, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(root, 'data/entries.json')
D = json.load(open(P)); E = D['entries']; BY = {e['id']: e for e in E}

def era(d):
    if d < '2023-12': return 'e0'
    if d < '2024-06': return 'e1'
    if d < '2025-07': return 'e2'
    if d < '2026-01': return 'e3'
    return 'e4'

def up(**k):
    k.setdefault('sources', []); k.setdefault('links', [])
    k['era'] = era(k['date'])
    if k['era'] == 'e0': k['prelude'] = True
    if k['id'] in BY: BY[k['id']].clear(); BY[k['id']].update(k)
    else: E.append(k); BY[k['id']] = k

def L(f, t, n): return {"from": f, "type": t, "note": n}

def relink(eid, links):
    BY[eid]['links'] = links

def addlink(eid, link):
    ls = BY[eid]['links']
    ls[:] = [x for x in ls if x['from'] != link['from']] + [link]

def droplink(eid, frm):
    BY[eid]['links'] = [x for x in BY[eid]['links'] if x['from'] != frm]

# ================= 前奏 =================
up(id="clocs", date="2020-05-27", dateLabel="arXiv 2020-05；ICML 2021", track="signal", org="oxford", type="paper",
   title="CLOCS: Contrastive Learning of Cardiac Signals Across Space, Time, and Patients",
   short="CLOCS：跨时间、导联与病人的心电对比学习", url="https://arxiv.org/abs/2005.13249",
   q="医院里有大量没有标注的心电，能否不靠标签先学到有用的表征？",
   how="提出一族对比学习方法，让同一病人在不同时间段、不同导联上的心电表征彼此靠近；论文报告线性评估与微调均优于 BYOL、SimCLR，只用 25% 标注也能泛化。",
   shift="较早把“同一个病人”当作对比学习的正样本来源，并指出学到的表征天然带有病人特异性，可用来度量病人相似度。后来“以人为锚”的思路在这里已有雏形（编者归类）。")
up(id="huawei-heart", date="2019-09-02", dateLabel="JACC 在线 2019-09-02（刊期 2019-11）", track="signal", org="huawei", orgNote="与解放军总医院等合作", type="paper",
   title="Mobile Photoplethysmographic Technology to Detect Atrial Fibrillation (Huawei Heart Study)",
   short="华为心脏研究：手环/手表 PPG 房颤筛查", url="https://doi.org/10.1016/j.jacc.2019.08.019",
   sources=[{"label": "PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov/31487545/"}],
   q="国产可穿戴设备的 PPG，能否在中国人群规模上筛查房颤？",
   how="187,912 名使用华为/荣耀 PPG 设备的参与者；对疑似房颤者随访确诊。论文报告 PPG 信号的阳性预测值为 91.6%，随访的 262 人中 227 人确诊。",
   shift="与 Apple Heart Study 同年发表，说明中国厂商同样有人群规模的远程研究能力。华为后来把“研究 App + 医院合作”做成长期平台，这是它最主要的数据资产（编者解读）。")
addlink("p-ahs2019", L("huawei-heart", "并行", "同年、同一问题：消费级 PPG 的人群级房颤筛查"))
up(id="biot", date="2023-05-10", dateLabel="arXiv 2023-05（附代码与预训练模型）", track="signal", org="uiuc", type="open",
   title="BIOT: Cross-data Biosignal Learning in the Wild", short="BIOT：把异构生物信号变成统一“句子”",
   url="https://arxiv.org/abs/2305.10351", sources=[{"label": "GitHub", "url": "https://github.com/ycq091044/BIOT"}],
   q="EEG、ECG 等生物信号的通道数、长度、缺失各不相同，能否像语言模型那样跨数据集联合预训练？",
   how="把每个通道切成固定长度片段，拼成统一的“生物信号句子”，再加通道嵌入与相对位置嵌入；在 EEG、ECG 与活动传感数据上评测，并公开代码与预训练模型。",
   shift="给出“先统一分词，再跨数据集预训练”的配方。EEG 大模型沿着这条路走下去；它要解决的通道异构问题，后来在可穿戴设备的跨布局迁移中再次出现（编者解读）。")
relink("labram", [L("biot", "继承", "同样把多源 EEG 切成通道片段做跨数据集预训练，改用神经分词器与掩码预测（编者解读）")])
up(id="google-fewshot", date="2023-05-24", dateLabel="arXiv 2023-05", track="agent", org="google", type="paper",
   title="Large Language Models are Few-Shot Health Learners", short="LLM 是少样本健康学习者",
   url="https://arxiv.org/abs/2305.15525",
   q="通用 LLM 只读文本，能否直接读心率、步数这类数值序列做健康推断？",
   how="对 LLM 做少样本微调，让它直接接收可穿戴与医疗传感器的生理和行为时序；在心脏信号分析、活动识别、能量消耗计算、压力与心理量表估计等任务上评测。",
   shift="最早把“让语言模型直接读传感器数值”作为研究问题提出，是谷歌“语言 × 可穿戴”研究线的起点。半年后的 Health-LLM（McDuff 同为作者）把它系统化（编者解读）。")
addlink("health-llm", L("google-fewshot", "继承", "同一问题的系统化评测（McDuff 同为作者）"))
up(id="fitbit-acq", date="2019-11-01", dateLabel="宣布 2019-11-01；完成 2021-01-14", track="param", org="google", type="announce",
   title="Google completes Fitbit acquisition", short="谷歌收购 Fitbit：买下数据入口",
   url="https://blog.google/products/devices-services/fitbit-acquisition/",
   sources=[{"label": "2019 宣布", "url": "https://blog.google/products/hardware/agreement-with-fitbit/"}],
   q="谷歌要做可穿戴健康，缺的是设备、用户和长期数据。",
   how="2019-11 宣布收购 Fitbit，2021-01-14 完成。",
   shift="它本身不是模型。但谷歌博客写明，LSM 的数据来自佩戴 Fitbit Sense 2 或 Pixel Watch 2 并同意用于研发的用户，SensorFM 覆盖 20 多款 Fitbit 与 Pixel Watch 设备；Fitbit App 也成了健康教练的落地入口。谷歌的数据资产靠收购获得，苹果的靠自建研究队列，路径不同（编者解读）。")
addlink("lsm", L("fitbit-acq", "奠基", "预训练数据来自经同意的 Fitbit / Pixel Watch 用户"))
relink("p-ahms2019", [])
BY["apple-iclr24"]["links"] = [x if x["from"] != "p-ahms2019" else L("p-ahms2019", "奠基", "约 14 万名 AHMS 参与者的手表 PPG/ECG 是预训练数据") for x in BY["apple-iclr24"]["links"]]
addlink("apple-iclr24", L("clocs", "继承", "同样用“同一个人”的不同片段构造正样本，从临床心电搬到消费级手表（编者解读）"))

# ================= 起点期 2023.12–2024.05 =================
up(id="hear", date="2024-03-04", dateLabel="arXiv 2024-03；后作为 HAI-DEF 开放模型发布", track="signal", org="google", type="open",
   title="HeAR – Health Acoustic Representations", short="HeAR：咳嗽与呼吸声的基础模型",
   url="https://arxiv.org/abs/2403.02522",
   sources=[{"label": "谷歌博客 2024-08", "url": "https://blog.google/innovation-and-ai/technology/health/ai-model-cough-disease-detection/"},
            {"label": "HAI-DEF 模型页", "url": "https://developers.google.com/health-ai-developer-foundations/hear"}],
   q="咳嗽、呼吸声里有健康信号，但现有模型多是单任务、数据少。",
   how="用掩码自编码器在 3.13 亿段 2 秒音频上自监督训练，在 6 个数据集、33 项健康声学任务上用线性探针评测；后来作为谷歌 Health AI Developer Foundations 的一员开放。",
   shift="把“自监督 + 线性探针”的配方复制到声音这一模态。生理基础模型的边界从光学和电信号扩展到声学（编者解读）。")
up(id="siamquality", date="2024-04-26", dateLabel="arXiv 2024-04；Physiological Measurement 2024-08", track="signal", org="emory", type="paper",
   title="SiamQuality: A ConvNet-Based Foundation Model for Imperfect Physiological Signals", short="SiamQuality：把差质量 PPG 变成监督",
   url="https://doi.org/10.1088/1361-6579/ad6747", sources=[{"label": "arXiv", "url": "https://arxiv.org/abs/2404.17667"}],
   q="真实 PPG 噪声大、质量参差，而大模型通常依赖干净数据。",
   how="在 ICU 患者 PPG 上，让来自相近生理状态的好质量与差质量信号表征彼此靠近；用 CNN 在 3,600 多万对 30 秒 PPG 上预训练，在 6 个外部下游任务上评测。",
   shift="把“信号质量差”从要剔除的噪声变成自监督的配对来源，也说明 CNN 可以做生理基础模型的骨干。同组一年后推出生成式的 GPT-PPG（编者据作者重合判断）。",
   links=[L("apple-iclr24", "并行", "同期的 PPG 预训练，数据来自 ICU 而非消费级手表")])
up(id="sleepfm", date="2024-05-28", dateLabel="arXiv 2024-05；扩展版 Nature Medicine 2026-01-06", track="signal", org="stanford", type="open",
   title="SleepFM: Multi-modal Representation Learning for Sleep Across Brain Activity, ECG and Respiratory Signals", short="SleepFM：多导睡眠图的多模态基础模型",
   url="https://arxiv.org/abs/2405.17766",
   sources=[{"label": "Nature Medicine 2026", "url": "https://doi.org/10.1038/s41591-025-04133-4"}, {"label": "GitHub", "url": "https://github.com/rthapa84/sleepfm-codebase"}],
   q="多导睡眠图同时记录脑电、心电和呼吸，能否学到一个统一的睡眠表征？",
   how="整理 1.4 万多名参与者、10 万多小时多导睡眠数据，用“留一模态”对比学习对齐各模态；论文报告其嵌入在睡眠分期与睡眠呼吸障碍检测上优于端到端 CNN。2026 年 Nature Medicine 版本（A multimodal sleep foundation model for disease prediction）转向疾病预测。",
   shift="把跨模态对比从两两配对推广到“留一模态”，并把睡眠模型的目标从分期推到疾病预测（编者解读）。")
up(id="apple-vitals", date="2024-06-10", dateLabel="WWDC 2024 公布（watchOS 11）", track="param", org="apple", type="product",
   title="Vitals app（watchOS 11）", short="Vitals：夜间个人基线与异常提示",
   url="https://www.apple.com/newsroom/2024/06/watchos-11-brings-powerful-health-and-fitness-insights/",
   q="单次读数意义有限。手表能否判断“今晚这个人和平时不一样”？",
   how="汇总睡眠期间的心率、呼吸率、手腕温度、睡眠时长与血氧，与个人常规范围比较，两项以上超出时提醒；官方称分类与提醒算法基于 Apple Heart and Movement Study 的真实世界数据开发。",
   shift="AHMS 第一次明确支撑参数层的个体基线产品。思路与 ICLR 2024 一致：先知道这个人平常什么样（编者解读）。",
   links=[L("p-ahms2019", "奠基", "官方称算法基于 AHMS 真实世界数据开发")])
up(id="amie", date="2024-01-11", dateLabel="arXiv 2024-01", track="agent", org="google", type="paper",
   title="Towards Conversational Diagnostic AI (AMIE)", short="AMIE：会问诊的对话 Agent",
   url="https://arxiv.org/abs/2401.05654",
   q="AI 能否像初级保健医生一样问诊？",
   how="以 LLM 为基础，用自博弈的模拟问诊环境扩展训练；在 149 个病例场景的随机双盲文字问诊中与 20 名初级保健医生比较，专科医生评价的 32 个维度中有 28 个更优。",
   shift="谷歌的“临床对话”Agent 线，与 PH-LLM、PHIA、PHA 的“个人数据”Agent 线平行发展。2026 年 Fitbit 教练接入病历后，两条线在产品形态上开始靠拢（编者解读）。")

# ================= 第二章 2024.06–2025.06 =================
up(id="ecg-fm", date="2024-08-09", dateLabel="arXiv 2024-08；JAMIA Open 2025-10", track="signal", org="uhn", type="open",
   title="ECG-FM: An Open Electrocardiogram Foundation Model", short="ECG-FM：开源权重的心电基础模型",
   url="https://arxiv.org/abs/2408.05178",
   sources=[{"label": "JAMIA Open", "url": "https://doi.org/10.1093/jamiaopen/ooaf122"}, {"label": "GitHub", "url": "https://github.com/bowang-lab/ECG-FM"}],
   q="开源权重的 ECG 基础模型很少，研究之间难以比较。",
   how="用对比与生成混合的自监督，在 150 万份 ECG 上预训练 Transformer；公开代码、权重与 MIMIC-IV-ECG 基准任务。论文报告房颤 AUROC 0.996、LVEF≤40% AUROC 0.929。",
   shift="ECG 一侧的开放基线。临床 ECG 的数据量远大于可穿戴，这类模型后来成为“ECG 教 PPG”路线的老师来源（编者解读）。")
up(id="ecgfounder", date="2024-10-05", dateLabel="arXiv 2024-10；NEJM AI 2025-09", track="signal", org="pku", orgNote="训练数据为 Harvard-Emory ECG Database", type="open",
   title="An Electrocardiogram Foundation Model Built on over 10 Million Recordings (ECGFounder)", short="ECGFounder：千万级专家标注心电",
   url="https://doi.org/10.1056/aix2500913",
   sources=[{"label": "arXiv", "url": "https://arxiv.org/abs/2410.04133"}, {"label": "GitHub", "url": "https://github.com/PKUDigitalHealth/ECGFounder"}],
   q="ECG 模型样本量不足、跨场景泛化差，单导联与多导联之间性能差距大。",
   how="用心内科专家标注的 1,000 多万份 ECG（150 类标签）训练通用模型，并扩展到任意单导联；论文报告内部验证中 80 种诊断 AUROC 超过 0.95，面向移动监测场景。",
   shift="与自监督路线不同，它用大规模专家标注训练“有监督的基础模型”，并把单导联（可穿戴形态）当作一等公民。同一北大团队随后做出 ECG 引导的 AnyPPG（编者据代码仓库归属判断）。",
   links=[L("p-hannun2019", "继承", "同样依赖大规模专家标注，从单任务扩展到 150 类的通用模型")])
addlink("anyppg", L("ecgfounder", "继承", "同一北大团队，用 ECG 侧能力引导 PPG 表征"))
addlink("papagei", L("ecg-fm", "并行", "同期开放权重的心血管信号模型（PPG 与 ECG）"))
up(id="hubert-ecg", date="2024-11-18", dateLabel="medRxiv 2024-11（附模型与代码）", track="signal", org="brescia", type="open",
   title="HuBERT-ECG: a self-supervised foundation model for broad and scalable cardiac applications", short="HuBERT-ECG：三种规模的自监督心电模型",
   url="https://doi.org/10.1101/2024.11.14.24317328",
   q="ECG 基础模型大多只在节律、传导类任务上评测，它的临床用途是否更广？",
   how="在来自四个国家的 910 万份 12 导联 ECG 上自监督预训练（名称取自语音模型 HuBERT），提供三种模型规模；在 21 个独立数据集、1,600 多个诊断与预后目标上微调评测（据 medRxiv 摘要）。",
   shift="把“规模”变成显式变量，并把评测从心律扩展到预后。ECG 基础模型的竞争从“谁更大”转向“评得多广”（编者解读）。",
   links=[L("ecg-fm", "并行", "同期开放的 ECG 基础模型")])
up(id="sensorllm", date="2024-10-14", dateLabel="arXiv 2024-10；EMNLP 2025", track="signal", org="unsw", type="open",
   title="SensorLLM: Aligning Large Language Models with Motion Sensors for Human Activity Recognition", short="SensorLLM：运动传感器与 LLM 对齐",
   url="https://arxiv.org/abs/2410.10624", sources=[{"label": "GitHub", "url": "https://github.com/zechenli03/SensorLLM"}],
   q="LLM 不擅长读数值时序。能否不靠人工标注，让它读懂运动传感器？",
   how="两阶段：先把传感器输入与自动生成的趋势描述对齐（用特殊标记分隔通道），再针对活动识别做任务微调。",
   shift="“传感器—语言对齐”的早期学术版本，比谷歌 SensorLM 早约 8 个月；两者都用自动生成的文字描述代替人工标注（编者对比）。",
   links=[L("health-llm", "转向", "从把数值写进提示词，改为先对齐表征")])
addlink("sensorlm", L("sensorllm", "并行", "同为自动生成文字描述的传感器—语言对齐"))
up(id="cgm-lsm", date="2024-12-12", dateLabel="arXiv 2024-12", track="world", org="jhu", type="paper",
   title="A Large Sensor Foundation Model Pretrained on Continuous Glucose Monitor Data for Diabetes Management (CGM-LSM)", short="CGM-LSM：160 万条血糖记录的自回归模型",
   url="https://arxiv.org/abs/2412.09727",
   q="血糖预测模型多为单任务，跨人群泛化差。",
   how="仿照语言模型的自回归范式，在 160 万条 CGM 记录上预训练 Transformer 解码器，预测未来 2 小时血糖；论文报告 1 小时预测 RMSE 降低 48.51%，在留出人群上零样本表现稳定。",
   shift="与 GluFormer 同期，把“预测下一个 token”用到血糖上。生成式时序模型成为代谢方向世界模型的第一步（编者解读）。",
   links=[L("gluformer", "并行", "同期的 CGM 生成式预训练")])
up(id="cbramod", date="2024-12-10", dateLabel="arXiv 2024-12；ICLR 2025", track="signal", org="zju", type="open",
   title="CBraMod: A Criss-Cross Brain Foundation Model for EEG Decoding", short="CBraMod：按空间与时间分解的 EEG 模型",
   url="https://arxiv.org/abs/2412.07236", sources=[{"label": "GitHub", "url": "https://github.com/wjq-learning/CBraMod"}],
   q="EEG 的空间（电极之间）与时间依赖性质不同，统一建模会忽略这一点；各数据集电极格式也不一。",
   how="十字交叉 Transformer 用两路并行注意力分别建模空间与时间，配合可适配不同电极布局的非对称条件位置编码；做掩码重建预训练，在 10 类脑机接口任务、12 个公开数据集上评测。",
   shift="EEG 基础模型从照搬语言模型，转向按信号结构设计骨干。可穿戴一侧的 HiMAE、xMAE 也在“尊重信号结构”（编者解读）。",
   links=[L("labram", "继承", "同为跨数据集 EEG 基础模型，改为分解空间与时间注意力")])
up(id="google-lop", date="2025-02-26", dateLabel="Nature 2025-02-26；Pixel Watch 3 功能", track="signal", org="google", type="product",
   title="Automated loss of pulse detection on a consumer smartwatch（Pixel Watch 3）", short="Pixel Watch 3：脉搏丢失检测",
   url="https://doi.org/10.1038/s41586-025-08810-9",
   sources=[{"label": "谷歌博客 2025-03-20", "url": "https://research.google/blog/loss-of-pulse-detection-on-the-google-pixel-watch-3/"}],
   q="无人目击的心脏骤停几乎无法存活，手表能否“替人目击”？",
   how="多级门控：PPG 交流分量骤降且加速度静止 → 机器学习模型判断有脉到无脉的转变 → 用额外 LED 与光电管复核 → 两次无响应后自动呼叫急救，全部在手表端运行。训练数据用止血带阻断手腕血流来模拟无脉；博客称日常佩戴测试中 21 人年以上仅 1 次误呼叫。",
   shift="单任务路线的高峰：数据靠巧妙的实验设计而非大规模预训练获得，强调可审计的多级门控与极低误报。今天的监管级与安全功能，大多仍由这类专门模型完成（编者解读）。")
up(id="gpt-ppg", date="2025-03-11", dateLabel="arXiv 2025-03；Physiological Measurement 2025-06", track="signal", org="emory", type="paper",
   title="GPT-PPG: A GPT-based Foundation Model for Photoplethysmography Signals", short="GPT-PPG：生成式 PPG 基础模型",
   url="https://doi.org/10.1088/1361-6579/add988", sources=[{"label": "arXiv", "url": "https://arxiv.org/abs/2503.08015"}],
   q="PPG 模型能否像 GPT 一样生成，而不只是分类？",
   how="把 GPT 架构改造成适合连续 PPG 的形式，在 2 亿多段 30 秒 PPG 上预训练，再用多种监督微调适配房颤检测等任务；不需微调即可做去噪等生成任务。",
   shift="PPG 走上生成式路线。从“生成波形”到“预测未来波形”，是通往信号级世界模型的一步（编者解读）。",
   links=[L("siamquality", "继承", "同一研究组，从对比式转向生成式预训练")])
up(id="healthbench", date="2025-05-13", dateLabel="arXiv 与博客 2025-05", track="agent", org="openai", type="paper",
   title="HealthBench: Evaluating Large Language Models Towards Improved Human Health", short="HealthBench：262 名医生写的健康对话评测",
   url="https://arxiv.org/abs/2505.08775", sources=[{"label": "OpenAI 博客", "url": "https://openai.com/index/healthbench/"}],
   q="健康对话的好坏无法用选择题衡量。怎样评测 LLM 在真实健康对话中的表现与安全？",
   how="5,000 段多轮对话，由 262 名医生撰写 48,562 条评分标准；同时发布 Consensus 与 Hard 两个子集。",
   shift="OpenAI 先建评测，半年后推出 ChatGPT Health。“先有尺子，再做产品”是通用 AI 公司进入健康领域的典型路径（编者解读）。")
relink("chatgpt-health", [L("healthbench", "落地", "评测先行，随后推出面向用户的健康产品（编者解读）"),
                          L("p-whoopcoach", "转向", "2023 年 OpenAI 为 WHOOP 提供模型；2026 年自己做面向用户的健康入口")])
up(id="oura-dexcom", date="2024-11-19", dateLabel="宣布 2024-11-19；随后 Oura App 上线 Stelo 血糖集成（美国）", track="param", org="oura", orgNote="与 Dexcom 合作，Dexcom 投资 7,500 万美元", type="announce",
   title="Dexcom and ŌURA Announce Strategic Partnership", short="Oura × Dexcom：把血糖接进戒指",
   url="https://investors.dexcom.com/news/news-details/2024/Dexcom-and-URA-Announce-Strategic-Partnership/default.aspx",
   sources=[{"label": "Oura 代谢健康博客", "url": "https://ouraring.com/blog/introducing-metabolic-health/"}],
   q="戒指能测睡眠、压力和活动，却测不到代谢，怎样补上？",
   how="Dexcom 投资 7,500 万美元并与 Oura 合作；双方数据互通，美国 Gen3 与 Ring 4 用户可在 Oura App 中查看 Stelo 血糖，与睡眠、压力、活动和饮食放在一起。",
   shift="设备公司用合作补齐自己没有的传感模态，数据资产从“单设备”变成“多源拼合”。WHOOP（化验）、Ultrahuman（血检 + CGM）后来走了同一条路（编者解读）。")
addlink("dexcom-genai", L("oura-dexcom", "并行", "同期，Dexcom 一边与 Oura 互通数据，一边在 Stelo 上做生成式 AI"))
droplink("dexcom-genai", "p-whoopcoach")
up(id="apple-sleepapnea", date="2024-09-09", dateLabel="发布 2024-09-09（随后获 FDA 许可）", track="signal", org="apple", type="product",
   title="Sleep apnea notifications（Breathing Disturbances，Apple Watch）", short="睡眠呼吸暂停提醒：加速度 + 30 天汇总",
   url="https://www.apple.com/newsroom/2024/09/apple-introduces-groundbreaking-health-features/",
   sources=[{"label": "验证文件", "url": "https://www.apple.com/health/pdf/sleep-apnea/Sleep_Apnea_Notifications_on_Apple_Watch_September_2024.pdf"}],
   q="睡眠呼吸暂停大多未被诊断。手表能否只靠加速度提示风险？",
   how="新指标 Breathing Disturbances 用加速度计捕捉睡眠中与呼吸中断相关的手腕微动；每 30 天分析一次，持续出现中重度迹象时提醒用户就医。",
   shift="苹果此时的监管级功能仍是专门模型：单一传感器、单一病种、长窗口汇总。一年后的高血压提醒保留了“30 天汇总 + 提醒”的形态，但把特征提取换成了自监督基础模型（编者对比）。")
addlink("apple-htn", L("apple-sleepapnea", "继承", "沿用“长窗口汇总 + 风险提醒”的产品形态，特征提取换成自监督 PPG 模型（编者解读）"))
up(id="apple-workout-buddy", date="2025-06-09", dateLabel="WWDC 2025 公布（watchOS 26）", track="agent", org="apple", type="product",
   title="Workout Buddy with Apple Intelligence", short="Workout Buddy：运动中的生成式语音教练",
   url="https://www.apple.com/newsroom/2025/06/watchos-26-delivers-more-personalized-ways-to-stay-active-and-connected/",
   q="运动中的实时数据很多，用户很难边跑边解读。",
   how="用 Apple Intelligence 结合本次运动数据与健身历史生成个性化提示，再由以 Fitness+ 教练声音数据训练的生成式语音播报；2026 年起可脱离 iPhone 使用，并支持西班牙语。",
   shift="苹果第一个生成式“教练”只做运动场景、只讲事实型数据，体现它在 Agent 上的克制：嵌入系统、窄场景、隐私优先（编者解读）。")
addlink("apple-health-app", L("apple-workout-buddy", "继承", "从运动场景的生成式提示扩展到整个健康 App"))
addlink("apple-health-app", L("apple-vitals", "继承", "夜间个人基线与 AHMS 开发的评分逻辑延续到 Readiness"))
up(id="csfm", date="2025-06-23", dateLabel="arXiv 2025-06", track="signal", org="oxford", type="paper",
   title="Sensing Cardiac Health Across Scenarios and Devices: A Multi-Modal Foundation Model Pretrained on Heterogeneous Data from 1.7 Million Individuals (CSFM)", short="CSFM：170 万人的心脏多模态模型",
   url="https://arxiv.org/abs/2507.01045",
   q="临床 ECG、监护 PPG 与文字报告格式各异，模型能否跨场景、跨设备通用？",
   how="用生成式掩码预训练，在 MIMIC-III-WDB、MIMIC-IV-ECG、CODE 等约 170 万人的心脏信号及对应临床或机器生成文字报告上学习统一表征；可随输入配置与传感模态迁移。",
   shift="“跨模态脚手架”的临床大数据版本：ECG、PPG 与文字在同一个模型里共享表征（编者解读）。",
   links=[L("ecg-fm", "并行", "同为大规模临床心电预训练，CSFM 加入 PPG 与文字")])
up(id="samsung-xealth", date="2025-07-08", dateLabel="宣布 2025-07-08", track="agent", org="samsung", type="announce",
   title="Samsung Electronics Acquires Xealth", short="三星收购 Xealth：通往医院的管道",
   url="https://news.samsung.com/global/samsung-electronics-acquires-xealth-bridging-the-gap-between-wellness-and-medical-care",
   q="手表上的健康数据怎样进入医生与医院的工作流？",
   how="三星宣布收购数字健康平台 Xealth；官方称其健康生态将扩展到 500 多家医院与 70 多种数字健康方案。",
   shift="设备公司开始买下“通往临床的管道”。一年后三星 Health Assistant 写明将通过 Xealth 连接临床照护；Oura 收购 Counsel Health 是同一方向（编者解读）。")
addlink("samsung-ha", L("samsung-xealth", "奠基", "官方称将通过 Xealth 连接临床照护"))
up(id="meta-neuralband", date="2025-09-17", dateLabel="发布 2025-09-17（美国 2025-09-30 上市）", track="signal", org="meta", type="product",
   title="Meta Ray-Ban Display with Meta Neural Band", short="Meta Neural Band：sEMG 腕带量产",
   url="https://about.fb.com/news/2025/09/meta-ray-ban-display-ai-glasses-emg-wristband/",
   q="跨人泛化的 sEMG 模型，能否成为量产的交互设备？",
   how="Meta Ray-Ban Display 眼镜随附 Meta Neural Band，用表面肌电把手腕与手指的细微动作转成滚动、点击等指令。",
   shift="生理信号模型最干净的一次“研究 → 产品”：Nature 论文发表约两个月后即成为量产交互设备。用途是交互而不是健康（编者解读）。",
   links=[L("meta-emg", "落地", "跨人泛化的 sEMG 解码进入量产腕带")])
up(id="whoop-labs", date="2025-09-30", dateLabel="上线 2025-09-30（美国）；2025-11-12 化验单上传向全体会员开放", track="agent", org="whoop", type="product",
   title="WHOOP Advanced Labs", short="WHOOP Advanced Labs：化验接入教练",
   url="https://www.whoop.com/us/en/press-center/whoop-launches-clinician-reviewed-advanced-labs/",
   sources=[{"label": "化验单上传 2025-11-12", "url": "https://www.whoop.com/us/en/press-center/whoop-launches-advanced-labs-uploads-us/"}],
   q="一年一次的抽血报告缺少语境，怎样把它和 24 小时连续数据放在一起？",
   how="会员可上传既往化验单，或通过 Quest Diagnostics 预约检测（官方称覆盖 65 项生物标志物）；结果经临床医生审核，再由 WHOOP Coach 结合连续生理数据给出 AI 指导。",
   shift="Agent 的输入从可穿戴指标扩展到血液化验。“化验 + 连续监测”随后成为谷歌、Oura、Ultrahuman、微软等健康 Agent 的共同配置（编者解读）。",
   links=[L("p-whoopcoach", "继承", "教练开始读化验结果")])
addlink("whoop-2026", L("whoop-labs", "奠基", "化验与临床审核流程为医生问诊打下基础"))
up(id="oppo-healthagent", date="2025-07", dateLabel="WAIC 2025 发布（新华网 2025-07-29 报道）", track="agent", org="oppo", type="product",
   title="OPPO AI 健康档案与 AI 健康管家", short="OPPO AI 健康管家与健康档案",
   url="http://www.news.cn/tech/20250729/dd108772aaa44e7988ff06742e1c3cd7/c.html",
   q="体检报告、手表数据、症状记录分散各处，用户看不懂也串不起来。",
   how="据新华网报道，OPPO 健康实验室在 WAIC 2025 发布 AI 健康档案与 AI 健康管家：依托设备监测与大模型，提供医疗报告解读、档案管理、症状自查、健康问答、趋势预警与个性化改善计划。",
   shift="OPPO 的 Agent 层与 PPG 基础模型研究（心脏年龄、HiPPT）同年推进，但公开材料尚未说明两者如何衔接（编者解读）。")
up(id="oura-aha-fm", date="2025-11", dateLabel="AHA 2025 科学年会海报（据 Oura 官方页面；仅题目可核）", track="param", org="oura", type="announce",
   title="Using Oura data for cardiovascular disease detection with a large-scale foundation model", short="Oura：用大规模基础模型检测心血管病",
   url="https://resources.ouraring.com/oura-aha-scientific-sessions-2026",
   q="Oura 是否在训练自己的生理基础模型？",
   how="Oura 官方页面列出其科学团队在 AHA 2025 的三个报告，其中之一题为“Using Oura data for cardiovascular disease detection with a large-scale foundation model”；摘要正文未能核实。",
   shift="这是 Oura 公开材料中唯一直接提到“基础模型”的研究成果：它在 Agent 之外也在补生理模型这一层，方法与规模未知（编者解读）。")

# ================= 第四章 2026 =================
up(id="claude-health", date="2026-01-11", dateLabel="发布 2026-01-11（美国，测试版）", track="agent", org="anthropic", type="product",
   title="Claude for Healthcare：personal health data integrations", short="Claude 接入 Apple Health 与病历",
   url="https://www.anthropic.com/news/healthcare-life-sciences",
   q="个人的化验、病历和可穿戴数据，能否交给通用助手统一解读？",
   how="美国 Claude Pro / Max 用户可授权访问化验与病历（HealthEx、Function 连接器），Apple Health 与 Android Health Connect 集成同周以测试版推出；用于总结病史、解释化验、发现健身与健康指标中的模式、准备就诊问题。官方称不用健康数据训练模型。",
   shift="与 ChatGPT Health 相隔四天发布。通用 AI 公司把“个人健康数据入口”做成标准连接器，设备公司的数据开始被别家的 Agent 读取（编者解读）。",
   links=[L("chatgpt-health", "并行", "同一周、同一形态")])
up(id="ultrahuman-jade", date="2026-02-27", dateLabel="发布 2026-02-27", track="agent", org="ultrahuman", type="product",
   title="Jade by Ultrahuman（real-time biointelligence AI）", short="Ultrahuman Jade：会触发测量的 Agent",
   url="https://cyborg.ultrahuman.com/press-releases/ultrahuman-unveils-ring-pro-with-category-defining-15-day-battery-and-jade-worlds-first-real-time-biointelligence-ai",
   q="健康 Agent 只会回答问题，能否直接在设备上采取行动？",
   how="官方称 Jade 汇总戒指、Blood Vision 血检、M1 CGM 与 Home 环境数据给出实时建议，并能直接启动呼吸练习或触发房颤检测；面向全球用户推出。",
   shift="Agent 从“回答问题”走向“调用设备上的测量与干预功能”，解释层开始直接驱动传感层（编者解读）。",
   links=[L("whoop-labs", "并行", "同样把血检与连续监测合并给 Agent")])
up(id="ms-copilot-health", date="2026-03-12", dateLabel="发布 2026-03-12（美国，分阶段推出）", track="agent", org="microsoft", type="product",
   title="Introducing Copilot Health", short="微软 Copilot Health",
   url="https://microsoft.ai/news/introducing-copilot-health/",
   q="通用助手每天回答大量健康问题，但看不到用户自己的数据。",
   how="在 Copilot 中开辟独立空间，汇总 50 多种可穿戴设备（含 Apple Health、Oura、Fitbit）的活动、睡眠与生命体征，经 HealthEx 接入 5 万多家美国医疗机构的病历，以及 Function 的化验结果；官方称数据不用于模型训练。",
   shift="2026 年一季度，通用 AI 公司的健康 Agent 形态趋同：可穿戴 + 病历 + 化验三类数据、医生参与把关。分野在于有没有自己的设备与生理模型（编者解读）。",
   links=[L("chatgpt-health", "并行", "同类的通用助手健康空间"), L("claude-health", "并行", "同样经 HealthEx、Function 接入病历与化验")])
up(id="ac-jepa", date="2026-04-24", dateLabel="arXiv 2026-04（附代码）", track="world", org="ufmg", type="paper",
   title="Beyond Patient Invariance: Learning Cardiac Dynamics via Action-Conditioned JEPAs", short="超越病人不变性：动作条件的心电动力学",
   url="https://arxiv.org/abs/2604.22618",
   q="“同一病人的不同视图应当相似”这一目标，会不会压制模型本该发现的病理变化？",
   how="论证不变性目标会抹去短暂的病理变化；改用动作条件的 JEPA 世界模型，把疾病发生视为作用在病人潜状态上的转移向量，在 MIMIC-IV-ECG 上预测发病后的心电状态。论文报告低资源下比监督学习高 0.05 以上 AUROC。",
   shift="对“以人为锚”的直接反思：不变性擅长刻画稳定的个体特征，却会把变化本身当作噪声。这为“从表征转向动力学”给出了一个技术理由（编者解读）。",
   links=[L("clocs", "转向", "同为心电上的病人级自监督，把“病人不变”换成“状态转移”（编者解读）")])
up(id="wavesfm", date="2026-05-09", dateLabel="arXiv 2026-05", track="signal", org="google", type="paper",
   title="WavesFM: Hierarchical Representation Learning for Longitudinal Wearable Sensor Waveforms", short="WavesFM：多日原始波形的层级模型",
   url="https://arxiv.org/abs/2605.09173",
   q="波形模型只看短片段，行为模型只看粗特征。能否兼得波形细节与多日动态？",
   how="两阶段自监督：先在 32.4 万人、680 万小时 PPG 与加速度上训练短波形编码器，再在 1 万人、530 万小时数据上训练跨多日的时序编码器；在 58 项人口学、生活方式、疾病与用药任务上评测。",
   shift="谷歌从分钟级指标回到原始波形，用层级结构保留多日动态，补上 LSM 系列放弃的波形细节。苹果从波形走向行为（WBM），谷歌从指标回到波形，两家在“两层兼得”上会合（编者解读）。",
   links=[L("lsm2", "转向", "从分钟级特征回到原始波形"), L("wbm", "并行", "都在回答“波形与长程行为如何兼得”")])
up(id="ecg-wm", date="2026-05-17", dateLabel="arXiv 2026-05", track="world", org="tsinghua", type="paper",
   title="ECG-WM: A Physiology-Informed ECG World Model for Clinical Intervention Simulation", short="ECG-WM：给药后心电的世界模型",
   url="https://arxiv.org/abs/2605.17580",
   q="ECG 模型擅长诊断，却不会回答“用了这个药，心电会怎样变”。",
   how="把生理常微分方程先验经能量正则融入潜扩散动力学，模拟给药等干预后的 ECG 轨迹，并利用扩散采样的随机性评估干预风险及其不确定性。",
   shift="世界模型落到单一器官信号上：动作是药物，状态是心电，机理先验用来抑制生成幻觉。思路上接近苹果 2020 年“机理模型 + 学习”的混合路线（编者解读）。",
   links=[L("p-miller2020", "继承", "机理先验约束学习到的动力学（思路上，编者解读）"), L("ac-jepa", "并行", "同期的动作条件心电动力学")])
up(id="ecg-scaling", date="2026-05-17", dateLabel="arXiv 2026-05", track="signal", org="uppsala", type="paper",
   title="How Do Electrocardiogram Models Scale?", short="心电模型怎样随规模变好？",
   url="https://arxiv.org/abs/2605.17276",
   q="ECG 模型加大参数或数据并不总能带来下游提升，尺度律在心电上成立吗？",
   how="在 230 万份 CODE 心电上预训练 120 多个模型（2 万到 2 亿参数），分开考察架构（ResNet 与 Transformer）与范式（监督与自监督）。结论：监督模型受数据瓶颈，自监督随模型与数据稳健扩展；分布外泛化时 ResNet 的参数效率高 1.3–2.5 倍，自监督的数据效率最高达 16 倍。",
   shift="尺度律在心电上被系统检验，答案不是“越大越好”，而是范式与归纳偏置决定收益（编者解读）。",
   links=[L("lsm", "分岔", "把可穿戴数据上的尺度律问题带到临床心电，并拆开架构与范式")])
up(id="openmhc", date="2026-06-25", dateLabel="arXiv 2026-06（数据向合格研究者开放，代码与权重开源）", track="param", org="stanford", orgNote="与帝国理工等合作", type="open",
   title="OpenMHC: Accelerating the Science of Wearable Foundation Models", short="OpenMHC：十年 MyHeart Counts 数据开放",
   url="https://arxiv.org/abs/2607.16235", sources=[{"label": "项目页", "url": "https://myheartcounts.stanford.edu/openmhc"}],
   q="最大的可穿戴数据集和最好的可穿戴基础模型都不公开，学术界怎么跟进？",
   how="发布 MyHeart Counts 研究 App 十年数据：11,894 名参与者、6,000 多万小时、19 个传感通道、最多 169 个关联变量；同时开源近期可穿戴基础模型的实现，建立下游预测、缺失插补、未来预测三类基准。",
   shift="参数层第一次有了接近企业规模的公开数据与可复现基线，直接回应“私有数据垄断”的问题（编者解读）。",
   links=[L("lsm", "分岔", "把分钟级可穿戴基础模型的研究带到公开数据上")])
up(id="weqa", date="2026-06-16", dateLabel="arXiv 2026-06", track="agent", org="cambridge", orgNote="与谷歌研究院等合作", type="paper",
   title="WEQA: Wearable hEalth Question Answering with Query-Adaptive Agentic Reasoning", short="WEQA：按问题调度模型的可穿戴问答 Agent",
   url="https://arxiv.org/abs/2606.18147",
   q="可穿戴数据的问题千差万别，固定流程或单个基础模型都应付不了。",
   how="LLM 控制器为每个问题生成执行计划，动态调用传感器分析工具与预训练模型，并用外部知识审计回答；在 4 个公开可穿戴数据集上构建基准。论文报告准确率比 LLM 与 Agent 基线高 24%，12 名医学专家与 8 名用户盲评认为更有用、更符合临床。",
   shift="学术界版本的“Agent 调用基础模型”：基础模型从被评测的对象变成被调度的工具（编者解读）。",
   links=[L("pha", "继承", "多工具分工的 Agent 框架")])
addlink("sensorfm", L("weqa", "并行", "同期把基础模型定位为 Agent 的工具"))
up(id="stepfm", date="2026-07-08", dateLabel="arXiv 2026-07", track="param", org="polyu", type="paper",
   title="Physical activities enable scalable foundation modelling for broad-spectrum health prediction (StepFM)", short="StepFM：只用步数的基础模型",
   url="https://arxiv.org/abs/2607.06954",
   q="基础模型一定要高频原始信号吗？最普及、最隐私友好的步数够不够？",
   how="只用步数：在 1.41 亿个分钟级步数观测上预训练 340 万参数的模型，迁移到 20 多项健康风险预测任务，并跨设备、跨地区、跨新病种评测。",
   shift="“层级上移”的极端情形：连心率都不用。它检验的是基础模型的收益来自信号细节，还是来自规模与时序结构（编者解读）。",
   links=[L("lsm", "分岔", "分钟级路线的极简版本：只保留步数")])
up(id="pwm", date="2026-08-15", dateLabel="arXiv 2026-08", track="world", org="fullive", type="paper",
   title="Physiological World Models for Human State Transitions", short="PWM：以事件为条件的人体状态转移",
   url="https://arxiv.org/abs/2608.15309",
   q="健康 AI 多在识别当前状态，怎样系统地建模“发生某件事之后，身体会怎样变”？",
   how="提出事件条件的生理世界模型框架：用“人体状态转移 token”把事件前状态、事件或行动、情境与干预、事件后轨迹、结果和数据质量打包；定义从状态表征到有边界干预规划的四级能力和六类基准任务。",
   shift="一篇框架与议程性质的论文：把“生理世界模型”拆成可验证的能力等级，并明确区分预测与因果推断（编者解读）。",
   links=[L("normwear-wm", "并行", "同年提出的生理世界模型")])
up(id="sensori", date="2026-08-30", dateLabel="arXiv 2026-08", track="signal", org="oxford", type="paper",
   title="Learning Human Health and Diseases from 24-hour Wrist Movement (Sensori)", short="Sensori：一天的腕部运动 → 全表型疾病",
   url="https://arxiv.org/abs/2608.29494",
   q="腕部加速度通常被压缩成几个行为指标，原始的 24 小时运动里还藏着多少健康信息？",
   how="在英国、中国、美国四个人群队列（122,640 人、683,617 人日）的 24 小时原始三轴腕部加速度上自监督训练；与常见临床协变量合用时，102 种现患疾病中 52 种、87 种新发疾病中 26 种的预测显著改善，神经与精神疾病收益最大。",
   shift="牛津大数据研究所从 2024 年的活动识别预训练，走到“一天的运动 → 全表型疾病风险”，加速度模型的目标从识别动作变成刻画健康（编者解读）。",
   links=[L("oxford-ssl", "继承", "同一机构的加速度预训练路线，从活动识别转向疾病预测")])
up(id="pulselm", date="2026-02-10", dateLabel="arXiv 2026-02（数据与代码公开）", track="signal", org="smu", type="open",
   title="PulseLM: A Foundation Dataset and Benchmark for PPG-Text Learning", short="PulseLM：PPG—文本问答数据集",
   url="https://arxiv.org/abs/2603.03331", sources=[{"label": "Hugging Face 数据集", "url": "https://huggingface.co/datasets/Manhph2211/PulseLM"}],
   q="PPG 数据集只有数值标签，无法直接用于语言接口与多模态大模型。",
   how="汇集 16 个公开来源的 PPG，统一为 12 类任务、100 多万段 10 秒 PPG 与近 250 万条问答；公开数据、代码并给出多模态 LLM 基线。",
   shift="PPG—语言对齐有了公开的标准数据集，后来的 PPG—文本模型可以在同一把尺子上比较（编者解读）。",
   links=[L("sensorlm", "分岔", "从分钟级指标的文字对齐，下沉到 PPG 波形与问答")])
up(id="sleepfm2", date="2026-09-06", dateLabel="arXiv 2026-09", track="signal", org="stanford", type="paper",
   title="Learning transferable human physiology from two million hours of sleep with SleepFM-2", short="SleepFM-2：200 万小时睡眠迁移到腕部",
   url="https://arxiv.org/abs/2609.06849",
   q="在临床多导睡眠图上学到的生理表征，能否迁移到更便宜的可穿戴传感器？",
   how="在 26 个队列的 282,511 份多导睡眠图（235,865 份用于预训练，超过 200 万小时）上训练；冻结编码器可迁移到清醒 EEG、头带与耳内 EEG、腕部 PPG 和加速度。结合年龄、性别、BMI，188 个后续病历表型达到预设标准。",
   shift="睡眠模型反过来服务可穿戴：临床信号上学到的表征迁移到腕部 PPG 和加速度，是“贵模态教便宜模态”的另一种形态（编者解读）。",
   links=[L("sleepfm", "继承", "同一斯坦福团队，规模扩大约 20 倍并迁移到可穿戴")])
up(id="ppg-lm", date="2026-09-27", dateLabel="arXiv 2026-09", track="signal", org="emory", orgNote="与 UCLA、谷歌、斯坦福等合作", type="paper",
   title="PPG-LM: A Photoplethysmography–Language Model with Multi-Level Clinical Alignment", short="PPG-LM：片段、事件、就诊三层文本对齐",
   url="https://arxiv.org/abs/2609.33516",
   q="PPG 模型靠任务头输出数字，LLM 的医学知识又不会自动变成波形理解，二者怎样接上？",
   how="从信号测量与结构化病历自动生成片段级、事件级、就诊级三层描述；先做片段—语言对比与波形条件描述，再扩展到事件与就诊级对齐。约 7.3 万小时 PPG 预训练，在 MC-MED、MIMIC-III、VitalDB 上评测。",
   shift="文本监督按时间尺度分层，与同期 OPPO HiPPT 的“按证据范围对齐”不谋而合：语言接口开始讲究“这句话描述的是多长一段信号”（编者对比）。",
   links=[L("pulselm", "并行", "同为 PPG—语言学习，PPG-LM 加入病历语境")])
addlink("hippt", L("ppg-lm", "并行", "同期的分层文本对齐"))
up(id="sla", date="2026-10-06", dateLabel="arXiv 2026-10（数据、代码与模型公开）", track="agent", org="ucla", type="open",
   title="Sensor-Language-Action Models (OpenSLA)", short="传感器—语言—行动模型",
   url="https://arxiv.org/abs/2610.08244", sources=[{"label": "项目页", "url": "https://yang-ai-lab.github.io/OpenSLA"}],
   q="传感器模型大多止步于感知：识别状态、预测结果。能否直接输出“下一步该做什么”？",
   how="以语言作为感知与行动之间的语义接口，构建覆盖 11.6 万多人、79 种传感模态、60 个行动组的基准和自动描述流水线，发布统一模型 OpenSLA，做分层行动预测、状态理解与行动解释。",
   shift="感知、语言、行动第一次在一个传感器模型里统一。Agent 不必在外部拼接模型，行动本身成了模型的输出（编者解读）。",
   links=[L("sensorlm", "继承", "在传感器—语言对齐之上加入行动")])
up(id="ppg-bench", date="2026-10-09", dateLabel="arXiv 2026-10（开源基准）", track="signal", org="mannas", type="open",
   title="PPG-Bench: A Unified Benchmark for PPG Foundation Models", short="PPG-Bench：公平比较下的开源 PPG 模型",
   url="https://arxiv.org/abs/2610.13435",
   q="各家 PPG 基础模型用的数据、任务、下游头和基线都不同，它们到底有多好？",
   how="在 9 个开放数据集、26 项任务上统一评测 5 个公开 PPG 基础模型，对照随机/常数基线、确定性的脉率变异性（PRV）特征和通用时序模型 MOMENT。68 个任务—适配方式组合中，35.3% 没有看到基础模型的实质优势；83.8% 中没有任何 PPG 专用模型同时胜过 PRV 与 MOMENT。",
   shift="作者的结论是：当前公开的 PPG 基础模型还不能宣称学到了通用、可迁移的表征。这与企业在私有大数据上的强结果形成张力，提示数据规模与评测口径仍是关键未知数（编者解读）。",
   links=[L("papagei", "转向", "从再发布一个模型，转向公平评测已有的开源模型")])
up(id="rethink-wm", date="2026-10-13", dateLabel="arXiv 2026-10", track="world", org="griffith", orgNote="与 UCLA、埃默里大学合作", type="paper",
   title="Rethinking World Models for Biosignals", short="反思生物信号世界模型：预测 ≠ 干预",
   url="https://arxiv.org/abs/2610.17510",
   q="能准确预测生理记录的模型，就能用来评估干预吗？",
   how="用“真实的动作”与“因果效应证据”两条要求检视现有生物信号世界模型，指出三个源于生理的瓶颈：动作到效果的可变时滞、模型之外的驱动因素、无干预时的内生演化；提出干预效应验证清单。",
   shift="世界模型一年之内从概念走到被批判性检查，门槛从“预测得准”抬高到“因果上站得住”（编者解读）。",
   links=[L("pwm", "并行", "同为对生理世界模型的议程性讨论")])
up(id="oura-plans", date="2026-11-03", dateLabel="2026-11-03 起逐步推出（英文）", track="agent", org="oura", type="product",
   title="Personalized plans with Oura Advisor", short="Oura Advisor 个性化计划：小步实验",
   url="https://ouraring.com/blog/personalized-plans-with-oura-advisor/",
   sources=[{"label": "Oura 帮助中心", "url": "https://support.ouraring.com/hc/en-us/articles/39512345699219-Oura-Advisor"}],
   q="知道了自己的数据，怎样变成能坚持的行动？",
   how="Advisor 先用睡眠、恢复与活动数据，再追问最多三个生活习惯问题，给出 2–3 个最长 7 天的行动计划；每日打卡，结束时回顾指标变化。官方称睡眠与准备度相关问题改由 Oura 用自身科学与数据训练的模型作答。",
   shift="Agent 从“解释过去”变成“小步实验”：计划、打卡、看数据变化，形成可度量的行为闭环。谷歌 SensorWM 用模拟推演未来，Oura 用真实打卡检验结果（编者对比）。",
   links=[L("oura-advisor", "继承", "同一 Advisor，从问答扩展到计划与打卡")])

# ================= 修正第一版中跨度过大的“并行” =================
relink("samsung-oneui8", [])
relink("oppo-embc2024", [])
BY["meta-emg"]["links"] = [L("apple-iclr24", "分岔", "“多人数据 → 通用模型”换到 EMG 与人机交互；Meta 用的是大规模监督而非自监督")]
relink("himae", [L("lsm", "分岔", "把“建在哪一层”细化为“用哪个时间分辨率”"), L("apple-iclr24", "分岔", "从云端大模型转向手表端小模型")])
relink("apple-passport", [L("apple-accel", "继承", "同一苹果可穿戴模型线"), L("biot", "继承", "通道异构问题的设备版：同一模型适配不同传感器布局（编者解读）")])
# 小修：Oura 女性健康模型的首发时间
BY["oura-womens"]["dateLabel"] = "Oura Labs 首发（TechCrunch 2026-02-24 报道）；官方博客 2026-04-08"
BY["oura-womens"].setdefault("sources", [])
if not any('techcrunch' in s['url'] for s in BY["oura-womens"]["sources"]):
    BY["oura-womens"]["sources"].append({"label": "TechCrunch 2026-02-24", "url": "https://techcrunch.com/2026/02/24/oura-launches-a-proprietary-ai-model-focused-on-womens-health/"})

for e in E:
    e['era'] = era(e['date'])
    if e['era'] == 'e0': e['prelude'] = True
    else: e.pop('prelude', None)
E.sort(key=lambda e: e['date'])
D['updated'] = '2026-11-13'
json.dump(D, open(P, 'w'), ensure_ascii=False, indent=1)
print('entries', len(E))

# v2.1 修正：去掉跨度过长的“并行”，主链接改为 https
for e in E:
    if e['id'] == 'apple-health-app':
        e['links'] = [l for l in e['links'] if l['from'] not in ('wbm', 'whoop-5')]
    if e['url'].startswith('http://www.news.cn/'): e['url'] = 'https://' + e['url'][7:]
json.dump(D, open(P, 'w'), ensure_ascii=False, indent=1)
