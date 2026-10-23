#!/usr/bin/env python3
"""Generate GitHub-profile terminal SVGs from public GitHub REST data.
Uses only Python standard library. Never embeds credentials in output.
"""
import json, os, re, urllib.request, urllib.parse, html, datetime, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'/'generated'; OUT.mkdir(parents=True,exist_ok=True)
USER=os.getenv('PROFILE_USERNAME','SanjanaGadamsetty')
TOKEN=os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN','')
API='https://api.github.com'

def request(path, default):
    headers={'Accept':'application/vnd.github+json','User-Agent':'neon-terminal-profile','X-GitHub-Api-Version':'2022-11-28'}
    if TOKEN: headers['Authorization']='Bearer '+TOKEN
    try:
        with urllib.request.urlopen(urllib.request.Request(API+path,headers=headers),timeout=20) as r:
            return json.load(r)
    except Exception as e:
        print('Warning:',path,repr(e)); return default

def esc(s): return html.escape(str(s),quote=True)
def fmt(n): return f'{n:,}' if isinstance(n,int) else '—'

def svg(name,w,h,body):
    base=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(name)}"><defs><linearGradient id="border" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#27d9ff"/><stop offset="1" stop-color="#e05aff"/></linearGradient><linearGradient id="fill" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0c1830"/><stop offset="1" stop-color="#080b19"/></linearGradient></defs><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="13" fill="url(#fill)" stroke="url(#border)" stroke-width="1.5"/><rect x="1" y="1" width="{w-2}" height="32" rx="13" fill="#0d1427"/><path d="M1 32 H{w-1}" stroke="#28344e"/><circle cx="19" cy="17" r="5" fill="#ff5e70"/><circle cx="35" cy="17" r="5" fill="#ffc65e"/><circle cx="51" cy="17" r="5" fill="#36d98d"/><text x="67" y="22" font-family="monospace" font-size="13" fill="#66e4ff">{esc(name)}</text>{body}</svg>'''
    (OUT/(name.split('/')[-1].replace(':','_').replace(' ','_')+'.svg')).write_text(base,encoding='utf-8')

def txt(x,y,t,color='#d7e4ff',size=14,weight='normal'):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" font-family="monospace">{esc(t)}</text>'

profile=request('/users/'+urllib.parse.quote(USER),{})
repos=request('/users/'+urllib.parse.quote(USER)+'/repos?per_page=100&type=owner&sort=updated',[])
if not isinstance(repos,list): repos=[]
repos=[r for r in repos if isinstance(r,dict) and not r.get('fork')]
# REST endpoint provides public stats only; starred and followers counts are reliable public metrics.
stars=sum(int(r.get('stargazers_count') or 0) for r in repos)
repo_count=profile.get('public_repos','—')
followers=profile.get('followers','—')
# public events API: latest ~90 days, limited to most recent 300; not all-time contributions.
events=[]
for page in range(1,4):
    batch=request(f'/users/{urllib.parse.quote(USER)}/events/public?per_page=100&page={page}',[])
    if not isinstance(batch,list) or not batch: break
    events.extend(batch)

body=txt(22,64,'$ gh api users/'+USER,'#b8a7ff',13)
metrics=[('PUBLIC REPOS',fmt(repo_count)),('STARS ON OWN REPOS',fmt(stars)),('FOLLOWERS',fmt(followers)),('RECENT PUBLIC EVENTS',fmt(len(events)))]
for i,(label,value) in enumerate(metrics):
    y=102+i*45
    body+=txt(25,y,label,'#8a9cbb',13)+txt(330,y,value,'#65e8ff',19,'bold')
body+=txt(22,303,'Updated '+datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC'),'#9f82ce',12)
svg('stats',490,325,body)

# 12-week heatmap of *public events* (not GitHub contributions). Explicit labeling prevents misrepresentation.
now=datetime.datetime.now(datetime.timezone.utc).date(); start=now-datetime.timedelta(days=83)
counts={}
for e in events:
    d=(e.get('created_at') or '')[:10]
    if d: counts[d]=counts.get(d,0)+1
body=txt(20,62,'$ cat public_activity.log','#ba91ff',13)
body+=txt(20,86,'Public events · last 12 weeks · capped by GitHub API','#8da0c2',11)
for i in range(84):
    day=start+datetime.timedelta(days=i); key=day.isoformat(); c=counts.get(key,0)
    color=('#1c2848' if c==0 else '#2d3f8b' if c==1 else '#6850b8' if c<4 else '#b449de' if c<8 else '#f36ce5')
    col=i//7; row=i%7
    body+=f'<rect x="{20+col*35}" y="{108+row*22}" width="25" height="15" rx="3" fill="{color}"><title>{key}: {c} public events</title></rect>'
body+=txt(20,286,'0    1    2-3    4-7    8+ events/day','#8da0c2',12)
svg('activity',490,309,body)

languages={}
for r in repos:
    lang=r.get('language')
    if lang: languages[lang]=languages.get(lang,0)+1
sorted_lang=sorted(languages.items(),key=lambda x:-x[1])[:7]
body=txt(22,64,'$ ls ~/tech-stack --sort=usage','#b8a7ff',13)
if not sorted_lang: body+=txt(22,100,'Public repository languages unavailable','#9ba9c6',14)
for i,(lang,num) in enumerate(sorted_lang):
    y=102+i*34
    body+=txt(24,y,lang,'#d8e6ff',14)+f'<rect x="190" y="{y-13}" width="220" height="13" rx="6" fill="#1c2744"/>'
    body+=f'<rect x="190" y="{y-13}" width="{max(6,round(220*num/max(1,sorted_lang[0][1])))}" height="13" rx="6" fill="{["#31c9ff","#bd63f5","#ed67b7","#7c9cff"][i%4]}"/>'
    body+=txt(425,y,str(num),'#9caed0',12)
body+=txt(22,365,'Based on primary language of public, non-fork repos','#8da0c2',11)
svg('languages',490,385,body)

# Recently updated non-fork public repos, not falsely labelled as deployment status.
body=txt(22,62,'$ ls ~/projects --sort=updated','#b8a7ff',13)
for i,r in enumerate(repos[:5]):
    y=99+i*45; name=r.get('name','repository')[:35]; desc=(r.get('description') or 'Public GitHub repository').replace('\n',' ')[:55]
    body+=txt(24,y,'> '+name,'#62e5ff',14,'bold')+txt(35,y+18,desc,'#aab9d2',11)
if not repos: body+=txt(24,103,'No public repositories returned','#aab9d2',13)
body+=txt(22,342,'Open repositories: github.com/'+USER,'#c77cf3',12)
svg('projects',700,365,body)

# recent public pull requests from GitHub Search, excludes non-public contributions
search=request('/search/issues?q='+urllib.parse.quote('author:'+USER+' type:pr')+'&sort=updated&order=desc&per_page=5',{})
prs=search.get('items',[]) if isinstance(search,dict) else []
body=txt(22,62,'$ gh search prs --author '+USER,'#b8a7ff',13)
for i,pr in enumerate(prs[:5]):
    y=98+i*43
    repo=(pr.get('repository_url') or '').split('/repos/')[-1]
    state='MERGED' if pr.get('pull_request',{}).get('merged_at') else pr.get('state','open').upper()
    body+=txt(22,y,repo[:46],'#60dfff',13)+txt(22,y+17,(pr.get('title') or '')[:63],'#d2dbf4',12)+txt(580,y+17,state,'#c27bff',11)
if not prs: body+=txt(22,106,'No public PR results available','#aab9d2',13)
body+=txt(22,345,'Public PR search · refreshes automatically','#8da0c2',12)
svg('opensource',700,365,body)
print('Generated SVGs for',USER)
