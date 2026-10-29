#!/usr/bin/env python3
"""Build the public site using only Python's standard library."""
from pathlib import Path
from html import escape
import json, shutil, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from content import COPY
BASE='/foleno-site/'
ORIGIN='https://szlab-ai.github.io'
SITE=ORIGIN+BASE
DIST=ROOT/'dist'

def url(lang,kind=''):return BASE+lang+'/'+(kind+'/' if kind else '')
def a(text,href,cls=''):return f'<a href="{escape(href,quote=True)}"'+(f' class="{cls}"' if cls else '')+'>'+text+'</a>'
def img(name,alt,cls='',eager=False):
    # Dimensions describe the actual shipped WebP assets.
    dims={'reader-ipad':(1800,1316),'tools-ipad':(1800,1316),'reader-iphone':(1013,2200),'notes-iphone':(1013,2200),'library-iphone':(1013,2200),'reader-mac':(1800,1213),'notes-mac':(1800,1213),'library-mac':(1800,1213)}
    w,h=dims[name]
    return f'<img src="{BASE}assets/{name}.webp" alt="{escape(alt,quote=True)}" width="{w}" height="{h}" loading="{"eager" if eager else "lazy"}" decoding="async"'+(f' class="{cls}"' if cls else '')+(' fetchpriority="high"' if eager else '')+'>'
def icon(size=180):return f'<img src="{BASE}assets/icon-{size}.png" alt="" width="{size}" height="{size}">'
def button(text,href,secondary=False,small=False):return a(text+' <span class="arrow" aria-hidden="true">↗</span>',href,'btn'+(' secondary' if secondary else '')+(' small' if small else ''))
def eyebrow(t):return f'<div class="eyebrow">{t}</div>'
def bullets(rows):return '<ul>'+''.join(f'<li>{escape(t)}</li>' for t in rows)+'</ul>'
def faq(c):return '<div class="faq-list">'+''.join(f'<details><summary>{escape(q)}</summary><p>{body}</p></details>' for q,body in c['faq'])+'</div>'
def layout(lang,kind,body):
 c=COPY[lang];other='en' if lang=='zh' else 'zh';title=c['title'] if not kind else c[kind+'Title'].replace('<br>',' ')+ ' · Foleno';canonical=ORIGIN+url(lang,kind)
 nav=f'<header class="site-header"><nav class="wrap nav" aria-label="{"主导航" if lang=="zh" else "Main navigation"}">{a(icon(180)+"<span>Foleno</span>",url(lang),"brand")}<div class="nav-links">'+''.join(a(c['nav'][i],url(lang)+'#'+anchor,'desktop-link') for i,anchor in enumerate(['features','devices','faq']))+a(c['nav'][3],url(lang,'support'))+a(c['other'],url(other,kind),'lang')+'</div>'+button(c['beta'],'https://testflight.apple.com/join/hAVJeFUM',small=True)+'</nav></header>'
 footer=f'<footer class="footer"><div class="wrap"><div class="footer-top">{a(icon(180)+"<span>Foleno</span>",url(lang),"brand")}<div class="footer-links">{a(c["privacy"],url(lang,"privacy"))}{a(c["support"],url(lang,"support"))}{a(c["contact"],"mailto:szlab.ai@outlook.com")}{a("Telegram 群组" if lang=="zh" else "Telegram group","https://t.me/sz_lab")}</div></div><div class="footer-bottom"><span>{c["copyright"]} · {a(c["other"],url(other,kind))}</span><span>{c["footerNote"]}</span></div></div></footer>'
 schema={'@context':'https://schema.org','@type':'SoftwareApplication','name':'Foleno','applicationCategory':'ProductivityApplication','operatingSystem':'iOS 17+, iPadOS 17+, macOS 14+','description':c['description'],'url':canonical}
 return f'''<!doctype html>
<html lang="{c['locale']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><meta name="theme-color" content="#faf9f5"><title>{escape(title)}</title><meta name="description" content="{escape(c['description'],quote=True)}"><link rel="canonical" href="{canonical}"><link rel="alternate" hreflang="zh-CN" href="{ORIGIN+url('zh',kind)}"><link rel="alternate" hreflang="en" href="{ORIGIN+url('en',kind)}"><link rel="alternate" hreflang="x-default" href="{ORIGIN+url('zh',kind)}"><meta property="og:type" content="website"><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(c['description'],quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE}assets/social.jpg"><meta name="twitter:card" content="summary_large_image"><link rel="icon" type="image/png" href="{BASE}assets/icon-32.png"><link rel="apple-touch-icon" href="{BASE}assets/icon-180.png"><link rel="stylesheet" href="{BASE}assets/site.css"><script defer src="{BASE}assets/site.js"></script><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body><a class="skip" href="#main">{c['skip']}</a>{nav}<main id="main">{body}</main>{footer}</body></html>'''
def home(lang):
 c=COPY[lang]
 hero=f'''<section class="hero"><div class="wrap"><div class="hero-grid"><div>{eyebrow(c['eyebrow'])}<h1>{c['headline']}</h1><p>{c['intro']}</p><div class="hero-actions">{button(c['beta'],'https://testflight.apple.com/join/hAVJeFUM')}{button(c['explore'],'#devices',True)}</div><small class="release-note">{c['release']}</small></div><div class="hero-stage"><div class="stage-ground"></div><span class="scene-label">{c['heroLabel']}</span><div class="tablet hero-tablet">{img('reader-ipad','Foleno iPad CAJ 阅读界面' if lang=='zh' else 'Foleno CAJ reader on iPad, Chinese demo interface',eager=True)}</div><div class="phone hero-phone">{img('library-iphone','Foleno iPhone 文献库' if lang=='zh' else 'Foleno library on iPhone, Chinese demo interface',eager=True)}</div></div></div><div class="hero-caption">{c['heroCaption']}</div></div></section><div class="wrap feature-strip">'''+''.join(f'<span>{t}<small>{s}</small></span>' for t,s in c['strip'])+'</div>'
 tabs='<div class="device-tabs" role="tablist" hidden aria-label="'+c['screensLabel']+'">'+''.join(f'<button type="button" role="tab" id="tab-{dev}" aria-controls="panel-{dev}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}">{dev}</button>' for i,dev in enumerate(['iPad','iPhone','Mac']))+'</div>'
 panels=''
 for i,(dev,asset,frame) in enumerate([('iPad','reader-ipad','tablet'),('iPhone','reader-iphone','phone'),('Mac','reader-mac','desktop')]):
  panels+=f'<figure class="device-panel" role="tabpanel" id="panel-{dev}" aria-labelledby="tab-{dev}" tabindex="0"'+(' hidden' if i else '')+f'><div class="{frame}">{img(asset,c["deviceCaptions"][i])}</div><figcaption>{c["deviceCaptions"][i]}</figcaption></figure>'
 reader=f'''<section class="section wrap" id="features"><div class="section-title-row"><div>{eyebrow(c['readEye'])}<h2>{c['readTitle']}</h2></div><p>{c['readIntro']}</p></div><div class="showcase" id="devices"><div class="showcase-top">{tabs}<span class="showcase-index">FOLENO / READER</span></div>{panels}<noscript>{img('reader-iphone',c['deviceCaptions'][1],'noscript-media')}{img('reader-mac',c['deviceCaptions'][2])}</noscript></div><p class="note format-note">{c['formatNote']}</p></section>'''
 notes=f'''<section class="section wrap"><div class="split"><div class="copy">{eyebrow(c['notesEye'])}<h2>{c['notesTitle']}</h2><p>{c['notesBody']}</p>{bullets(c['notesList'])}</div><div class="annotation-art"><div class="desktop">{img('notes-mac','Mac 文献高亮与批注界面' if lang=='zh' else 'Actual Mac app with highlighted passages and comments')}</div><div class="annotation-callout"><small>{c['calloutLabel']}</small>{c['callout']}</div></div></div></section>'''
 library=f'''<section class="section wrap library-section"><div class="split"><div class="library-art"><div class="library-kicker"><span>{c['libraryCaption']}</span><span>CAJ / PDF</span></div><div class="desktop">{img('library-mac','原创论文构成的 Foleno 文献库' if lang=='zh' else 'Foleno library containing original demonstration papers')}</div></div><div class="copy">{eyebrow(c['libraryEye'])}<h2>{c['libraryTitle']}</h2><p>{c['libraryBody']}</p>{bullets(c['libraryList'])}</div></div></section>'''
 device_icons=[('iPhone','<rect x="23" y="3" width="22" height="47" rx="4"/><path d="M30 8h8M31 45h6"/>'),('iPad','<rect x="13" y="3" width="42" height="47" rx="4"/><circle cx="34" cy="46" r="1"/>'),('Mac','<rect x="6" y="7" width="56" height="35" rx="3"/><path d="M3 47h62M27 42l-2 5m16-5 2 5"/>')]
 devices=''.join(f'<div class="device-symbol"><svg viewBox="0 0 68 55" aria-hidden="true">{svg}</svg><span>{name}</span></div>' for name,svg in device_icons)
 sync=f'''<section class="section sync-section"><div class="wrap"><div class="section-title-row"><div>{eyebrow(c['syncEye'])}<h2>{c['syncTitle']}</h2></div><p>{c['syncIntro']}</p></div><div class="sync-visual"><div class="sync-node"><small>iCloud</small><h3>{c['syncLibrary']}</h3><div class="sync-tags">{''.join(f'<span>{t}</span>' for t in c['syncTags'])}</div></div><div class="sync-route" aria-hidden="true">↔</div><div class="sync-node"><small>{c['syncDevices']}</small><div class="device-names">{devices}</div></div></div><div class="sync-bottom"><span>{c['syncNote']}</span><span>{c['syncMac']}</span></div></div></section>'''
 ai=f'''<section class="section wrap"><div class="ai-grid"><div class="copy">{eyebrow(c['aiEye'])}<h2>{c['aiTitle']}</h2><p>{c['aiBody']}</p>{bullets(c['aiList'])}</div><div><div class="ai-flow"><div class="flow-label">{c['flowLabel']}</div><div class="flow-source"><small>{c['flowSource']}</small>{c['flowText']}</div><div class="flow-arrow" aria-hidden="true">↓</div><div class="flow-model"><span class="model-mark" aria-hidden="true">AI</span><div><strong>{c['flowService']}</strong><small>{c['flowKey']}</small></div></div></div><p class="note">{c['aiNote']}</p></div></div><div class="native-band"><div><h3>{c['nativeTitle']}</h3><p>{c['nativeBody']}</p></div><div class="themes"><div class="theme-swatch" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div><div class="theme-swatch dark" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div><div class="swatch-caption">{c['themeLabel']}</div></div></div></section>'''
 questions=f'''<section class="section faq-section" id="faq"><div class="wrap faq-grid"><div class="section-heading">{eyebrow(c['faqEye'])}<h2>{c['faqTitle']}</h2><p>{c['faqIntro']}</p>{a(c['faqMore']+' →',url(lang,'support'),'note')}</div>{faq(c)}</div></section>'''
 download=f'''<section class="download wrap">{icon(180)}<h2>{c['downloadTitle']}</h2><p>{c['downloadBody']}</p>{button(c['beta'],'https://testflight.apple.com/join/hAVJeFUM')}<div class="release-note">{a(c['supportCTA'],url(lang,'support'))} · iOS / iPadOS 17+</div></section>'''
 return hero+reader+notes+library+sync+ai+questions+download

def sub_intro(lang,kind):
 c=COPY[lang]
 return f'<div class="breadcrumbs">{a(c["home"],url(lang))} <span aria-hidden="true">/</span> {c[kind+"Title"].replace("<br>"," ")}</div><div class="page-intro">{eyebrow("FOLENO / "+kind.upper())}<h1>{c[kind+"Title"]}</h1><p>{c[kind+"Intro"]}</p></div>'
def support(lang):
 c=COPY[lang]
 contacts=f'<div class="support-contact"><a class="contact-card" href="mailto:szlab.ai@outlook.com"><small>{c["emailLabel"]}</small><strong>szlab.ai@outlook.com <span aria-hidden="true">↗</span></strong><p>{c["emailBody"]}</p></a><a class="contact-card" href="https://t.me/sz_lab"><small>{c["groupLabel"]}</small><strong>{c["groupName"]} <span aria-hidden="true">↗</span></strong><p>{c["groupBody"]}</p></a></div>'
 steps=f'<section class="quick-start"><h2>{c["startTitle"]}</h2><div class="steps">'+''.join(f'<div class="step"><span>0{i+1}</span><h3>{title}</h3><p>{body}</p></div>' for i,(title,body) in enumerate(c['steps']))+'</div></section>'
 questions=f'<section class="support-faq"><h2>{c["faqEye"]}</h2>{faq(c)}</section>'
 feedback=f'<section class="feedback-box"><h3>{c["feedbackTitle"]}</h3><p>{c["feedbackBody"]}</p><ul>'+''.join(f'<li>{x}</li>' for x in c['feedbackItems'])+f'</ul><p>{c["feedbackSafety"]}</p></section>'
 return f'<div class="subpage wrap">{sub_intro(lang,"support")}{contacts}{steps}{questions}{feedback}</div>'
def privacy(lang):
 c=COPY[lang]
 nav='<nav class="policy-nav" aria-label="'+('隐私政策目录' if lang=='zh' else 'Privacy policy contents')+'">'+''.join(a(title,'#'+id) for id,title,body in c['policy'])+'</nav>'
 text='<article class="policy-content"><p class="policy-date">'+c['updated']+'</p>'+''.join(f'<section id="{id}"><h2>{title}</h2><p>{body}</p></section>' for id,title,body in c['policy'])+'</article>'
 return f'<div class="subpage wrap">{sub_intro(lang,"privacy")}<div class="policy-layout">{nav}{text}</div></div>'

if DIST.exists():shutil.rmtree(DIST)
shutil.copytree(ROOT/'public',DIST)
for lang in COPY:
 for kind,fn in [('',home),('support',support),('privacy',privacy)]:
  path=DIST/lang/kind;path.mkdir(parents=True,exist_ok=True);(path/'index.html').write_text(layout(lang,kind,fn(lang)))
(DIST/'index.html').write_text(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url={BASE}zh/"><meta name="robots" content="noindex"><title>Foleno</title></head><body><p><a href="{BASE}zh/">Foleno · 简体中文</a> / <a href="{BASE}en/">English</a></p></body></html>')
(DIST/'404.html').write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found · Foleno</title><body><h1>Page not found</h1><p><a href="{BASE}en/">Foleno home</a> · <a href="{BASE}zh/">返回首页</a></p></body></html>')
urls=[SITE+lang+'/'+(kind+'/' if kind else '') for lang in COPY for kind in ['', 'support','privacy']]
(DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{u}</loc></url>' for u in urls)+'</urlset>')
(DIST/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n')
(DIST/'.nojekyll').touch()
print('Built 6 localized pages, root redirect, 404, sitemap and self-hosted assets.')
