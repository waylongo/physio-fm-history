#!/usr/bin/env python3
"""第三版小修（2026-11-13 午后）：SensorWM 细化、审阅意见与补录条目。幂等。JSON 为唯一数据源。"""
import json as _j, os as _o
if _j.load(open(_o.path.join(_o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))), 'data/meta.json'))).get('dataVersion', 0) >= 5:
    print('数据已是第五版（做过减法），历史迁移不再运行'); raise SystemExit(0)
import json, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(root, 'data/entries.json')
D = json.load(open(P)); E = D['entries']; BY = {e['id']: e for e in E}
def L(f, t, n): return {"from": f, "type": t, "note": n}
def src(eid, label, url):
    e = BY[eid]; e.setdefault('sources', [])
    if url not in [s['url'] for s in e['sources']]: e['sources'].append({"label": label, "url": url})

# ---- SensorWM：按博客与 arXiv 核对后细化 ----
w = BY['sensorwm']
w['how'] = ("两部分。其一，“可教练健康年龄”（CHA）：只用可改变的日常行为与生理（静息心率、步数、睡眠时长、每周活跃区间分钟，可选 VO2max 等），"
            "在 All of Us 队列中与 8 年内高血压、心血管病、2 型糖尿病风险相关。其二，SensorWM：在约 10 万名 Fitbit 用户、228 万人周的数据上预训练的动作条件世界模型；"
            "给定两周基线，按步数、睡眠、有氧安排预测 20 个生理指标未来 12 周的变化，再用优化器筛选可行方案，由语言模型生成教练计划。")
w['shift'] = ("四条纲第一次在同一个系统里闭合：参数层信号 → 世界模型推演 → 可修改的健康年龄目标 → Agent 输出计划。博客称其预测优于 TimesFM 等通用时序模型；"
              "盲评中，生活方式教练在 71.4% 的评估里把基于反事实推演的计划选为最佳，医生评定 99.2% 的计划在安全运动强度内。"
              "它仍是研究框架（博客称 investigational），尚非产品功能；预测准确也不等于干预因果成立（编者解读）。")
w['links'] = [
    L("sensorfm", "继承", "同一谷歌可穿戴模型线，由表征转向动作条件的动力学"),
    L("ir-wearme", "奠基", "健康年龄与 CKM 扩展在 WEAR-ME 研究中验证"),
    L("p-nazaret2022", "继承", "个体对行为输入的生理响应，被扩展为可反事实推演的世界模型（编者解读）"),
    L("pha", "继承", "延续谷歌个人健康 Agent 的分工：模型推演，语言模型写计划"),
    L("p-timesfm", "转向", "从通用预测改为以动作为条件"),
    L("normwear-wm", "并行", "同年的另一种生理世界模型：信号级 vs 指标级"),
]
src('sensorwm', '配套研究：CKM 健康年龄（arXiv 2603.27787）', 'https://arxiv.org/abs/2603.27787')
w['dateLabel'] = "arXiv 2026-11-05；谷歌研究博客 2026-11-11"

BY['whoop-5']['shift'] = ("参数层的产品形态从“单项分数”走向“生理年龄”这类综合指标。2026 年苹果在健康 App 中推出 Health Age，"
    "谷歌在研究中提出可教练健康年龄（CHA），OPPO 发表手表心脏年龄（编者对比）。")

MP = os.path.join(root, 'data/meta.json'); M = json.load(open(MP))

# ================= 逻辑审阅（2026-11-13 12:55 版）逐条核对后采纳 =================
R = M['relations']
R['检验'] = {"key": "critique", "color": "#a33b2b", "desc": "对前作的主张做独立评测、复现或批评"}
R['呼应'] = {"key": "echo", "color": "#a8a49c", "desc": "不同时期、无直接承接证据，但问题或思路可对照（编者解读）"}
R['接入'] = {"key": "plug", "color": "#4f6fa0", "desc": "一个模型被另一个系统作为组件或工具调用"}
R['并行']['desc'] = "同期（约一年内）独立出现的相近思路"
M['relationNote'] = "关系线是编者对思想承接的解读，除注明“官方称”或“论文称”外，并非原作者自述。四条纲按条目的主要贡献归类：信号、参数按数据粒度，世界模型、Agent 按能力，后两者的数据可以在任何一层。"
if not any(t['id'] == 'cohort' for t in M['types']):
    M['types'].insert(3, {"id": "cohort", "label": "研究队列/数据集"})
TR = {t['id']: t for t in M['tracks']}
TR['signal']['desc'] = "主要贡献是从原始波形（PPG、ECG、加速度、EEG、EMG、声音）学习可迁移的通用表征。"
TR['param']['desc'] = "主要贡献是在已提取的指标（心率、HRV、睡眠、步数、血糖等）及其组成的行为序列上学习表征。"
TR['world']['desc'] = "主要贡献是建模状态如何随时间、行为与干预演化，用于预测、补全和反事实推演；数据可以在任何一层。通用时序预测模型作为无动作的对照放在这里。"
TR['agent']['desc'] = "主要贡献是把生理理解变成解释、计划与行动，并逐步接入化验、病历与医生；数据可以在任何一层。"

def setlink(eid, frm, typ=None, note=None, delete=False):
    e = BY[eid]; ls = e['links']; cur = [l for l in ls if l['from'] == frm]
    if delete: e['links'] = [l for l in ls if l['from'] != frm]; return
    if cur:
        if typ: cur[0]['type'] = typ
        if note: cur[0]['note'] = note
    else: ls.append(L(frm, typ, note))

# P1 SensorWM（数字已对照 arXiv 摘要与谷歌博客）
w['title'] = "Personalized health coaching via coachable health age and counterfactual wearable trajectories (SensorWM)"
w['how'] = ("先构建“可教练健康年龄”（CHA）：只用静息心率、步数、睡眠时长、活跃区间分钟等可改变的指标，在 WEAR-ME（2,780 人）、All of Us（22,748 人）、纵向 Fitbit（1,464 人）三个队列中与心代谢健康评分一致，"
            "并在年龄、性别、BMI 之外提升心血管与代谢疾病的预后区分。再在约 10 万名 Fitbit 用户、超过 220 万人周的数据上预训练动作条件世界模型 SensorWM：给定两周基线，"
            "按步数、睡眠、有氧安排预测 20 项指标未来 12 周的轨迹（R²=0.664），优于通用时序基础模型；最后由优化器与语言模型 Agent 写成 12 周计划。")
w['shift'] = ("参数层表征、动作条件的动力学、一个可改变的目标（CHA）和语言模型 Agent，第一次在同一个公开系统里串起来（编者所见）；信号纲没有进入，因为输入是周级指标而非波形。"
              "盲评中，持证生活方式教练在 71.4% 的配对里更偏好基于反事实推演的计划，医生判定 99.2% 的这类计划符合安全标准。局限同样清楚：反事实来自观察数据训练的模型，"
              "评测的是计划质量而非健康结局；《Rethinking World Models》要求的干预效应验证尚未完成（编者解读）。")
setlink('sensorwm', 'sensorfm', '继承', "同一谷歌可穿戴研究线；论文未说明是否以 SensorFM 为编码器（编者解读）")
setlink('sensorwm', 'pha', '接入', "世界模型的推演交给语言模型教练 Agent 生成计划")
setlink('sensorwm', 'p-nazaret2022', '呼应', "苹果 2022 年的个体“运动→心率”响应模型，是动作条件生理模型的早期形态；两者无引用承接（编者解读）")
setlink('sensorwm', 'whoop-5', '呼应', "“生理年龄”从展示用的综合分数，变成可以优化的目标")
setlink('sensorwm', 'healthformer', '并行', "都以干预为条件模拟个体轨迹；HealthFormer 用深度表型与营养试验，SensorWM 用可穿戴行为")
setlink('sensorwm', 'rethink-wm', '呼应', "三周前提出的干预效应要求，SensorWM 尚未逐项满足（编者解读）")
setlink('sensorwm', 'oura-plans', '并行', "同一周：Oura 用真实打卡检验计划，谷歌用反事实模拟挑选计划")
setlink('sensorwm', 'samsung-oneui8', '呼应', "同为对行为方案的前瞻推演：三星用睡眠压力 × 昼夜节律的机理模型，谷歌用学习式世界模型")
setlink('sensorwm', 'normwear-wm', delete=True)

# P2 PPG-Bench（核对原文：35.3% 是相对随机/常数基线）
pb = BY['ppg-bench']
pb['how'] = ("在 9 个开放数据集、26 项任务上统一评测 5 个公开 PPG 基础模型（AnyPPG、PaPaGei-S、PaPaGei-P、Pulse-PPG、SigmaPPG），对照随机/常数基线、确定性的脉率变异性（PRV）特征和通用时序模型 MOMENT。"
             "68 个任务—适配方式组合中，35.3% 里基础模型相对随机/常数基线都没有实质优势；83.8% 里没有任何 PPG 专用模型能同时胜过 PRV 与 MOMENT。")
pb['links'] = [L('papagei', '检验', "在统一口径下重新评测已发布的开源 PPG 模型"),
               L('pulse-ppg', '检验', "Pulse-PPG 是 5 个被测模型之一"),
               L('anyppg', '检验', "AnyPPG 是 5 个被测模型之一")]

# P3 新关系类型
setlink('ac-jepa', 'clocs', '检验', "直接批评“病人不变性”目标：它会抹掉短暂的病理变化")
setlink('ac-jepa', 'apple-iclr24', '检验', "同一批评适用于参与者级正样本（编者解读）")
setlink('ecg-scaling', 'lsm', '检验', "把“规模越大越好”放到临床心电上系统检验，并拆开架构与范式")
setlink('rethink-wm', 'normwear-wm', '检验', "用“真实动作 + 因果证据”两条要求检视已有生物信号世界模型（编者解读）")
setlink('rethink-wm', 'ecg-wm', '检验', "同上")
setlink('sensorfm', 'pha', '接入', "官方把 SensorFM 定位为个人健康 Agent 的数据接地工具")
setlink('chatgpt-health', 'healthbench', '奠基', "HealthBench 是产品的评测基础（编者解读）")

# P4 下调证据不足的边
setlink('lsm', 'p-timesfm', '呼应', "同为时序基础模型；LSM 是掩码重建的表征模型，不是 TimesFM 式零样本预测的特化")
setlink('anyppg', 'apple-accel', '并行', "同为“贵模态当老师”的跨模态预训练，对象换成 ECG→PPG")
setlink('anyppg', 'papagei', delete=True)
setlink('health-llm', 'p-whoopcoach', delete=True)
setlink('delphi', 'gluformer', '呼应', "同为生成式健康轨迹，对象不同（病历事件 vs 血糖）")
setlink('ecg-wm', 'p-miller2020', '呼应', "同为机理先验约束学习到的动力学；无引用承接（编者解读）")
setlink('mira', 'chronos', '分岔', "从通用时序基础模型分出医疗特化与连续时间动力学")
setlink('himae', 'apple-iclr24', delete=True)
setlink('pulse-ppg', 'apple-relcon', '继承', "直接沿用 RelCon 的相对对比学习（Maxwell A. Xu 为两篇共同作者）")

# P6 + 日期口径：按最早公开日期放置
ox = BY['oxford-ssl']; ox['date'] = '2022-06-06'; ox['dateShort'] = '2022.06 / npj 2024'
ox['dateLabel'] = "arXiv 2022-06-06；npj Digital Medicine 2024-04"
ox['shift'] = ("在加速度上较早独立证明“大规模无标签 → 跨数据集、跨设备泛化”（预印本 2022-06，早于苹果 ICLR 2024），与苹果的 PPG/ECG 工作是并行的两条腿。"
               "2026 年同一团队的 Sensori 把目标从识别动作推进到全表型疾病风险（编者解读）。")
src('oxford-ssl', 'arXiv 2206.02909', 'https://arxiv.org/abs/2206.02909')
ox['links'] = []
setlink('apple-iclr24', 'oxford-ssl', '呼应', "同一判断先在加速度上成立：大规模无标签预训练可跨数据集泛化")
me = BY['meta-emg']; me['date'] = '2024-02-28'; me['dateShort'] = '2024.02 / Nature 2025'
me['dateLabel'] = "bioRxiv 2024-02-28；Nature 2025-07-23"
src('meta-emg', 'bioRxiv 预印本', 'https://www.biorxiv.org/content/10.1101/2024.02.23.581779v1')
setlink('meta-emg', 'apple-iclr24', '并行', "同期：“足够多的人换来跨人泛化”，但 Meta 用的是数千人的大规模监督，不是自监督")
BY['meta-neuralband']['shift'] = ("生理信号模型最干净的一次“研究 → 产品”：预印本 2024-02 公开，Nature 论文 2025-07 发表，约两个月后随量产腕带上市（产品研发显然并行进行）。用途是交互而不是健康（编者解读）。")

# P5 归类
BY['oppo-bp2026']['track'] = 'signal'
BY['gluformer']['shift'] = BY['gluformer']['shift'].rstrip('。') + "。注意它是无动作条件的生成式预训练，干预推演要到 2026 年的 HealthFormer。" if '无动作条件' not in BY['gluformer']['shift'] else BY['gluformer']['shift']
BY['p-ahms2019']['type'] = 'cohort'
BY['lsm']['shift'] = ("两个转向：建模对象从原始波形上移到分钟级参数；目标从判别式对比改为掩码重建，模型因此能补全缺失、外推短程。掩码重建不含动作或干预，它为后来的预测任务铺路，但本身不是世界模型（编者解读）。")

# P10 孤立节点
setlink('fitbit-2026', 'amie', '呼应', "接入病历后，个人数据教练开始靠近临床对话 Agent 的形态")
setlink('oura-counsel', 'amie', '呼应', "同属问诊型 Agent，Counsel 已有真人医生兜底")
setlink('hear', 'apple-iclr24', '并行', "同期在声学模态上的大规模自监督")
setlink('apple-htn', 'google-lop', '呼应', "同年两条获许可/安全功能路线：专门模型 + 多级门控 vs. 自监督特征 + 线性头")
setlink('apple-health-app', 'whoop-5', '呼应', "“生理年龄”类综合指标进入两家产品")
setlink('huawei-watch6', 'oppo-healthagent', '呼应', "中国手机/手表厂商的大模型健康助手")
setlink('oura-plans', 'oura-aha-fm', '呼应', "官方称睡眠与准备度问题改由自训模型作答；与 AHA 2025 海报是否同一模型未公开")

# P11 / P12 文字
fa = BY['fitbit-acq']; fa['title'] = "Google to acquire Fitbit（2021-01-14 完成）"
fa['url'], fa['sources'] = "https://blog.google/products/hardware/agreement-with-fitbit/", [{"label": "2021-01-14 完成收购", "url": "https://blog.google/products/devices-services/fitbit-acquisition/"}]
BY['p-whoopcoach']['shift'] = ("Agent 线实际上比基础模型线更早出现。但此时的 LLM 只读汇总指标，背后没有生理基础模型；这个缺口到 2025–2026 年才由谷歌（SensorFM 接入 Agent）等开始补上，WHOOP 自己则到 2026 年才组建基础模型团队（编者解读）。")
BY['hubert-ecg']['shift'] = "把模型规模作为显式变量，并把评测从心律扩展到预后。ECG 基础模型的比较重点开始从“谁更大”转向“覆盖多少临床任务”（编者解读）。"
BY['ms-copilot-health']['shift'] = "到 2026 年一季度，通用 AI 公司的健康 Agent 已经长得差不多：读可穿戴、病历、化验三类数据，由医生把关。区别在于有没有自己的设备和生理模型（编者解读）。"
BY['chatgpt-health']['shift'] = "通用大模型公司直接站到了可穿戴 Agent 的位置上。可穿戴厂商的护城河，从“有没有 LLM”变成“有没有生理模型和连续数据”（编者解读）。"

# ---- meta：脉络补全 ----
TH = {t['id']: t for t in M['threads']}
def add_step(tid, eid, role):
    t = TH[tid]
    if any(x['id'] == eid for x in t['steps']): 
        for x in t['steps']:
            if x['id'] == eid: x['role'] = role
        return
    t['steps'].append({"id": eid, "role": role})
    t['steps'].sort(key=lambda x: BY[x['id']]['date'])
add_step('modality', 'normwear', '多传感器：任意传感器组合共用一个模型')
add_step('modality', 'gpt-ppg', 'PPG：GPT 式生成预训练')
add_step('modality', 'samsung-mmr', 'PPG：小波多尺度掩码重建')
add_step('modality', 'apple-passport', '跨设备：同一模型适配不同传感器布局')
add_step('modality', 'dna-ppg', 'PPG：把血压、心率、血氧作为连续语义写进表征')
add_step('dynamics', 'chronos', '把时序当语言：通用时序模型成为生理预测的基线')
add_step('deploy', 'huawei-trusense', '华为：先把指标测准、测全的多传感器感知平台')
add_step('platform', 'oura-aha-fm', 'Oura 首次公开提到自研“大规模基础模型”（仅海报题目可证）')
add_step('crossmodal', 'sensori', '只用一天的腕部加速度预测全表型疾病：便宜模态本身被推到极限')

def T(id, name, q, problem, approach, changed, unlocked, open_, steps):
    return {"id": id, "name": name, "question": q, "problem": problem, "approach": approach, "changed": changed,
            "unlocked": unlocked, "open": open_, "desc": q, "steps": [{"id": a, "role": b} for a, b in steps]}
NEW = [
 T("data", "数据从哪里来：研究队列、收购与多源拼合",
   "基础模型的前提是大规模、长期、可授权的数据，各家怎么拿到它？",
   "单次临床研究的数据量远不够预训练；消费设备数据量大，但缺标签、缺临床结局。",
   "三条路：自建研究 App 队列（苹果、华为），收购数据入口（谷歌买 Fitbit），把化验、血糖、病历拼进来（Oura × Dexcom、WEAR-ME、WHOOP Labs、Xealth）。",
   "预训练规模从千人级到十万、百万人级；可穿戴数据开始与化验、病历对齐。",
   "无标签预训练（起点论文）、参数层尺度律、跨模态与临床结局验证。",
   "数据集中在少数公司手里，学界只能依赖 OpenMHC、UK Biobank 等公开资源；授权与再利用的边界仍不清楚。",
   [("huawei-heart", "华为：研究 App + 医院网络的房颤筛查"),
    ("p-ahms2019", "苹果：Research App 里的长期研究队列"),
    ("fitbit-acq", "谷歌：直接买下数据入口"),
    ("oura-dexcom", "Oura：通过合作接入血糖"),
    ("ir-wearme", "谷歌：可穿戴 + 常规血检的远程研究"),
    ("samsung-xealth", "三星：收购通往医院的通道"),
    ("whoop-labs", "WHOOP：化验结果进入同一数据账户"),
    ("openmhc", "学术：十年 MyHeart Counts 数据公开"),
    ("oppo-bp2026", "OPPO：65 万人参与的血压研究")]),
 T("healthage", "健康年龄：从描述性指标到可干预的目标",
   "把多项生理指标压缩成一个“年龄”，它能否从描述走向行动？",
   "单项分数难以理解，也难以说明长期风险。",
   "把多项指标或表征映射为生理年龄、心脏年龄，再把它变成可修改、可推演的目标。",
   "2025–2026 年，WHOOP、OPPO、苹果、谷歌先后推出或发表年龄类指标。",
   "长期追踪与教练目标；谷歌把它与世界模型推演结合。",
   "年龄类指标的临床效度与可比性：各家定义不同，彼此无法换算（编者判断）。",
   [("whoop-5", "WHOOP Age：9 项长期健康指标"),
    ("oppo-heartage", "OPPO：PPG 心脏年龄作为血管老化标志物"),
    ("apple-health-app", "苹果：健康 App 中的 Health Age"),
    ("sensorwm", "谷歌：可教练健康年龄 + 世界模型推演")]),
]

OBJ = T("objective", "预训练目标：对比 → 掩码 → 生成 → 动作条件",
   "没有标签时，模型被要求“预测什么”？",
   "自监督的目标决定了表征能回答什么：对比学习擅长“是谁、是否相似”，却难以生成或外推。",
   "从实例与个体对比出发，转向掩码重建与自回归生成，最后把动作或干预作为条件来预测未来潜状态。",
   "同一类数据上，目标函数的变化把模型从“识别”推向“补全、生成、推演”。",
   "缺失补全（LSM-2）、波形生成（GPT-PPG）、血糖轨迹（GluFormer）、反事实推演（SensorWM）。",
   "PPG-Bench 等评测显示，在公开数据上，目标函数之间的差异往往小于数据规模与评测口径带来的差异（编者解读）。",
   [("clocs", "对比：同一病人的片段互为正样本"), ("apple-iclr24", "对比：参与者级正样本"),
    ("siamquality", "对比：好坏质量信号按生理状态配对"), ("labram", "掩码：向量量化分词 + 掩码预测"),
    ("gluformer", "生成：预测下一个血糖读数"), ("lsm", "掩码重建：分钟级多模态"),
    ("apple-relcon", "相对对比：可学习距离代替二分正负"), ("gpt-ppg", "生成：GPT 式 PPG 预训练"),
    ("lsm2", "掩码：把真实缺失纳入目标"), ("himae", "掩码：层级多分辨率"),
    ("samsung-mmr", "掩码：小波时频系数重建"), ("ac-jepa", "动作条件 JEPA：预测转移后的潜状态"),
    ("xmae", "跨模态掩码：带方向的 ECG→PPG 重建"), ("dna-ppg", "软邻域对比 + 连续参数语义"),
    ("sensorwm", "动作条件：以行为预测 12 周轨迹")])
AGE = T("healthage", "生理年龄：从嵌入里的副产品到可教练的目标",
   "怎样把复杂的生理状态压成一个人人看得懂、又能指导行动的数字？",
   "几十项指标和高维嵌入，用户无法理解，也无法比较干预前后。",
   "先发现嵌入编码了年龄，再把“预测年龄与实际年龄之差”做成生物标志物和产品指标，最后只用可改变的指标构建年龄，让它成为优化目标。",
   "“年龄差”成为基础模型、产品与 Agent 之间共用的接口（编者解读）。",
   "心脏年龄作为血管老化标志物；以“降低几岁”为目标的反事实教练。",
   "不同年龄指标之间缺少互相校准；年龄差的变化是否对应真实的风险下降，缺少干预证据。",
   [("apple-iclr24", "发现：自监督嵌入里编码了年龄等人口学信息"), ("whoop-5", "产品：9 项指标算 WHOOP Age 与衰老速度"),
    ("oppo-heartage", "研究：PPG 心脏年龄差作为血管老化标志物"), ("apple-health-app", "产品：Health Age，可纳入化验"),
    ("sensorwm", "目标：只用可改变指标的“可教练健康年龄”，由世界模型优化")])
NEW = [x for x in NEW if x['id'] != 'healthage'] + [AGE, OBJ]
for t in NEW:
    if t['id'] in TH: M['threads'][[x['id'] for x in M['threads']].index(t['id'])] = t
    else:
        # 数据脉络放在最前，健康年龄放在世界模型之后
        idx = 0 if t['id'] == 'data' else [x['id'] for x in M['threads']].index('dynamics') + 1
        M['threads'].insert(idx, t)

# ---- 逻辑审阅：meta 部分 ----
BY['oura-womens']['date'] = '2026-02-24'
TH = {t['id']: t for t in M['threads']}
def set_role(tid, eid, role):
    for x in TH[tid]['steps']:
        if x['id'] == eid: x['role'] = role
def rm_step(tid, eid): TH[tid]['steps'] = [x for x in TH[tid]['steps'] if x['id'] != eid]
TH['person']['steps'] = [x for x in TH['person']['steps'] if x['id'] != 'apple-symbolic']
set_role('person', 'apple-vitals', "产品侧的同一直觉：以这个人平常的范围为参照（规则式，非基础模型）")
rm_step('crossmodal', 'sensori')
TH['dynamics']['changed'] = "模型可以给出个体在不同行为方案下的 12 周生理轨迹，并以可改变的健康年龄为目标，交给语言模型生成计划（SensorWM）；但评测仍停留在预测精度与专家偏好。"
set_role('dynamics', 'p-timesfm', "对照基线：通用时序预测（无动作、无生理先验）")
TH['open']['open'] = "PPG-Bench 显示，多数情况下没有一个开源 PPG 模型能同时胜过简单的 PRV 特征和通用时序模型，三分之一的组合甚至不比随机/常数基线好。是公开数据规模不够、评测口径不同，还是方法本身的问题？仍未回答。"
set_role('open', 'ppg-bench', "公平比较：开源 PPG 模型很少能同时胜过简单特征与通用时序模型")
set_role('open', 'oxford-ssl', "70 万人日加速度，公开预训练模型（预印本早于苹果起点）")
mo = TH['modality']
mo['name'] = "配方外推：大规模预训练走向 EEG、声音、睡眠与肌电"
mo['question'] = mo['desc'] = "“大规模预训练 + 通用表征”的判断，能否在每一种生理信号上成立？"
mo['changed'] = "每种主要生理信号都有了基础模型；但“规模换泛化”不一定要靠自监督（Meta 肌电走的是监督）。"
set_role('modality', 'biot', "先声：统一的“生物信号句子”，早于苹果工作")
set_role('modality', 'meta-emg', "反例式的印证：EMG 靠数千人的大规模监督而非自监督，同样换来跨人泛化")
TH['level']['open'] = "收益来自信号细节，还是来自规模与时序结构？只用步数的 StepFM（2026-07）和用 24 小时原始运动的 Sensori（2026-08）给出了相反方向的证据，还缺同数据、同任务的正面对比。"
add_step('crossmodal', 'apple-symbolic', "独立训练的不同模态模型可线性对齐，分类器跨模型迁移仍保留 95% 以上性能")
add_step('crossmodal', 'dna-ppg', "把血压、心率、血氧作为连续语义当老师")
add_step('level', 'dna-ppg', "把参数当作信号表征的连续语义，两层在表征里接合")
add_step('level', 'sensori', "反方向的极端：24 小时原始加速度预测上百种疾病，说明压缩成指标会丢信息")
for t in M['threads']: t['steps'].sort(key=lambda x: BY[x['id']]['date'])

# ---- 公司卡与叙事（P7、P8、P6、P12） ----
CO = {c['org']: c for c in M['companies']}
g = CO['google']
g['path'] = "收购数据入口 → 分钟级模型与语言对齐 → 多智能体 → Fitbit 教练 → 世界模型；四条纲在 2024–2026 年都有论文，且层与层之间的接口公开"
g['model'] = {"text": "LSM → LSM-2 → SensorFM（参数层），WavesFM（回到波形），SensorLM（语言），SensorWM（世界模型）；Agent 研究线：少样本 → PH-LLM → PHIA → PHA，另有临床对话 AMIE；另有 HeAR 与 TimesFM。",
              "ids": ["lsm", "lsm2", "sensorlm", "wavesfm", "sensorfm", "sensorwm", "hear", "p-timesfm", "google-fewshot", "ph-llm", "phia", "pha", "amie"]}
g['product'] = {"text": "Fitbit 个人健康教练（PHA 研究落地，2026 年接入病历）；Pixel Watch 脉搏丢失检测走专门模型路线。", "ids": ["fitbit-coach", "fitbit-2026", "google-lop"]}
a = CO['apple']
a['model'] = {"text": "被试感知对比（2021）与个体动力学（血糖 2020、运动心率 2022）的先声 → PPG/ECG 起点模型 → 相对对比的运动模型 → PPG 蒸馏进加速度 → 行为模型 WBM → 跨设备、跨模态与多源报告的表征研究。动力学方向停在 2022 年，之后没有公开的世界模型工作。",
              "ids": ["p-miller2020", "p-cheng2021", "p-nazaret2022", "apple-iclr24", "apple-relcon", "apple-accel", "wbm", "apple-symbolic", "apple-passport", "ms-ecg-fm"]}
o = CO['oura']
if 'oura-plans' not in o['model']['ids']:
    o['model']['ids'].append('oura-plans')
    o['model']['text'] = "女性健康专用 LLM（首个自研模型）；Advisor 的睡眠与准备度问题改由自训模型作答（官方称）；AHA 2025 海报提到“大规模基础模型”，细节未公开。"
CO['whoop']['model']['text'] = "WHOOP Coach 使用 OpenAI 模型；2026 年公开招聘 Foundation AI 团队（只有招聘与访谈，尚无论文）。"
Q = {q['id']: q for q in M['questions']}
def cell(qid, era, text, ids):
    for c in Q[qid]['cells']:
        if c['era'] == era: c['text'], c['ids'] = text, ids
cell('sup', 'e1', "同一个人（参与者级正样本）；或同一生理状态（好坏质量信号配对）。", ["apple-iclr24", "siamquality"])
cell('sup', 'e3', "ECG 教 PPG；按时间分辨率分层的掩码重建。", ["anyppg", "himae"])
cell('sup', 'e0', "专家标注；少数工作用生理耦合（心率监督加速度）或“同一病人”做监督；加速度上的大规模自监督已经出现。", ["p-hannun2019", "p-spathis2021", "clocs", "oxford-ssl"])
cell('level', 'e1', "短波形片段，聚合到人。", ["apple-iclr24", "labram"])
cell('level', 'e4', "多日原始波形的层级模型；500 万人的分钟级模型；两个极端：只用步数 vs. 24 小时原始运动。", ["wavesfm", "sensorfm", "stepfm", "sensori"])
cell('ask', 'e4', "接下来会怎样？如果改变行为或用药呢？以及：预测得准，就能拿来指导干预吗？", ["healthformer", "sensorwm", "ecg-wm", "rethink-wm"])
cell('open', 'e0', "私有队列为主；少量公开代码与模型（牛津加速度模型、BIOT）。", ["p-ahms2019", "oxford-ssl", "biot"])
cell('open', 'e1', "公开的睡眠、声音模型；肌电研究以预印本公开。", ["sleepfm", "hear", "meta-emg"])
cell('open', 'e3', "开源的跨模态 PPG 模型。", ["anyppg"])
ER = {e['id']: e for e in M['eras']}
ER['e1']['thesis'] = ("苹果在约 14 万名参与者的手表 PPG/ECG 上做自监督预训练，把同一参与者的两段信号当作正样本，证明没有医学标签也能学到编码人口学与健康状态的表征。"
    "同一时期，“大规模预训练换泛化”的判断也在加速度（牛津，预印本更早）、EEG（LaBraM）、声音（HeAR）、睡眠（SleepFM）、ICU PPG（SiamQuality）和肌电（Meta，监督学习）上各自成立，"
    "它们多是独立工作，目标从对比学习到掩码重建各不相同。语言一侧，Health-LLM 与 AMIE 分别从个人数据和临床问诊起步。")
ER['e3']['thesis'] = ("WBM 回答了“建在波形还是行为上”：两层互补，组合最好。苹果高血压提醒是编者所见第一个写明以自监督基础模型提取特征的获许可功能；Meta 的 sEMG 研究（预印本 2024-02，Nature 2025-07）随量产腕带上市；"
    "三星 HiMAE 把模型做进手表算力；AnyPPG 让 ECG 教 PPG。Agent 从聊天走向多智能体（PHA → Fitbit 教练），并开始接入化验（WHOOP Advanced Labs）和临床通道（三星收购 Xealth）。")
ES = M['essay']
ES[2] = ES[2].replace("PPG-Bench 发现开源 PPG 模型在多数任务上不敌简单的脉率变异性特征或通用时序模型", "PPG-Bench 发现，在 83.8% 的任务—适配组合中，没有任何开源 PPG 模型能同时胜过确定性的脉率变异性特征和通用时序模型 MOMENT，35.3% 的组合里基础模型甚至不比随机/常数基线有实质优势")
ES[3] = ES[3].replace("Meta 的肌电模型则在论文发表两个月后进入量产腕带", "Meta 的肌电模型（预印本 2024-02）则在 Nature 论文发表约两个月后随量产腕带上市")
ES[5] = ("<b>终点暂停在世界模型。</b>“状态如何演化”这条线从苹果 2020 年的机理与学习混合模型开始，经过 GluFormer、CGM-LSM、Delphi-2M 的生成式轨迹，到 2026 年 HealthFormer 的干预模拟、NormWear-2 与 ECG-WM 的信号级动力学。"
    "2026 年 11 月，谷歌 SensorWM 以步数、睡眠、有氧为动作，推演 20 项指标未来 12 周的变化，用可改变的“可教练健康年龄”作目标，再交给语言模型写成计划：参数、世界模型、Agent 三条纲第一次在一个公开系统里接上（编者所见）。"
    "它的证据也划出了下一道门槛：教练更偏好它的计划，但计划能否改善健康，需要前瞻的干预研究来回答，这正是同年《Rethinking World Models》提出的要求。")
ES[6] = ES[6].replace("谷歌是唯一四条纲都有公开工作、且各层接口清楚的一家", "谷歌是唯一在 2024–2026 年四条纲都有论文、且层与层接口公开的一家（苹果的动力学工作停在 2022 年）")
json.dump(M, open(MP, 'w'), ensure_ascii=False, indent=1)

# ================= 事实核查（2026-11-13）核对后采纳 =================
c = BY['p-cheng2021']; c['date'] = '2020-06-30'; c['dateLabel'] = "arXiv 2020-06-30（2007.04871）"; c.pop('dateShort', None)
lb = BY['labram']; lb['date'] = '2024-01-16'; lb['dateLabel'] = "ICLR 2024 录用（OpenReview 2024-01-16）；arXiv 2024-05"
ew = BY['ecg-wm']; ew['org'] = 'oxford'; ew['orgNote'] = "与清华大学、南方科技大学合作"
hw = BY['huawei-watch6']; hw['date'] = '2026-09-02'; hw['dateLabel'] = "全球发布 2026-09-02（慕尼黑）；中国发布 2026-09-07（据报道）"
wh = BY['whoop-2026']
wh['how'] = ("已上线：My Memory 让会员查看和编辑 AI 的个人上下文，Proactive Check-Ins 主动推送建议。已宣布：App 内按需的临床医生视频问诊（官方称 2026 年夏季在美国上线），"
             "以及经 HealthEx 同步电子病历（官方用语为 will support）。")
op = BY['oppo-bp2026']; op['how'] = op['how'].replace("已发出超过 15 万次风险预警", "已向 15 万多名用户发出高血压风险预警")
sq = BY['siamquality']; sq['title'] = "SiamQuality: a ConvNet-based foundation model for photoplethysmography signals"
sq['dateLabel'] = "arXiv 2024-04；Physiological Measurement 2024-08"
ap = BY['apple-passport']; ap['date'] = '2026-06-30'
src('apple-passport', 'arXiv 2607.00249', 'https://arxiv.org/abs/2607.00249')
pl = BY['oura-plans']
pl['how'] = pl['how'].replace("给出 2–3 个最长 7 天的行动计划", "从最多三个建议选项中选定一个计划（一次一个，最长 7 天）")
pl['dateLabel'] = "2026-11-03 起逐步推出（英文）；官方博客 2026-11-10"

def era(d):
    return 'e0' if d < '2023-12' else 'e1' if d < '2024-06' else 'e2' if d < '2025-07' else 'e3' if d < '2026-01' else 'e4'
for e in E:
    e['era'] = era(e['date'])
    if e['era'] == 'e0': e['prelude'] = True
    else: e.pop('prelude', None)
E.sort(key=lambda e: e['date'])
json.dump(D, open(P, 'w'), ensure_ascii=False, indent=1)
M = json.load(open(MP))
for t in M['threads']: t['steps'].sort(key=lambda x: BY[x['id']]['date'])
json.dump(M, open(MP, 'w'), ensure_ascii=False, indent=1)
print('v3 ok', len(E))
