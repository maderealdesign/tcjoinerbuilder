"""Browsable local guides and service navigation for the calm homepage."""
from html import escape
import re

def coverage_guide():
    return '<figure class="coverage-map-card"><div class="coverage-map" id="coverage-map" role="region" aria-label="Map of our joinery and building service areas"><p class="map-fallback">Explore our service areas on the map, or choose a location from the buttons.</p></div><figcaption><span class="map-legend-dot" aria-hidden="true"></span>Serving Lancashire &amp; the Ribble Valley, across to Airedale.<small>Pins show the towns we serve, not branch offices. Select a pin to explore.</small></figcaption></figure>'

def coverage_section(areas):
    buttons=''.join(f'<a href="/areas/{d["slug"]}">{escape(d["name"])}</a>' for d in areas)
    return '<section class="coverage" id="coverage"><div class="wrap coverage-grid"><div><div class="eyebrow">Where we work</div><h2>Local to you.</h2><p>Based in Colne, working across Lancashire, the Ribble Valley and towards Silsden, Sutton-in-Craven and Cross Hills. Choose your area for project guidance and local information.</p><nav class="area-buttons" aria-label="Find your service area">'+buttons+'</nav><a class="text-link" href="/areas-we-cover">See our full coverage guide <span aria-hidden="true">↗</span></a></div>'+coverage_guide()+'</div></section>'

def service_tiles(image):
    entries=[('Bespoke joinery','/services-joinery','gallery-wardrobes.jpg'),('Media walls & panelling','/services-media-walls','gallery-media-wall.jpg'),('Kitchen fitting','/services-kitchens','kitchen-inspiration.webp'),('Extensions & conversions','/services-extensions','gallery-extension.jpg'),('Home renovations','/services-renovations','hallway-staircase-oak-balustrade.webp'),('Commercial work','/commercial','worker-installing-cedar-cladding.webp')]
    tiles=[]
    arrow='<span class="tile-arrow" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M6 18 18 6M6 6h12v12"/></svg></span>'
    for name,url,photo in entries:
        note='<span class="photo-label">Inspiration photo</span>' if photo=='kitchen-inspiration.webp' else ''
        tiles.append(f'<a class="service-tile" href="{url}">'+image(photo,'')+arrow+note+'<h4>'+escape(name)+'</h4></a>')
    return '<div class="all-services"><h3>More for your home &amp; business.</h3><div class="service-tiles">'+''.join(tiles)+'</div></div>'

def render_areas(area_data,services,render,hero,image,contact,base):
    lookup={d['slug']:d for d in area_data}
    for d in area_data:
        path='/areas/'+d['slug'];name=d['name']
        description=d['description']
        content=hero(name,'Joinery &amp; building in<br>'+escape(name)+'.',escape(d['intro']))
        content=content.replace('<a href="/">Home</a>','<a href="/">Home</a><span aria-hidden="true">/</span><a href="/areas-we-cover">Areas we cover</a>',1)
        body=''.join('<h2>'+escape(s['heading'])+'</h2><p>'+escape(s['text'])+'</p>' for s in d['sections'])
        body+='<h2>Your project checklist</h2><ul>'+''.join('<li>'+escape(t)+'</li>' for t in d['brief'])+'</ul>'
        resource=d['resource']
        body+='<div class="local-resource"><h3>Useful local information</h3><p>'+escape(resource['note'])+'</p><a class="text-link" href="'+escape(resource['url'],quote=True)+'" target="_blank" rel="noopener">'+escape(resource['label'])+' ↗</a><p class="small-note">Confirm any permissions and specialist requirements for your property before work starts.</p></div>'
        photo='<figure>'+image(d['photo'],'Joinery and building workmanship from the Tom Cutts project gallery')+'<figcaption>Our workmanship · photographs from the wider project gallery</figcaption></figure>'
        aside='<aside class="service-aside"><h3>Discuss your '+escape(name)+' project</h3><p>Our joinery and building team works from Colne. Share your postcode and plans to confirm the scope and arrange the next step.</p><a class="button" href="#contact">Request a quotation ↗</a><a class="text-link" href="tel:07816937159">Call 07816 937 159</a><a class="text-link" href="https://wa.me/447816937159" target="_blank" rel="noopener">Send photos on WhatsApp ↗</a><p>18+ years’ experience · Up to £5m public liability cover</p></aside>'
        # Link to relevant evidence and planning help without claiming these jobs were in this town.
        primary=d['focus'][0]
        collection={'garden-rooms':'garden-rooms','decking':'decking','joinery':'interior-joinery','media-walls':'interior-joinery','renovations':'interior-joinery','kitchens':'interior-joinery'}.get(primary)
        evidence='/projects/'+collection if collection else '/gallery'
        evidence_label={'garden-rooms':'garden-room construction photographs','decking':'decking and outdoor project photographs','interior-joinery':'fitted joinery and interior photographs'}.get(collection,'our wider project gallery')
        body+='<aside class="context-links"><h2>Ideas for your '+escape(name)+' project</h2><p>Explore <a href="'+evidence+'">'+evidence_label+'</a> to choose the details you would like to discuss.</p>'
        if 'decking' in d['focus']:body+='<p>Considering an outdoor space? Our <a href="/guides/timber-or-composite-decking">timber and composite decking guide</a> explains the material and maintenance questions to compare.</p>'
        elif 'garden-rooms' in d['focus']:body+='<p>Planning a room outside? Read <a href="/guides/garden-room-costs">what affects a garden-room quotation</a> before deciding on size and specification.</p>'
        else:body+='<p>For a wider brief, see <a href="/services">all our joinery and building services</a> and tell us which jobs need to be coordinated.</p>'
        body+='</aside>'
        content+='<section class="section wrap service-layout area-content"><article class="page-content">'+body+photo+'</article>'+aside+'</section>'
        content+='<section class="section light"><div class="wrap"><h2>Explore the work you’re planning.</h2><div class="related-grid">'+''.join('<article class="related-card"><h3><a href="'+services[k]['path']+'">'+escape(services[k]['title'].split('|')[0].strip())+'</a></h3><p>'+escape(services[k]['description'])+'</p></article>' for k in d['focus'])+'</div><h3 style="margin-top:30px">Nearby service areas</h3><nav class="area-buttons" aria-label="Nearby areas">'+''.join('<a href="/areas/'+n+'">'+escape(lookup[n]['name'])+'</a>' for n in d['nearby'])+'</nav></div></section>'
        content+=contact.replace('homepage-enquiry','contact-enquiry').replace('value="/"','value="'+path+'"')
        render(path,d['title'],description,content,name,extra={'@type':'Service','name':'Joinery and building in '+name,'provider':{'@id':base+'/#business'},'areaServed':{'@type':'Place','name':name},'url':base+path})
