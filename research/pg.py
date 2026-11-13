import sys,re,html,subprocess
u=sys.argv[1]
t=subprocess.run(['curl','-sL','--max-time','40','-A','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36',u],capture_output=True).stdout.decode('utf8','ignore')
t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S); t=re.sub(r'<(br|p|div|li|h\d|tr)[^>]*>','\n',t); t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
print(t)
