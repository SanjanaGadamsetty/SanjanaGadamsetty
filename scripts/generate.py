#!/usr/bin/env python3
"""Neon visual infographic cards from public GitHub API (standard library)."""
from pathlib import Path
import os,json,html,urllib.request,urllib.parse,datetime,math
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/generated';OUT.mkdir(parents=True,exist_ok=True)
USER=os.getenv('PROFILE_USERNAME','SanjanaGadamsetty')
TOKEN=os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN','')
def api(path,default):
 try:
  headers={'User-Agent':'neon-visual-readme','Accept':'application/vnd.github+json'}
  if TOKEN:headers['Authorization']='Bearer '+TOKEN
  with urllib.request.urlopen(urllib.request.Request('https://api.github.com'+path,headers=headers),timeout=12) as r:return json.load(r)
 except Exception as e:print('API unavailable:',str(e)[:100]);return default
def esc(s):return html.escape(str(s),quote=True)
def tx(x,y,s,size=18,color='#EAF2FF',weight='normal',anchor=None):
 a=f' text-anchor="{anchor}"' if anchor else ''
 return f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}"{a}>{esc(s)}</text>'
def rect(x,y,w,h,fill='#142044',r=10,stroke=None):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+'/>'
def shell(title,tag,body,w=700,h=360):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}"><defs><linearGradient id="edge"><stop stop-color="#FF4BD8"/><stop offset=".5" stop-color="#8E69FF"/><stop offset="1" stop-color="#36DFFF"/></linearGradient><linearGradient id="back" x2="1" y2="1"><stop stop-color="#0A0D24"/><stop offset="1" stop-color="#140C2A"/></linearGradient></defs>{rect(1,1,w-2,h-2,'url(#back)',18,'#543A89')}<path d="M24 72H{w-24}" stroke="#2A3158"/>{tx(25,35,tag,12,'#66DFFF','bold')}{tx(25,59,title,23,'#FFFFFF','bold')}{body}<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="none" stroke="url(#edge)" stroke-width="1.5"/></svg>'''
def save(name,content): (OUT/(name+'.svg')).write_text(content,encoding='utf-8')
def unavailable(msg):return tx(350,188,msg,16,'#8E9CC5',anchor='middle')+tx(350,218,'Waiting for live public GitHub data',13,'#667AA6',anchor='middle')
user=api('/users/'+urllib.parse.quote(USER),{})
repos=api('/users/'+urllib.parse.quote(USER)+'/repos?per_page=100&type=owner&sort=updated',[])
if not isinstance(repos,list):repos=[]
repos=[r for r in repos if isinstance(r,dict) and not r.get('fork')]
events=[]
for page in range(1,4):
 batch=api(f'/users/{urllib.parse.quote(USER)}/events/public?per_page=100&page={page}',[])
 if not isinstance(batch,list) or not batch:break
 events.extend(batch)
# Neon metric cards: real values only, no invented stats.
metrics=[('PUBLIC REPOS',user.get('public_repos'),'#44DFFF'),('FOLLOWERS',user.get('followers'),'#F15DE4'),('STARS ON OWN REPOS',sum(int(r.get('stargazers_count') or 0) for r in repos) if repos else None,'#AB7BFF'),('RECENT PUBLIC EVENTS',len(events) if user else None,'#5C8DFF')]
b=''
for i,(name,num,color) in enumerate(metrics):
 x=26+(i%2)*330;y=95+(i//2)*112
 b+=rect(x,y,314,96,'#121B39',13,'#35416C')+rect(x,y,5,96,color,2)+tx(x+18,y+27,name,12,'#9DAFD1','bold')+tx(x+18,y+70,str(num) if num is not None else '—',34,color,'bold')
save('stats',shell('Developer Metrics','GITHUB / PUBLIC PROFILE',b,700,340))
# Heatmap (events, not official contributions)
counts={}
for e in events:
 key=(e.get('created_at') or '')[:10]
 if key:counts[key]=counts.get(key,0)+1
now=datetime.datetime.now(datetime.timezone.utc).date();start=now-datetime.timedelta(days=83)
b=tx(28,98,'12 weeks of public events (not contributions)',13,'#9FAFD5')
for i in range(84):
 d=start+datetime.timedelta(days=i);n=counts.get(d.isoformat(),0)
 color=('#1D2850' if n==0 else '#304DA2' if n==1 else '#7860E4' if n<4 else '#CE58DD' if n<8 else '#46D9F7')
 b+=rect(35+(i//7)*52,116+(i%7)*28,36,20,color,5)
b+=tx(35,342,'0',11,'#9DAED2')
for i,c in enumerate(['#1D2850','#304DA2','#7860E4','#CE58DD','#46D9F7']):b+=rect(65+i*50,330,32,13,c,3)
b+=tx(340,342,'8+ public events/day',11,'#9DAED2')
save('activity',shell('Coding Activity','ACTIVITY / VISUAL HEATMAP',b,700,370))
# Language horizontal bars
lang={}
for r in repos:
 if r.get('language'):lang[r['language']]=lang.get(r['language'],0)+1
ordered=sorted(lang.items(),key=lambda x:-x[1])[:6];b=''
if not ordered:b=unavailable('Repository languages unavailable')
for i,(name,count) in enumerate(ordered):
 y=106+i*41; color=['#FF58D9','#40DFFF','#9D70FF','#638BFF','#FF82B7','#5EE3E6'][i]
 b+=tx(29,y,name,15,'#DDE8FF','bold')+rect(190,y-16,440,17,'#1B2750',8)+rect(190,y-16,max(12,round(440*count/ordered[0][1])),17,color,8)
b+=tx(30,345,'Primary languages of public, non-fork repositories',12,'#8296C0')
save('languages',shell('Language Spectrum','TECH / REPOSITORY LANGUAGES',b,700,365))
# Projects as tiled cards
b=''
for i,r in enumerate(repos[:4]):
 x=25+(i%2)*335;y=90+(i//2)*115
 b+=rect(x,y,315,102,'#121D3C',13,'#3B437A')+tx(x+15,y+29,(r.get('name') or '')[:26],18,['#4BE3FF','#FA62D9','#A879FF','#73B3FF'][i],'bold')+tx(x+15,y+53,'★ '+str(r.get('stargazers_count') or 0)+'   •   '+(r.get('language') or 'Repository'),12,'#AFBCE1')
 desc=(r.get('description') or 'Explore this public repository').replace('\n',' ')[:39]
 b+=tx(x+15,y+78,desc,12,'#A2B2D2')
if not repos:b=unavailable('Repositories unavailable')
save('projects',shell('Project Orbit','BUILD / RECENT REPOSITORIES',b,700,350))
# PRs visual status lanes
search=api('/search/issues?q='+urllib.parse.quote('author:'+USER+' type:pr')+'&sort=updated&order=desc&per_page=4',{})
prs=search.get('items',[]) if isinstance(search,dict) else [];b=''
for i,p in enumerate(prs[:4]):
 y=90+i*60;state='MERGED' if p.get('pull_request',{}).get('merged_at') else ('OPEN' if p.get('state')=='open' else 'CLOSED')
 color='#49DCCB' if state=='MERGED' else '#51BFFF' if state=='OPEN' else '#F36DC5'
 b+=rect(25,y,650,50,'#141D3D',10,'#384477')+rect(36,y+12,82,25,color,7)+tx(77,y+30,state,12,'#080D20','bold','middle')+tx(134,y+30,(p.get('title') or 'Pull request')[:58],14,'#E3ECFF')
if not prs:b=unavailable('No public pull requests returned')
save('opensource',shell('Open-Source Pulse','COLLABORATE / PULL REQUESTS',b,700,355))
