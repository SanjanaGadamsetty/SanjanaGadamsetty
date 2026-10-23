#!/usr/bin/env python3
"""40-feature README visibility controller, Python standard library only."""
from pathlib import Path
import json,html,urllib.request
ROOT=Path(__file__).resolve().parents[1]
def load(file):return json.loads((ROOT/'config'/file).read_text())
def img(url,alt):return f'<div align="center"><img src="{html.escape(url,quote=True)}" alt="{html.escape(alt)}" width="700" /></div>'
def link(url,label):return f'[{label}]({url})'
def code(text):return '<pre>\n'+html.escape(text)+'\n</pre>'
def info(text):return '> ℹ️ '+text

def render(k,p):
 u=p['github_username'];gh='https://github.com/'+u;gen='./assets/generated/'
 images={'contribution_activity_graph':gen+'activity.svg','github_stats_cards':gen+'stats.svg','most_used_languages':gen+'languages.svg','pull_request_tracker':gen+'opensource.svg','latest_github_activity':gen+'activity.svg','featured_repository_rotation':gen+'projects.svg','dynamic_neofetch_card':'./assets/neon-hero.svg','animated_typing_header':'https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&duration=2700&pause=950&color=FF55D8&center=true&vCenter=true&width=750&lines=Building+what%27s+next;AI+%2B+Full-Stack+%2B+Open+Source'}
 if k=='contribution_snake':return link(gh+'/actions/workflows/snake.yml','🐍 View contribution snake workflow and output')
 if k in images:return img(images[k],k.replace('_',' '))
 links={'contribution_heatmap':(gh,'View contribution heatmap'),'year_in_code_calendar':(gh,'View contribution calendar'),'leetcode_statistics':('https://leetcode.com/u/'+p['leetcode_username']+'/','LeetCode profile'),'codeforces_rating_tracker':('https://codeforces.com/profile/'+p['codeforces_username'],'Codeforces rating'),'codechef_rating_tracker':('https://www.codechef.com/users/'+p['codechef_username'],'CodeChef rating'),'hackerrank_badges':('https://www.hackerrank.com/profile/'+p['hackerrank_username'],'HackerRank badges'),'issue_contribution_tracker':(f'https://github.com/issues?q=is%3Aissue+author%3A{u}','Public issues'),'open_source_journey_timeline':(f'https://github.com/pulls?q=is%3Apr+author%3A{u}','Pull request history'),'daily_coding_challenge':(p['daily_challenge_url'],'Coding challenges'),'repository_statistics':(gh+'?tab=repositories','Public repositories')}
 if k in links:return link(*links[k])
 if k=='milestone_tracker':
  n=max(0,int(p['milestone_current']));total=max(1,int(p['milestone_target']));filled=min(20,round(20*n/total));return code(f'{n}/{total}  '+ '█'*filled+'░'*(20-filled))
 if k=='dsa_progress_tracker':return code('\n'.join(('✓ ' if done else '○ ')+topic for topic,done in p['dsa_topics'].items()))
 if k=='terminal_status_dashboard':return code('DEVELOPER STATUS\n● Building new projects\n● Pink / Blue / Purple / Black\n● Always learning')
 if k=='daily_developer_quote':return '> ✦ '+(p.get('quotes') or ['Keep building.'])[0]
 if k in ('currently_building','learning_progress_dashboard'):return code('\n'.join('❯ '+s for s in p['learning_now']))
 if k=='wakatime_statistics' and p.get('wakatime_username'):return link('https://wakatime.com/@'+p['wakatime_username'],'WakaTime profile')
 if k=='latest_blog_posts' and p.get('blog_feed_url'):return link(p['blog_feed_url'],'Blog feed')
 if k=='spotify_now_playing' and p.get('spotify_profile_url'):return link(p['spotify_profile_url'],'Spotify profile (not live now-playing)')
 setup={'pacman_graph':'Pac-Man animation generator','contribution_skyline_3d':'3D contributions generator','contribution_galaxy':'custom galaxy SVG generator','github_streak_stats':'contribution streak data integration','github_trophy_wall':'trophy renderer','github_metrics_dashboard':'GitHub Metrics integration','productive_hours_graph':'timestamped coding data','contributor_leaderboard':'repository scope and contributor data','developer_radar_chart':'skill scores and chart generator','developer_xp_system':'XP rules and event tracking','github_achievement_game':'badge rules and assets','cosmic_developer_dashboard':'custom SVG dashboard','wakatime_statistics':'WakaTime API integration','latest_blog_posts':'blog feed collector','spotify_now_playing':'Spotify OAuth and token refresh'}
 return info('Setup required: '+setup.get(k,'custom data source')+'. This switch works, but live content is not implemented yet.')

def main():
 groups=load('groups.json');flags=load('features.json')['features'];p=load('profile.json')
 allkeys=[k for ks in groups.values() for k in ks]
 if len(allkeys)!=40 or set(allkeys)!=set(flags) or not all(isinstance(v,bool) for v in flags.values()):raise ValueError('Exactly 40 boolean switches required')
 path=ROOT/'README.md';source=path.read_text();a='<!-- NEON:FEATURES:START -->';b='<!-- NEON:FEATURES:END -->'
 if source.count(a)!=1 or source.count(b)!=1:raise ValueError('Missing unique README markers')
 chunks=['<!-- Generated. Edit config/features.json, not this section. -->','']
 for group,keys in groups.items():
  visible=[k for k in keys if flags[k]]
  if not visible:continue
  chunks+=['### ✦ '+group.upper(),'']
  for k in visible:
   label=k.replace('_',' ').title()
   chunks += [f'#### 💠 {label}', '', render(k,p), '', '---', '']

 if not any(flags.values()):chunks+=['`All 40 optional features are disabled.`']
 result=source.split(a)[0]+a+'\n'+'\n'.join(chunks).rstrip()+'\n'+b+source.split(b,1)[1]
 if result!=source:path.write_text(result)
 print(f'Enabled: {sum(flags.values())}/40. README '+('updated.' if result!=source else 'unchanged.'))
if __name__=='__main__':main()
