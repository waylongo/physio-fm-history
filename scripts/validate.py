#!/usr/bin/env python3
"""校验 data/meta.json 与 data/entries.json 的结构与引用完整性。"""
import json, os, re, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(os.path.join(root,'data/meta.json')))
E = json.load(open(os.path.join(root,'data/entries.json')))['entries']
err = []
ids = {}
REQ = ['id','date','dateLabel','track','org','type','era','title','short','url','q','how','shift','links']
for i,e in enumerate(E):
    for k in REQ:
        if k not in e or e[k] in ('',None): err.append(f"{e.get('id',i)} 缺少字段 {k}")
    if e['id'] in ids: err.append(f"重复 id {e['id']}")
    ids[e['id']] = e
    if not re.fullmatch(r'\d{4}-\d{2}(-\d{2})?', e['date']): err.append(f"{e['id']} 日期格式错误 {e['date']}")
    if e['track'] not in {t['id'] for t in M['tracks']}: err.append(f"{e['id']} 未知 track {e['track']}")
    if e['org'] not in M['orgs']: err.append(f"{e['id']} 未知 org {e['org']}")
    if e['type'] not in {t['id'] for t in M['types']}: err.append(f"{e['id']} 未知 type {e['type']}")
    if e['era'] not in {x['id'] for x in M['eras']}: err.append(f"{e['id']} 未知 era")
    for u in [e['url']] + [s['url'] for s in e.get('sources',[])]:
        if not u.startswith('https://'): err.append(f"{e['id']} 非 https 链接 {u}")
for e in E:
    for l in e['links']:
        if l['from'] not in ids: err.append(f"{e['id']} 引用不存在的 {l['from']}")
        elif ids[l['from']]['date'] > e['date']: err.append(f"{e['id']} 的来源 {l['from']} 晚于自身")
        if l['type'] not in M['relations']: err.append(f"{e['id']} 未知关系 {l['type']}")
era_ids = {x['id'] for x in M['eras']}
warn = []
from datetime import date
def d(x):
    p = [int(v) for v in x.split('-')] + [15]
    return date(p[0], p[1], p[2] if len(p) > 3 else 15)
for e in E:
    for l in e['links']:
        if l['type'] == '并行' and l['from'] in ids:
            gap = (d(e['date']) - d(ids[l['from']]['date'])).days
            if gap > 430: warn.append(f"{e['id']} ← {l['from']} 标为并行但相隔 {gap} 天")
def need(ref, where):
    if ref not in ids: err.append(f"{where} 引用不存在的条目 {ref}")
for t in M['threads']:
    for k in ('name','problem','approach','changed','unlocked','open'):
        if not t.get(k): err.append(f"脉络 {t['id']} 缺少 {k}")
    for s in t['steps']:
        if not s.get('role'): err.append(f"脉络 {t['id']} 的步骤 {s.get('id')} 缺少 role")
        need(s['id'], f"脉络 {t['id']}")
    ds = [ids[s['id']]['date'] for s in t['steps'] if s['id'] in ids]
    if ds != sorted(ds): err.append(f"脉络 {t['id']} 未按时间排序")
for c in M.get('companies', []):
    if c['org'] not in {g['id'] for g in M['orgGroups']} and c['org'] not in M['orgs']: err.append(f"公司卡 {c['org']} 未知")
    for k in ('data','model','product'):
        for r in c[k]['ids']: need(r, f"公司卡 {c['org']}.{k}")
for q in M.get('questions', []):
    if [c['era'] for c in q['cells']] != [x['id'] for x in M['eras']]: err.append(f"问题 {q['id']} 的时期列不完整")
    for c in q['cells']:
        for r in c['ids']:
            need(r, f"问题 {q['id']}")
            if r in ids and ids[r]['era'] != c['era']: err.append(f"问题 {q['id']} 的 {c['era']} 格引用了 {ids[r]['era']} 的 {r}")
for o, v in M['orgs'].items():
    if v['group'] not in {g['id'] for g in M['orgGroups']}: err.append(f"机构 {o} 的分组 {v['group']} 未定义")
# era 与日期一致
bounds = [('e0','0000','2023-12'),('e1','2023-12','2024-06'),('e2','2024-06','2025-07'),('e3','2025-07','2026-01'),('e4','2026-01','9999')]
for e in E:
    for k, lo, hi in bounds:
        if lo <= e['date'] < hi and e['era'] != k: err.append(f"{e['id']} 日期 {e['date']} 应属 {k}")
XP = os.path.join(root, 'data/sources-extra.json')
if os.path.exists(XP):
    X = json.load(open(XP)); gids = {g['id'] for g in X['groups']}
    main_urls = {e['url'] for e in E} | {s['url'] for e in E for s in e.get('sources', [])}
    seen = set()
    for x in X['items']:
        for k in ('title', 'org', 'date', 'url', 'group', 'reason'):
            if not x.get(k): err.append(f"补充来源 {x.get('title','?')} 缺少 {k}")
        if x.get('group') not in gids: err.append(f"补充来源 {x.get('title')} 分组未知")
        if not str(x.get('url','')).startswith('https://'): err.append(f"补充来源 {x.get('title')} 非 https")
        if x.get('date') != '—' and not re.fullmatch(r'\d{4}(-\d{2}(-\d{2})?)?', str(x.get('date',''))): err.append(f"补充来源 {x.get('title')} 日期格式错误")
        if x.get('url') in main_urls: warn.append(f"补充来源与年谱条目重复：{x['url']}")
        if x.get('url') in seen: err.append(f"补充来源重复：{x['url']}")
        seen.add(x.get('url'))
        if x.get('track') and x['track'] not in {t['id'] for t in M['tracks']}: err.append(f"补充来源 {x['title']} track 未知")
    print('补充来源', len(X['items']))
starts = [e['id'] for e in E if e.get('start')]
if len(starts) != 1: err.append(f"起点条目应恰好 1 个：{starts}")
# 私有关键词检查：词表放在仓库之外（默认 ../physio-fm-private-terms.txt，或环境变量 PRIVATE_TERMS），不随仓库发布
terms_path = os.environ.get('PRIVATE_TERMS', os.path.join(os.path.dirname(root), 'physio-fm-private-terms.txt'))
if os.path.exists(terms_path):
    terms = [t.strip() for t in open(terms_path) if t.strip()]
    for dp, _, fs in os.walk(root):
        if '/.git' in dp: continue
        for f in fs:
            fp = os.path.join(dp, f)
            try: txt = open(fp, encoding='utf-8').read().lower()
            except Exception: continue
            for t in terms:
                if t.lower() in txt: err.append(f"{os.path.relpath(fp, root)} 中出现私有关键词")
from collections import Counter
print('条目', len(E), '| 按纲', dict(Counter(e['track'] for e in E)), '| 按类型', dict(Counter(e['type'] for e in E)))
print('按机构', dict(Counter(e['org'] for e in E)))
for w in warn: print('! '+w)
if err:
    print('\n'.join('✗ '+x for x in err)); sys.exit(1)
print('✓ 校验通过')
