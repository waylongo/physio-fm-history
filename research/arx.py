import sys,urllib.request,xml.etree.ElementTree as ET,json,time
ids=sys.argv[1:]
url='https://export.arxiv.org/api/query?max_results=100&id_list='+','.join(ids)
x=urllib.request.urlopen(url,timeout=60).read()
ns={'a':'http://www.w3.org/2005/Atom','arxiv':'http://arxiv.org/schemas/atom'}
r=ET.fromstring(x)
for e in r.findall('a:entry',ns):
    t=' '.join(e.find('a:title',ns).text.split())
    au=[a.find('a:name',ns).text for a in e.findall('a:author',ns)]
    pub=e.find('a:published',ns).text[:10]; upd=e.find('a:updated',ns).text[:10]
    jr=e.find('arxiv:journal_ref',ns); cm=e.find('arxiv:comment',ns)
    print(json.dumps({'id':e.find('a:id',ns).text,'title':t,'authors':au[:6]+(['...%d'%len(au)] if len(au)>6 else []),'published':pub,'updated':upd,'journal':jr.text if jr is not None else None,'comment':cm.text if cm is not None else None,'abs':' '.join(e.find('a:summary',ns).text.split())[:1500]},ensure_ascii=False))
