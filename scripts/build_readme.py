#!/usr/bin/env python3
"""Render a high-contrast visual README from 40 true/false flags."""
from pathlib import Path
import json,html,math,random
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/modules';OUT.mkdir(parents=True,exist_ok=True)
def load(name):return json.loads((ROOT/'config'/name).read_text())
G=load('groups.json');F=load('features.json')['features'];P=load('profile.json')
ALL=[key for values in G.values() for key in values]
if len(ALL)!=40 or set(ALL)!=set(F) or not all(type(x) is bool for x in F.values()):raise ValueError('40 boolean flags required')
def t(x,y,text,size=17,color='#ECF2FF',weight='normal',anchor='start'):
 return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{html.escape(str(text))}</text>'
def rect(x,y,w,h,color,r=8,stroke=None):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{color}"'+(f' stroke="{stroke}"' if stroke else '')+'/>'
def line(x1,y1,x2,y2,c,w=2):return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{c}" stroke-width="{w}" fill="none"/>'
def circle(x,y,r,c,stroke=None):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"'+(f' stroke="{stroke}"' if stroke else '')+'/>'
def card(key,title,group):
 random.seed(key);w=700;h=290
 colors=['#FF58D9','#4CDBFF','#9A6BFF','#5F91FF','#FF7EC4']; accent=colors[ALL.index(key)%5]
 body=''
 # Different visual metaphors across the cards: orbital, bars, constellation, roadmap, code tiles, rings, heatmap
 mode=ALL.index(key)%7
 if mode==0:
  for i in range(4):body+=f'<circle cx="350" cy="172" r="{27+i*30}" fill="none" stroke="{colors[i]}" stroke-width="{5 if i==1 else 2}" opacity=".85"/>'
  for i in range(5):
   angle=i*math.tau/5;body+=circle(round(350+115*math.cos(angle)),round(172+115*math.sin(angle)),9,colors[i])
  body+=t(350,180,'✦',30,'#FFFFFF','bold','middle')
 elif mode==1:
  for i in range(6):
   x=66+i*98; ht=[73,116,55,147,103,126][i]
   body+=rect(x,245-ht,55,ht,colors[i%5],7)+t(x+27,263,str(i+1).zfill(2),12,'#A7B7DD',anchor='middle')
 elif mode==2:
  pts=[(90,205),(170,125),(260,172),(360,102),(445,198),(540,120),(616,173)]
  for a,b in zip(pts,pts[1:]):body+=line(*a,*b,'#6C71C9',3)
  for i,(x,y) in enumerate(pts):body+=circle(x,y,9,colors[i%5])+circle(x,y,17,'none',colors[i%5])
 elif mode==3:
  for i in range(4):
   x=43+i*165;body+=rect(x,112,150,112,'#152344',12,'#465386')+t(x+75,148,['IDEA','DESIGN','BUILD','SHIP'][i],16,colors[i],'bold','middle')+t(x+75,189,['01','02','03','04'][i],31,'#FFFFFF','bold','middle')
 elif mode==4:
  for i in range(5):
   y=99+i*32;body+=t(45,y,['01','02','03','04','05'][i],13,'#A5B7DC')+rect(96,y-13,545,17,'#1A2750',8)+rect(96,y-13,[470,335,418,245,385][i],17,colors[i],8)
 elif mode==5:
  for i in range(9):
   x=70+(i%3)*210;y=97+(i//3)*55;body+=rect(x,y,175,43,'#142141',10,'#364578')+circle(x+22,y+21,8,colors[i%5])+t(x+43,y+28,['DATA','CODE','DESIGN','AI','CLOUD','BUILD','IDEAS','GROWTH','IMPACT'][i],14,'#DCE9FF','bold')
 else:
  for row in range(6):
   for col in range(20):body+=rect(42+col*31,96+row*28,23,18,['#1B2850','#324C9D','#725BD4','#C653D8','#3ACFE8'][(row*3+col*7)%5],4)
 # Cards without an implemented live integration explicitly state the limitation
 supported={'contribution_activity_graph','github_stats_cards','most_used_languages','pull_request_tracker','featured_repository_rotation','latest_github_activity','contribution_snake','animated_typing_header'}
 if key not in supported:
  body+=rect(16,266,668,17,'#111B37',4)+t(350,279,'VISUAL PREVIEW  •  CONNECT DATA SOURCE FOR LIVE VALUES',10,'#C0A4E9','bold','middle')
 else:body+=t(350,279,'VISUAL MODULE  /  PROFILE DASHBOARD',10,'#9AAAD2',anchor='middle')
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs><linearGradient id="edge"><stop stop-color="#F552D8"/><stop offset=".55" stop-color="#8C6EFF"/><stop offset="1" stop-color="#3BDFFF"/></linearGradient><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#0C102A"/><stop offset="1" stop-color="#150B29"/></linearGradient></defs>{rect(1,1,w-2,h-2,'url(#bg)',16,'#4B397F')}{rect(1,1,8,h-2,accent,3)}{t(28,31,group.upper(),11,accent,'bold')}{t(28,66,title,26,'#FFFFFF','bold')}{line(28,77,670,77,'#2A325B',1)}{body}<rect x="1" y="1" width="698" height="288" rx="16" fill="none" stroke="url(#edge)" stroke-width="1.4"/></svg>'''
 (OUT/(key+'.svg')).write_text(svg)
def image(path,alt,width=700):return f'<img src="{path}" alt="{html.escape(alt)}" width="{width}" />'
def render():
 src=(ROOT/'README.md').read_text();a='<!-- NEON:FEATURES:START -->';b='<!-- NEON:FEATURES:END -->'
 if src.count(a)!=1 or src.count(b)!=1:raise ValueError('Missing README markers')
 chunks=['<!-- AUTO-GENERATED VISUAL MODULES: edit config/features.json -->','']
 live={'contribution_activity_graph':'activity','github_stats_cards':'stats','most_used_languages':'languages','pull_request_tracker':'opensource','featured_repository_rotation':'projects','latest_github_activity':'activity'}
 for group,keys in G.items():
  enabled=[k for k in keys if F[k]]
  if not enabled:continue
  chunks+=['## '+group.title(),'','<div align="center">','']
  for k in enabled:
   title=k.replace('_',' ').title();card(k,title,group)
   chunks+=[image('./assets/modules/'+k+'.svg',title),'<br>','']
   if k in live:chunks+=[image('./assets/generated/'+live[k]+'.svg',title+' live public data'),'<br>','']
   elif k=='contribution_snake':
    chunks+=['[🐍 View contribution snake animation workflow](https://github.com/'+P['github_username']+'/actions/workflows/snake.yml)','<br>','']
   elif k=='animated_typing_header':chunks+=['![Animated introduction](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=22&duration=2500&pause=1000&color=FF58D9&center=true&vCenter=true&width=680&lines=Build+Boldly;Learn+Relentlessly;Create+Differently)','<br>','']
  chunks+=['</div>','','---','']
 if not any(F.values()):chunks+=['All optional visual modules are disabled.']
 out=src.split(a)[0]+a+'\n'+'\n'.join(chunks).rstrip()+'\n'+b+src.split(b,1)[1]
 (ROOT/'README.md').write_text(out)
 print('Rendered',sum(F.values()),'of 40 enabled modules')
if __name__=='__main__':render()
