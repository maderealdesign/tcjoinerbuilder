# Tom Cutts Joinery & Building

Live website: https://tcjoinerbuilder.co.uk

## Edit and build

- `src/site-chrome.html` and `src/site-chrome.css`: the shared header, footer, navigation and typography used on every page.
- `src/calm-homepage.html` and `src/calm-homepage.css`: approved calm homepage body, live enquiry form and brand styles.
- `src/homepage.html` and `src/homepage-compact.css`: shared supporting-page styles and source sections for About and Gallery.
- `src/services.json`: eight service pages.
- `src/areas.json`: eleven individually written service-area guides.
- `src/coverage-map.js`, `src/coverage-map.css` and `src/map-points.json`: lazy-loaded Leaflet map with cached OpenStreetMap town-centre coordinates, never branch addresses. Library/licence in `public/vendor/leaflet/`; visible tile attribution must remain. See https://operations.osmfoundation.org/policies/tiles/ and https://operations.osmfoundation.org/policies/nominatim/ (one-time geocoding only, no visitor address lookup).
- `scripts/local_pages.py`: area pages, coverage navigation and homepage service photo cards.
- `src/guides.json`: three researched buyer guides and the guide index.
- `scripts/build.py`: static page templates, navigation, forms, metadata, sitemap and redirects.
- `src/site.js`: menu, forms, consent choices and enquiry tracking.
- `src/analytics.json`: GA4 public measurement/property IDs.
- `public/assets/` and `public/fonts/`: prepared, optimized assets. These must stay in Git; the build does not regenerate image variants.
- `public/`: generated website. Older root HTML and images are recovery material and are not published.

Run with Python 3.9 or later (no third-party packages):

```sh
python3 scripts/build.py
python3 scripts/check_site.py
```

## Publishing

Canonical client source folder:
`/Users/dom/Library/CloudStorage/OneDrive-Personal/madereal/Madereal 2026/Websites/tcjoinery`

Production flow: canonical local source → GitHub `maderealdesign/tcjoinerbuilder` main → Netlify `tcjoinery` → live domain. Netlify runs the build and publishes `public/`. Do not deploy a production copy manually without an explicit emergency request. Draft deploys are permitted for review.

Netlify site ID: `3c0c8eef-6c7a-4803-a362-95fa85ba3057`.

## Enquiries and measurement

The three Netlify forms are `homepage-enquiry`, `contact-enquiry` and `commercial-enquiry`. The site-wide submission notification sends to `tcuttsjoinery@outlook.com`. Verify the enabled notification in Netlify; do not put credentials in this repo.

GA4 property `556305475`, stream `15861578304`, measurement ID `G-D26ZBMHC24`, in the existing Madreal websites account. Analytics loads only on the production domain after consent. `generate_lead` fires after a successful form POST and is a key event; `contact_click` records a contact-link click, not a completed conversation. Visitor form values never enter Analytics. Explicit known Google Business Profile and Facebook campaign tags are passed as safe fixed campaign values after consent; other URL query values are excluded. Google Ads click attribution and imported conversions are not yet configured or verified. Enhanced automatic form-interaction measurement is off. Cookie choices can be changed in the footer.

Search Console has the verified domain property. Submit `/sitemap.xml` after a release that adds indexable pages. Do not invent ratings, project locations, client claims or physical offices. The hero is labelled as illustrative; project photographs are actual supplied work. Google review excerpts are a dated static snapshot.

## Recovery

Pre-launch production deploy: `6ab56547d360cc1161a23c14` (24 September 2026). Netlify retains deployment rollback; preserve the matching Git history and canonical source when rolling back. No hosting, mailbox or Google credentials are stored here.

Review-request short link: `/review` redirects to the official Google Business Profile review form. The printable review kit and operational enquiry tracker are private working artifacts, not in the published directory.

Navigation checks enforce one header/footer, unique titles/descriptions, all 33 indexable pages reachable within two clicks, sitemap completeness and Googlebot access. Service, location, guide and gallery pages cross-link through relevant project context. The production Netlify alias redirects to the custom domain.
