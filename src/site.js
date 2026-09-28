'use strict';
const analyticsId = '__GA_MEASUREMENT_ID__';
const production = location.hostname === 'tcjoinerbuilder.co.uk' || location.hostname === 'www.tcjoinerbuilder.co.uk';
const consentKey = 'tc-analytics-consent-v1';
let consent = 'denied';
try { consent = localStorage.getItem(consentKey) || 'unset'; } catch (_) {}
let analyticsLoaded = false;
function loadAnalytics() {
  if (!production || !/^G-[A-Z0-9]+$/.test(analyticsId) || consent !== 'granted' || analyticsLoaded) return;
  analyticsLoaded = true;
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag('consent', 'default', { analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' });
  window.gtag('js', new Date());
  let referrer = '';
  try { const u = new URL(document.referrer); referrer = u.origin + u.pathname; } catch (_) {}
  window.gtag('config', analyticsId, { page_location: location.origin + location.pathname, page_referrer: referrer, allow_google_signals: false, allow_ad_personalization_signals: false });
  const tag = document.createElement('script'); tag.async = true; tag.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(analyticsId); document.head.appendChild(tag);
}
function track(name, details) { if (production && consent === 'granted' && typeof window.gtag === 'function') window.gtag('event', name, details); }
const panel = document.getElementById('cookie-panel');
if (panel && consent === 'unset') panel.hidden = false;
loadAnalytics();
document.querySelectorAll('[data-cookie-settings]').forEach(button => button.addEventListener('click', () => { if (panel) { panel.hidden = false; panel.querySelector('button').focus(); } }));
document.querySelectorAll('[data-consent]').forEach(button => button.addEventListener('click', () => {
  const previous = consent; consent = button.dataset.consent;
  try { localStorage.setItem(consentKey, consent); } catch (_) {}
  if (panel) panel.hidden = true;
  if (consent === 'granted') loadAnalytics();
  else {
    if (typeof window.gtag === 'function') window.gtag('consent', 'update', {analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});
    document.cookie.split(';').forEach(item => {
      const name = item.split('=')[0].trim(); if (!/^_ga(?:_|$)/.test(name)) return;
      ['','.tcjoinerbuilder.co.uk','tcjoinerbuilder.co.uk',location.hostname].forEach(domain => { document.cookie = name + '=; Max-Age=0; path=/' + (domain ? '; domain=' + domain : '') + '; SameSite=Lax'; });
    });
    // Reload removes the already loaded analytics library after consent is withdrawn.
    if (previous === 'granted' && analyticsLoaded) location.reload();
  }
}));
const menu = document.querySelector('.menu-toggle'); const navigation = document.getElementById('navigation');
if (menu && navigation) {
  menu.addEventListener('click', () => { const open = menu.getAttribute('aria-expanded') !== 'true'; menu.setAttribute('aria-expanded', String(open)); navigation.classList.toggle('open', open); });
  navigation.addEventListener('click', e => { if (e.target.closest('a')) { menu.setAttribute('aria-expanded', 'false'); navigation.classList.remove('open'); } });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') { menu.setAttribute('aria-expanded','false'); navigation.classList.remove('open'); menu.focus(); } });
  navigation.querySelectorAll('a').forEach(a => { if (new URL(a.href).pathname === location.pathname && !new URL(a.href).hash) a.setAttribute('aria-current','page'); });
}
document.addEventListener('click', e => {
  const link = e.target.closest('a'); if (!link) return;
  const href = link.getAttribute('href') || '';
  const method = href.startsWith('tel:') ? 'phone' : href.startsWith('https://wa.me/') ? 'whatsapp' : href.startsWith('mailto:') ? 'email' : null;
  if (method) track('contact_click', { contact_method: method, page_path: location.pathname });
});
document.querySelectorAll('form[data-netlify],form[name$="-enquiry"]').forEach(form => {
  const page = form.querySelector('input[name="page"]'); if (page) page.value = location.pathname;
  form.addEventListener('submit', async event => {
    event.preventDefault(); if (!form.reportValidity()) return;
    const status = form.querySelector('[role="status"]'); const submit = form.querySelector('[type="submit"]');
    if (submit.disabled) return;
    submit.disabled = true; submit.textContent = 'Sending your enquiry…'; status.textContent = ''; status.classList.remove('form-error');
    try {
      const response = await fetch('/', { method: 'POST', headers: { 'Content-Type':'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(form)).toString() });
      if (!response.ok) throw new Error('Submission failed');
      track('generate_lead', { form_name: form.getAttribute('name'), page_path: location.pathname, transport_type: 'beacon' });
      location.assign('/thank-you');
    } catch (_) {
      status.textContent = 'Your enquiry could not be sent. Please try again, call 07816 937 159 or use WhatsApp.';
      status.classList.add('form-error'); submit.disabled = false; submit.textContent = 'Send your enquiry';
    }
  });
});
