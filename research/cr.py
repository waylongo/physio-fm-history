import sys,json,urllib.request
for d in sys.argv[1:]:
    try:
        j=json.load(urllib.request.urlopen('https://api.crossref.org/works/'+d,timeout=40))['message']
        au=[(a.get('given','')+' '+a.get('family','')).strip() for a in j.get('author',[])]
        def dp(k): 
            v=j.get(k,{}).get('date-parts',[[None]])[0]; return '-'.join(str(x) for x in v if x)
        print(json.dumps({'doi':d,'title':j.get('title',[''])[0],'container':j.get('container-title',[''])[:1],'authors':au[:5]+(['…%d'%len(au)] if len(au)>5 else []),'online':dp('published-online'),'print':dp('published-print'),'issued':dp('issued')},ensure_ascii=False))
    except Exception as e: print(d,'ERR',e)
