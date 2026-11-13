#!/usr/bin/env python3
"""把 research/RESEARCH.head.md 与条目索引拼成 RESEARCH.md。"""
import json, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(f'{root}/data/meta.json')); E = json.load(open(f'{root}/data/entries.json'))['entries']
tn = {t['id']: t['name'] for t in M['tracks']}; ty = {t['id']: t['label'] for t in M['types']}
by = {e['id']: e for e in E}
out = [open(f'{root}/research/RESEARCH.head.md').read()]
for era in M['eras']:
    es = sorted([e for e in E if e['era'] == era['id']], key=lambda e: e['date'])
    out.append(f"\n### {era['no']} · {era['title']}\n")
    for e in es:
        org = M['orgs'][e['org']]['label'] + (f"（{e['orgNote']}）" if e.get('orgNote') else '')
        out.append(f"- **{e['short']}** `{e['id']}`{' **【起点】**' if e.get('start') else ''} — {tn[e['track']]} · {ty[e['type']]} · {org} · {e['dateLabel']}  ")
        out.append(f"  原题：{e['title']}  ")
        out.append(f"  主链接：<{e['url']}>" + ''.join(f"；{s['label']}：<{s['url']}>" for s in e.get('sources', [])) + "  ")
        if e['links']:
            out.append("  关系：" + '；'.join(f"{l['type']}「{by[l['from']]['short']}」— {l['note']}" for l in e['links']) + "  ")
        out.append(f"  改变：{e['shift']}")
X = json.load(open(f'{root}/data/sources-extra.json'))
if X['items']:
    out.append(f"\n## 6. 相关但未上年谱的工作（{len(X['items'])} 项）\n\n来自公司与学术两轮检索；链接均经 scripts/check_links.py 检查可访问。按不上年谱的原因分组。页面底部“全部来源”中同样列出。\n")
    for g in X['groups']:
        its = sorted([x for x in X['items'] if x['group'] == g['id']], key=lambda x: x['date'])
        if not its: continue
        out.append(f"\n### {g['label']}（{len(its)}）\n")
        for x in its:
            out.append(f"- **{x['title']}** — {x['org']} · {x.get('dateLabel') or x['date']} · <{x['url']}>  ")
            out.append(f"  原因：{x['reason']}")
open(f'{root}/RESEARCH.md', 'w').write('\n'.join(out) + '\n')
print('RESEARCH.md written')
