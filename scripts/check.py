#!/usr/bin/env python3
"""Check the shipped site, not only the source templates."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re,json
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'dist';BASE='/foleno-site/'
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.links=[];self.assets=[];self.ids=set();self.lang=None;self.headings=0;self.canonical=[];self.alternates={};self.language_links=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if tag=='html':self.lang=a.get('lang')
  if tag=='a' and 'href'in a:self.links.append(a['href'])
  if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a['href'])
  if tag=='link' and a.get('rel')=='alternate':self.alternates[a.get('hreflang')]=a.get('href')
  if tag=='a' and a.get('class')=='lang':self.language_links.append(a.get('href'))
  if tag in ['img','script'] and a.get('src'):self.assets.append(a['src'])
  if tag=='link' and a.get('rel') in ['stylesheet','icon','apple-touch-icon']:self.assets.append(a['href'])
  if tag=='img':assert 'alt'in a and int(a.get('width',0))>0 and int(a.get('height',0))>0,a
  if tag=='h1':self.headings+=1
pages={p:Page(p.read_text()) for p in DIST.rglob('*.html')}
for p,page in pages.items():
 text=p.read_text();assert page.lang,p
 for link in page.links+page.assets:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  if not u.path:target=p
  else:
   assert u.path.startswith(BASE),(p,link,'Incorrect project base path')
   target=DIST/unquote(u.path[len(BASE):]);target=target/'index.html' if target.is_dir() else target
  assert target.is_file(),(p,link,'Broken internal URL')
  if u.fragment:assert u.fragment in pages.get(target,page).ids,(p,link,'Missing fragment')
 if p.parent.name in ['zh','en','support','privacy']:
  assert page.headings==1,(p,page.headings)
  rel=p.relative_to(DIST).parent.as_posix()
  expected='https://szlab-ai.github.io'+BASE+rel+'/'
  assert page.canonical==[expected],(p,page.canonical)
  parts=rel.split('/');language=parts[0];suffix='/'.join(parts[1:])
  routes={l:BASE+l+'/'+(suffix+'/' if suffix else '') for l in ['zh','en']}
  assert page.alternates=={'zh-CN':'https://szlab-ai.github.io'+routes['zh'],'en':'https://szlab-ai.github.io'+routes['en'],'x-default':'https://szlab-ai.github.io'+routes['zh']},p
  assert page.language_links==[routes['en' if language=='zh' else 'zh']],p
  assert not re.search(r'永久免费|无内购|永不收费|free forever|no in.app purchases|no subscriptions',text,re.I),p
  assert 'szlab.ai@outlook.com'in text and 'https://t.me/sz_lab'in text,p
 assert not re.search(r'googletagmanager|google-analytics|cloudflareinsights|sendBeacon|localStorage|document.cookie',text,re.I),p
for locale in ['zh','en']:
 home=(DIST/locale/'index.html').read_text();privacy=(DIST/locale/'privacy/index.html').read_text()
 for value in ['CAJ','PDF','iPhone','iPad','Mac','iCloud','API Key' if locale=='zh' else 'API key']:assert value in home,(locale,value)
 for value in ['GitHub','CloudKit','Keychain' if locale=='en' else '钥匙串','TestFlight']:assert value in privacy,(locale,value)
 assert 'https://testflight.apple.com/join/hAVJeFUM'in home
 assert not re.search(r'href="https://apps.apple.com/',home), 'Do not publish a dead store link before release'
 assert all(s in home for s in ['role="tablist"','aria-selected="true"','aria-controls="panel-Mac"'])
assert not any(p.suffix in ['.swift','.sqlite','.db','.p8','.p12','.mobileprovision'] for p in ROOT.rglob('*'))
assert (DIST/'assets/site.js').stat().st_size<5000
print(f'PASS: {len(pages)} HTML pages; all internal links/assets/fragments, language routes, metadata, content boundaries and privacy disclosures checked.')
