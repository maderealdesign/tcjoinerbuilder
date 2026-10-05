#!/usr/bin/env python3
"""Build the approved TC Joinery site using Python's standard library only."""
from pathlib import Path
import re,json,html,hashlib,shutil
from datetime import date
from local_pages import coverage_section, coverage_guide, service_tiles, render_areas
ROOT=Path(__file__).resolve().parent.parent
SRC=ROOT/'src'; OUT=ROOT/'public'; BASE='https://tcjoinerbuilder.co.uk'
OUT.mkdir(exist_ok=True)
def esc(s):return html.escape(str(s),quote=True)
services=json.loads((SRC/'services.json').read_text());assets=json.loads((SRC/'assets.json').read_text());analytics=json.loads((SRC/'analytics.json').read_text());social=json.loads((SRC/'social.json').read_text())
guides=json.loads((SRC/'guides.json').read_text())
raw=(SRC/'homepage.html').read_text()
calm=(SRC/'calm-homepage.html').read_text()
area_data=json.loads((SRC/'areas.json').read_text())
map_js=(SRC/'coverage-map.js').read_text().replace('__MAP_POINTS__',json.dumps(json.loads((SRC/'map-points.json').read_text())['points']))
MAP_JS='coverage-map-'+hashlib.sha256(map_js.encode()).hexdigest()[:10]+'.js'
(OUT/'assets'/MAP_JS).write_text(map_js)
map_css=(SRC/'coverage-map.css').read_text()
MAP_CSS='coverage-map-'+hashlib.sha256(map_css.encode()).hexdigest()[:10]+'.css'
(OUT/'assets'/MAP_CSS).write_text(map_css)
calm_css=(SRC/'calm-homepage.css').read_text()
CALM_CSS='home-'+hashlib.sha256(calm_css.encode()).hexdigest()[:10]+'.css'
(OUT/'assets'/CALM_CSS).write_text(calm_css)
js=(SRC/'site.js').read_text().replace('__GA_MEASUREMENT_ID__',analytics.get('measurementId',''))
JS_FILE='site-'+hashlib.sha256(js.encode()).hexdigest()[:10]+'.js'
(OUT/'assets'/JS_FILE).write_text(js)
css=re.search(r'<style>(.*?)</style>',raw,re.S).group(1)
css="""@font-face{font-family:Montserrat;src:url('/fonts/montserrat-latin.woff2') format('woff2');font-weight:400 800;font-display:swap}@font-face{font-family:'Open Sans';src:url('/fonts/open-sans-latin.woff2') format('woff2');font-weight:400 700;font-display:swap}\n"""+css
css+='''
/* Production pages share the approved brand. */
body{overflow-wrap:break-word}.button,.text-link,.footer-links a,.nav-links a{min-height:44px}.text-link{align-items:center}.nav-links a{display:flex;align-items:center}.footer-links a{display:inline-flex;align-items:center}.eyebrow,.number{color:#b92041}.hero .eyebrow{background:#b92041}.button{background:#e11d48}.button:hover{background:#ab1735}.hero h1 span,.brand strong{color:var(--accent)}.proof-strip{background:#b92041}.about .eyebrow,.contact .eyebrow,.together .eyebrow{color:#ff8aa1}.page-hero{padding:65px 0;background:var(--light)}.page-hero h1{font-size:clamp(35px,4.2vw,56px);max-width:800px}.page-hero p{margin-top:20px;max-width:740px}.page-hero-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:55px;align-items:center}.page-hero-grid img{height:420px;border-radius:10px}.breadcrumbs{display:flex;gap:9px;flex-wrap:wrap;font-size:12px;margin-bottom:24px;color:var(--muted)}.breadcrumbs a{text-decoration:underline;text-underline-offset:3px}.page-content{max-width:850px}.page-content h2{font-size:30px;margin:40px 0 20px}.page-content h2:first-child{margin-top:0}.page-content p+p{margin-top:18px}.page-content ul{padding-left:22px;color:var(--muted);font-size:15px}.page-content li{margin:10px 0}.service-layout{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(230px,.8fr);gap:75px;align-items:start}.service-aside{padding:27px;border:1px solid var(--line);border-top:4px solid var(--accent);border-radius:6px;background:var(--light)}.service-aside p{font-size:13px;margin:15px 0}.service-aside ul{font-size:13px;padding-left:18px}.service-aside li{margin-bottom:10px}.service-aside .button{margin-top:15px;width:100%;font-size:12px}.related-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:30px}.related-card{border:1px solid var(--line);border-radius:8px;padding:24px;background:white}.related-card h3{font-size:19px}.related-card p{font-size:13px;margin:15px 0}.service-photos{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:30px}.service-photos img{height:300px;border-radius:8px}.service-photos figcaption{font-size:12px;margin-top:12px;color:var(--muted)}.service-area-line{font-size:13px;margin-top:25px!important}.cta-band{background:var(--dark);color:white;padding:50px 0}.cta-band .wrap{display:flex;justify-content:space-between;align-items:center;gap:35px}.cta-band h2{font-size:32px}.cta-band p{color:#cbd5e1;margin-top:15px;max-width:700px}.cta-band .button{flex-shrink:0}.page-faq{padding-top:50px}.form-note{font-size:11px;margin:8px 0 20px}.form-note a{text-decoration:underline}.form-error{color:#9f1239}.footer-legal{display:flex;gap:18px;flex-wrap:wrap;font-size:11px;margin-top:20px}.footer-legal a{color:#cbd5e1;text-decoration:underline;min-height:28px}.cookie-panel{position:fixed;left:20px;bottom:85px;z-index:50;max-width:440px;width:calc(100% - 40px);background:#fff;padding:24px;border:1px solid #cbd5e1;border-radius:8px;box-shadow:0 8px 40px #0f172a35}.cookie-panel[hidden]{display:none}.cookie-panel p{font-size:13px}.cookie-panel h2{font-size:22px;margin-bottom:12px}.cookie-actions{display:flex;gap:10px;margin-top:18px}.cookie-actions button{flex:1;padding:12px;border-radius:5px;border:1px solid var(--dark);background:var(--dark);color:#fff;cursor:pointer;font-size:12px;font-weight:700}.cookie-actions button:first-child{background:#fff;color:var(--dark)}.cookie-panel a{font-size:12px;text-decoration:underline}.cookie-settings{background:none;color:inherit;border:0;text-decoration:underline;font:inherit;cursor:pointer;padding:0;min-height:28px}.photo-note{font-size:12px;margin-top:20px}.section-jump{display:flex;gap:16px;flex-wrap:wrap;margin-top:24px}.section-jump a{text-decoration:underline;font-size:13px}.nav-links a[aria-current=page]{color:#ff8aa1}.page-hero .button{margin-top:24px}.footer .brand strong{color:var(--accent)}.service-intro-photo{position:relative}.service-intro-photo figcaption{font-size:11px;margin-top:10px}.stars{color:#966000}.review-source,.project p,.review-footer p{color:#475569}.project figcaption .detail-photo-link{color:#a91636}.build-detail+.light{border-top:1px solid var(--line)}.privacy-content h2{font-size:25px}.thanks{min-height:50vh;padding:90px 0}.thanks p{margin:22px 0;max-width:650px}.error-main{min-height:50vh}.service-index{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.service-index a{display:block;border:1px solid var(--line);border-radius:8px;padding:22px}.service-index h3{margin-bottom:14px}.service-index p{font-size:13px}.gallery-project-links{display:flex;flex-wrap:wrap;gap:18px;margin:25px 0 0}.gallery-project-links a{text-decoration:underline;font-size:13px}.form-status{margin-top:15px;font-size:13px}.form-status:empty{display:none}.business-facts{font-size:14px;display:grid;gap:12px;margin-top:25px}.footer{scroll-margin-bottom:70px}@media(max-width:760px){.page-hero{padding:40px 0}.page-hero-grid,.service-layout{grid-template-columns:1fr;gap:30px}.page-hero-grid img{height:300px}.service-aside{order:2}.related-grid,.service-index{grid-template-columns:1fr}.service-photos{grid-template-columns:1fr 1fr;gap:15px}.service-photos img{height:235px}.service-photos figure:last-child:nth-child(odd){grid-column:1/-1}.cta-band .wrap{flex-direction:column;align-items:start}.page-content h2{font-size:26px}.cookie-panel{bottom:80px;padding:20px}.hero{min-height:720px}.hero h1{font-size:43px}.hero .eyebrow{font-size:8px}.contact-actions .button,.hero-actions .button{min-height:46px}.page-hero h1{font-size:36px}.review-card blockquote{font-size:19px}}
'''
css+='\n.guide-checklist{padding:22px;border-left:4px solid var(--accent);background:var(--light);margin-top:20px}.guide-checklist p{line-height:2.1}.page-content ol{padding-left:24px;color:var(--muted);font-size:15px}.page-content a:not(.button){text-decoration:underline;text-underline-offset:3px}.guide-card-image{height:200px;border-radius:6px;margin-bottom:22px}.guide-aside a{display:block;font-size:13px;margin:14px 0;text-decoration:underline}.guide-date{font-size:12px;margin-bottom:24px}.guide-card h2{font-size:19px}\n'
css+='\n'+(SRC/'homepage-compact.css').read_text()
css+='''
.area-buttons{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}.area-buttons a{display:flex;align-items:center;min-height:44px;padding:8px 14px;border:1px solid #cbd5e1;background:white;border-radius:5px;font-size:13px}.area-content .page-content figure{margin-top:30px}.area-content .page-content figure img{max-height:420px;border-radius:7px}.area-content figcaption{font-size:12px;margin-top:10px;color:#475569}.local-resource{margin-top:30px;padding:24px;background:#f8fafc;border-left:3px solid #f43f5e}.local-resource p{font-size:14px;margin:12px 0}.local-resource .small-note{font-size:12px}.area-hub{display:grid;grid-template-columns:1fr 1fr;gap:45px;align-items:center}@media(max-width:760px){.area-hub{grid-template-columns:1fr}.area-content .page-content figure img{max-height:320px}}
'''
CSS_FILE='site-'+hashlib.sha256(css.encode()).hexdigest()[:10]+'.css'
(OUT/'assets'/CSS_FILE).write_text(css)
nav='''<header class="header"><div class="wrap nav"><a class="brand" href="/" aria-label="Tom Cutts homepage"><strong>Tom Cutts</strong><small>JOINERY &amp; BUILDING</small></a><nav class="nav-links" id="navigation" aria-label="Main navigation"><a href="/">Home</a><a href="/about">About</a><a href="/services">Services</a><a href="/commercial">Commercial</a><a href="/gallery">Gallery</a><a href="/#reviews">Reviews</a><a href="/areas-we-cover">Areas</a></nav><a class="button" href="tel:07816937159">07816 937 159 ↗</a><button class="menu-toggle" type="button" aria-controls="navigation" aria-expanded="false">Menu <span aria-hidden="true">☰</span></button></div></header>'''
footer=re.search(r'<footer class="footer">.*?</footer>',raw,re.S).group(0)
for a,b in [('href="#home"','href="/"'),('href="#about"','href="/about"'),('href="#services"','href="/services"'),('href="#gallery"','href="/gallery"'),('href="#contact"','href="/contact"')]:footer=footer.replace(a,b)
footer=footer.replace(' · Homepage design preview','')
settings='<button class="cookie-settings" type="button" data-cookie-settings>Cookie settings</button>' if analytics.get('measurementId') else ''
footer=footer.replace('</footer>',f'<div class="wrap footer-legal"><a href="/guides">Project guides</a><a href="/privacy">Privacy &amp; cookies</a><a href="/areas-we-cover">Areas we cover</a>{settings}<span>Website by <a href="https://madereal.uk" rel="noopener">madereal.uk</a></span></div></footer>')
quick=re.search(r'<div class="quick-contact".*?</div>',raw,re.S).group(0)
contact=re.search(r'<section class="section contact".*?</section>',raw,re.S).group(0)
contact=contact.replace('id="preview-form"','id="enquiry-form" name="homepage-enquiry" method="POST" action="/thank-you" data-netlify="true" netlify-honeypot="bot-field"')
contact=contact.replace('Preview form only — no message will be sent.','Send your enquiry to our team. <a href="/privacy">How we use your details</a>.').replace('class="demo-note"','class="form-note"')
contact=contact.replace('Preview your enquiry','Send your enquiry')
contact=contact.replace('<div class="form-title">','<input type="hidden" name="form-name" value="homepage-enquiry"><input type="hidden" name="subject" value="Website enquiry — Tom Cutts Joinery"><input type="hidden" name="page" value="/"><p hidden><label>Leave this empty<input name="bot-field" tabindex="-1" autocomplete="off"></label></p><div class="form-title">',1)
contact=contact.replace('<p id="form-status"','<p class="form-status" id="form-status"')
# Add an optional telephone field: useful for quotations, never sent to Analytics.
contact=contact.replace('<label for="project">','<label for="phone">Phone number (optional)<input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="Your contact number"></label><label for="project">')
contact=contact.replace('<textarea id="message"','<textarea maxlength="5000" id="message"')
reviews=re.search(r'<section class="section light reviews".*?</section>',raw,re.S).group(0)
areas=['Colne','Pendle','Clitheroe','Whalley','Barrow (Ribble Valley)','Ribble Valley','Silsden','Sutton','Cross Hills','Burnley','Lancashire']
business={'@type':'Organization','@id':BASE+'/#business','name':'Tom Cutts Joinery & Building','url':BASE+'/','telephone':'+447816937159','email':'tcuttsjoinery@outlook.com','foundingDate':'2020','logo':BASE+'/favicon-48x48.png','areaServed':areas,'sameAs':[social['facebook'],social['google']]}
pages=[]
def image(name,alt,hero=False):
 m=assets.get(name)
 if not m: m=next((v for v in assets.values() if v['file']==name),None)
 if not m: raise ValueError('Unknown image '+name)
 sizes='(max-width: 760px) 100vw, 50vw' if hero else '(max-width: 760px) 48vw, 30vw'
 return f'<img src="/assets/{m["file"]}" srcset="'+', '.join('/assets/'+f+' '+str(w)+'w' for f,w in m['srcset'])+f'" sizes="{sizes}" width="{m["width"]}" height="{m["height"]}" alt="{esc(alt)}" '+('fetchpriority="high"' if hero else 'loading="lazy" decoding="async"')+'>'
def optimize_images(s):
 def fix(m):
  tag=m.group(0)
  if ' srcset=' in tag:return tag
  src=re.search(r'src="(?:/)?assets/([^"]+)"',tag)
  if not src:return tag
  name=src.group(1)
  if name=='hero.jpg':
   return '<img class="hero-image" src="/assets/hero-1280.webp" srcset="/assets/hero-768.webp 768w, /assets/hero-1280.webp 1280w, /assets/hero-1672.webp 1672w" sizes="100vw" width="1672" height="941" alt="Illustrative concept of a timber garden room opening onto a deck" fetchpriority="high">'
  if name not in assets:return tag
  a=assets[name];tag=tag.replace('assets/'+name,'/assets/'+a['file']).replace('//assets/','/assets/')
  tag=re.sub(r'width="[^"]+"',f'width="{a["width"]}"',tag);tag=re.sub(r'height="[^"]+"',f'height="{a["height"]}"',tag)
  tag=tag[:-1]+' srcset="'+', '.join('/assets/'+f+' '+str(w)+'w' for f,w in a['srcset'])+'" sizes="(max-width: 760px) 100vw, 50vw">';return tag
 s=re.sub(r'<img\b[^>]*>',fix,s)
 for name,a in assets.items():s=s.replace('href="assets/'+name+'"','href="/assets/'+a['file']+'"')
 return s

contact=optimize_images(contact)

def render(path,title,description,content,label=None,noindex=False,extra=None,hero_home=False):
 content=optimize_images(content)
 canonical=BASE+path
 graph=[business,{'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':'Tom Cutts Joinery & Building','publisher':{'@id':BASE+'/#business'}},{'@type':'WebPage','@id':canonical+'#page','url':canonical,'name':title,'description':description,'isPartOf':{'@id':BASE+'/#website'},'about':{'@id':BASE+'/#business'}}]
 if path!='/':graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':BASE+'/'},{'@type':'ListItem','position':2,'name':label or title.split('|')[0].strip(),'item':canonical}]})
 if path.startswith('/areas/'):
  graph[-1]['itemListElement'].insert(1,{'@type':'ListItem','position':2,'name':'Areas we cover','item':BASE+'/areas-we-cover'})
  graph[-1]['itemListElement'][-1]['position']=3
 if extra:graph.append(extra)
 preload='<link rel="preload" as="image" href="/assets/hero-1280.webp" imagesrcset="/assets/hero-768.webp 768w, /assets/hero-1280.webp 1280w, /assets/hero-1672.webp 1672w" imagesizes="100vw">' if hero_home else ''
 page_nav=re.search(r'<header-template>(.*?)</header-template>',calm,re.S).group(1) if hero_home else nav
 page_footer=re.search(r'<footer-template>(.*?)</footer-template>',calm,re.S).group(1) if hero_home else footer
 page_quick='' if hero_home else quick
 page_css=CALM_CSS if hero_home else CSS_FILE
 map_assets=f'<link rel="stylesheet" href="/vendor/leaflet/leaflet.css"><link rel="stylesheet" href="/assets/{MAP_CSS}"><script src="/assets/{MAP_JS}" defer></script>' if 'id="coverage-map"' in content else ''
 structured=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False)
 doc=f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#1e293b"><meta name="robots" content="{'noindex, follow' if noindex else 'index, follow, max-image-preview:large'}"><title>{esc(title)}</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="{canonical}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><meta property="og:type" content="website"><meta property="og:locale" content="en_GB"><meta property="og:site_name" content="Tom Cutts Joinery &amp; Building"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{BASE}/assets/wooden-clad-building-grey-doors-windows.webp"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:image" content="{BASE}/assets/wooden-clad-building-grey-doors-windows.webp"><link rel="preload" href="/fonts/montserrat-latin.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/assets/{page_css}">{preload}{map_assets}<script type="application/ld+json">{structured}</script><script src="/assets/{JS_FILE}" defer></script></head><body><a class="skip-link" href="#main">Skip to content</a>{page_nav}<main id="main">{content}</main>{page_footer}{page_quick}{{COOKIE_PANEL}}</body></html>'''
 cookie=''
 if analytics.get('measurementId'):
  cookie='<section class="cookie-panel" id="cookie-panel" aria-labelledby="cookie-title" hidden><h2 id="cookie-title">Optional website analytics</h2><p>May we use Google Analytics to understand where visitors come from and which pages and contact buttons help them? It is off unless you accept. Your enquiry details are never sent to Analytics.</p><div class="cookie-actions"><button type="button" data-consent="denied">Reject analytics</button><button type="button" data-consent="granted">Accept analytics</button></div><a href="/privacy">Privacy &amp; cookie information</a></section>'
 doc=doc.replace('{COOKIE_PANEL}',cookie)
 if hero_home:doc=doc.replace('<body>','<body class="calm-page">',1)
 dest=OUT/('index.html' if path=='/' else path.lstrip('/')+'.html');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(doc)
 if not noindex:pages.append(path)

def crumb(label):return f'<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span>{esc(label)}</span></nav>'
def hero(label,h1,paragraph='',photo=None,alt='Project photograph'):
 copy=crumb(label)+f'<div class="eyebrow">Tom Cutts Joinery &amp; Building</div><h1>{h1}</h1>'+(f'<p>{paragraph}</p>' if paragraph else '')
 if photo:return '<section class="page-hero"><div class="wrap page-hero-grid"><div>'+copy+'<a class="button" href="/contact">Discuss your project ↗</a></div><figure class="service-intro-photo">'+image(photo,alt,True)+'<figcaption>From our project gallery</figcaption></figure></div></section>'
 return '<section class="page-hero"><div class="wrap">'+copy+'</div></section>'
def cta(title='Tell us what you have in mind.',text='Share a few photos, your postcode and the work you’re considering. Our team can discuss the options and arrange a free, no-obligation quotation.'):
 return f'<section class="cta-band"><div class="wrap"><div><h2>{title}</h2><p>{text}</p></div><a class="button" href="/contact">Get a free quote ↗</a></div></section>'
def faq(items):return '<section class="section wrap faq page-faq"><div><div class="eyebrow">Useful answers</div><h2>Before you begin.</h2></div><div>'+''.join('<details><summary>'+esc(i['q'])+'</summary><p>'+esc(i['a'])+'</p></details>' for i in items)+'</div></section>'
def section_from_raw(id):return re.search(r'<section\b[^>]*\bid="'+id+r'"[^>]*>.*?</section>',raw,re.S).group(0)
# The approved calmer homepage uses the existing live form names and shared tracking.
home=re.search(r'<main-template>(.*?)</main-template>',calm,re.S).group(1)
home=home.replace('{{ALL_SERVICES}}',service_tiles(image)).replace('{{COVERAGE}}',coverage_section(area_data))
render('/','Garden Rooms, Decking & Joinery in Colne | Tom Cutts','Garden rooms, decking and bespoke joinery in Colne, Clitheroe, Whalley and the Ribble Valley. 18+ years’ experience. Contact our team for a free quotation.',home,hero_home=True)
# Eight distinct service pages using the real business scope and photo evidence.
for key,d in services.items():
 label={'garden-rooms':'Garden rooms','decking':'Decking & pergolas','joinery':'Bespoke joinery','kitchens':'Kitchen fitting','extensions':'Extensions','renovations':'Renovations','commercial':'Commercial work','media-walls':'Media walls & panelling'}[key]
 photos=d.get('assets',[])
 content=hero(label,esc(d['h1']),esc(d['intro'][0]),photos[0] if photos else None,'Example of '+('joinery craftsmanship' if key in ('kitchens','commercial') else label.lower())+' from the Tom Cutts project gallery')
 body='<p>'+esc(d['intro'][1])+'</p>'
 for section in d['sections']:body+='<h2>'+esc(section['heading'])+'</h2>'+''.join('<p>'+esc(v)+'</p>' for v in section['paragraphs'])
 aside='<aside class="service-aside"><h3>Talk through your project</h3><ul>'+''.join('<li>'+esc(v)+'</li>' for v in d['bullets'])+'</ul><p>Free, no-obligation quotations. Established in 2020, backed by 18+ years’ experience.</p><a class="button" href="/contact">Enquire about '+esc(label.lower())+' ↗</a><p><a class="text-link" href="tel:07816937159">07816 937 159</a></p></aside>'
 content+='<section class="section wrap service-layout"><div class="page-content">'+body+'<p class="service-area-line">Serving Colne, Pendle, Clitheroe, Whalley, Barrow and the Ribble Valley, and towards Silsden, Sutton and Cross Hills. <a class="text-link" href="/areas-we-cover">Check our service areas ↗</a></p></div>'+aside+'</section>'
 content+='<section class="section light"><div class="wrap"><div class="eyebrow">Our workmanship</div><h2>Details from our project gallery.</h2><div class="service-photos">'+''.join('<figure><a href="/gallery">'+image(n,'Joinery and building work from our project gallery')+'</a></figure>' for n in photos[:3])+'</div>'
 if key=='kitchens':content+='<p class="photo-note">These photographs show our fitted cabinetry and interior joinery, rather than a completed kitchen installation.</p>'
 if key=='commercial':content+='<p class="photo-note">These photographs illustrate our workmanship; they are not labelled as projects for the named organisations.</p>'
 content+='</div></section>'+faq(d['faqs'])
 content+='<section class="section light"><div class="wrap"><h2>Related services.</h2><div class="related-grid">'+''.join('<article class="related-card"><h3><a href="'+services[k]['path']+'">'+esc(services[k]['h1'])+'</a></h3><p>'+esc(services[k]['description'])+'</p></article>' for k in d['related'])+'</div></div></section>'
 if key=='commercial':content+=contact.replace('homepage-enquiry','commercial-enquiry').replace('value="/"','value="/commercial"')
 else:content+=cta()
 render(d['path'],d['title'],d['description'],content,label,extra={'@type':'Service','name':label,'provider':{'@id':BASE+'/#business'},'areaServed':areas,'url':BASE+d['path']})
# Service directory.
content=hero('Services','Joinery &amp; building services.','Explore garden rooms, decking, interior joinery and wider building work for homes and commercial projects across Lancashire and the surrounding areas.')
content+='<section class="section wrap service-index">'+''.join('<a href="'+d['path']+'"><h2 style="font-size:24px">'+esc(d['title'].split('|')[0])+'</h2><p>'+esc(d['description'])+'</p></a>' for d in services.values())+'</section>'+cta()
render('/services','Joinery & Building Services in Lancashire | Tom Cutts','Explore garden rooms, decking, kitchens, bespoke joinery, extensions, renovations and commercial building services from Tom Cutts in Colne.',content,'Services')
# About retains approved experience and trust signals.
about=optimize_images(section_from_raw('about'))
values=re.search(r'<section class="section wrap"><div class="values-head[^"]*">.*?</section>',raw,re.S).group(0)
render('/about','About Tom Cutts | Joinery & Building in Lancashire','Meet Tom Cutts Joinery & Building: established in 2020, backed by 18+ years of hands-on and site management experience. Domestic and commercial work.',hero('About','Cutts Above the Rest.','Careful craftsmanship, practical building experience and a straightforward approach to your project.')+about+values+cta(),'About')
# Gallery links to focused, evidence-led photo collections.
gallery=optimize_images(section_from_raw('gallery')).replace('<h2>See the possibilities.<br>Look at the details.</h2>','<h2>Our work, inside and out.</h2>')
gallery+='<section class="section light"><div class="wrap"><h2>Take a closer look.</h2><div class="related-grid"><article class="related-card"><h3><a href="/projects/garden-rooms">Garden rooms &amp; timber construction</a></h3><p>Room exteriors, framing and cladding details.</p></article><article class="related-card"><h3><a href="/projects/decking">Decking &amp; outdoor living</a></h3><p>Steps, seating areas and connections to the garden.</p></article><article class="related-card"><h3><a href="/projects/interior-joinery">Interior joinery &amp; fitted details</a></h3><p>Cabinetry, staircases, media walls and sauna interiors.</p></article></div></div></section>'
render('/gallery','Joinery, Garden Room & Decking Gallery | Tom Cutts','See real project photographs from Tom Cutts: garden rooms, composite decking, fitted storage, staircases, media walls and building work.',hero('Gallery','See the work.<br>Look at the details.')+gallery+cta(),'Gallery')
collections=[('garden-rooms','Garden rooms & timber construction','Explore real photographs of garden buildings and the work behind the finish. These images show timber cladding, dark-framed glazing, structural framing and exterior preparation across our project collection.','garden-rooms',['wooden-clad-building-grey-doors-windows.webp','brown-composite-garden-room-office.webp','wood-frame-room-construction.webp','shed-construction-blue-membrane.webp','worker-installing-cedar-cladding.webp','wooden-shed-dark-windows-doors.webp'],['Clad garden building and glazing','Brown-clad garden room','Timber framing during construction','Exterior membrane and battens','Cladding work in progress','Exterior timber and glazing details']),('decking','Decking & outdoor living','Take a closer look at the deck layouts, steps and outdoor spaces in our project photographs. When planning a similar project, the layout, ground levels, material choice and route from the house or garden room all need consideration.','decking',['composite-decking-steps-garden.webp','white-hot-tub-composite-decking.webp','decking.jpg','pergola.jpg'],['Composite decking with broad steps','Deck with a hot tub and balustrade','Garden decking','Timber pergola']),('interior-joinery','Interior joinery & fitted details','Our interior work ranges from fitted cabinetry and wardrobes to stairs, media walls and timber-lined spaces. These photographs show the different materials, layouts and finishing details in our project collection.','joinery',['hallway-cabinet-decor.webp','hallway-staircase-oak-balustrade.webp','gallery-media-wall.jpg','gallery-wardrobes.jpg','cedar-sauna-interior-with-heater-and-window.webp','boat-cockpit-interior.webp'],['Painted hallway cabinetry','Staircase and oak balustrade','Bespoke media wall','Fitted wardrobes','Sauna interior with timber benches','Boat interior details'])]
for slug,title,intro,service,photos,captions in collections:
 content=hero(title,esc(title)+'.',esc(intro))+'<section class="section wrap"><div class="service-photos">'+''.join('<figure><a href="/assets/'+assets[n]['file']+'" target="_blank" rel="noopener">'+image(n,cap)+'</a><figcaption>'+esc(cap)+'</figcaption></figure>' for n,cap in zip(photos,captions))+'</div><div class="page-content"><h2>Planning something similar?</h2><p>Send the photos that interest you with your postcode, approximate dimensions and intended use. Our team can discuss which details might suit your home, the work involved and the next step towards a quotation.</p><p>Every site and brief is different. These photographs show our work; they are not a specification or a promise that the same layout will suit every property.</p><div class="quick-links"><a class="text-link" href="'+services[service]['path']+'">Explore '+esc(title.lower())+' services ↗</a><a class="text-link" href="/gallery">Back to the full gallery ↗</a></div></div></section>'+cta()
 render('/projects/'+slug,title+' | Tom Cutts Project Gallery',intro[:155],content,title)
# Area hub and individually written, directly usable local guides.
area_content=hero('Areas we cover','Find your area.<br>Plan your project.','Our Colne team works across Pendle, Burnley, the Ribble Valley and towards Silsden, Sutton-in-Craven and Cross Hills. Choose a local guide for services, project preparation and useful property information.')
area_content+='<section class="section wrap area-hub"><div><h2>Local to you.</h2><p>Each guide has a project checklist and direct enquiry options. These are service areas covered from Colne, not separate branch offices. For other Lancashire locations, send your postcode and outline of work so we can confirm coverage.</p><nav class="area-buttons" aria-label="All service areas">'+''.join('<a href="/areas/'+d['slug']+'">'+esc(d['name'])+'</a>' for d in area_data)+'</nav></div>'+coverage_guide()+'</section>'+cta()
render('/areas-we-cover','Joinery & Building Service Areas | Tom Cutts','Find local joinery, garden-room and decking guidance for Colne, Pendle, the Ribble Valley, Burnley, Silsden, Sutton-in-Craven and Cross Hills.',area_content,'Areas we cover')
render_areas(area_data,services,render,hero,image,contact,BASE)
render('/contact','Contact Tom Cutts | Free Joinery & Building Quote','Call 07816 937 159, WhatsApp us or request a free quote for garden rooms, decking, joinery and building work in Colne, Lancashire and nearby areas.',hero('Contact','Let’s talk about your project.','Send your postcode, a few details and any dimensions you have. You can send photographs to our team on WhatsApp.')+contact.replace('homepage-enquiry','contact-enquiry').replace('value="/"','value="/contact"'),'Contact')
privacy='''<section class="section wrap page-content privacy-content"><h2>Who handles your enquiry</h2><p>Tom Cutts Joinery &amp; Building is responsible for the personal information you send when asking about our services. Contact <a href="mailto:tcuttsjoinery@outlook.com">tcuttsjoinery@outlook.com</a> or call 07816 937 159 with a privacy question.</p><h2>Information you send us</h2><p>Our enquiry form asks for your name, email address, postcode, project type and message, with an optional phone number. We use these details to respond to your enquiry, discuss the work and prepare or manage a quotation. Please do not include sensitive personal information that is not needed for the job.</p><h2>How the website handles enquiries</h2><p>The website is hosted on Netlify. Its form service processes submitted enquiries and sends notifications to our business email inbox, provided by Microsoft Outlook. These providers handle information to deliver the hosting, form and email services. We do not sell enquiry details or add you to a marketing list through this form.</p><h2>How long information is kept</h2><p>We keep enquiry and project information for as long as it is needed to respond, carry out the work and meet record-keeping obligations. You can contact our team to ask about the information held for your enquiry or request its correction or deletion where applicable.</p><h2>Links to other services</h2><p>WhatsApp, Facebook and Google links open those services, where their own privacy policies apply. Their widgets are not embedded on this website. Review excerpts are displayed as static text and link to the original Google listing.</p>'''
if analytics.get('measurementId'):privacy+='''<h2>Optional Google Analytics</h2><p>Google Analytics loads only after you choose Accept analytics. It helps us understand page visits, service interest and use of contact links. Our published Google Business Profile and Facebook campaign links identify those sources without sending other URL query details. We measure a completed website form as an enquiry; clicking a phone or WhatsApp link does not prove that a conversation happened. We do not send your name, email address, phone numbers, postcodes or messages to Analytics.</p><p>Your choice is stored locally in your browser. You can reject analytics and still use the website and forms, or reopen Cookie settings in the footer to change your choice. Google Analytics uses its own cookies after consent; Google explains them in its <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">privacy policy</a>.</p>'''
else:privacy+='''<h2>Cookies and analytics</h2><p>This website does not currently load Google Analytics or advertising tags. The contact form and external contact links work without analytics cookies.</p>'''
privacy+='''<h2>Service-area map</h2><p>Our map uses OpenStreetMap tiles, loaded when the map comes into view. Your browser connects to OpenStreetMap to display them; we do not request your location. Town pins show service locations, not separate offices. See the <a href="https://osmfoundation.org/wiki/Privacy_Policy" target="_blank" rel="noopener">OpenStreetMap Foundation privacy policy</a>.</p><h2>Your choices</h2><p>You can ask to access or correct your personal information, ask about deletion or object to its use where applicable. Contact our team using the details above. You can also raise a concern with the <a href="https://ico.org.uk/make-a-complaint/" target="_blank" rel="noopener">Information Commissioner’s Office</a>.</p><p>Last updated 28 September 2026.</p></section>'''
render('/privacy','Privacy & Cookies | Tom Cutts Joinery & Building','How Tom Cutts Joinery & Building handles website enquiries, optional analytics and links to WhatsApp, Facebook and Google.',hero('Privacy','Privacy &amp; cookies.')+privacy,'Privacy')
render('/thank-you','Enquiry Received | Tom Cutts Joinery & Building','Your enquiry has been received by Tom Cutts Joinery & Building. Contact our team directly if you need to add any details.','<section class="wrap thanks"><div class="eyebrow">Thank you</div><h1>Your enquiry has been received.</h1><p>Our team will be in touch to discuss your project. To add photos or more information, use WhatsApp or call <a href="tel:07816937159">07816 937 159</a>.</p><a class="button" href="/">Back to the homepage ↗</a></section>','Thank you',True)
render('/404','Page Not Found | Tom Cutts Joinery & Building','Find the right page for Tom Cutts garden rooms, decking, joinery and building services.','<section class="section wrap error-main"><div class="eyebrow">Page not found</div><h1>Let’s get you to the right place.</h1><p style="margin:24px 0">This page may have moved. Explore our services or contact our team about your project.</p><div class="quick-links"><a class="button" href="/services">Our services ↗</a><a class="text-link" href="/contact">Contact our team ↗</a></div></section>','Page not found',True)
# Buyer guides answer distinct planning questions without expanding the homepage.
guide_cards=''
for d in guides:
 path='/guides/'+d['slug']
 guide_cards+='<article class="related-card guide-card">'+image(d['photo'],d['photoAlt']).replace('<img ','<img class="guide-card-image" ',1)+'<h2><a href="'+path+'">'+esc(d['heading'])+'</a></h2><p>'+esc(d['summary'])+'</p><a class="text-link" href="'+path+'">Read the guide ↗</a></article>'
 aside='<aside class="service-aside guide-aside"><h3>Plan your project</h3><a href="'+services[d['service']]['path']+'">Explore the service ↗</a><a href="/projects/'+d['service']+'">View project photographs ↗</a>'+''.join('<a href="/guides/'+g['slug']+'">'+esc(g['heading'])+'</a>' for g in guides if g['slug']!=d['slug'])+'<a class="button" href="/contact">Ask our team for a quotation ↗</a></aside>'
 content=hero('Project guide',esc(d['heading']),esc(d['summary']),d['photo'],d['photoAlt'])+'<section class="section wrap service-layout"><article class="page-content"><p class="guide-date">Published 28 September 2026 · Tom Cutts Joinery &amp; Building</p>'+d['body']+'</article>'+aside+'</section>'+cta('Ready to discuss your outdoor space?')
 render(path,d['title'],d['description'],content,d['heading'])
render('/guides','Garden Room & Decking Planning Guides | Tom Cutts','Practical guides to garden-room costs, timber versus composite decking and comparing quotations. Plan your outdoor project with Tom Cutts in Lancashire.',hero('Project guides','Plan with a clearer picture.','Useful questions and practical information to help you choose materials, compare quotations and make a start.')+'<section class="section wrap"><div class="related-grid">'+guide_cards+'</div></section>'+cta(),'Project guides')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+BASE+'/sitemap.xml\n')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('<url><loc>'+BASE+path+'</loc><lastmod>'+('2026-10-05' if path in ('/','/services','/services-media-walls','/areas-we-cover') or path.startswith('/areas/') else '2026-09-28')+'</lastmod></url>\n' for path in pages)+'</urlset>\n')
redirects=['/index.html / 301!','/index / 301!','/menu.html /services 301!','/menu /services 301!','/_recovered-live-site/index.html / 301!','/_recovered-live-site/ / 301!','/review https://g.page/r/CWTtpNavvoM0EBM/review 302!']
for path in pages+['/thank-you']:
 if path!='/':redirects.append(path+'.html '+path+' 301!')
(OUT/'_redirects').write_text('\n'.join(redirects)+'\n')
(OUT/'_headers').write_text('''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
/assets/*
  Cache-Control: public, max-age=604800
/fonts/*
  Cache-Control: public, max-age=31536000, immutable
/thank-you
  X-Robots-Tag: noindex, follow
/404.html
  X-Robots-Tag: noindex, follow
/review
  X-Robots-Tag: noindex, follow
''')
print('Built',len(pages),'indexable pages; 2 utility pages. GA4:',analytics.get('measurementId') or 'not configured')
