"""Keep homepage summaries short while retaining the full source for detail pages."""
import re


def compact_homepage(home, image):
    def replace(old, new):
        nonlocal home
        if home.count(old) != 1:
            raise ValueError('Homepage source changed: ' + old[:80])
        home = home.replace(old, new, 1)

    replacements = {
        'Bespoke garden rooms and decking, backed by 18+ years of joinery and building experience. Make space to work, unwind and enjoy more of life at home.': 'Bespoke garden rooms and decking, built on 18+ years of joinery and building experience.',
        'Your local joiner and builder.<br>More potential for your home.': 'Your local joiner<br>&amp; builder.',
        '<p>Based in Colne, we build garden rooms, decking and bespoke joinery across Pendle, the Ribble Valley and towards Silsden, Sutton and Cross Hills.</p><p>From fitted storage and kitchens to extensions and commercial work, bring us your ideas. We’ll help you make more of your space.</p>': '<p>Garden rooms, decking and home improvements from our Colne team, serving Lancashire and the Ribble Valley.</p>',
        'Bespoke garden rooms in Colne &amp; the Ribble Valley.': 'Garden rooms.<br>Space of your own.',
        'Space to work, train, create or switch off. We plan your garden room around how you’ll use it, from the layout and light to insulation, ventilation and power.': 'A garden office, gym or retreat, planned around your space and how you’ll use it.',
        '<ul><li>Garden offices and a quieter place to work</li><li>Home gyms, hobby rooms and creative studios</li><li>Spaces for relaxing, entertaining and everyday use</li><li>Decking and outdoor joinery planned alongside the room</li></ul>': '<ul><li>Offices, gyms &amp; hobby rooms</li><li>Layout, insulation &amp; power considered</li><li>Decking planned alongside your room</li></ul>',
        '<p class="small-note">Send your ideas and a few photos. We’ll discuss the site, preparation and any permissions or specialist work to check.</p>': '',
        'Garden decking, pergolas &amp; outdoor joinery.': 'Decking &amp; pergolas.<br>More life outdoors.',
        '<p>Make room for outdoor dining, quiet mornings and evenings with friends. We build decking and pergolas to connect your home, garden and garden room.</p><p>We’ll help you compare timber and composite finishes, with the layout, groundwork and maintenance considered from the start.</p>': '<p>Timber or composite decking, with steps, seating and pergolas shaped around your garden.</p>',
        '<ul><li>Decking for seating, dining and garden-room entrances</li><li>Timber pergolas and outdoor structures</li><li>Steps, edges and transitions that suit your layout</li><li>A choice of finishes discussed around your budget</li></ul>': '<ul><li>Timber &amp; composite options</li><li>Layouts for dining &amp; relaxing</li><li>Groundwork &amp; maintenance considered</li></ul>',
        'See the possibilities.<br>Look at the details.': 'Our work, inside &amp; out.',
        'Real garden rooms, decking and interiors from our project gallery. Take a closer look.': 'Real projects. Take a closer look.',
        'Our project photos show the details that sit behind the completed space, from timber framing and exterior preparation to cladding and glazing.': 'Framing, cladding and glazing: the details behind the finish.',
        'Joinery &amp; building services for the whole home.': 'More for your home.',
        'One room or a wider renovation, we bring the same attention to the practical details. Explore our domestic and commercial services, then tell us what you have in mind.': 'Joinery, fitting &amp; building work.',
        'Fitted wardrobes, alcove storage, staircases and finishing joinery, made to work with your home.': 'Fitted storage, wardrobes, staircases and finishing details.',
        'Media walls, fitted shelving and decorative panelling that bring a room together.': 'Media walls, shelving and decorative wall panelling.',
        'Kitchen installation, cabinetry, worktops and the finishing details, with associated trades coordinated where needed.': 'Kitchen installation, worktops and finishing joinery.',
        'Home extensions and garage conversions, with the scope, structural requirements and project management planned from the start.': 'Home extensions, garage conversions and project management.',
        'Single-room improvements and wider refurbishments, bringing building alterations and interior joinery together.': 'Room improvements, building alterations and wider refurbishments.',
        'Fit-outs, new-build work, restoration and site management for developers, housing providers and commercial clients.': 'Fit-outs, restoration, new builds and site management.',
        'Established in 2020.<br>Backed by 18+ years of experience.': 'Experience you<br>can build on.',
        '<p>Founded by Tom Cutts in 2020, our team brings 18+ years of hands-on construction and site management experience to homes and commercial projects.</p><p>From bespoke joinery to heritage restoration, we combine careful finishing with the practical experience to manage a bigger build.</p><p>Expect clear communication, respect for your property and an honest quotation.</p>': '<p>Tom has <strong>18+ years of joinery and building experience.</strong> He founded Tom Cutts Joinery &amp; Building in <strong>2020.</strong></p><p>Today, the team handles domestic and commercial projects with the same care for the details.</p><a class="text-link" href="/about">Meet Tom &amp; the team ↗</a>',
        '<p>From a small domestic job to a major commercial build, the principles behind our work stay the same.</p>': '',
        'Our experience extends to local authorities, housing associations and private developers, including work with Bury Council and Muir Housing. Tom’s background includes care-home builds and heritage restoration projects valued at over £1 million.': 'Work with Bury Council and Muir Housing, plus Tom’s experience on care-home builds and heritage restoration projects valued at over £1 million.',
        'From the Ribble Valley to Silsden &amp; Cross Hills.': 'Local to you.',
        'Based in Colne, working across the Ribble Valley, Lancashire and towards Silsden, Sutton and Cross Hills. Send your postcode so we can confirm coverage.': 'Based in Colne, covering Lancashire, the Ribble Valley and towards Silsden, Sutton and Cross Hills. Send your postcode to check.',
        'Share your ideas, photos, location and rough budget. We’ll discuss the space and arrange a visit where needed.': 'Send your ideas, photos, postcode and rough budget.',
        'We work through the materials, preparation, scope and timing, then provide a clear quotation for the agreed job.': 'Agree the scope, materials and timing, with a clear quotation.',
        'We keep you informed as the job progresses and walk through the finished work with you at handover.': 'We keep you updated through the build and handover.',
        'Planning a garden room, weighing up decking or thinking about work inside the house? These are a few useful starting points.': 'Useful answers before you start.',
        'A garden room, new decking or a bigger change at home — tell us what you’re planning. We’re here to help you understand the options and take the next step.': 'Tell us what you’re planning. Send your postcode, a few photos and your ideas.',
    }
    for old, new in replacements.items():
        replace(old, new)

    # Each outdoor service gets its own visual section, rather than one long block.
    replace('<section class="section light"><div class="wrap">\n<article class="feature" id="garden-rooms">', '<section class="section light feature-section" id="garden-rooms"><div class="wrap feature">')
    replace('</div></article>\n<article class="feature reverse" id="decking">', '</div></div></section>\n<section class="section feature-section" id="decking"><div class="wrap feature reverse">')
    replace('</div></article>\n<div class="together photo-panel">', '</div></div></section>\n<section class="section light together-section"><div class="wrap"><div class="together photo-panel">')
    replace('<div class="commercial" id="commercial">', '</section><section class="section light commercial-section" id="commercial"><div class="wrap commercial">')

    # All work remains available in a native, keyboard-accessible photo strip.
    replace('<div class="gallery">', '<p class="gallery-hint" id="gallery-hint">Scroll sideways to explore · select a photo to enlarge</p><div class="gallery" tabindex="0" role="region" aria-label="Project photographs" aria-describedby="gallery-hint">')
    gallery = re.search(r'<section[^>]*id="gallery".*?</section>', home, re.S).group(0)
    shorter = re.sub(r'(<figcaption><h3>.*?</h3>)<p>.*?</p>', r'\1', gallery)
    replace(gallery, shorter)

    # Service photos decorate the links; the stock kitchen image is clearly labelled.
    service_photos = {
        'Bespoke joinery': ('gallery-wardrobes.jpg', 'joinery'),
        'Media walls &amp; panelling': ('gallery-media-wall.jpg', 'media-walls'),
        'Kitchen fitting': ('kitchen-inspiration.webp', 'kitchens'),
        'Extensions & conversions': ('gallery-extension.jpg', 'extensions'),
        'Home renovations': ('hallway-staircase-oak-balustrade.webp', 'renovations'),
        'Commercial work': ('worker-installing-cedar-cladding.webp', 'commercial'),
    }
    def service_card(match):
        card = match.group(0)
        title = re.search(r'<h3>(.*?)</h3>', card, re.S).group(1)
        title = {'Bespoke joinery & fitted storage': 'Bespoke joinery', 'Media walls & wall panelling': 'Media walls &amp; panelling', 'Commercial joinery & site work': 'Commercial work'}.get(title, title)
        href = re.search(r'<a class="text-link" href="([^"]+)"', card).group(1)
        photo, key = service_photos[title]
        backdrop = image(photo, '').replace('<img ', '<img class="service-card-photo" ', 1)
        arrow = '<span class="service-card-arrow" aria-hidden="true"><svg viewBox="0 0 24 24" focusable="false"><path d="M6 18 18 6M6 6h12v12"/></svg></span>'
        note = '<span class="service-photo-note">Inspiration photo</span>' if key == 'kitchens' else ''
        return f'<a class="service-card service-photo-tile tile-{key}" href="{href}">{backdrop}{arrow}{note}<h3>{title}</h3></a>'
    home = re.sub(r'<article class="service-card">.*?</article>', service_card, home, flags=re.S)
    replace('<div class="review-grid">', '<div class="review-grid" tabindex="0" role="region" aria-label="Customer reviews — scroll sideways on a phone to read more">')

    # Give coverage, the enquiry process and customer reviews separate purposes.
    local = re.search(r'<section class="section light"><div class="wrap local-grid">.*?</section>', home, re.S).group(0)
    replace(local, '''<section class="section coverage-section" id="coverage"><div class="wrap coverage-grid"><div><div class="eyebrow">Where we work</div><h2>Local to you.</h2></div><div><p>Based in Colne, serving Lancashire and the Ribble Valley, and towards Silsden, Sutton and Cross Hills.</p><a class="text-link" href="/areas-we-cover">See all areas we cover ↗</a></div></div></section>
<section class="section process-section" id="how-it-works"><div class="wrap"><div class="process-heading"><div class="eyebrow">A straightforward start</div><h2>Your project, in three steps.</h2></div><ol class="project-steps"><li><span aria-hidden="true">01</span><div><h3>Share your idea</h3><p>Send photos, your postcode and a rough budget.</p></div></li><li><span aria-hidden="true">02</span><div><h3>Agree your quote</h3><p>We agree the work, materials and timing.</p></div></li><li><span aria-hidden="true">03</span><div><h3>Build &amp; hand over</h3><p>We keep you updated through to the finish.</p></div></li></ol></div></section>''')
    replace('A reputation built<br>on the work.', 'Trusted by<br>our customers.')
    reviews = re.search(r'<section class="section light reviews".*?</section>', home, re.S).group(0)
    google_mark = '<svg class="google-mark" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="#4285F4" d="M21.6 12.23c0-.71-.06-1.39-.18-2.05H12v3.88h5.38a4.6 4.6 0 0 1-2 3.02v2.51h3.24c1.89-1.74 2.98-4.3 2.98-7.36Z"/><path fill="#34A853" d="M12 22c2.7 0 4.96-.9 6.62-2.41l-3.24-2.51c-.9.6-2.05.96-3.38.96-2.6 0-4.81-1.76-5.6-4.12H3.06v2.59A10 10 0 0 0 12 22Z"/><path fill="#FBBC05" d="M6.4 13.92a6 6 0 0 1 0-3.84V7.49H3.06a10 10 0 0 0 0 9.02l3.34-2.59Z"/><path fill="#EA4335" d="M12 5.96c1.47 0 2.79.5 3.82 1.49l2.87-2.87A9.6 9.6 0 0 0 12 2a10 10 0 0 0-8.94 5.49l3.34 2.59C7.19 7.72 9.4 5.96 12 5.96Z"/></svg>'
    def google_review(match):
        card = match.group(0)
        author = re.search(r'<figcaption><strong>(.*?)</strong>', card).group(1)
        quote = re.search(r'<blockquote>.*?</blockquote>', card, re.S).group(0)
        link = re.search(r'<figcaption>.*?(<a .*?</a>)</figcaption>', card, re.S).group(1)
        initials, tone = {'Nick': ('N', 'teal'), 'Emily J': ('E', 'purple'), 'Thomas Eastwood': ('T', 'blue')}[author]
        return f'<figure class="review-card google-review-card"><figcaption class="google-review-person"><span class="review-avatar avatar-{tone}" aria-hidden="true">{initials}</span><span class="review-author"><strong>{author}</strong><span>Google review</span></span>{google_mark}</figcaption><div class="stars" aria-label="5 out of 5 stars">★★★★★</div>{quote}<div class="google-review-link">{link}</div></figure>'
    reviews_simple = re.sub(r'<figure class="review-card">.*?</figure>', google_review, reviews, flags=re.S)
    reviews_simple = reviews_simple.replace('<strong>5.0<span>', '<span class="google-review-brand">' + google_mark + 'Google reviews</span><strong>5.0<span>', 1)
    replace(reviews, reviews_simple)

    # A real work photograph, not an implied portrait of Tom or a decorative strip.
    about = re.search(r'<section class="section about".*?</section>', home, re.S).group(0)
    about_simple = about.replace('Craftsmanship in the details · The work behind the finish', 'Our team at work · timber cladding')
    about_simple = re.sub(r'<div class="signature">.*?</div>', '', about_simple)
    replace(about, about_simple)

    # Four useful starting questions; the service pages retain the fuller answers.
    faq = re.search(r'<section[^>]*id="questions".*?</section>', home, re.S).group(0)
    items = re.findall(r'<details>.*?</details>', faq, re.S)
    for index in (2, 3, 5, 7):
        faq = faq.replace(items[index], '')
    home = re.sub(r'<section[^>]*id="questions".*?</section>', lambda _: faq, home, count=1, flags=re.S)

    # Keep the real form and all fields, with contact details sharing a row.
    home = re.sub(r'(<label for="email"[^>]*>.*?</label>)(<label for="phone">.*?</label>)', r'<div class="form-row">\1\2</div>', home, count=1, flags=re.S)
    # Titles stay readable without JavaScript; motion is progressive enhancement.
    home = home.replace('<h2>', '<h2 class="section-title">')
    replace('<h3>The room. The deck. The whole idea.</h3>', '<h3 class="section-title">The room. The deck. The whole idea.</h3>')
    return home
