#!/usr/bin/env python3
"""Check publish output, canonical URLs, internal links and form configuration."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent.parent/'public';BASE='https://tcjoinerbuilder.co.uk';issues=[];pages={}
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.h1=0;self.canonical=[];self.description=[];self.robots='';self.title='';self.in_title=False;self.in_json=False;self.json='';self.schemas=[];self.forms=[];self.form=None
 def handle_starttag(self,t,attrs):
  d=dict(attrs)
  if d.get('id'):self.ids.append(d['id'])
  if t=='h1':self.h1+=1
  if t=='title':self.in_title=True
  if t=='meta' and d.get('name')=='robots':self.robots=d.get('content','')
  if t=='meta' and d.get('name')=='description':self.description.append(d.get('content',''))
  if t=='link' and d.get('rel')=='canonical':self.canonical.append(d.get('href'))
  if t in ['a','link','script','img']:
   if t=='a' and d.get('href'):self.links.append(d['href'])
   if t in ['img','script'] and d.get('src'):self.links.append(d['src'])
   if t=='link' and d.get('rel') in ['stylesheet','icon','preload']:self.links.append(d.get('href',''))
  if t=='img' and ('alt' not in d or not all(d.get(k) for k in ['width','height'])):issues.append(self.path+': image lacks alt/dimensions')
  if t=='script' and d.get('type')=='application/ld+json':self.in_json=True;self.json=''
  if t=='form':self.form={'attrs':d,'fields':{}};self.forms.append(self.form)
  if self.form and t in ['input','select','textarea'] and d.get('name'):self.form['fields'][d['name']]=d
 def handle_endtag(self,t):
  if t=='title':self.in_title=False
  if t=='form':self.form=None
  if t=='script' and self.in_json:
   try:self.schemas.append(json.loads(self.json))
   except Exception as e:issues.append(self.path+': invalid JSON-LD '+str(e))
   self.in_json=False
 def handle_data(self,data):
  if self.in_title:self.title+=data
  if self.in_json:self.json+=data
for f in ROOT.rglob('*.html'):
 rel=str(f.relative_to(ROOT));url='/' if rel=='index.html' else '/'+rel[:-5];p=Page();p.path=url;p.feed(f.read_text());pages[url]=p
 if p.h1!=1:issues.append(url+': expected one H1')
 if len(p.ids)!=len(set(p.ids)):issues.append(url+': duplicate IDs')
 if p.canonical!=[BASE+url]:issues.append(url+': wrong canonical')
 if len(p.description)!=1 or not p.description[0]:issues.append(url+': missing description')
 if not p.schemas:issues.append(url+': missing structured data')
 if 'preview' in p.title.lower():issues.append(url+': preview title')
 if url not in ['/404','/thank-you'] and 'noindex' in p.robots:issues.append(url+': accidentally noindex')
 for form in p.forms:
  a=form['attrs'];fields=form['fields']
  if a.get('method')!='POST' or a.get('data-netlify')!='true' or a.get('action')!='/thank-you':issues.append(url+': wrong live form')
  if a.get('netlify-honeypot')!='bot-field' or fields.get('form-name',{}).get('value')!=a.get('name'):issues.append(url+': invalid form identity/honeypot')
  if not all(k in fields for k in ['name','email','message','page','bot-field']):issues.append(url+': missing form fields')
for url,p in pages.items():
 for link in p.links:
  u=urlsplit(link)
  if u.scheme and u.netloc not in ['tcjoinerbuilder.co.uk','www.tcjoinerbuilder.co.uk']:continue
  path=unquote(u.path) or url
  if not path.startswith('/'):issues.append(url+': relative link '+link);continue
  target=pages.get(path)
  if target:
   if u.fragment and unquote(u.fragment) not in target.ids:issues.append(url+': missing anchor '+link)
  elif not (ROOT/path.lstrip('/')).is_file():issues.append(url+': broken local link '+link)
urls=[n.text for n in ET.parse(ROOT/'sitemap.xml').getroot().findall('{*}url/{*}loc')]
for u in urls:
 path=u.removeprefix(BASE)
 if path not in pages or 'noindex' in pages[path].robots:issues.append('Invalid sitemap entry '+u)
if len({p.title for p in pages.values()})!=len(pages):issues.append('Duplicate page titles')
if 'Disallow: /\n' in (ROOT/'robots.txt').read_text():issues.append('Robots blocks production')
if 'noindex, nofollow' in (ROOT/'_headers').read_text():issues.append('Global preview header')
# New local guides must be discoverable and have a direct, attributable enquiry route.
area_data=json.loads((ROOT.parent/'src/areas.json').read_text())
if len({d['intro'] for d in area_data})!=len(area_data):issues.append('Duplicate area introductions')
for d in area_data:
 path='/areas/'+d['slug']
 for entry in ['/', '/areas-we-cover']:
  if path not in pages[entry].links:issues.append(entry+': missing area link '+path)
 if BASE+path not in urls:issues.append('Area missing from sitemap: '+path)
 if not any(f['attrs'].get('name')=='contact-enquiry' and f['fields'].get('page',{}).get('value')==path for f in pages[path].forms):issues.append(path+': missing local enquiry form')
for service in json.loads((ROOT.parent/'src/services.json').read_text()).values():
 if service['path'] not in pages['/'].links:issues.append('Homepage missing service: '+service['path'])
for issue in issues:print('FAIL',issue)
if issues:raise SystemExit(1)
print(f'PASS: {len(pages)} HTML pages, {len(urls)} sitemap URLs, local links, metadata, JSON-LD, images and live forms.')
