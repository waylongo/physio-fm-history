#!/usr/bin/env python3
"""第五版（2026-11-13 13:05 后）：做减法与梳理逻辑。幂等，按 v2 → v3 → v4 → v5 → build_sources_extra 的顺序运行。
1) 从年谱移出样本量小、支撑不足、重复或偏离主线的条目（写入 research/v5_removed.json，由 build_sources_extra.py 并入“全部来源”）；
2) 13 条脉络合并为 9 条；3) 删去装饰性关系（大部分“呼应”与跨度过大的“并行”）；4) 重写时期要点、主叙事，并让公司卡、问题矩阵与新条目集一致。"""
import json, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(root, 'data/entries.json'); MP = os.path.join(root, 'data/meta.json')
D = json.load(open(P)); E = D['entries']; BY = {e['id']: e for e in E}; M = json.load(open(MP))
def L(f, t, n): return {"from": f, "type": t, "note": n}

S, W, R, O = '样本量小', '支撑不足', '重复', '偏离主线'
REMOVE = {
    'motionprint': ('重复', '设备与佩戴位置异构问题由 Device Passport 承接；本条只是数据集与端侧模型，未进入任何脉络'),
    'apple-llm-fusion': ('偏离主线', '任务是活动识别而非健康，只是语言接口线的旁证'),
 # 样本量小
 'gptcoach': (S, '16 名参与者的实验室研究；教练方法论由后来的 PHA、Fitbit 教练承接'),
 'sonata': (S, '739 人、19 万窗口的小规模预训练；预训练目标的对照意义由 AC-JEPA 等代表'),
 'apple-physiomtl': (S, '小规模 HRV 研究，与后来的个体基线产品没有公开承接'),
 'healthjev': (S, '20 名模拟用户、90 天的模拟基准，非真实可穿戴数据'),
 # 支撑不足：workshop、立场论文、只有题目或招聘的宣布、预印本且尚无后续
 'apple-ecg-denoise': (W, '统计模型而非预训练；与主线没有可证的承接'),
 'apple-ltf': (W, '苹果动力学前史已由 2020 血糖与 2022 运动心率两篇代表'),
 'maeeg': (W, 'workshop 论文；掩码一支由 LaBraM、LSM 代表'),
 'apple-pars': (W, 'workshop 论文，未改变主线'),
 'apple-speech-fm': (W, 'workshop 论文；跨域复用的观察，未有后续'),
 'apple-cpep': (W, 'workshop 论文；同一工作的主会版本 EMBridge 已收录'),
 'apple-xmodal': (W, 'workshop 论文；跨模态机制的证据由正式发表的工作代表'),
 'apple-symbolic': (W, '表征收敛的分析性工作，暂无后续'),
 'beyond-static': (W, '立场论文；“走向动力学”的论证由实际的世界模型条目承担'),
 'ms-waveform-position': (W, '立场论文，没有模型或数据'),
 'pwm': (W, '小团队预印本，与 NormWear-2、HealthFormer 思路重复且证据更弱'),
 'biolt': (W, '2026-11 新预印本，尚无可评估的影响'),
 'sla': (W, '单篇预印本，“感知—语言—行动”统一的说法缺少后续验证'),
 'whoop-fm': (W, '只有招聘页与访谈，没有论文或产品'),
 'oura-aha-fm': (W, '只有会议海报题目，摘要未能核实'),
 'google-biomarker-agent': (W, '研究博客介绍的工具，未有评测论文'),
 'pheno-agent': (W, '预印本中的示例对比，非系统评测'),
 'samsung-galaxyai-watch': (W, 'Energy Score 等综合分，官方未说明模型，与基础模型主线无关'),
 'ultrahuman-jade': (W, '产品介绍较少，未说明模型'),
 # 重复：已有更强的同类条目
 'heartbeit': (R, '临床心电预训练由 ECG-FM、ECGFounder 代表'),
 'hubert-ecg': (R, '与 ECG-FM、ECGFounder 同类'),
 'heartlang': (R, '心电表征同类工作'),
 'opera': (R, '呼吸声基础模型由 HeAR 代表'),
 'reve': (R, 'EEG 基础模型由 LaBraM 代表'),
 'cbramod': (R, 'EEG 基础模型由 LaBraM 代表'),
 'neurolm': (R, 'EEG—语言对齐；“信号 + 语言”由 SensorLM、OpenTSLM 代表'),
 'gpt-ppg': (R, 'PPG 开源模型由 PaPaGei、Pulse-PPG 代表'),
 'samsung-mmr': (R, '三星多尺度思路由 HiMAE 代表'),
 'siamquality': (R, 'PPG 自监督由 PaPaGei、Pulse-PPG 代表'),
 'osf-sleep': (R, '尺度律证据由 LSM、心电尺度律与 Aether 代表'),
 'inertia-1': (R, '加速度预训练由牛津模型与 Sensori 代表'),
 'sleepfounder': (R, '睡眠方向由 SleepFM、SleepFM-2、sleep2vec 代表'),
 'robust-ppg-dolby': (R, '“用贵模态定义监督”由 AnyPPG、xMAE 代表'),
 'soter': (R, '连续时间生成模型，与 NormWear-2 等重复，且以临床波形为主'),
 'dna-ppg': (R, '“参数语义引导 PPG”与 AnyPPG、OPPO 心脏年龄的思路重复'),
 'llm-clin-insights': (R, '与 Health-LLM 同期同题'),
 'gloss': (R, '与 PHIA 同题（LLM 解读个人传感数据）'),
 'pulselm': (R, 'PPG—文本方向由 HiPPT 代表'),
 'ppg-lm': (R, 'PPG—文本方向由 HiPPT 代表'),
 'weqa': (R, 'Agent 调度模型的思路由 PHA 代表'),
 'ms-ecg-fm': (R, '报告对齐心电由 CSFM 代表'),
 'chronos': (R, '通用时序基线由 TimesFM 代表'),
 'abbott-google': (R, '可穿戴 + CGM 合作由 Oura × Dexcom 代表；作为 Google Health app 的补充来源'),
 'garmin-ai': (R, '“AI 解释层进订阅”由 WHOOP、Oura、Dexcom 代表'),
 'chatgpt-health-ga': (R, '已并入 ChatGPT Health 条目的补充来源'),
 # 偏离主线：不涉及可穿戴或生理信号的通用医疗 AI、ICU 模拟
 'amie': (O, '临床问诊 Agent，不读可穿戴数据'),
 'mai-dxo': (O, '基于病例的诊断编排，不涉及可穿戴'),
 'healthbench': (O, '通用健康对话评测，不涉及生理数据'),
 'hanghaomeng': (O, '医院睡眠专科 Agent，不以可穿戴数据为主'),
 'amazon-health-ai': (O, '基于病历与诊所服务，不读可穿戴数据'),
 'amazon-halo': (O, '设备已停产，未涉及模型'),
 'organ-agents': (O, 'ICU 病人数据上的 LLM 模拟，不涉及可穿戴'),
 'healthflux': (O, 'UK Biobank 病历、化验与影像，不含可穿戴信号'),
 'mira': (O, 'ICU/EHR 时序，非可穿戴'),
}
# 先把要并入的来源挂好
def src(eid, label, url):
    e = BY.get(eid)
    if e and url not in [s['url'] for s in e.get('sources', [])]: e.setdefault('sources', []).append({"label": label, "url": url})
if 'chatgpt-health-ga' in BY:
    src('chatgpt-health', 'OpenAI 2026-07-23：Health in ChatGPT（美国全面推送）', BY['chatgpt-health-ga']['url'])
if 'abbott-google' in BY:
    src('google-health-app', '雅培新闻稿 2026-08-11：Lingo 血糖数据进入 Google Health Coach', BY['abbott-google']['url'])
CACHE = os.path.join(root, 'research/v5_removed.json')
removed = json.load(open(CACHE)) if os.path.exists(CACHE) else []
have = {r['id'] for r in removed}
for i, (cat, why) in REMOVE.items():
    if i in BY and i not in have:
        e = BY[i]
        removed.append({"id": i, "title": e['title'], "short": e['short'], "org": M['orgs'][e['org']]['label'], "date": e['date'],
                        "dateLabel": e['dateLabel'], "url": e['url'], "track": e['track'], "cat": cat, "why": why,
                        "sources": e.get('sources', [])})
removed.sort(key=lambda r: r['date'])
json.dump(removed, open(CACHE, 'w'), ensure_ascii=False, indent=1)
E[:] = [e for e in E if e['id'] not in REMOVE]; BY = {e['id']: e for e in E}
if 'chatgpt-health' in BY and '2026-07' not in BY['chatgpt-health']['dateLabel']:
    BY['chatgpt-health']['dateLabel'] += '；2026-07-23 在美国全面推送'

# ---- 关系：删去指向已移出条目的边；只保留承载论证的“呼应”；“并行”限于约半年内 ----
from datetime import date
def dd(a, b):
    f = lambda x: date(int(x[:4]), int(x[5:7]) if len(x) >= 7 else 1, int(x[8:10]) if len(x) >= 10 else 1)
    return abs((f(a) - f(b)).days)
KEEP_ECHO = {('apple-htn', 'apple-iclr24'), ('apple-iclr24', 'oxford-ssl'), ('sensorwm', 'p-nazaret2022'), ('sensorwm', 'whoop-5'),
             ('apple-ppgage', 'oura-cvage'), ('lsm', 'p-timesfm'), ('normwear-wm', 'sonata'), ('delphi', 'gluformer'),
             ('ecg-wm', 'p-miller2020'), ('fitbit-2026', 'amie'), ('apple-health-app', 'whoop-5'), ('google-htn-nature', 'apple-htn')}
for e in E:
    keep = []
    for l in e['links']:
        if l['from'] not in BY: continue
        if l['type'] == '呼应' and (e['id'], l['from']) not in KEEP_ECHO: continue
        if l['type'] == '并行' and dd(e['date'], BY[l['from']]['date']) > 200: continue
        keep.append(l)
    e['links'] = keep
def addlink(eid, l):
    if eid in BY and l['from'] in BY and not any(x['from'] == l['from'] for x in BY[eid]['links']): BY[eid]['links'].append(l)
# 删边后补上承载主线的关系（每条都能在条目原文中找到依据）
for eid, l in [
    ('google-htn-nature', L('apple-htn', '并行', '同为自监督 PPG 表征 + 少量标注的高血压筛查；苹果走 FDA 许可的提醒，谷歌发表 Nature 论文')),
    ('apple-ppgage', L('apple-iclr24', '继承', '同一队列的手腕 PPG，作者有重合')),
    ('oura-cvage', L('apple-iclr24', '转向', '把 PPG 的生理信息直接做成“年龄差”指标（编者解读）')),
    ('whoop-5', L('oura-cvage', '继承', '“年龄差”类指标从单项（心血管）扩展到综合（编者解读）')),
    ('oppo-heartage', L('apple-ppgage', '并行', '同为从手表 PPG 推算可追踪的“年龄”')),
    ('sensorwm', L('whoop-5', '转向', '从回顾式的“年龄”指标变成可通过行为改变的“可教练健康年龄”（编者解读）')),
    ('glucofm', L('gluformer', '转向', '从预测下一个读数转向潜空间预测与慢/快双流结构')),
    ('healthformer', L('gluformer', '继承', '同一团队，从单一血糖扩展到多系统联合生成')),
    ('opentslm', L('sensorllm', '继承', '时序 + LLM 的开源路线')),
    ('hearts', L('health-llm', '检验', '系统检验 LLM 读生理时序的能力：明显不如专门模型')),
    ('hippt', L('sensorlm', '继承', '传感器—文本对齐，从分钟级指标回到 PPG 波形')),
    ('withings-mcp', L('claude-health', '接入', '设备数据以连接器进入通用助手')),
    ('ms-copilot-health', L('chatgpt-health', '并行', '同一季度推出、读取可穿戴与病历的健康空间')),
    ('claude-health', L('chatgpt-health', '并行', '同月推出的通用助手健康连接')),
    ('samsung-lvsd', L('p-hannun2019', '继承', '把医院里的专门心电 AI 搬到手表单导联上')),
    ('apple-sleepapnea', L('samsung-sleepapnea', '并行', '同年先后获 FDA 授权的手表睡眠呼吸暂停功能')),
    ('har-scaling', L('apple-iclr24', '检验', '从尺度律角度检验“以人为锚”：人的多样性比单人数据量更重要（编者解读）')),
    ('csfm', L('apple-accel', '并行', '同为跨模态脚手架：苹果用 PPG 教加速度，CSFM 在临床大数据上让 ECG、PPG、文字共享表征')),
    ('samsung-oneui8', L('p-miller2020', '呼应', '机理式的个体前瞻推演进入产品：睡眠压力 × 昼夜节律（编者解读）')),
    ('oppo-healthagent', L('oppo-embc2024', '继承', '同一公司从单项 PPG 功能走到 Agent 层（编者解读）')),
    ('oura-health-radar', L('fda-wellness-2026', '落地', 'FDA 放宽后，不给数值的血压信号类功能上线（编者解读）')),
    ('google-health-guardian', L('fda-wellness-2026', '落地', '同上')),
    ('sleep2vec', L('sleepfm', '继承', '跨模态对比对齐，扩展到九种模态任意子集')),
    ('sleepfm2', L('sleepfm', '继承', '同一团队，迁移到腕部')),
    ('aether-scaling', L('lsm', '继承', '把尺度律研究带到临床生理波形，并加入“标注病人数”')),
    ('ecg-scaling', L('lsm', '检验', '在心电上系统测量尺度律，结论取决于范式与架构')),
    ('apple-embridge', L('meta-emg', '转向', '肌电从“数千人监督”转向跨模态对齐与零样本手势（编者解读）')),
    ('xmae', L('anyppg', '继承', 'ECG → PPG 的跨模态监督，加入时序先后关系')),
    ('stepfm', L('lsm', '分岔', '把分钟级参数推到极简：只用步数')),
    ('sensori', L('oxford-ssl', '继承', '大规模腕部加速度预训练，扩展到全表型疾病')),
    ('google-health-app', L('fitbit-coach', '继承', '教练从预览到正式版，并成为整个健康入口')),
    ('oura-counsel', L('oura-advisor', '继承', 'Advisor 接入真人医生，从合作试点到收购')),
    ('huawei-watch6', L('huawei-trusense', '继承', '感知系统之上加大模型解释层')),
    ('apple-health-app', L('apple-workout-buddy', '继承', '生成式解释从运动场景扩展到整个健康 App')),
    ('samsung-ha', L('samsung-xealth', '继承', 'Health Assistant 与收购的临床通道同年推进')),
    ('dexcom-genai', L('stelo-otc', '继承', '同一款非处方 CGM 加上生成式周报')),
    ('oura-dexcom', L('stelo-otc', '奠基', '非处方 CGM 提供数据来源')),
    ('ir-wearme', L('fitbit-acq', '奠基', 'Fitbit 设备与用户提供研究数据')),
    ('openmhc', L('p-ahms2019', '呼应', '公开的长期心脏研究队列，对照苹果的私有队列（编者解读）')),
]: addlink(eid, l)
KEEP_ECHO.add(('openmhc', 'p-ahms2019'))

# ---- 脉络：13 → 9 ----
def T(id, name, q, problem, approach, changed, unlocked, open_, steps):
    return {"id": id, "name": name, "question": q, "problem": problem, "approach": approach, "changed": changed,
            "unlocked": unlocked, "open": open_, "desc": q, "steps": [{"id": i, "role": r} for i, r in steps if i in BY]}
M['threads'] = [
 T('data', '数据从哪里来', '基础模型需要大规模、长期、可授权的数据，各家怎么拿到？',
   '单次临床研究的数据量远不够预训练；消费设备数据多，但缺标签和临床结局。',
   '三条路：自建研究队列（苹果、华为），收购数据入口（谷歌买 Fitbit），把化验、血糖、病历拼进来（Oura × Dexcom、WEAR-ME、WHOOP Labs、三星 Xealth）。',
   '预训练规模从千人级到十万、百万人级；可穿戴数据开始与化验和病历对齐。',
   '无标签预训练、参数层尺度律、与临床结局的对照验证。',
   '数据集中在少数公司；学界依赖 OpenMHC 等少量公开队列。',
   [('huawei-heart', '华为：研究 App + 医院网络'), ('p-ahms2019', '苹果：Research App 里的长期队列（后来的预训练数据）'),
    ('fitbit-acq', '谷歌：收购 Fitbit，买下数据入口'), ('stelo-otc', '监管：首个非处方 CGM，血糖数据走向普通人'),
    ('oura-dexcom', 'Oura：戒指 + 血糖'), ('ir-wearme', '谷歌：可穿戴 + 常规血检'), ('samsung-xealth', '三星：收购通往医院的管道'),
    ('whoop-labs', 'WHOOP：化验接入'), ('openmhc', '学界：十年 MyHeart Counts 数据开放'), ('oppo-bp2026', 'OPPO：65 万人的手表血压研究')]),
 T('supervision', '监督从哪里来：同一个人，或更贵的模态', '没有医学标签，模型从哪里得到监督？',
   '专家标注昂贵，且每个新任务都要重来。',
   '两种答案：把“同一个人”的不同片段当正样本（以人为锚）；让更贵、更准的模态在训练时当老师（心率教加速度、PPG 教加速度、ECG 教 PPG、睡眠多导教腕部）。掩码重建与潜空间预测是并行的第三种目标。',
   '表征编码了人口学与健康状态；便宜的传感器在推理时可以单独工作。',
   '可迁移到多任务的通用表征；跨设备的“传感器迁移”。',
   '以人为锚的不变性目标会抹掉短暂的病理变化（AC-JEPA 的批评）；跨模态监督要求同步采集的数据。',
   [('clocs', '雏形：同一病人不同时间、导联的心电互为正样本'), ('p-cheng2021', '苹果：以被试为单位组织对比学习'),
    ('p-spathis2021', '心率监督加速度：生理耦合本身是监督'), ('biofame', '苹果的掩码一支：频域掩码、任意模态组合'),
    ('apple-iclr24', '起点：14 万人手表 PPG/ECG，同一参与者互为正样本'), ('apple-relcon', '相对对比：运动数据上的改进'),
    ('apple-accel', 'PPG 教加速度：贵模态当老师'), ('pulse-ppg', '野外数据 + 相对对比，开源'), ('har-scaling', '尺度律：增加“人数”比增加每人数据更有效'),
    ('csfm', '心电、PPG 与临床报告联合'), ('anyppg', 'ECG 教 PPG，并做全表型筛查'), ('ac-jepa', '反思：不变性抹掉变化，改为动作条件的潜空间预测'),
    ('xmae', '三星：利用 ECG → PPG 的时间先后'), ('oppo-heartage', 'OPPO：ECG 引导的 PPG 预训练'), ('sleepfm2', '睡眠多导教腕部')]),
 T('level', '建在哪一层：波形、分钟级指标，还是行为', '基础模型应该建在原始波形上，还是建在设备算好的指标上？',
   '原始波形信息多但昂贵、难以长期存储；分钟级指标便宜、覆盖广，但丢掉形态细节。',
   '谷歌用分钟级指标验证尺度律并把缺失当信息；苹果上移到行为层再与波形组合；三星按时间分辨率分层并压到手表端；2026 年出现多日原始波形的层级模型和只用步数的极简模型。',
   '“二选一”变成“两层互补”：行为层擅长睡眠等行为驱动的任务，波形层擅长心血管任务，组合最好。',
   '参数层模型成为 Agent 的组件（SensorFM）；跨设备迁移（Device Passport）。',
   '原始波形的长期上下文仍然昂贵；不同设备、不同代际之间的迁移仍不稳定。',
   [('apple-iclr24', '短波形片段，聚合到人'), ('lsm', '谷歌：分钟级指标与尺度律'), ('lsm2', '缺失本身是信息'),
    ('wbm', '苹果：行为层，与波形层互补'), ('himae', '三星：按时间分辨率分层，手表端推理'), ('wavesfm', '谷歌：回到多日原始波形'),
    ('apple-passport', '苹果：跨设备、跨通道的迁移'), ('sensorfm', '谷歌：500 万人分钟级数据，定位为 Agent 的工具'),
    ('stepfm', '极简：只用步数'), ('sensori', '另一端：一天的原始腕部运动 → 全表型疾病')]),
 T('open', '开放、外推与检验', '同一套配方能否复制到其他信号？公开的模型经得起检验吗？',
   '起点模型和数据都不公开；各模态各自为战。',
   '同一套“大规模预训练换泛化”的配方被复制到加速度、EEG、呼吸声、睡眠、肌电、心电与 PPG，并公开权重；2026 年出现统一基准与系统的尺度律研究。',
   '社区有了可复现的基线；但公平比较下，开源 PPG 模型相对简单特征和通用时序模型的优势有限。',
   '跨模态通用模型（BIOT、NormWear）；尺度律（心电、生理波形）。',
   '企业私有大数据上的强结果与开放模型的有限优势之间的差距，是这个领域目前最大的张力。',
   [('oxford-ssl', '加速度：70 万人日的自监督模型（开源）'), ('biot', '异构生物信号统一成“句子”'), ('labram', 'EEG：通用大模型'),
    ('hear', '呼吸声：HeAR'), ('meta-emg', '肌电：数千人、跨人泛化'), ('sleepfm', '睡眠：多导睡眠图多模态'),
    ('ecg-fm', '心电：开源权重'), ('ecgfounder', '心电：千万级专家标注'), ('papagei', 'PPG：开源基础模型'),
    ('normwear', '任意传感器组合'), ('sleep2vec', '睡眠：九种模态任意子集，报告尺度律'), ('apple-embridge', '苹果肌电：跨模态对齐，零样本手势'),
    ('ecg-scaling', '检验：心电尺度律取决于范式与架构'), ('aether-scaling', '检验：生理波形的算力最优尺度律'),
    ('ppg-bench', '检验：公平比较下开源 PPG 模型优势有限')]),
 T('dynamics', '从表征到动力学：世界模型', '模型能否回答“接下来会怎样、如果改变行为或用药会怎样”？',
   '表征模型描述“此刻的状态”，不回答干预问题；通用时序模型不懂生理约束。',
   '两条线汇合：苹果 2020 年起的“机理 + 学习”个体动力学；血糖与病历的生成式轨迹模型（GluFormer、Delphi-2M）。2026 年出现以药物、事件、行为为动作的世界模型。',
   '对象从“状态”变成“状态的转移”；SensorWM 把行为当动作，把可改变的健康年龄当目标，交给语言模型写计划。',
   '反事实推演、虚拟干预、个性化计划。',
   '观察数据上的反事实不等于因果效应（Rethinking World Models 的批评）；尚无前瞻干预试验。',
   [('p-miller2020', '苹果：胰岛素—血糖的机理 + 序列模型'), ('p-nazaret2022', '苹果：运动心率响应的个体动力学'),
    ('apple-hybrid-cv', '苹果：心血管模拟器 + 学习'), ('p-timesfm', '通用时序基础模型（后来的对照基线）'),
    ('gluformer', '血糖的生成式基础模型'), ('cgm-lsm', '160 万条血糖记录的自回归模型'), ('samsung-oneui8', '产品里的机理式推演：就寝建议'),
    ('delphi', '病历事件的生成式模型（参照）'), ('apple-ppg-hybrid', '苹果：PPG 的血流动力学混合建模'),
    ('healthformer', '多系统联合生成，提出“模拟干预”'), ('ac-jepa', '动作条件的心电潜空间预测'), ('normwear-wm', '信号级世界模型，显式建模干预'),
    ('ecg-wm', '以给药为动作的心电世界模型'), ('glucofm', '谷歌：血糖的慢趋势与短期偏离'),
    ('rethink-wm', '检验：预测准不等于能指导干预'), ('sensorwm', '谷歌：以行为为动作，推演 12 周、20 项指标')]),
 T('healthage', '健康年龄：把表征变成可追踪的指标', '怎样把复杂的生理表征变成用户看得懂、能长期追踪的一个数？',
   '基础模型的嵌入用户看不懂；单项指标又太零散。',
   '用“年龄差”做输出：从 PPG 推算心血管年龄（Oura），综合多项指标（WHOOP Age），在大队列上训练衰老时钟（苹果 PpgAge），用 ECG 引导 PPG 学心脏年龄（OPPO），最后变成可通过行为改变的目标（SensorWM）。',
   '“年龄差”成为连接研究与产品的通用接口。',
   '纵向追踪、行为干预的目标函数。',
   '多为观察性关联；“年龄差”的改善是否对应健康结局的改善尚无证据。',
   [('apple-iclr24', '起点：嵌入中已编码年龄等人口学信息'), ('oura-cvage', 'Oura：PPG 推算心血管年龄（2024）'),
    ('whoop-5', 'WHOOP Age：综合指标的年龄'), ('apple-ppgage', '苹果：21 万人队列上的 PPG 衰老时钟'),
    ('oppo-heartage', 'OPPO：手表 PPG 心脏年龄'), ('sensorwm', '可教练的健康年龄：可通过行为改变的目标')]),
 T('language', '语言接口：从读数字到调用模型', '怎样让语言模型可靠地读懂个人生理数据？',
   'LLM 直接读数值会算错、会编造；生理信号不是文本。',
   '依次尝试：提示读数（少样本、Health-LLM）→ 领域微调（PH-LLM）→ 写代码计算（PHIA）→ 传感器与文本对齐（SensorLLM、SensorLM、HiPPT）→ 多智能体分工、调用基础模型（PHA）。',
   'LLM 从“自己算”变成“调度工具和模型”。',
   'Agent 产品的技术底座；开源的时序语言模型。',
   '系统评测显示 LLM 读健康时序明显不如专门模型（HEARTS）。',
   [('google-fewshot', '谷歌：LLM 是少样本健康学习者'), ('health-llm', 'Health-LLM：直接读可穿戴指标'),
    ('ph-llm', 'PH-LLM：领域微调与专家对照'), ('phia', 'PHIA：写代码算，而不是记住'), ('sensorllm', 'SensorLLM：运动传感器与 LLM 对齐'),
    ('sensorlm', 'SensorLM：传感器与语言对齐'), ('pha', 'PHA：多智能体，调用基础模型'), ('opentslm', 'OpenTSLM：开源时序语言模型'),
    ('hearts', '检验：LLM 读健康时序不如专门模型'), ('hippt', 'OPPO：按证据范围的 PPG—文本对齐')]),
 T('agent', 'Agent 与入口：设备公司 vs 通用助手', '谁拥有用户的健康入口：设备公司的 Agent，还是通用 AI 助手？',
   '设备公司有数据没有大模型，通用 AI 公司有模型没有设备。',
   '设备公司先把 LLM 当解释层（WHOOP、Oura、Dexcom），再接入化验、病历和医生，并开始自研模型；通用 AI 公司在 2026 年第一季度通过连接器读取 Apple Health 与病历；Withings 反过来把数据交给通用助手。',
   'Agent 从回答问题变成“有记忆、会主动、能转诊”的服务。',
   '订阅制健康服务；设备数据与临床服务的连接。',
   '通用助手读的是汇总数据，没有生理层模型；设备 Agent 的临床效果缺少评测。',
   [('p-whoopcoach', 'WHOOP：GPT-4 驱动的教练（2023）'), ('oura-advisor', 'Oura Advisor'), ('dexcom-genai', 'Dexcom：生成式血糖周报'),
    ('apple-workout-buddy', '苹果：运动中的生成式语音教练'), ('oppo-healthagent', 'OPPO：AI 健康管家'),
    ('fitbit-coach', '谷歌：PHA 研究落地为 Fitbit 教练'), ('chatgpt-health', 'OpenAI：ChatGPT Health'), ('claude-health', 'Anthropic：Claude 健康连接'),
    ('ms-copilot-health', '微软：Copilot Health'), ('fitbit-2026', '谷歌：教练接入病历'), ('oura-womens', 'Oura：自研女性健康 LLM'),
    ('google-health-app', '谷歌：Google Health app 与正式版教练'), ('whoop-2026', 'WHOOP：记忆、主动关怀与医生'),
    ('samsung-ha', '三星：Health Assistant'), ('huawei-watch6', '华为：WATCH 6 的 AI 健康洞察'), ('apple-health-app', '苹果：以 Apple Intelligence 重做健康 App'),
    ('withings-mcp', 'Withings：以连接器把数据交给通用助手'), ('oura-plans', 'Oura：个性化计划'), ('oura-counsel', 'Oura：收购 Counsel Health')]),
 T('deploy', '落地：从专门模型到基础模型特征', '监管级功能用的是专门模型，还是基础模型？',
   '获许可功能需要明确的适应症与验证，长期由单任务模型完成。',
   '2019–2024 年的房颤、睡眠呼吸暂停、脉搏丢失都是专门模型；2025 年苹果高血压提醒的验证文件写明用自监督基础模型提取特征（编者所见首例）；2026 年 FDA 放宽低风险健康功能，谷歌、Oura 推出不给数值的血压信号功能。',
   '基础模型开始以“特征提取器 + 线性头”的形式进入获许可功能。',
   '一次预训练、多个功能；更快的功能迭代。',
   '各家多数产品仍未说明是否使用基础模型；OPPO 走“先专门模型、后基础模型”的相反顺序。',
   [('p-hannun2019', '专家级单导联心电分类（2019）'), ('huawei-heart', '华为：PPG 房颤筛查'), ('p-ahs2019', '苹果：手表房颤提醒'),
    ('samsung-sleepapnea', '三星：睡眠呼吸暂停（FDA De Novo）'), ('apple-vitals', '苹果：夜间个人基线'), ('oppo-embc2024', 'OPPO：专门的高血压风险模型'),
    ('huawei-trusense', '华为：玄玑感知系统'), ('apple-sleepapnea', '苹果：睡眠呼吸暂停提醒'), ('google-lop', '谷歌：脉搏丢失检测'),
    ('apple-htn', '苹果：自监督 PPG 特征 + 线性头的高血压提醒'), ('meta-neuralband', 'Meta：肌电模型随量产腕带上市'),
    ('samsung-lvsd', '三星：医院心电 AI 搬到手表'), ('fda-wellness-2026', 'FDA：放宽低风险健康功能'), ('oura-health-radar', 'Oura：血压信号与夜间呼吸'),
    ('google-health-guardian', '谷歌：官方称建在健康基础模型上的血压趋势'), ('oppo-bp2026', 'OPPO：65 万人血压研究'),
    ('google-htn-nature', '谷歌：自监督 PPG + 加速度的高血压筛查（Nature）')]),
]
for t in M['threads']:
    if t['id'] == 'language' and not any(x['id'] == 'pulse-ecg' for x in t['steps']):
        t['steps'].append({'id': 'pulse-ecg', 'role': '另一入口：把心电图当图像交给多模态大模型'})
for t in M['threads']: t['steps'].sort(key=lambda x: BY[x['id']]['date'])

# ---- 会议/期刊补扫（2026-11-13 13:17 收尾）：按更严格的标准只升格 SleepJEPA ----
for x in BY['sensorwm']['sources']:
    if '8SH3daIGHz' in x['url']:
        x['label'] = 'NeurIPS 2026 世界模型（CWM）workshop 论文，已录用：Developing World Models from Wearable Sensors（Lee & Heydari，谷歌；OpenReview 2026-10-02 发布）；在潜空间建模周级可穿戴指标，不重建原始信号'
for r in removed:
    if r['id'] == 'amie' and not any('s41591-025-04190-9' in x['url'] for x in r['sources']):
        r['sources'].append({'label': 'Nature Medicine 2026-02-06：A large language model for complex cardiology care（AMIE 扩展到心内科复杂病例，斯坦福 × 谷歌）', 'url': 'https://doi.org/10.1038/s41591-025-04190-9'})
json.dump(removed, open(CACHE, 'w'), ensure_ascii=False, indent=1)
SJ = {"id": "sleepjepa", "date": "2026-04-03", "dateLabel": "medRxiv 2026-04-03（v3）", "track": "signal", "org": "mountsinai", "type": "paper", "era": "e4",
      "title": "SleepJEPA: Learning the latent world of sleep with at-home sleep data to estimate disease risk",
      "short": "SleepJEPA：在潜空间预测整夜睡眠，估计 15 年疾病风险",
      "url": "https://doi.org/10.64898/2026.03.20.26348834", "sources": [],
      "q": "居家多导睡眠数据量大但与远期疾病的关系不清楚，换成潜空间预测目标能否学到更有预后价值的整夜表征？",
      "how": "用联合嵌入预测架构（JEPA）在潜空间学习整夜多通道居家睡眠表征；训练、验证与测试共用 55,518 次睡眠研究、422,035 小时信号。论文称可估计 1–15 年内 10 种疾病的累计风险（如心血管死亡 iAUC15 = 0.83、充血性心衰 0.85），在独立队列上复现，并在所有结局上优于 SleepFM 等睡眠基础模型。",
      "shift": "预训练目标从对比与重建转向潜空间预测，并且直接以远期疾病风险检验表征（编者解读）。对象是居家多导睡眠而非消费级手表。",
      "links": [{"from": "sleepfm", "type": "转向", "note": "同为睡眠多导基础模型；目标从“留一模态”对比换成 JEPA 潜空间预测，论文称各项结局优于 SleepFM"}]}
if 'sleepjepa' not in BY: E.append(SJ); BY['sleepjepa'] = SJ
addlink('ac-jepa', L('sleepjepa', '并行', '同月出现的 JEPA 潜空间预测：一个用于居家睡眠的疾病风险，一个用来反思“以人为锚”的不变性'))
for t in M['threads']:
    if t['id'] == 'supervision' and not any(x['id'] == 'sleepjepa' for x in t['steps']):
        t['steps'].append({'id': 'sleepjepa', 'role': '潜空间预测（JEPA）：5.5 万次居家睡眠研究，直接检验远期疾病风险'})
    t['steps'].sort(key=lambda x: BY[x['id']]['date'])

# ---- 去掉对已移出条目的悬空引用 ----
def rep(eid, field, a, b):
    if eid in BY and a in BY[eid][field]: BY[eid][field] = BY[eid][field].replace(a, b)
rep('normwear-wm', 'shift', '一个月前的 Sonata 已在 IMU 上用“预测未来潜状态”作预训练目标，但没有动作变量（编者解读）。', '')
rep('apple-embridge', 'q', 'CPEP 的直接对齐还不够', '苹果此前的肌电–姿态直接对齐（CPEP，见全部来源）还不够')
rep('apple-embridge', 'how', '在 CPEP 的基础上', '在此前直接对齐（CPEP）的基础上')
C0 = {c['org']: c for c in M['companies']}
if 'samsung' in C0: C0['samsung']['data']['text'] = C0['samsung']['data']['text'].replace('（MMR 论文使用三星手表数据）', '')

# ---- 时期要点：结论先行 ----
TH = {
 'e0': '单任务模型先证明价值，数据底座先建起来。心律失常分类、房颤提醒都是“一病一模型”；苹果、华为建研究队列，谷歌买下 Fitbit。“同一个人做监督”（CLOCS、苹果 2021）、机理 + 学习的个体动力学（苹果 2020）、让 LLM 读数值（谷歌 2023）已经出现，但还没有连起来。',
 'e1': '不靠标签，以人为锚。苹果在约 14 万人的手表 PPG/ECG 上自监督预训练，把同一参与者的两段信号当正样本，证明没有医学标签也能学到编码健康状态的表征。同期，同一判断在加速度、EEG、呼吸声、睡眠、肌电上各自成立。',
 'e2': '四个方向同时扩张。向上：谷歌在分钟级指标上验证尺度律，苹果再上移到行为层。横向：PPG 教加速度。开放：心电、PPG 模型公开权重。语言：PH-LLM、PHIA、SensorLLM、SensorLM。产品仍以专门模型为主，Agent 读的是汇总指标。',
 'e3': '分层与落地。WBM 表明行为层与波形层互补；苹果高血压提醒写明用自监督基础模型提取特征（编者所见首例）；Meta 肌电模型随量产腕带上市。Agent 走向多智能体（PHA → Fitbit 教练），并接入化验与临床通道。',
 'e4': '动力学、闭环与自我检验。建模对象从“状态”转向“状态如何演化”，到 SensorWM 以行为为动作；Agent 接入病历与医生，通用 AI 公司入场；领域开始检验自己（PPG-Bench、尺度律、Rethinking World Models、HEARTS）；FDA 放宽后，不给数值的血压信号功能上线。',
}
for e in M['eras']:
    if e['id'] in TH: e['thesis'] = TH[e['id']]

M['essay'] = [
 '<b>一句话：问题换了四次。</b>能不能不靠标签学到一个人的通用生理表征？→ 该建在哪一层、怎样迁移到便宜的传感器？→ 公开的模型经得起检验吗？→ 能不能推演“如果改变行为会怎样”，并交给 Agent 去执行？',
 '<b>起点改写了监督。</b>2019 年前后的标准做法是“一个病、一套标注、一个模型”。苹果 ICLR 2024 的论文用“同一个人”代替标签，在约 14 万人的手表数据上学到通用表征。之后的扩张有两种监督：以人为锚（RelCon、Pulse-PPG），以及让贵模态教便宜模态（PPG 教加速度、ECG 教 PPG、睡眠多导教腕部）。2026 年 AC-JEPA 指出，以人为锚的不变性会抹掉短暂的病理变化。',
 '<b>层次之争以互补收场。</b>谷歌在分钟级指标上验证尺度律，苹果上移到行为层，结论是两层互补、组合最好；2026 年谷歌又用层级模型回到原始波形，并把 500 万人的参数模型定位为 Agent 的工具。',
 '<b>开放之后是检验。</b>心电、PPG、EEG、睡眠、肌电都有了公开模型，但 PPG-Bench 发现，在 83.8% 的任务—适配组合中，没有任何开源 PPG 模型能同时胜过简单的脉率变异性特征和通用时序模型；心电尺度律也取决于范式与架构。企业私有数据上的强结果与开放模型的有限优势之间，是这个领域目前最大的张力。',
 '<b>落地有两种节奏。</b>监管级功能长期由专门模型完成；2025 年苹果高血压提醒写明用自监督基础模型提取特征、下游只用线性模型（编者所见首例）。OPPO 走相反的顺序，先上专门模型，2026 年才转向 ECG 引导的预训练。2026 年 FDA 放宽低风险健康功能，谷歌称 Health Guardian 建在健康基础模型之上。',
 '<b>终点暂停在世界模型 + Agent。</b>“状态如何演化”从苹果 2020 年的机理 + 学习模型开始，经过血糖与病历的生成式轨迹，到 2026 年以药物、事件、行为为动作的世界模型。SensorWM 用周级指标推演 12 周的变化，以可改变的健康年龄为目标，再交给语言模型写计划：参数、世界模型、Agent 三条纲在一个公开系统里接上（编者所见；信号纲没有进入）。它也划出了下一道门槛：观察数据上的反事实不等于因果效应，计划能否改善健康还需要前瞻试验。',
 '<b>各家位置（编者判断）。</b>苹果“队列 → 模型 → 获许可功能”的链条最完整、最公开，但没有以行为为动作的世界模型；谷歌从数据入口到世界模型、Agent 都有公开论文，且层与层之间有接口；三星偏端侧与机理；OPPO 由产品回溯到基础模型；WHOOP 与 Oura 以 Agent 和服务为先；华为数据与研究网络强，模型层公开材料少；通用 AI 公司拥有入口和模型，缺设备和生理层模型。',
]

# ---- 公司卡 ----
C = {c['org']: c for c in M['companies']}
C['apple']['model'] = {"text": "前史：被试感知对比（2021）、个体动力学（血糖 2020、运动心率 2022）→ 频域掩码（bioFAME）与起点 PPG/ECG 模型（2023）→ 相对对比的运动模型、PPG 蒸馏进加速度、行为模型 WBM → PpgAge 衰老时钟、跨设备迁移（Device Passport）、肌电 EMBridge。学习式动力学停在 2022 年，之后转为“模拟 + 学习”（心血管模拟器 2023、PPG 混合建模 2025）。",
    "ids": ['p-miller2020', 'p-cheng2021', 'p-nazaret2022', 'apple-hybrid-cv', 'biofame', 'apple-iclr24', 'apple-relcon', 'apple-accel', 'wbm', 'apple-ppg-hybrid', 'apple-ppgage', 'apple-embridge', 'apple-passport']}
C['google']['path'] = '收购数据入口 → 分钟级模型与语言对齐 → 多智能体 → Fitbit / Google Health 教练 → 世界模型'
C['google']['model'] = {"text": "参数层 LSM → LSM-2 → SensorFM；WavesFM 回到原始波形；SensorLM 对齐语言；GlucoFM（血糖）；Nature 高血压筛查（自监督 PPG + 加速度）；SensorWM 世界模型。Agent 研究线：少样本 → PH-LLM → PHIA → PHA。另有 HeAR、TimesFM、DeepMind 活动识别尺度律。",
    "ids": ['lsm', 'lsm2', 'sensorfm', 'wavesfm', 'sensorlm', 'glucofm', 'google-htn-nature', 'sensorwm', 'google-fewshot', 'ph-llm', 'phia', 'pha', 'hear', 'p-timesfm', 'har-scaling']}
C['google']['product'] = {"text": "脉搏丢失检测（专门模型）；Fitbit 个人健康教练（PHA 研究落地，2026 年接入病历）；Google Health app 与正式版教练；Pixel Watch 5 的 Health Guardian（官方称建在健康基础模型之上）。",
    "ids": ['google-lop', 'fitbit-coach', 'fitbit-2026', 'google-health-app', 'google-health-guardian']}
C['samsung']['model'] = {"text": "HiMAE（多分辨率、手表端推理）→ xMAE（利用 ECG → PPG 的时间先后）。", "ids": ['himae', 'xmae']}
C['samsung']['product'] = {"text": "睡眠呼吸暂停（FDA De Novo，2024-02）、就寝建议（睡眠压力 × 昼夜节律）、LVSD 检测（与 Medical AI 合作）、Health Assistant 测试版。",
    "ids": ['samsung-sleepapnea', 'samsung-oneui8', 'samsung-lvsd', 'samsung-ha']}
C['oura']['model'] = {"text": "女性健康专用 LLM（首个自研模型）；Advisor 部分问题改由自训模型作答（官方称）。AHA 2025 海报提到“大规模基础模型”，只有题目可证，见全部来源。", "ids": ['oura-womens', 'oura-plans']}
C['oura']['note'] = '从解释层往下补：先有 Agent，再有自研语言模型；生理基础模型尚无公开论文。'
C['whoop']['model'] = {"text": "WHOOP Coach 使用 OpenAI 模型；2026 年招聘 Foundation AI 团队（只有招聘与访谈，见全部来源）。", "ids": ['p-whoopcoach']}
C['aico']['model'] = {"text": "通用 LLM；TimesFM 等通用时序模型作为生理世界模型的基线。", "ids": ['p-timesfm']}
C['aico']['product'] = {"text": "ChatGPT Health（2026-01 推出，7 月在美国全面推送）、Claude 健康连接、Copilot Health；设备公司 Withings 反向以连接器接入通用助手。",
    "ids": ['chatgpt-health', 'claude-health', 'ms-copilot-health', 'withings-mcp']}
for c in M['companies']:
    for k in ('data', 'model', 'product'):
        c[k]['ids'] = [i for i in c[k]['ids'] if i in BY]

# ---- 问题矩阵 ----
Q = {
 'sup': {'e0': ('专家标注；少数工作用生理耦合或“同一病人”做监督。', ['p-hannun2019', 'p-spathis2021', 'clocs', 'oxford-ssl']),
         'e1': ('同一个人（参与者级正样本）；频域掩码重建。', ['apple-iclr24', 'labram']),
         'e2': ('更贵的模态当老师；缺失本身；自动生成的文字。', ['apple-accel', 'csfm', 'lsm2', 'sensorlm']),
         'e3': ('ECG 教 PPG；按时间分辨率分层的掩码重建。', ['anyppg', 'himae']),
         'e4': ('潜空间预测（JEPA）；动作与干预（行为、药物）；对“不变性”本身的反思。', ['sleepjepa', 'ac-jepa', 'ecg-wm', 'sensorwm', 'xmae'])},
 'level': {'e0': ('单段波形或单个指标。', ['p-hannun2019', 'p-ahs2019']),
           'e1': ('短波形片段，聚合到人。', ['apple-iclr24']),
           'e2': ('分钟级指标与尺度律；小时级行为。', ['lsm', 'wbm']),
           'e3': ('按时间分辨率分层，并压到手表端。', ['himae']),
           'e4': ('多日原始波形的层级模型；500 万人的分钟级模型；两端：只用步数 vs. 一天的原始运动。', ['wavesfm', 'sensorfm', 'stepfm', 'sensori'])},
 'ask': {'e0': ('这段信号里有没有某种病？', ['p-hannun2019', 'huawei-heart']),
         'e1': ('这个人是什么状态？（通用表征）', ['apple-iclr24']),
         'e2': ('能覆盖多少下游任务？规模越大越好吗？', ['lsm', 'papagei']),
         'e3': ('能否成为获许可功能的特征？“年龄差”能否预示疾病？', ['apple-htn', 'apple-ppgage']),
         'e4': ('接下来会怎样？如果改变行为或用药呢？预测得准就能指导干预吗？', ['healthformer', 'sensorwm', 'ecg-wm', 'rethink-wm'])},
 'act': {'e0': ('规则提醒 + 医生复核；GPT-4 读汇总指标。', ['p-ahs2019', 'p-whoopcoach']),
         'e1': ('通用 LLM 读可穿戴指标。', ['health-llm']),
         'e2': ('微调模型与写代码的 Agent。', ['ph-llm', 'phia']),
         'e3': ('多智能体与教练产品；化验与临床通道接入。', ['pha', 'fitbit-coach', 'whoop-labs']),
         'e4': ('Agent 调用基础模型与世界模型，接入病历与医生；通用 AI 公司入场。', ['sensorfm', 'fitbit-2026', 'whoop-2026', 'chatgpt-health'])},
 'open': {'e0': ('私有队列为主；少量公开代码与模型。', ['p-ahms2019', 'oxford-ssl', 'biot']),
          'e1': ('公开的 EEG、睡眠、声音模型；肌电以预印本公开。', ['labram', 'sleepfm', 'hear', 'meta-emg']),
          'e2': ('公开权重的心电、PPG 模型。', ['ecg-fm', 'ecgfounder', 'papagei']),
          'e3': ('开源的跨模态 PPG 模型。', ['anyppg']),
          'e4': ('公开数据集与公平基准；尺度律；开源 PPG 模型的优势受到质疑。', ['openmhc', 'ppg-bench', 'ecg-scaling', 'aether-scaling'])},
}
for q in M['questions']:
    for c in q['cells']:
        t, ids = Q[q['id']][c['era']]
        c['text'] = t; c['ids'] = [i for i in ids if i in BY]

M['dataVersion'] = 5
E.sort(key=lambda e: e['date'])
json.dump(D, open(P, 'w'), ensure_ascii=False, indent=1)
json.dump(M, open(MP, 'w'), ensure_ascii=False, indent=1)
print('v5 entries', len(E), 'removed', len(removed), 'threads', len(M['threads']))
