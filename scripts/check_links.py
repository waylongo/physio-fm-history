#!/usr/bin/env python3
"""检查 data/entries.json 中所有链接的 HTTP 状态（curl）。404 需要替换；403/超时通常是反爬，可保留。"""
import json, subprocess, sys, concurrent.futures as cf, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = json.load(open(os.path.join(root, 'data/entries.json')))['entries']
urls = {}
for e in E:
    urls.setdefault(e['url'], []).append(e['id'])
    for s in e.get('sources', []): urls.setdefault(s['url'], []).append(e['id'])
XP = os.path.join(root, 'data/sources-extra.json')
if os.path.exists(XP):
    for x in json.load(open(XP))['items']: urls.setdefault(x['url'], []).append('extra:' + x['title'][:30])
def st(u):
    r = subprocess.run(['curl','-s','-o','/dev/null','-L','--max-time','25','-A','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36','-w','%{http_code}',u], capture_output=True, text=True)
    return r.stdout.strip() or 'ERR'
bad = 0
with cf.ThreadPoolExecutor(8) as ex:
    for u, code in zip(urls, ex.map(st, urls)):
        flag = '' if code.startswith(('2','3')) else ('  <-- 需处理' if code == '404' else '  (非 2xx)')
        if code == '404': bad += 1
        print(code, u, ','.join(urls[u]), flag)
print(len(urls), 'urls;', bad, '个 404')
sys.exit(1 if bad else 0)
