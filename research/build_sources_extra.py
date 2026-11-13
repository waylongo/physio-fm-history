#!/usr/bin/env python3
"""生成 data/sources-extra.json：检索到、已核对存在、但没有上年谱的条目，各附原因。
输入：/workspace/physio-fm-sources-companies.json、/workspace/physio-fm-sources-academic.json（推荐 + 观察名单）、
/workspace/physio-fm-gap-candidates.json（第 17–19 名）。凡 URL 已在年谱条目或其来源中出现的不再列出。
不读取、不复制任何未过滤的检索原始目录。输出前按隐私词表过滤。"""
import json, os, re
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = json.load(open(os.path.join(root, 'data/entries.json')))['entries']
def norm(u):
    u = u.split('#')[0].replace('http://', 'https://').replace('www.', '').rstrip('/')
    if 'arxiv.org/abs/' in u: u = re.sub(r'v\d+$', '', u)
    return u.lower()
ON = {norm(e['url']) for e in E} | {norm(s['url']) for e in E for s in e.get('sources', [])}
TP = os.environ.get('PRIVATE_TERMS', os.path.join(os.path.dirname(root), 'physio-fm-private-terms.txt'))
BAN = [l.strip() for l in open(TP) if l.strip()] if os.path.exists(TP) else []
ORG = {'apple': '苹果', 'google': '谷歌', 'samsung': '三星', 'oura': 'Oura', 'whoop': 'WHOOP', 'meta': 'Meta', 'microsoft': '微软', 'amazon': '亚马逊',
       'openai': 'OpenAI', 'anthropic': 'Anthropic', 'withings': 'Withings', 'garmin': 'Garmin', 'polar': 'Polar', 'dexcom': 'Dexcom', 'abbott': '雅培',
       'irhythm': 'iRhythm', 'alivecor': 'AliveCor', 'eko': 'Eko', 'huawei': '华为', 'oppo': 'OPPO', 'vivo': 'vivo', 'honor': '荣耀', 'verily': 'Verily'}
def creason(x):
    r = (x.get('reason') or '').lower(); rec = x.get('rec')
    rules = [
        (r'biometric', 'weak', '身份识别类工作，不属于健康建模'),
        (r'non-wearable|contactless|nest hub|radar|camera', 'weak', '非可穿戴传感（床头设备、雷达、手机摄像头等）'),
        (r'rumor|secondary|media|linkedin|hiring|talk only', 'media', '仅有媒体报道、招聘或演讲信息，缺少一手技术材料'),
        (r'clinical agent line|amie', 'dup', '临床诊断对话 Agent 支线，与可穿戴主线关系较远'),
        (r'regulator', 'context', '监管背景资料'),
        (r'incremental|hardware|precedes|explainer|supporting|supports existing|optional|context', 'context', '增量功能、硬件发布或已收条目的补充材料'),
        (r'task|not fm|auscultation|observational|study result|methodolog|mental-health|behavio', 'weak', '单一任务模型、观察性研究或方法学工作，不是基础模型主线'),
    ]
    for pat, g, z in rules:
        if re.search(pat, r): return g, z
    if rec in ('add', 'add-as-link'):
        return 'dup', '已核对存在；与已收条目思路相近，本版为控制密度未单列'
    return 'weak', '与主线关系较弱'
items = []
def push(**k):
    t = json.dumps(k, ensure_ascii=False)
    if any(b.lower() in t.lower() for b in BAN): return
    if norm(k['url']) in ON or norm(k['url']) in {norm(i['url']) for i in items}: return
    items.append(k)
def dfmt(d):
    d = (d or '').strip()
    m = re.fullmatch(r'(\d{4})-(\d{1,2})(?:-(\d{1,2}))?', d)
    if m: d = m.group(1) + '-' + m.group(2).zfill(2) + ('-' + m.group(3).zfill(2) if m.group(3) else '')
    return d if re.fullmatch(r'\d{4}(-\d{2}(-\d{2})?)?', d) else ''
rp = os.path.join(root, 'research/v5_removed.json')  # 第五版从年谱移出的条目，排在最前
if os.path.exists(rp):
    for x in json.load(open(rp)):
        push(title=x['title'], org=x['org'], date=x['date'], url=x['url'], group='removed', track=x.get('track'),
             reason='【' + x['cat'] + '】' + x['why'] + '。原摘要：' + x['short'], src='removed')
        for s_ in x.get('sources', []):
            push(title=s_['label'], org=x['org'], date=x['date'], url=s_['url'], group='removed', track=x.get('track'),
                 reason='【' + x['cat'] + '】“' + x['title'] + '”的配套来源', src='removed')
cp = '/workspace/physio-fm-sources-companies.json'
if os.path.exists(cp):
    d = json.load(open(cp)); ci = d['items'] if isinstance(d, dict) else d
    for x in ci:
        if not x['url'].startswith('https://'): continue
        g, z = creason(x)
        push(title=x['title'], org=ORG.get(x['company'], x['company']), date=dfmt(x.get('date')) or '—', url=x['url'], group=g,
             reason=z + '。检索备注：' + (x.get('reason') or ''), src='company')
ap = '/workspace/physio-fm-sources-academic.json'
TR = {'signal': 'signal', 'param': 'param', 'world': 'world', 'agent': 'agent'}
if os.path.exists(ap):
    a = json.load(open(ap))
    for k in ('recommended', 'watchlist'):
        for x in a[k]:
            rs = x.get('reason') or ''
            g = 'context' if re.search('综述|立场', rs) else 'weak' if re.search('非生理|非可穿戴', rs) else 'watch' if k == 'watchlist' else 'dup'
            z = rs if k == 'watchlist' else '检索推荐；本版核对后未单列（与已收条目重复或作者单位未核实）。' + rs
            push(title=x['title'], org=(x.get('org') or '学术'), date=dfmt(x.get('date')) or '—', url=x['url'], group=g, reason=z,
                 track=TR.get(x.get('track')), src='academic')
vp = '/workspace/physio-fm-sources-venues.json'
if os.path.exists(vp):
    for x in json.load(open(vp))['recommended']:
        if not x['url'].startswith('https://'): continue
        rs = x.get('reason') or ''
        why = ('OpenReview 页面对脚本需人机验证，未能亲自核对摘要，暂列观察名单。' if 'openreview.net' in x['url'] else '会议/期刊补扫推荐；本版未单列（严格说不是基础模型，或与已收条目重复）。')
        push(title=x['title'], org='、'.join((x.get('orgs') or [])[:2]) or '学术', date=dfmt(x.get('date')) or '—', url=x['url'],
             group='watch', reason=why + rs, track=TR.get(x.get('track')), src='venue')
gp = '/workspace/physio-fm-gap-candidates.json'
if os.path.exists(gp):
    for x in json.load(open(gp)):
        if x['rank'] in (17, 18, 19):
            push(title=x['title'], org=x.get('orgNote') or x['org'], date=x['date'], url=x['url'], group='media' if x['rank'] == 17 else 'watch',
                 reason='补漏检索低置信候选：' + (x.get('confidence') or ''), track=x.get('track'), src='gap')
for i in items:
    if not i.get('track'): i.pop('track', None)
    i.pop('src', None)
GO = ['removed', 'dup', 'watch', 'weak', 'media', 'context']
items.sort(key=lambda i: (GO.index(i['group']), i['date']))
out = {"updated": "2026-11-13",
       "note": "检索到、已核对链接存在、但没有放上年谱的条目（含第五版做减法时移出的条目）。每条注明原因；“检索备注”为检索时的原始英文备注。",
       "groups": [
           {"id": "removed", "label": "第五版从年谱移出（样本量小 / 支撑不足 / 重复 / 偏离主线）"},
           {"id": "dup", "label": "与已收条目思路重复（控制密度）"},
           {"id": "watch", "label": "相关工作，未单列（观察名单）"},
           {"id": "weak", "label": "与主线关系较弱：单一任务、非可穿戴或 workshop 短文"},
           {"id": "media", "label": "仅有媒体报道或信息不足"},
           {"id": "context", "label": "背景、监管与配套资料"}],
       "items": items}
json.dump(out, open(os.path.join(root, 'data/sources-extra.json'), 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print('sources-extra', len(items), Counter(i['group'] for i in items))
