#!/usr/bin/env python3
"""第四版（2026-11-13 下午）：合并补漏检索（gap / companies / academic）中核实过的条目。幂等。
来源文件只作输入、不入站：/workspace/physio-fm-gap-candidates.json 等。"""
import json as _j, os as _o
if _j.load(open(_o.path.join(_o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))), 'data/meta.json'))).get('dataVersion', 0) >= 5:
    print('数据已是第五版（做过减法），历史迁移不再运行'); raise SystemExit(0)
import json, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(root, 'data/entries.json'); MP = os.path.join(root, 'data/meta.json')
D = json.load(open(P)); E = D['entries']; BY = {e['id']: e for e in E}; M = json.load(open(MP))
def L(f, t, n): return {"from": f, "type": t, "note": n}
def up(**k):
    k.setdefault('sources', []); k.setdefault('links', [])
    if k['id'] in BY: BY[k['id']].clear(); BY[k['id']].update(k)
    else: E.append(k); BY[k['id']] = k
def src(eid, label, url):
    e = BY[eid]; e.setdefault('sources', [])
    if url not in [s['url'] for s in e['sources']]: e['sources'].append({"label": label, "url": url})
def addlink(eid, l):
    if not any(x['from'] == l['from'] for x in BY[eid]['links']): BY[eid]['links'].append(l)
def org(k, label, group):
    if k not in M['orgs']: M['orgs'][k] = {"label": label, "group": group}

org('fda', 'FDA（美国食药监局）', 'other'); org('dolby', '杜比实验室 × 佐治亚理工', 'other'); org('unc', '北卡罗来纳大学教堂山分校', 'academic')
org('fudan', '复旦大学 等', 'academic'); org('withings', 'Withings', 'other'); org('imt', 'IMT Atlantique × 蒙特利尔大学', 'academic')
org('tju', '天津大学 等', 'academic'); org('ucla', 'UCLA', 'academic')

# ---- 1. 补漏候选（gap-candidates）：逐条抽查官方页面后采纳，部分日期按“最早公开”修正 ----
G = {x['id']: x for x in json.load(open('/workspace/physio-fm-gap-candidates.json'))} if os.path.exists('/workspace/physio-fm-gap-candidates.json') else {}
KEEP = ['google-health-app', 'google-health-guardian', 'google-htn-nature', 'glucofm', 'fda-wellness-2026', 'oura-health-radar',
        'chatgpt-health-ga', 'amazon-health-ai', 'mai-dxo', 'opentslm', 'sleep2vec', 'robust-ppg-dolby', 'aether-scaling', 'soter', 'apple-speech-fm']
FIELDS = ['id', 'date', 'dateLabel', 'track', 'org', 'type', 'title', 'short', 'url', 'sources', 'q', 'how', 'shift', 'links']
CACHE = os.path.join(root, 'research/v4_gap_entries.json')
if G:
    json.dump([{k: G[i][k] for k in FIELDS if k in G[i]} | ({'orgNote': G[i]['orgNote']} if G[i].get('orgNote') else {}) for i in KEEP], open(CACHE, 'w'), ensure_ascii=False, indent=1)
for x in json.load(open(CACHE)):
    up(**json.loads(json.dumps(x)))

# ---- 1b. 深读（deepread）：苹果补缺论文与 2026 学术论文，站点 schema，已逐条核实 ----
org('fiveseasons', '五季医学 × 清华大学', 'other'); org('ucsf', 'UCSF 等（中美合作）', 'academic')
M['orgs']['unc']['label'] = '北卡罗来纳大学教堂山分校 × Foci Labs'
DR = '/workspace/physio-fm-deepread.json'; DC = os.path.join(root, 'research/v4_deepread_entries.json')
if os.path.exists(DR):
    json.dump([x['entry'] for x in json.load(open(DR))['items']], open(DC, 'w'), ensure_ascii=False, indent=1)
for x in json.load(open(DC)):
    x = json.loads(json.dumps(x))
    old = BY.get(x['id'])
    keep = old.get('sources', []) if old else []
    up(**x)
    for sct in keep: src(x['id'], sct['label'], sct['url'])

BY['glucofm'].update(date='2026-05-29', dateLabel="arXiv 2026-05-29；谷歌研究博客 2026-08-26")
src('glucofm', 'arXiv 2605.30865', 'https://arxiv.org/abs/2605.30865')
BY['glucofm']['how'] = BY['glucofm']['how'].replace("平均 PR-AUC 比同语料预训练的最佳 GluFormer 变体高 5.8 个百分点", "平均 PR-AUC 比同语料预训练的最佳 GluFormer 变体高 5.8 个百分点（博客口径；论文摘要为比最佳 CGM 基础模型高 4.1 个百分点）")
BY['mai-dxo'].update(date='2025-06-27', dateLabel="arXiv 2025-06-27；微软 AI 博客 2025-06-30")
BY['apple-speech-fm'].update(date='2025-08-29', dateLabel="arXiv 2025-08-29；NeurIPS 2025 TS4H workshop")
src('apple-speech-fm', 'arXiv 2509.00221', 'https://arxiv.org/abs/2509.00221')
BY['robust-ppg-dolby']['orgNote'] = "佐治亚理工与杜比实验室合作"
BY['sleep2vec'].setdefault('orgNote', '据论文首页')
for e in ('whoop-5',):
    src(e, 'FDA 警告信 2025-07-14（Blood Pressure Insights）', 'https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/whoop-inc-709755-07142025')
    src(e, 'FDA 2026-06-17 致函：对修改后的 Blood Pressure Insights 不再执法', 'https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/whoop-inc-709755-06172026')
    src(e, 'MedTech Dive 2026-06-23：FDA 撤回对 WHOOP 的警告信', 'https://www.medtechdive.com/news/fda-drops-whoop-warning-letter-over-blood-pressure-feature/823652/')
for e in ('xmae', 'himae'):
    src(e, '三星新闻稿 2026-08-14：From Biosignals to Health Insights', 'https://news.samsung.com/global/from-biosignals-to-health-insights-samsung-researchs-work-on-health-foundation-models')
src('meta-emg', 'emg2qwerty / emg2pose 数据集（2024-12）', 'https://ai.meta.com/blog/open-sourcing-surface-electromyography-datasets-neurips-2024/')
src('google-lop', 'FDA 许可（谷歌 2025-02-26）', 'https://blog.google/feed/pixel-watch-3-loss-of-pulse-detection-fda/')
src('pha', '谷歌研究博客：The anatomy of a personal health agent', 'https://research.google/blog/the-anatomy-of-a-personal-health-agent/')
src('fitbit-coach', '谷歌研究博客：How we are building the personal health coach', 'https://research.google/blog/how-we-are-building-the-personal-health-coach/')
src('oura-womens', 'Oura 博客 2026-03-02：Designing Trustworthy Health AI', 'https://ouraring.com/blog/designing-trustworthy-health-ai/')
src('apple-sleepapnea', 'FDA 510(k) K240929', 'https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K240929')
src('sensorfm', 'arXiv 2605.22759', 'https://arxiv.org/abs/2605.22759')


# 公司检索中的“配套材料”挂到对应条目，而不是列为未收录
for eid, label, url in [
    ('google-health-guardian', '谷歌博客：Health Guardian features on Pixel and Fitbit', 'https://blog.google/products-and-platforms/products/google-health/pixel-watch-health-guardian/'),
    ('google-lop', '谷歌博客 2024-08-13：Pixel Watch 3 introduces Loss of Pulse Detection', 'https://blog.google/products-and-platforms/devices/pixel/pixel-watch-3-loss-of-pulse-detection/'),
    ('ph-llm', '谷歌研究博客：Advancing personal health and wellness insights with AI', 'https://research.google/blog/advancing-personal-health-and-wellness-insights-with-ai/'),
    ('himae', '三星研究博客：The Resolution Hypothesis', 'https://research.samsung.com/blog/The-Resolution-Hypothesis-Discovering-how-Time-Scale-Maps-to-Health-Outcomes'),
    ('claude-health', 'Claude 帮助中心：与 iOS 健康数据集成', 'https://support.claude.com/en/articles/11869619-use-claude-with-ios-apps'),
    ('fitbit-coach', '谷歌博客：Pixel Watch 4（宣布教练预览）', 'https://blog.google/products-and-platforms/devices/pixel/pixel-watch-4/'),
    ('whoop-2026', 'WHOOP：How WHOOP AI guidance turns your health data into personalized coaching', 'https://www.whoop.com/us/en/thelocker/new-ai-guidance-from-whoop/'),
]:
    src(eid, label, url)

# ---- 2. 公司检索补录（官方页面已核对） ----
up(id='oura-cvage', date='2024-05-10', dateLabel='发布 2024-05-10', track='param', org='oura', type='product',
   title='ŌURA Announces Two New Heart Health Features: Cardiovascular Age and Cardio Capacity', short='Oura 心血管年龄：PPG 估计的血管年龄',
   url='https://ouraring.com/blog/heart-health-at-oura/',
   q='怎样让用户理解自己的血管状态，并知道哪些行为能改善它？',
   how='Cardiovascular Age 从 PPG 信号中与年龄相关的特征（含估计的脉搏波传导速度）推算心血管年龄，并与实际年龄比较；Cardio Capacity 估计 VO2max（官方称）。',
   shift='“年龄差”作为产品指标在戒指上出现，比 WHOOP Age 早一年；它是 PPG 形态特征的产物，官方未说明使用基础模型（编者解读）。',
   links=[])
up(id='samsung-sleepapnea', date='2024-02-06', dateLabel='FDA De Novo DEN230041（2024-02）', track='signal', org='samsung', type='product',
   title='Samsung Health Monitor sleep apnea feature (FDA De Novo DEN230041)', short='三星睡眠呼吸暂停功能：FDA De Novo 授权',
   url='https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPMN/denovo.cfm?knumber=DEN230041',
   q='手表能否在家中提示睡眠呼吸暂停风险？',
   how='FDA 以 De Novo 方式为“评估睡眠呼吸暂停风险的非处方设备”建立新分类，授权三星健康监测 App 的睡眠呼吸暂停功能（Galaxy Watch）。',
   shift='同类功能的首个监管路径由三星打开，苹果同年 9 月的睡眠呼吸暂停提醒随后获 510(k) 许可。两者都是专门模型，不是基础模型（编者解读）。',
   links=[])
BY['apple-sleepapnea']['links'] = [l for l in BY['apple-sleepapnea']['links'] if l['from'] != 'samsung-sleepapnea'] + [L('samsung-sleepapnea', '并行', '同年先后获 FDA 授权的手表睡眠呼吸暂停功能：三星走 De Novo，苹果走 510(k)')]
up(id='samsung-lvsd', date='2025-10', dateLabel='三星新闻稿 2025-10（韩国 MFDS 批准）', track='signal', org='samsung', type='product',
   title="Samsung's LVSD detection on Galaxy Watch (with Medical AI)", short='三星手表左心室收缩功能障碍（LVSD）检测',
   url='https://news.samsung.com/global/samsungs-breakthrough-wearable-technologies-driven-by-innovation-and-collaboration',
   q='心衰的主要前兆 LVSD 能否在手表上提前发现？',
   how='与韩国医疗 AI 公司 Medical AI 合作，把其在 100 多家医院使用的 12 导联心电 AI 算法迁移到 Galaxy Watch 的单导联心电上（官方称为“全球首个”手表 LVSD 检测）。',
   shift='监管级功能的另一种来源：不是自研基础模型，而是把医院里的临床 AI 模型搬到手表上（编者解读）。',
   links=[L('p-hannun2019', '呼应', '同为把专家级心电 AI 带到单导联设备上')])
up(id='withings-mcp', date='2026-10', dateLabel='2026-10 向 Withings+ 会员推出', track='agent', org='withings', type='product',
   title='Withings AI Connector for Claude, ChatGPT, Vibe and Grok', short='Withings AI 连接器：把体重、血压数据开放给通用助手',
   url='https://static.withings.com/content/v2/app/mcp/en/index.html',
   q='设备公司的数据，应该自己做 Agent，还是交给别家的 Agent 读？',
   how='以 MCP 连接器的形式，让 Withings+ 会员把 Withings 设备数据接入 Claude、ChatGPT、Vibe 与 Grok（官方页面称在各助手目录中上架尚待批准）。',
   shift='与 Oura、WHOOP 自研 Agent 相反，Withings 选择做通用助手的数据源：设备公司在“入口”之争中的另一种站位（编者解读）。',
   links=[L('claude-health', '接入', '通用助手通过连接器读取设备数据'), L('ms-copilot-health', '呼应', '通用 AI 公司汇集多种设备数据')])
up(id='ms-waveform-position', date='2026-06-19', dateLabel='微软研究院 2026-06（立场论文）', track='agent', org='microsoft', type='paper',
   title='Position: Beyond Prediction: Toward Verifiable Physiological Waveform Reasoning with Foundation Models and Agentic LLMs', short='微软立场论文：可核验的生理波形推理',
   url='https://www.microsoft.com/en-us/research/publication/position-beyond-prediction-toward-verifiable-physiological-waveform-reasoning-with-foundation-models-and-agentic-llms/',
   q='ECG、PPG、EEG 的信息在细节形态里，端到端预测能否给出可核验的结论？',
   how='主张“可核验的生理波形推理”：先从原始信号中提取可定位、可测量的证据，再解释为生理语义，最后支持临床判断；由基础模型与 Agent 式 LLM 分工完成。',
   shift='语言接口一线出现了对“只做预测”的反思，与 PPG-LM、HiPPT 的分层文本监督方向一致（编者解读）。',
   links=[L('pulselm', '呼应', '把波形与文字推理连起来')])

# ---- 3. 学术检索补录（arXiv 页面已核对标题、日期、摘要与作者单位） ----
up(id='neurolm', date='2024-08-27', dateLabel='arXiv 2024-08；ICLR 2025', track='signal', org='sjtu', orgNote='与微软亚洲研究院合作', type='open',
   title='NeuroLM: A Universal Multi-task Foundation Model for Bridging the Gap between Language and EEG Signals', short='NeuroLM：把 EEG 当作外语交给 LLM',
   url='https://arxiv.org/abs/2409.00101',
   q='EEG 预训练模型每个任务都要全量微调，能否像语言模型一样多任务通用？',
   how='先训练与文本对齐的向量量化神经分词器，把 EEG 编成离散 token，再送入 LLM 做多通道自回归，最后多任务指令微调。',
   shift='LaBraM 团队把 EEG 从“表征”推到“与语言同一模型”，信号与语言纲在脑电上会合（编者解读）。',
   links=[L('labram', '继承', '同一团队，沿用向量量化的神经分词')])
up(id='reve', date='2025-10-24', dateLabel='arXiv 2025-10；NeurIPS 2025', track='signal', org='imt', type='open',
   title='REVE: A Foundation Model for EEG -- Adapting to Any Setup with Large-Scale Pretraining on 25,000 Subjects', short='REVE：25,000 人、任意电极布局的 EEG 模型',
   url='https://arxiv.org/abs/2510.21585',
   q='公开 EEG 数据的设备、电极布局各不相同，模型能否适配任意配置？',
   how='用 4D 位置编码处理任意长度与电极布局；以掩码自编码在 92 个数据集、25,000 人、6 万多小时 EEG 上预训练，在 10 项下游任务上取得领先。',
   shift='把“通道异构”（BIOT、Device Passport 的问题）放到最大规模的 EEG 数据上解决（编者解读）。',
   links=[L('cbramod', '并行', '同期的 EEG 基础模型，侧重不同'), L('biot', '继承', '异构通道统一建模的思路')])
up(id='gptcoach', date='2024-05-09', dateLabel='arXiv 2024-05；CHI 2025', track='agent', org='stanford', type='paper',
   title='GPTCoach: Towards LLM-Based Physical Activity Coaching', short='GPTCoach：按动机访谈做运动教练的 LLM',
   url='https://arxiv.org/abs/2405.06061',
   q='LLM 教练如何既个性化，又遵循循证的教练方法？',
   how='访谈 12 名健康专业人员与 10 名潜在用户形成设计原则；实现循证教练项目的入门对话、动机访谈话术，并结合可穿戴数据制定运动计划；16 人实验室研究。',
   shift='学术界最早把“教练方法论”而不只是“数据解读”写进 LLM 教练，后来的 PHA、Oura 计划都延续这一点（编者解读）。',
   links=[L('health-llm', '分岔', '从“LLM 能否读指标”转向“LLM 怎样当教练”')])
up(id='heartlang', date='2025-02-15', dateLabel='arXiv 2025-02；ICLR 2025', track='signal', org='pku', orgNote='与华南师范大学合作', type='paper',
   title='Reading Your Heart: Learning ECG Words and Sentences via Pre-training ECG Language Model', short='HeartLang：把心搏当词、节律当句',
   url='https://arxiv.org/abs/2502.10707',
   q='固定窗口切分的 ECG 自监督忽略了形态与节律，能否按心电本身的结构来切？',
   how='QRS 分词器把每个心搏变成“词”、节律变成“句”，在此之上做自监督，并构建最大的心搏词表；在 6 个公开 ECG 数据集上评测。',
   shift='“分词”从语言模型借来，按生理结构而非固定窗口切分信号（编者解读）。',
   links=[L('labram', '呼应', '分词 + 掩码的路线用到心电')])
up(id='opera', date='2024-06-23', dateLabel='arXiv 2024-06；NeurIPS 2024 数据集与基准', track='signal', org='cambridge', type='open',
   title='Towards Open Respiratory Acoustic Foundation Models: Pretraining and Benchmarking (OPERA)', short='OPERA：开放的呼吸声基础模型与基准',
   url='https://arxiv.org/abs/2406.16148',
   q='咳嗽与呼吸声缺标签，且医疗场景要求可复现，能否有开放的声学基础模型？',
   how='整理约 13.6 万条、400 多小时呼吸音频，预训练三个模型，建立 19 项下游任务的基准；在 16 项上优于通用音频预训练模型。',
   shift='与谷歌 HeAR 同一问题，但走“开源 + 基准”路线（编者解读）。',
   links=[L('hear', '并行', '同为呼吸声基础模型，OPERA 全部开放')])
up(id='osf-sleep', date='2026-02-27', dateLabel='arXiv 2026-02', track='signal', org='ucla', orgNote='与埃默里大学合作', type='paper',
   title='OSF: On Pre-training and Scaling of Sleep Foundation Models', short='OSF：睡眠基础模型的预训练与尺度',
   url='https://arxiv.org/abs/2603.00190',
   q='睡眠基础模型的预训练方式与规模，各自贡献多少？',
   how='系统比较睡眠基础模型的预训练选择与规模，得到在 9 个数据集上领先的 OSF 模型族，并分析样本效率、层级聚合与跨数据集扩展。',
   shift='睡眠方向从“发布一个模型”转向“研究怎样预训练”，与 ECG 尺度律、Aether 属于同一轮自我检验（编者解读）。',
   links=[L('sleepfm', '检验', '系统研究睡眠预训练的设计选择')])
up(id='hearts', date='2026-02-25', dateLabel='arXiv 2026-02', track='agent', org='ucla', orgNote='与谷歌研究院合作', type='open',
   title='HEARTS: Benchmarking LLM Reasoning on Health Time Series', short='HEARTS：LLM 在健康时序上的推理基准',
   url='https://arxiv.org/abs/2603.06638',
   q='LLM 读健康时序到底行不行？',
   how='整合 16 个数据集、12 个健康领域、20 种信号模态，定义感知、推断、生成、演绎四类共 110 项任务，评测 16 个大模型、2 万多个样本。',
   shift='结论直接：LLM 明显不如专门模型，且多步时间推理薄弱，“只靠扩大模型”不够。这为“Agent 调用基础模型”的架构提供了证据（编者解读）。',
   links=[L('health-llm', '检验', '系统检验 LLM 读生理数据的能力'), L('opentslm', '检验', '时序原生 LLM 也在被测之列的路线')])
up(id='inertia-1', date='2026-07-07', dateLabel='arXiv 2026-07', track='signal', org='ucla', orgNote='与约翰斯·霍普金斯、杜克大学合作', type='open',
   title='Inertia-1: An Open Exploration of Wearable Motion Foundation Models', short='Inertia-1：1,820 万小时加速度的开放研究',
   url='https://arxiv.org/abs/2607.06617',
   q='运动基础模型的数据、模型、训练选择，哪些真正重要？',
   how='用全球来源的 1,820 万小时以上加速度数据，系统研究传感器、佩戴位置、采样率、窗口、架构、规模、预训练目标与数据量；在 15 个数据集上评测。',
   shift='加速度方向的“配方研究”，与 Sensori 同年给出开放的大规模结论（编者解读）。',
   links=[L('oxford-ssl', '继承', '大规模加速度预训练的延续'), L('apple-relcon', '呼应', '同为运动基础模型')])
up(id='har-scaling', date='2025-02-05', dateLabel='arXiv 2025-02', track='signal', org='google', orgNote='Google DeepMind', type='paper',
   title='Scaling laws in wearable human activity recognition', short='可穿戴活动识别的尺度律（DeepMind）',
   url='https://arxiv.org/abs/2502.03364',
   q='活动识别的预训练能否像语言、视觉一样建立尺度律？',
   how='对预训练数据量与 Transformer 规模做网格搜索，发现预训练损失与数据量、参数量呈幂律；增加用户数比增加每人数据量收益更大。',
   shift='“人的多样性比单人数据量更重要”，从尺度律角度支持了“以人为锚”的直觉（编者解读）。',
   links=[L('lsm', '呼应', '同在谷歌的可穿戴尺度律研究，对象不同')])
up(id='beyond-static', date='2026-03-20', dateLabel='arXiv 2026-03（立场论文）', track='world', org='cambridge', orgNote='与 KAIST 合作', type='paper',
   title='Wearable Foundation Models Should Go Beyond Static Encoders', short='立场：可穿戴基础模型应超越静态编码器',
   url='https://arxiv.org/abs/2603.19564',
   q='把短窗口映射到标签的“静态编码器”，能处理慢性、进展性的健康问题吗？',
   how='论证可穿戴基础模型需要三种转变：结构更丰富的长期个人数据、面向纵向与个性化的多模态建模，以及面向未来风险的推理。',
   shift='为 2026 年转向动力学与世界模型提供了明确的论证（编者解读）。',
   links=[L('apple-iclr24', '检验', '批评短窗口静态表征的范式（编者解读）')])
up(id='organ-agents', date='2025-08-20', dateLabel='arXiv 2025-08', track='world', org='tju', orgNote='天津大学、天津医科大学总医院、特伦托大学', type='paper',
   title='Organ-Agents: Virtual Human Physiology Simulator via LLMs', short='Organ-Agents：多 LLM Agent 模拟器官系统',
   url='https://arxiv.org/abs/2508.14357',
   q='能否用 LLM 模拟多器官生理，并比较不同治疗方案？',
   how='每个器官系统一个模拟 Agent，先在系统时序上监督微调，再强化学习协调；用 7,134 例脓毒症与 7,895 例对照、9 个系统 125 个变量训练，支持替代治疗的反事实模拟。',
   shift='世界模型的另一种做法：不是单一潜空间模型，而是多个 LLM Agent 协作模拟（编者解读）。对象是 ICU 数据而非可穿戴。',
   links=[])


org('abbott', 'Abbott（雅培）', 'other')
up(id='amazon-halo', date='2020-08-27', dateLabel='发布 2020-08-27；2023-04-26 宣布停止支持（2023-07-31 生效）', track='param', org='amazon', type='product',
   title='Introducing Amazon Halo and Amazon Halo Band（2023 年停止支持）', short='Amazon Halo：通用科技公司进入可穿戴，三年后退出',
   url='https://press.aboutamazon.com/2020/8/introducing-amazon-halo-and-amazon-halo-band-a-new-service-that-helps-customers-improve-their-health-and-wellness',
   sources=[{"label": "Amazon 2023-04-26：Our decision to wind down Amazon Halo", "url": "https://www.aboutamazon.com/news/company-news/amazon-halo-discontinued"}],
   q='没有健康数据积累的通用科技公司，能否靠自有手环建立健康入口？',
   how='2020 年推出 Halo 手环与订阅服务（活动、睡眠、语气、体成分）；2023 年 4 月宣布 7 月 31 日起停止支持并为近 12 个月的购买退款。',
   shift='反面案例：亚马逊 2026 年重回健康 AI 时不再做设备，而是从 One Medical 病历与医生服务切入（编者解读）。',
   links=[])
BY['amazon-health-ai']['shift'] = BY['amazon-health-ai']['shift'].replace('时间线上亚马逊目前只有 Chronos 一条。', '亚马逊此前的两条线是通用时序模型 Chronos 和 2023 年停掉的 Halo 手环。')
addlink('amazon-health-ai', L('amazon-halo', '转向', '从自有手环转为以病历和医生服务为入口（编者解读）'))
up(id='stelo-otc', date='2024-03-05', dateLabel='FDA 新闻稿 2024-03-05', track='param', org='dexcom', type='announce',
   title='FDA Clears First Over-the-Counter Continuous Glucose Monitor (Dexcom Stelo)', short='首个非处方 CGM 获 FDA 许可',
   url='https://www.fda.gov/news-events/press-announcements/fda-clears-first-over-counter-continuous-glucose-monitor',
   q='连续血糖数据能否从糖尿病患者扩展到普通人？',
   how='FDA 许可 Dexcom Stelo 为首个非处方 CGM，面向不使用胰岛素的成人。',
   shift='为血糖数据进入消费可穿戴与基础模型打开了数据来源：随后有 Oura × Dexcom、CGM-LSM、GlucoFM（编者解读）。',
   links=[])
for eid in ('oura-dexcom', 'dexcom-genai'):
    if eid in BY: addlink(eid, L('stelo-otc', '奠基', '非处方 CGM 提供数据来源'))
up(id='abbott-google', date='2026-08-11', dateLabel='雅培新闻稿 2026-08-11', track='agent', org='abbott', type='announce',
   title='Abbott and Google launch first-of-its-kind partnership to transform everyday health through glucose insights and AI', short='雅培 × 谷歌：Lingo 血糖数据进入 Google Health Coach',
   url='https://abbott.mediaroom.com/2026-08-11-Abbott-and-Google-launch-first-of-its-kind-partnership-to-transform-everyday-health-through-glucose-insights-and-AI',
   q='教练 Agent 怎样获得血糖这类代谢数据？',
   how='多年合作：雅培 Lingo 生物传感器的连续血糖洞察进入 Google Health app，由 Google Health Coach 给出营养、活动、睡眠与恢复建议（需 Google Health Premium）；合作包含一项大规模研究。',
   shift='与 Oura × Dexcom 对称：设备 Agent 通过合作补上血糖数据（编者解读）。',
   links=[L('oura-dexcom', '呼应', '同为可穿戴 + CGM 的合作，Oura 选 Dexcom、谷歌选雅培'), L('google-health-app', '接入', '血糖数据进入 Google Health Coach')])
up(id='google-biomarker-agent', date='2026-08-21', dateLabel='谷歌研究博客 2026-08-21', track='agent', org='google', type='paper',
   title='An AI tool for prioritizing candidate biomarkers from wearable sensor data (Biomarker Discovery Framework)', short='谷歌：从可穿戴数据筛选候选生物标志物的多 Agent 系统',
   url='https://research.google/blog/an-ai-tool-for-prioritizing-candidate-biomarkers-from-wearable-sensor-data/',
   q='Agent 能否帮研究者从可穿戴数据中发现新的生物标志物？',
   how='多 Agent 系统在人类监督下迭代：规划、数据检查、检索文献、构造特征、统计关联与多重检验、对抗式审查（泄漏、过拟合、混杂），最后生成供专家审阅的草稿；官方强调关联不等于因果。',
   shift='Agent 的用途从“回答用户”扩展到“做研究”，与 PHA 的数据科学家角色一脉相承（编者解读）。',
   links=[L('pha', '继承', 'PHA 中的数据科学 Agent 发展为独立的科研工具')])
up(id='samsung-galaxyai-watch', date='2024-05-29', dateLabel='三星新闻稿 2024-05-29', track='param', org='samsung', type='product',
   title='Galaxy AI Is Coming to New Galaxy Watch for More Motivational Health', short='三星：Galaxy AI 进入手表（Energy Score）',
   url='https://news.samsung.com/global/galaxy-ai-is-coming-to-new-galaxy-watch-for-more-motivational-health',
   q='手表上的多项指标怎样汇成一个可行动的每日判断？',
   how='One UI 6 Watch 把端侧 AI 与 Samsung Health 结合，推出综合睡眠、活动、心率等的 Energy Score 与个性化建议（官方称）。',
   shift='三星的“Galaxy AI 健康”起点；它是指标层的综合分，与之后的 HiMAE、X-MAE 等基础模型研究分属不同层次（编者解读）。',
   links=[])
addlink('apple-vitals', L('samsung-galaxyai-watch', '并行', '同年各家推出“每日状态”类综合指标'))


org('mountsinai', '西奈山伊坎医学院', 'academic'); org('osu', '俄亥俄州立大学 等', 'academic'); org('timetrace', 'TimeTrace Labs × 牛津大学', 'other')
up(id='apple-ppgage', date='2025-10-20', dateLabel='Nature Communications 2025-10-20', track='signal', org='apple', type='paper',
   title='A wearable-based aging clock associates with disease and behavior (PpgAge)', short='苹果 PpgAge：手腕 PPG 的衰老时钟',
   url='https://www.nature.com/articles/s41467-025-64275-4',
   q='手表 PPG 能否给出可反复测量的“生理年龄”，并与疾病和行为相关？',
   how='在 Apple Heart & Movement Study（213,593 名参与者、超过 1.49 亿参与者日）上构建 PpgAge，使其在健康人群中预测实际年龄；“PpgAge 差”与心脏病事件、吸烟、运动、睡眠相关，孕期与部分心脏事件时明显上升（论文称；观察性分析）。',
   shift='健康年龄一线的学术源头之一：同一队列、同一 PPG 信号，从“表征”走到“年龄差”这一可解释指标。论文作者与起点论文团队有重叠（编者解读）。',
   links=[L('apple-iclr24', '继承', '同一队列的手腕 PPG 与同一团队成员'), L('oura-cvage', '呼应', '同为从 PPG 推算的“年龄”指标')])
addlink('apple-health-app', L('apple-ppgage', '呼应', '“年龄差”类指标的学术基础（官方未说明是否用于产品）'))
up(id='heartbeit', date='2023-06-06', dateLabel='npj Digital Medicine 2023-06-06', track='signal', org='mountsinai', type='paper',
   title='A foundational vision transformer improves diagnostic performance for electrocardiograms (HeartBEiT)', short='HeartBEiT：850 万份心电的掩码图像预训练',
   url='https://doi.org/10.1038/s41746-023-00840-9',
   q='在自然图像上预训练再迁移到心电，是否不如直接在心电上预训练？',
   how='把心电波形当作图像，用掩码图像建模在 850 万份心电上预训练视觉 Transformer，在肥厚型心肌病、低射血分数、ST 段抬高心梗等诊断上与标准 CNN 比较（论文称）。',
   shift='起点论文之前、临床心电一侧的“基础模型”尝试；数据来自医院 12 导联而非可穿戴（编者解读）。',
   links=[])
addlink('ecgfounder', L('heartbeit', '继承', '临床心电大规模预训练的延续')) if 'ecgfounder' in BY else None
up(id='pulse-ecg', date='2024-10-21', dateLabel='arXiv 2024-10；npj Digital Medicine 2026', track='agent', org='osu', type='open',
   title='Teach Multimodal LLMs to Comprehend Electrocardiographic Images (PULSE)', short='PULSE：教多模态大模型读心电图图像',
   url='https://arxiv.org/abs/2410.19008',
   q='只有打印或拍照心电图时，多模态大模型能否读懂？',
   how='构建 100 多万条样本的心电图像指令微调数据集 ECGInstruct，训练 PULSE，并建立心电图像理解基准。',
   shift='语言接口的另一入口：不从原始波形，而从“图像化的心电”接入大模型（编者解读）。',
   links=[L('ecgfounder', '分岔', '同为心电通用模型，PULSE 走图像 + 语言')] if 'ecgfounder' in BY else [])
up(id='sonata', date='2026-04-20', dateLabel='arXiv 2026-04', track='world', org='timetrace', type='paper',
   title='Sonata: A Hybrid World Model for Inertial Kinematics under Clinical Data Scarcity', short='Sonata：小数据下的 IMU 潜空间世界模型',
   url='https://arxiv.org/abs/2604.18058',
   q='临床队列只有几十到几百人，掩码重建式预训练是否合适？',
   how='377 万参数的紧凑模型，在 9 个公开数据集（739 人、19 万窗口）上以“预测未来潜状态”而非重建原始信号为目标预训练；在相同骨干上与自回归预测基线对照，冻结探针的临床判别、跌倒风险预测与跨队列迁移均更好（论文称）。',
   shift='预训练目标轴上的一个对照实验：在可穿戴 IMU 上直接比较“世界模型目标”与重建 / 预测目标（编者解读）。',
   links=[])
addlink('ac-jepa', L('sonata', '呼应', '同为潜空间预测目标'))
up(id='healthjev', date='2026-07-15', dateLabel='arXiv 2026-07', track='agent', org='fudan', type='open',
   title='A Self-Evolving Agent for Longitudinal Personal Health Management (HealthJev)', short='HealthJev：会积累经验的长期健康 Agent',
   url='https://arxiv.org/abs/2607.13940',
   q='健康 Agent 怎样跨多次对话积累经验，又不把错误经验记下来？',
   how='把共享的安全规则与医学知识和私有的长期记忆分开，从完成的案例中提炼经验；自训练轻量门控模型 JevGate 决定哪些经验写入记忆。在基于 MIMIC-IV 轨迹、20 名用户 90 天模拟交互的基准上优于无记忆的 ReAct 与三种记忆增强框架（论文称）。',
   shift='Agent 一线从“单次回答”转向“长期记忆治理”（编者解读）。',
   links=[L('pha', '呼应', '个人健康 Agent 的长期化')])


# ---- 3b. 会议/期刊补扫（venues）：核对 Crossref / medRxiv API / 期刊页面后补录 ----
org('neu', '东北大学（美国）× RMIT', 'academic'); org('uw', '华盛顿大学 等', 'academic'); org('pheno', 'Pheno.AI × MBZUAI', 'other')
up(id='gloss', date='2025-09-03', dateLabel='IMWUT 2025-09', track='agent', org='neu', type='paper',
   title='GLOSS: Group of LLMs for Open-ended Sensemaking of Passive Sensing Data for Health and Wellbeing', short='GLOSS：多 LLM 协作解读被动感知数据',
   url='https://doi.org/10.1145/3749474',
   q='手机与可穿戴的被动感知数据，能否由 LLM 做开放式、可交叉印证的解读？',
   how='由多个 LLM 分工协作，对被动感知数据做开放式的“意义建构”（sensemaking）与数据交叉印证，面向研究者等不同使用者（论文称）。',
   shift='与谷歌 PHIA 同一问题在 UbiComp 社区的回答：多智能体、开放式，而非单一问答（编者解读）。',
   links=[L('phia', '呼应', '同为让 LLM 解读个人传感数据')])
up(id='llm-clin-insights', date='2024-05-13', dateLabel='IMWUT 2024-05', track='agent', org='uw', orgNote='与 MIT、UCSD 合作', type='paper',
   title='From Classification to Clinical Insights: Towards Analyzing and Reasoning About Mobile and Behavioral Health Data With Large Language Models', short='从分类到临床洞见：LLM 推理行为健康感知数据',
   url='https://doi.org/10.1145/3659604',
   q='LLM 能否从多传感器数据中为心理健康专业人员综合出临床洞见？',
   how='用思维链提示让 LLM 推理活动、睡眠、社交数据与抑郁、焦虑等状况的关系，并生成面向临床的洞见（论文称）。',
   shift='与 Health-LLM 同期，从“预测标签”转向“生成解释”，是 Agent 一线在 UbiComp 侧的起点之一（编者解读）。',
   links=[L('health-llm', '并行', '同期让 LLM 读可穿戴 / 行为数据')])
up(id='hanghaomeng', date='2026-02-09', dateLabel='npj Digital Medicine 2026-02-09（Perspective）', track='agent', org='zju', orgNote='杭州市第七人民医院、浙江大学、蚂蚁集团', type='product',
   title='Toward integrated sleep health: multimodal AI in Hang Hao Meng agent', short='“杭好梦”：已规模部署的睡眠健康专家 Agent',
   url='https://doi.org/10.1038/s41746-026-02432-9',
   q='睡眠医学的专科能力能否由 Agent 规模化提供？',
   how='介绍睡眠健康专家 Agent“杭好梦”：量表评估、自由文本分析、分诊与失眠认知行为治疗等；文章称已为 400 多万人提供分诊、完成 9 万多次筛查（Perspective，非对照研究）。',
   shift='中国医院与互联网公司合作的专科 Agent，入口来自医院与平台而非可穿戴设备（编者解读）。',
   links=[L('oppo-healthagent', '呼应', '国内健康 Agent 的另一种入口：医院 + 平台')])
up(id='pheno-agent', date='2026-08-17', dateLabel='medRxiv 2026-08', track='agent', org='pheno', type='paper',
   title='Grounding Health AI: Architecture and Evaluation of a Domain-Expert Metabolic Health Agent', short='代谢健康 Agent：用工具计算，避免编造指标',
   url='https://doi.org/10.64898/2026.08.11.26359946',
   q='通用大模型写 CGM 报告会编造派生指标，怎样让 Agent 的数字可靠？',
   how='示例对比中，主流基础模型在相同的两周 CGM 与饮食数据上编造了 MAGE 等派生指标；作者提出以 Human Phenotype Project（1.3 万多名深度表型参与者）为参照、配 21 个领域工具的代谢健康 Agent，分层“接地”生成（论文称）。',
   shift='为“Agent 调用工具与模型、而不是自己算”的架构提供了直接的失败案例（编者解读）。',
   links=[L('pha', '呼应', '同为个人健康 Agent，强调计算接地'), L('gluformer', '奠基', '同一深度表型队列（编者解读：均来自 HPP 研究体系）')])
up(id='healthflux', date='2026-09-21', dateLabel='medRxiv 2026-09', track='world', org='stanford', orgNote='与华盛顿大学等合作', type='paper',
   title='A world model simulates the latent dynamics of human health (HealthFlux)', short='HealthFlux：全模态的人体健康世界模型',
   url='https://doi.org/10.64898/2026.09.19.26363460',
   q='诊断、化验、分子与影像各看到健康的一面，能否推断一个统一、随时间演化的潜在健康状态？',
   how='在 UK Biobank 502,166 名参与者、11 个数据域的 4,920 项特征与三维脑和身体 MRI 上，用 ODE 演化 + 连续时间循环更新的混合状态空间模型学习潜在健康动力学；无新观测的递归模拟可预测 20 年内 1,256 种疾病与死亡，并做用药条件的虚拟临床试验（论文称）。',
   shift='世界模型纲在学术侧的“全模态”版本：与 SensorWM 同期，但不含可穿戴原始信号（编者解读）。',
   links=[L('delphi', '继承', '从疾病事件序列的生成扩展到全模态潜在状态'), L('healthformer', '并行', '同年的健康状态动力学与干预模拟')])
up(id='biolt', date='2026-11-09', dateLabel='medRxiv 2026-11-09', track='signal', org='oxford', orgNote='与帝国理工学院合作', type='paper',
   title='BioLT: Streaming Biosignal Modeling', short='BioLT：把窗口级生理模型变成小时级流式模型',
   url='https://doi.org/10.64898/2026.11.06.26367429',
   q='ECG、PPG、EEG 越来越是小时级、断断续续的流，10 秒窗口的模型怎么用？',
   how='仅解码器的流式框架：把窗口间隔时间作为显式输入，配固定大小、以累计统计量监督的压缩记忆，训练与推理随记录长度线性增长；可把任何窗口级特征或六种生理基础模型的嵌入变成流式模型，在心律失常、脓毒症、癫痫检测与 20 分钟预测上评测（论文称）。',
   shift='“建在哪一层”的另一种回答：不换模型，而在已有基础模型之上加长上下文（编者解读）。',
   links=[L('beyond-static', '呼应', '从短窗口走向长期上下文'), L('lsm2', '呼应', '把缺失与间隔当作信息')])
src('sleepfounder', 'DOI 10.1101/2025.09.06.25335216', 'https://doi.org/10.1101/2025.09.06.25335216')
src('sensorwm', 'NeurIPS 2026 世界模型 workshop 论文：Developing World Models from Wearable Sensors（OpenReview，2026-10-02 发布）', 'https://openreview.net/forum?id=8SH3daIGHz')
if 'workshop' not in BY['sensorwm']['dateLabel']: BY['sensorwm']['dateLabel'] = BY['sensorwm']['dateLabel'].rstrip('；') + '；世界模型部分先以 NeurIPS 2026 workshop 论文在 OpenReview 公开（2026-10-02，两位谷歌作者）'

# 链接到新条目
addlink('delphi', L('organ-agents', '呼应', '同为生成式的健康轨迹模拟'))
for eid, f in [('mai-dxo','amie'),('apple-speech-fm','hear'),('glucofm','cgm-lsm'),('robust-ppg-dolby','pulse-ppg')]:
    for l in BY[eid]['links']:
        if l['from'] == f: l['type'] = '呼应'
addlink('whoop-5', L('oura-cvage', '呼应', '“年龄差”类指标：Oura 2024 年先推出心血管年龄'))



# 深读条目中指向“后来者”的关系：反转方向（挂到较晚的条目上），并把跨度过大的“并行”改为“呼应”
from datetime import date as _d
def _dd(a, b):
    f = lambda x: _d(*[int(t) for t in (x + '-01-01')[:10].split('-')[:3]]) if len(x) >= 7 else _d(int(x), 1, 1)
    return abs((f(a[:10] if len(a) >= 10 else a + '-01'[:10 - len(a)] if len(a) == 7 else a) - f(b[:10] if len(b) >= 10 else b + '-01' if len(b) == 7 else b)).days)
DRIDS = [x['id'] for x in json.load(open(DC))]
for eid in DRIDS:
    e = BY[eid]; keep = []
    for l in e['links']:
        if BY[l['from']]['date'] > e['date']:
            addlink(l['from'], {"from": eid, "type": l['type'], "note": l['note']})
        else: keep.append(l)
    e['links'] = keep
for e in E:
    for l in e['links']:
        if l['type'] == '并行' and _dd(e['date'], BY[l['from']]['date']) > 430: l['type'] = '呼应'

# ---- 4. 脉络、公司、问题 ----
TH = {t['id']: t for t in M['threads']}
def step(tid, eid, role):
    if eid not in [x['id'] for x in TH[tid]['steps']]: TH[tid]['steps'].append({"id": eid, "role": role})
for tid, eid, role in [
    ('deploy', 'samsung-sleepapnea', '三星：睡眠呼吸暂停功能获 FDA De Novo（新分类）'),
    ('deploy', 'samsung-lvsd', '三星：医院心电 AI 迁移到手表（LVSD，韩国批准）'),
    ('deploy', 'fda-wellness-2026', '监管：FDA 放宽低风险健康功能的指南'),
    ('deploy', 'oura-health-radar', 'Oura：血压信号与夜间呼吸，不给数值'),
    ('deploy', 'google-health-guardian', '谷歌：官方称建立在健康基础模型之上的血压趋势'),
    ('deploy', 'google-htn-nature', '谷歌：自监督 PPG + 加速度的高血压筛查（Nature）'),
    ('person', 'har-scaling', '尺度律：增加“人数”比增加每人数据更有效'),
    ('person', 'google-htn-nature', '以人为单位、长期佩戴数据上的筛查'),
    ('healthage', 'oura-cvage', 'Oura：从 PPG 推算心血管年龄（2024）'),
    ('dynamics', 'glucofm', '谷歌：血糖的慢趋势与短期偏离双流建模'),
    ('dynamics', 'soter', '连续时间解码器：任意时刻预测与插补'),
    ('dynamics', 'beyond-static', '立场：从静态编码器走向纵向、前瞻'),
    ('dynamics', 'organ-agents', '多 Agent 模拟器官系统与反事实治疗（ICU）'),
    ('objective', 'glucofm', '潜空间预测 + 双流动力学预测'),
    ('objective', 'robust-ppg-dolby', '用同步 ECG/呼吸定义“生理相似”做对比'),
    ('objective', 'heartlang', '按心搏分词再做自监督'),
    ('objective', 'osf-sleep', '系统比较睡眠预训练选择'),
    ('objective', 'inertia-1', '系统比较加速度预训练的目标与数据'),
    ('modality', 'sleep2vec', '九种睡眠模态的对齐与尺度律'),
    ('modality', 'reve', 'EEG：任意电极布局、25,000 人'),
    ('modality', 'opera', '呼吸声：开放模型与 19 项基准'),
    ('crossmodal', 'apple-speech-fm', '苹果：语音模型的特征迁移到可穿戴时序'),
    ('crossmodal', 'sleep2vec', '睡眠多模态对比对齐'),
    ('open', 'aether-scaling', '生理波形的计算最优尺度律（最大到 21 亿参数）'),
    ('open', 'har-scaling', '活动识别的尺度律'),
    ('open', 'inertia-1', '1,820 万小时加速度的开放研究'),
    ('open', 'opera', '开放呼吸声模型'),
    ('open', 'soter', '2,260 亿时间点预训练的生成式模型'),
    ('language', 'neurolm', 'EEG 当外语：神经 token 交给 LLM'),
    ('language', 'opentslm', '时序作为原生模态接入 LLM'),
    ('language', 'hearts', '基准：LLM 读健康时序明显不如专门模型'),
    ('language', 'ms-waveform-position', '微软立场：可核验的波形推理'),
    ('care', 'gptcoach', '学界：按动机访谈设计 LLM 教练'),
    ('care', 'google-health-app', '谷歌：Health app 与正式版 Coach'),
    ('care', 'oura-health-radar', 'Oura：Health Radar 与医生问诊导流'),
    ('care', 'mai-dxo', '微软：多角色辩论的诊断编排（研究）'),
    ('platform', 'chatgpt-health-ga', 'OpenAI：ChatGPT Health 在美国全面推送'),
    ('platform', 'amazon-health-ai', '亚马逊：One Medical 健康 AI 助手'),
    ('platform', 'withings-mcp', 'Withings：以连接器把数据交给通用助手'),
    ('healthage', 'apple-ppgage', '苹果：PpgAge，21 万人队列上的 PPG 衰老时钟（Nature Communications）'),
    ('modality', 'heartbeit', '临床心电：掩码图像预训练（2023）'),
    ('language', 'pulse-ecg', '心电图像 + 多模态大模型'),
    ('objective', 'sonata', 'IMU 上对照“预测未来潜状态”与重建目标'),
    ('dynamics', 'sonata', '小数据临床场景的潜空间世界模型'),
    ('care', 'healthjev', '学界：带长期记忆治理的健康 Agent'),
    ('dynamics', 'apple-ltf', '苹果：可穿戴多变量时序的潜空间生成流（2022）'),
    ('dynamics', 'apple-hybrid-cv', '苹果：心血管机理模型 + 机器学习（模拟推断）'),
    ('dynamics', 'apple-ppg-hybrid', '苹果：PPG 的混合建模，机理先验进入表征'),
    ('person', 'apple-physiomtl', '苹果：用最优传输的多任务学习做个人化生理模式'),
    ('objective', 'maeeg', '苹果：EEG 掩码自编码（掩码一支的早期节点）'),
    ('objective', 'biofame', '苹果：频率感知的多模态掩码自编码'),
    ('objective', 'apple-pars', '苹果：EEG 成对相对位移预测'),
    ('modality', 'biofame', '任意模态组合的生理信号预训练'),
    ('modality', 'apple-cpep', '苹果肌电：姿态—EMG 对比预训练'),
    ('modality', 'sleepfounder', '睡眠：只用心肺信号的低负担模型'),
    ('crossmodal', 'apple-xmodal', '苹果：促进跨模态表征的机制研究'),
    ('crossmodal', 'apple-cpep', '用姿态作为肌电的“老师”'),
    ('crossmodal', 'apple-embridge', '苹果：EMG 跨模态表征（ICLR 2026）'),
    ('crossmodal', 'robust-ppg-dolby', '用同步 ECG/呼吸给 PPG 定义相似度'),
    ('level', 'motionprint', '苹果：设备与佩戴位置无关的运动模型'),
    ('language', 'apple-llm-fusion', '苹果：LLM 做多传感器的后期融合'),
    ('objective', 'apple-ecg-denoise', '苹果前史：手表 ECG 的表征与去噪（2020）'),
    ('care', 'samsung-galaxyai-watch', '三星：Galaxy AI 进入手表，Energy Score 与建议'),
    ('language', 'llm-clin-insights', '学界：LLM 从行为感知数据生成临床洞见（IMWUT 2024）'),
    ('language', 'gloss', '学界：多 LLM 开放式解读被动感知数据'),
    ('language', 'pheno-agent', '代谢健康 Agent：通用模型会编造指标，计算要交给工具'),
    ('platform', 'hanghaomeng', '国内：医院 + 平台的睡眠专科 Agent（400 多万人分诊）'),
    ('dynamics', 'healthflux', '学界：UK Biobank 上的全模态健康世界模型'),
    ('level', 'biolt', '在基础模型之上做小时级流式上下文'),
    ('platform', 'amazon-halo', '亚马逊：自有手环入口（2020），2023 年退出'),
    ('data', 'stelo-otc', '监管：首个非处方 CGM，血糖数据走向大众'),
    ('care', 'abbott-google', '雅培 × 谷歌：血糖进入教练'),
    ('language', 'google-biomarker-agent', '谷歌：多 Agent 从可穿戴数据筛选生物标志物'),
    ('platform', 'google-health-app', '谷歌：Fitbit 应用改为 Google Health app'),
]: step(tid, eid, role)
for t in M['threads']: t['steps'].sort(key=lambda x: BY[x['id']]['date'])
C = {c['org']: c for c in M['companies']}
def cadd(o, part, ids, text=None):
    c = C.get(o)
    if not c: return
    for i in ids:
        if i not in c[part]['ids']: c[part]['ids'].append(i)
    if text and text not in c[part]['text']: c[part]['text'] += text
cadd('google', 'model', ['har-scaling', 'glucofm', 'google-htn-nature'], ' 2025–2026：活动识别尺度律、GlucoFM（血糖）与 Nature 高血压筛查（自监督 PPG + 加速度）。')
cadd('google', 'model', ['google-biomarker-agent'], None)
cadd('google', 'product', ['abbott-google', 'google-health-app', 'google-health-guardian'], ' 2026：Fitbit 应用改为 Google Health app、Coach 正式版；Pixel Watch 5 的 Health Guardian（官方称建立在健康基础模型之上）。')
cadd('samsung', 'product', ['samsung-galaxyai-watch', 'samsung-sleepapnea', 'samsung-lvsd'], ' 睡眠呼吸暂停（FDA De Novo，2024-02）与 LVSD 检测（与 Medical AI 合作，2025-10）。')
cadd('oura', 'product', ['oura-cvage', 'oura-health-radar'], ' 心血管年龄（2024-05）；Health Radar 的血压信号与夜间呼吸（2026-05）。')
cadd('apple', 'model', ['apple-ecg-denoise', 'apple-physiomtl', 'apple-ltf', 'maeeg', 'apple-hybrid-cv', 'biofame', 'motionprint', 'apple-xmodal', 'apple-speech-fm', 'apple-cpep', 'apple-llm-fusion', 'apple-pars', 'apple-ppg-hybrid', 'apple-ppgage', 'apple-embridge'], None)
C['apple']['model']['text'] = ('前史：可穿戴 ECG 表征与去噪（2020）、被试感知对比（2021）、个体动力学（血糖 2020、运动心率 2022）、潜空间生成流（2022）、EEG 掩码自编码（2022）'
  ' → 起点 PPG/ECG 模型与频率感知的多模态掩码自编码（2023）→ 相对对比的运动模型、PPG 蒸馏进加速度、行为模型 WBM → 跨模态、跨设备、多源报告的表征研究，'
  '以及肌电（CPEP、EMBridge）、语音模型迁移、PpgAge 衰老时钟。机理一支没有停：心血管模拟推断（2023）与 PPG 混合建模（2025）把生理模型与学习结合，但尚无公开的“动作条件”世界模型。')
for c in M['companies']:
    if c['org'] == 'aico':
        cadd('aico', 'product', ['amazon-halo', 'chatgpt-health-ga', 'amazon-health-ai', 'withings-mcp'], ' 2026：ChatGPT Health 全面推送、亚马逊 One Medical 健康 AI；设备公司 Withings 反向以连接器接入通用助手。')
        cadd('aico', 'model', ['mai-dxo', 'ms-waveform-position'], None)


# ---- 5. 叙事与判断随新条目修订 ----
ES = M['essay']
ES[6] = ES[6].replace('谷歌是唯一在 2024–2026 年四条纲都有论文、且层与层接口公开的一家（苹果的动力学工作停在 2022 年）',
    '谷歌在 2024–2026 年四条纲都有论文，且层与层的接口公开（苹果的论文同样覆盖四条纲，但动力学一侧是机理与学习的混合建模，没有以行为为动作的推演）')
if 'Health Guardian' not in ES[3]:
    ES[3] = ES[3].rstrip() + ' 2026 年谷歌给出第二个例子：Pixel Watch 5 的 Health Guardian 官方称建立在健康基础模型之上，同期 Nature 论文报告了自监督 PPG + 加速度的高血压筛查（编者解读：两者的对应关系以官方“helped inform”的表述为准）。'
for e in M['eras']:
    if e['id'] == 'e4' and 'Aether' not in e['thesis']:
        e['thesis'] = e['thesis'].rstrip('。') + '；尺度律（Aether、睡眠 OSF、加速度 Inertia-1）与基准（HEARTS）给出更系统的结论，立场论文主张越过“静态编码器”。监管与入口也在变：FDA 放宽低风险健康功能，谷歌、Oura 推出不显示数值的血压信号功能，ChatGPT Health 全面推送，Withings 以连接器把数据交给通用助手。'
    if e['id'] == 'e1' and 'bioFAME' not in e['thesis']:
        e['thesis'] = e['thesis'].rstrip() + ' 起点论文之前三个月，苹果已公开频率感知的多模态掩码自编码（bioFAME，2023-09），与起点论文分属掩码与对比两支。'
for c in M['companies']:
    if c['org'] == 'google' and isinstance(c.get('note'), str):
        c['note'] = c['note'].replace('唯一', '').replace('谷歌是在', '谷歌在')


addlink('apple-passport', L('biofame', '继承', '苹果内部延续：任意模态组合的生理信号预训练 → 跨设备、跨通道的表征'))
addlink('apple-passport', L('apple-xmodal', '继承', '苹果内部延续：跨模态表征研究'))
src('whoop-2026', 'WHOOP：2026 What’s New', 'https://www.whoop.com/us/en/thelocker/2026-whats-new/')
src('apple-ppgage', 'DOI 10.1038/s41467-025-64275-4', 'https://doi.org/10.1038/s41467-025-64275-4')
C['apple']['model']['text'] = C['apple']['model']['text'].replace('机理一支没有停：心血管模拟推断（2023）与 PPG 混合建模（2025）把生理模型与学习结合，但尚无公开的“动作条件”世界模型。',
    '学习式的动力学工作停在 2022 年，之后转为“模拟 + 学习”：心血管模拟推断（2023）与 PPG 混合建模（2025）把生理机理模型与学习结合；尚无公开的“以行为为动作”的世界模型。')
ES[6] = ES[6].replace('但动力学一侧是机理与学习的混合建模，没有以行为为动作的推演', '但学习式动力学停在 2022 年，之后转为机理模拟与学习的混合建模，没有以行为为动作的推演')

BY['normwear-wm']['shift'] = '世界模型的思路落到原始信号层，而不只是分钟、天级参数，并且显式建模干预变量。一个月前的 Sonata 已在 IMU 上用“预测未来潜状态”作预训练目标，但没有动作变量（编者解读）。'
addlink('normwear-wm', L('sonata', '呼应', '同为原始信号层的潜空间动力学，Sonata 无动作变量'))


QS = {q['id']: q for q in M['questions']}
def qadd(qid, era_, ids, text):
    c = [c for c in QS[qid]['cells'] if c['era'] == era_][0]
    for i in ids:
        if i not in c['ids']: c['ids'].append(i)
    k = 'text' if 'text' in c else 'a'
    if text not in c[k]: c[k] = c[k].rstrip('。') + '；' + text + '。'
qadd('sup', 'e0', ['maeeg'], '掩码重建也已出现（苹果 MAEEG）')
qadd('sup', 'e4', ['sonata', 'robust-ppg-dolby'], '预测未来潜状态（Sonata）；用同步 ECG 与呼吸派生的“生理相似度”')
qadd('level', 'e4', ['biolt'], '或者不换模型，在基础模型之上加小时级的流式上下文')
qadd('ask', 'e3', ['apple-ppgage'], '“年龄差”这类可长期追踪的指标能否预示疾病')
qadd('ask', 'e4', ['healthflux'], '学术侧也在问：能否从全模态证据模拟 20 年的健康演化')
qadd('act', 'e4', ['chatgpt-health-ga', 'pheno-agent'], '通用模型会编造派生指标，计算要交给工具')
qadd('open', 'e2', ['opera'], '开放的呼吸声模型与基准')
qadd('open', 'e4', ['aether-scaling', 'hearts', 'inertia-1'], '尺度律、LLM 时序基准与开放的运动模型研究')

# era / 排序
def era(d): return 'e0' if d < '2023-12' else 'e1' if d < '2024-06' else 'e2' if d < '2025-07' else 'e3' if d < '2026-01' else 'e4'
for e in E:
    e['era'] = era(e['date'])
    if e['era'] == 'e0': e['prelude'] = True
    else: e.pop('prelude', None)
E.sort(key=lambda e: e['date'])
json.dump(D, open(P, 'w'), ensure_ascii=False, indent=1)
json.dump(M, open(MP, 'w'), ensure_ascii=False, indent=1)
print('v4 entries', len(E))
