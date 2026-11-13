# 生成 data/meta.json —— 改这里或直接改 JSON 都可以（JSON 是最终数据源）
import json
meta = {
 "updated": "2026-11-13",
 "tracks": [
  {"id":"signal","name":"生理信号基础模型","short":"信号","en":"Signal FMs · 原始波形","color":"#2e6b6e",
   "desc":"直接面向原始波形（PPG、ECG、加速度、EEG、EMG）学习可迁移的通用表征。"},
  {"id":"param","name":"生理参数基础模型","short":"参数","en":"Parameter & behavior FMs · 分钟到周","color":"#9a6a24",
   "desc":"面向已提取的心率、HRV、睡眠、步数、血糖等指标，以及由它们组成的行为序列。"},
  {"id":"world","name":"生理世界模型","short":"世界模型","en":"Physiological world models · 动力学","color":"#8c4a3f",
   "desc":"建模生理状态如何随时间、行为与干预演化，用于预测、补全和“如果……会怎样”的推演。"},
  {"id":"agent","name":"Agent","short":"Agent","en":"Health agents · 解释与行动","color":"#3e5677",
   "desc":"把生理理解变成解释、提醒、计划与行动，并逐步接入病历、化验与医生。"}
 ],
 "types": [
  {"id":"paper","label":"论文"},
  {"id":"open","label":"开源模型"},
  {"id":"product","label":"产品"},
  {"id":"announce","label":"宣布/在建"}
 ],
 "relations": {
  "继承": {"key":"inherit","color":"#4a4844","desc":"沿用前作的核心做法并推进"},
  "转向": {"key":"pivot","color":"#8c4a3f","desc":"保留问题，换了建模对象或范式"},
  "分岔": {"key":"branch","color":"#9a6a24","desc":"从同一思路分出新的方向或模态"},
  "并行": {"key":"parallel","color":"#7c7871","desc":"同期独立出现的相近思路"},
  "落地": {"key":"deploy","color":"#2e6b6e","desc":"研究进入产品或服务"}
 },
 "orgGroups": [
  {"id":"apple","label":"苹果"},{"id":"google","label":"谷歌"},{"id":"samsung","label":"三星"},
  {"id":"oura","label":"Oura"},{"id":"whoop","label":"WHOOP"},{"id":"oppo","label":"OPPO"},
  {"id":"other","label":"其他公司"},{"id":"academic","label":"学术源头"}
 ],
 "orgs": {
  "apple":{"label":"苹果","group":"apple"},
  "google":{"label":"谷歌","group":"google"},
  "samsung":{"label":"三星","group":"samsung"},
  "oura":{"label":"Oura","group":"oura"},
  "whoop":{"label":"WHOOP","group":"whoop"},
  "oppo":{"label":"OPPO","group":"oppo"},
  "huawei":{"label":"华为","group":"other"},
  "xiaomi":{"label":"小米","group":"other"},
  "garmin":{"label":"Garmin","group":"other"},
  "meta":{"label":"Meta","group":"other"},
  "amazon":{"label":"Amazon","group":"other"},
  "microsoft":{"label":"微软","group":"other"},
  "irhythm":{"label":"iRhythm × 斯坦福","group":"other"},
  "dexcom":{"label":"Dexcom","group":"other"},
  "openai":{"label":"OpenAI","group":"other"},
  "nokia":{"label":"诺基亚贝尔实验室","group":"other"},
  "weizmann":{"label":"魏茨曼研究所 × NVIDIA","group":"other"},
  "cambridge":{"label":"剑桥大学","group":"academic"},
  "oxford":{"label":"牛津大学","group":"academic"},
  "mit":{"label":"MIT","group":"academic"},
  "sjtu":{"label":"上海交通大学","group":"academic"},
  "uiuc":{"label":"孟菲斯大学 × UIUC","group":"academic"},
  "ucsd":{"label":"加州大学圣迭戈分校","group":"academic"},
  "pku":{"label":"北京大学","group":"academic"},
  "embl":{"label":"EMBL-EBI × DKFZ 等","group":"academic"}
 },
 "eras": [
  {"id":"e0","no":"前奏 · 2019–2023","prelude":True,"title":"单任务监测与几处先声",
   "thesis":"深度学习先在单个任务上证明了可穿戴信号的价值（心律失常、房颤提醒）。“用个体本身做监督”、机理与学习混合的动力学模型、套在指标上的 LLM 教练，都已零星出现，但彼此还没有连起来。"},
  {"id":"e1","no":"起点 · 2023.12–2024.05","title":"不靠标签，以人为锚的通用表征",
   "thesis":"苹果在约 14 万名参与者的手表 PPG/ECG 上做自监督预训练，把同一参与者的两段信号当作正样本。它证明：没有医学标签，也能学到编码人口学与健康状态的表征。同期，学术界在加速度、EEG 和“让 LLM 直接读指标”上各自起步。"},
  {"id":"e2","no":"第二章 · 2024.06–2025.06","title":"扩张：模态、层级、开放与语言",
   "thesis":"表征从 PPG/ECG 扩散到加速度和其他模态；谷歌把建模对象从波形上移到分钟级指标，并在可穿戴数据上验证尺度律；开源 PPG 模型出现；LLM 与 Agent 开始以代码和检索读懂个人数据。"},
  {"id":"e3","no":"第三章 · 2025.07–2025.12","title":"分层与落地",
   "thesis":"上一章末苹果 WBM 给出了“波形还是行为”的答案：两层互补。本章苹果用自监督 PPG 特征提取器做出获 FDA 许可的高血压提醒；三星把基础模型做进手表算力；跨模态脚手架扩展到 ECG 教 PPG；Agent 从单一聊天变成多智能体框架和教练产品。"},
  {"id":"e4","no":"第四章 · 2026.01–2026.11","title":"动力学与闭环",
   "thesis":"建模对象从“此刻的状态”转向“状态如何演化”：生成式补全、干预模拟，再到以行为为动作的世界模型。Agent 开始把基础模型和世界模型当工具，并接入病历、化验和医生。"}
 ],
 "threads": [
  {"id":"person","name":"个体即监督：以人为锚的自监督",
   "desc":"缺少医学标签时，最便宜也最稳定的监督来自“同一个人”。从苹果早期的被试感知对比学习，到 ICLR 2024 的参与者级正样本，再到相对对比（RelCon、Pulse-PPG）和 OPPO 的被试感知预训练；2026 年苹果进一步发现，不同模态、独立训练的模型会收敛到相近的生理表征。",
   "steps":["p-cheng2021","apple-iclr24","apple-relcon","pulse-ppg","oppo-heartage","apple-symbolic"]},
  {"id":"crossmodal","name":"跨模态脚手架：贵模态教便宜模态",
   "desc":"训练时用信息更丰富或更接近生理机制的模态当老师，推理时只用便宜的模态：心率教加速度，PPG 教加速度，ECG 教 PPG，临床报告和文本教 ECG、PPG。这条线决定了基础模型能不能落到低功耗、单传感器的设备上。",
   "steps":["p-spathis2021","apple-accel","anyppg","xmae","oppo-heartage","ms-ecg-fm","hippt"]},
  {"id":"level","name":"层级上移：波形 → 指标 → 行为",
   "desc":"表征该建在哪一层？苹果从原始波形起步；谷歌 LSM 改用分钟级指标并验证尺度律；苹果 WBM 进一步上移到小时级行为并证明它与波形模型互补；LSM-2 把缺失本身纳入建模；SensorFM 在 500 万人上把这一层做大。",
   "steps":["apple-iclr24","lsm","lsm2","wbm","himae","sensorfm"]},
  {"id":"dynamics","name":"从表征到动力学：世界模型的形成",
   "desc":"表征回答“现在是什么状态”，世界模型回答“接下来会怎样、如果改变行为又会怎样”。这条线从苹果的机理与学习混合模型出发，经过生成式时序和疾病轨迹模型，到 2026 年以行为为动作、可做反事实推演的 SensorWM。",
   "steps":["p-miller2020","p-nazaret2022","lsm","gluformer","delphi","lsm2","healthformer","normwear-wm","sensorfm","sensorwm"]},
  {"id":"language","name":"语言接口：让模型读懂指标",
   "desc":"Agent 线其实最早出现（2023 年的 WHOOP Coach），但起初只是把摘要指标交给通用 LLM。此后的进展是让模型真正“读懂”数据：先微调和写代码分析（PH-LLM、PHIA），再做传感器与语言的对齐（SensorLM、HiPPT），最后由多智能体分工完成分析、解释和教练（PHA）。",
   "steps":["p-whoopcoach","health-llm","ph-llm","phia","sensorlm","pha","fitbit-coach","hippt"]},
  {"id":"care","name":"从建议到照护：Agent 的闭环",
   "desc":"可穿戴 Agent 的终点不是聊天，而是把洞察接到行动和照护上。2025 年前后是教练与问答；2026 年，Fitbit、WHOOP、ChatGPT 接入病历，WHOOP 引入医生问诊，Oura 收购 AI 原生初级保健公司 Counsel Health。",
   "steps":["p-whoopcoach","oura-advisor","dexcom-genai","garmin-ai","fitbit-coach","chatgpt-health","fitbit-2026","oura-womens","whoop-2026","samsung-ha","huawei-watch6","apple-health-app","oura-counsel"]},
  {"id":"apple","name":"苹果：从论文到产品",
   "desc":"苹果的路径最接近“基础模型先行，产品随后”：先建大型纵向研究（AHMS），再在其上训练 PPG/ECG、加速度、行为三类基础模型，随后把自监督 PPG 特征提取器用于高血压提醒，2026 年把 Apple Intelligence 放进健康 App 的核心。",
   "steps":["p-ahs2019","p-ahms2019","apple-iclr24","apple-accel","apple-relcon","wbm","apple-htn","apple-symbolic","apple-passport","ms-ecg-fm","apple-health-app"]},
  {"id":"google","name":"谷歌：四条纲唯一全部贯通的一家",
   "desc":"谷歌公开工作覆盖全部四条纲，而且彼此有明确接口：LSM 系列给出分钟级表征，SensorLM 接上语言，PH-LLM、PHIA、PHA 组成 Agent，SensorFM 被定位为 Agent 的“落地工具”，SensorWM 再用世界模型为教练提供反事实推演。",
   "steps":["lsm","ph-llm","phia","ir-wearme","lsm2","sensorlm","pha","fitbit-coach","fitbit-2026","sensorfm","sensorwm"]},
  {"id":"oppo","name":"OPPO：先单任务落地，再走向基础模型",
   "desc":"OPPO 的顺序与苹果相反：先用专门模型做手表高血压风险评估并大规模上线（参与者超过 65 万），随后与北大合作，用 ECG 引导的跨模态预训练学 PPG 表征，再用文本对齐做可复用的 PPG 表征。",
   "steps":["oppo-embc2024","oppo-heartage","hippt","oppo-bp2026"]}
 ],
 "essay": ["<b>一句话主线。</b>这四年里，核心问题换了四次：<em>没有标签，能不能学到一个人的通用生理表征？</em>→ <em>该在哪一层建模，怎样迁移到便宜的传感器？</em>→ <em>表征能不能被语言读懂、做成产品？</em>→ <em>能不能推演“如果我改变行为，身体会怎样”，并据此行动？</em>", "<b>起点：以人为锚。</b>2023 年 12 月，苹果在 Apple Heart and Movement Study 约 14 万人的手表 PPG/ECG 上做自监督预训练（ICLR 2024）。关键设计是把“同一个人”当作正样本：在缺少医学标签时，个体身份是最便宜也最稳定的监督。这一思路有清晰的前史（苹果 2021 年的被试感知对比学习、剑桥用心率监督加速度），也有清晰的后续（RelCon、Pulse-PPG 的相对对比，OPPO 心脏年龄的被试感知预训练）。2026 年苹果更发现，不同模态独立训练的健康模型会收敛到相近的表征。", "<b>扩张：层级与脚手架。</b>2024–2025 年出现两种扩张。其一是向上：谷歌 LSM 把对象从波形换成分钟级指标并验证尺度律，苹果 WBM 再上移到小时级行为，结论是两层互补；LSM-2 把缺失纳入建模，SensorFM 扩到 500 万人。其二是横向：训练期用信息更丰富的模态当老师，推理期只用便宜的模态（PPG 教加速度、ECG 教 PPG、临床报告教 ECG、文本教 PPG）。三星的 HiMAE 则把“哪一层”细化为“哪个时间分辨率”，并把模型做进手表 CPU。", "<b>落地：两条路通向同一个病。</b>苹果走“基础模型 → 产品”：2025 年获 FDA 许可的高血压提醒，第一步就是在 AHMS 无标签数据上自监督训练的 PPG 特征提取器。OPPO 走相反的路：先用专门模型在 65 万人规模上做高血压风险评估，2026 年才转向 ECG 引导的跨模态预训练与 PPG–文本对齐。两家最终都落在手表的高血压筛查上。", "<b>Agent 先行，接地在后。</b>Agent 纲出现得最早：2023 年的 WHOOP Coach 就把 GPT-4 套在指标上，Oura、Dexcom、Garmin、OpenAI 随后跟进。但很长时间里，这些 LLM 读的只是汇总分数。谷歌的研究线（PH-LLM → PHIA → PHA → Fitbit 教练）把它推进成多智能体分工；2026 年，SensorFM 被定位为 Agent 的数据接地工具，Agent 才真正接上生理基础模型。与此同时，WHOOP、Oura、谷歌都把 Agent 接到了病历、化验与真人医生。", "<b>终点暂停在世界模型。</b>“状态如何演化”这条线从苹果 2020 年的血糖动力学和 2022 年的运动心率响应开始，经过 GluFormer、Delphi-2M 的生成式轨迹，再到 HealthFormer 的干预模拟和 NormWear-2 的信号级动力学。2026 年 11 月，谷歌 SensorWM 以步数、睡眠、有氧为“动作”，预测 20 项生理指标未来 12 周的变化，再交给语言模型生成教练计划。四条纲第一次在同一个系统里闭合：表征 → 推演 → 目标 → 行动。", "<b>各家位置。</b>谷歌是唯一四条纲都有公开工作的公司。苹果在信号与参数层最深，Agent 选择嵌入系统（健康 App）而非独立教练。三星偏端侧与机理（HiMAE、xMAE、就寝建议）。OPPO 由产品回溯到基础模型。WHOOP 与 Oura 以 Agent 和服务为先，基础模型目前只有招聘与访谈信息。华为、小米等中国厂商的公开材料以产品与研究项目为主，可核实的基础模型论文较少（小米有 IJCAI 2026 的 DNA-PPG）。"]
}
import os
_ep='/workspace/physio-fm-history/data/entries.json'
if os.path.exists(_ep):
    _d={e['id']:e['date'] for e in json.load(open(_ep))['entries']}
    for t in meta['threads']: t['steps'].sort(key=lambda x:_d.get(x,''))
json.dump(meta, open('/workspace/physio-fm-history/data/meta.json','w'), ensure_ascii=False, indent=1)
print("meta ok")
