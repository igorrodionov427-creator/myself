"""Voriq site build.

Sources live in _src/ (Jekyll on GitHub Pages ignores folders starting with "_").
Run:  python build.py
Outputs: index.html, en/index.html, privacy/, en/privacy/, 404.html, blog/, en/blog/,
         assets/site.css (Tailwind, compiled), sitemap.xml, robots.txt.
"""
import re, sys, json, hashlib, subprocess, pathlib, datetime

R = pathlib.Path(__file__).parent
S = R / '_src'
sys.path.insert(0, str(S))
from i18n_en import EN  # noqa: E402

# Switch to 'https' once GitHub Pages issues the certificate for voriq.ru
SCHEME = 'https'
SITE = 'https://voriq.ru'  # sources are written with https; outputs are rewritten to SCHEME below
NODE = pathlib.Path.home() / 'tools' / 'node-v24.22.1-win-x64' / 'node.exe'
TAILWIND = R.parent / 'v2' / 'node_modules' / 'tailwindcss' / 'lib' / 'cli.js'
TODAY = datetime.date.today().isoformat()

# ---------------------------------------------------------------- icons
ICON_RE = re.compile(r'<iconify-icon icon="([a-z-]+):([a-z0-9-]+)"([^>]*)></iconify-icon>')

def _icon(m):
    prefix, name, attrs = m.group(1), m.group(2), m.group(3)
    f = R / 'assets' / 'icons' / f'{prefix}--{name}.svg'
    if not f.exists():
        raise SystemExit(f'missing icon {prefix}:{name} — download it into assets/icons/')
    svg = f.read_text(encoding='utf-8').strip()
    w = re.search(r'width="(\d+)"', attrs); cls = re.search(r'class="([^"]*)"', attrs)
    size = w.group(1) if w else '24'
    svg = re.sub(r'width="1em" height="1em"', f'width="{size}" height="{size}"', svg, count=1)
    extra = f' class="{cls.group(1)}"' if cls else ''
    return svg.replace('<svg ', f'<svg aria-hidden="true" focusable="false"{extra} ', 1)

# ---------------------------------------------------------------- head assets
ICONS = ('<link rel="icon" href="/favicon.ico" sizes="any">\n'
         '<link rel="icon" type="image/png" sizes="48x48" href="/media/icon-48.png">\n'
         '<link rel="icon" type="image/png" sizes="192x192" href="/media/icon-192.png">\n'
         '<link rel="apple-touch-icon" sizes="180x180" href="/media/apple-touch-icon.png">')

def localize_assets(s):
    s = s.replace('<link rel="apple-touch-icon" href="/media/logo.png">\n', '')
    s = s.replace('<link rel="icon" type="image/png" href="/media/favicon.png">', ICONS, 1)
    s = s.replace('<script src="https://cdn.tailwindcss.com/3.4.17"></script>', '<link rel="stylesheet" href="/assets/site.css?v=__CSSV__">')
    s = re.sub(r'<script src="https://code\.iconify\.design/[^"]+"></script>\n?', '', s)
    s = re.sub(r'<link rel="stylesheet" href="https://api\.fontshare\.com/[^"]+">\n?', '', s)
    s = re.sub(r'<!-- Satoshi has no Cyrillic[^>]*-->\n?', '', s)
    s = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/[^"]+">\n?',
               '<link rel="preload" href="/assets/fonts/satoshi-400.woff2" as="font" type="font/woff2" crossorigin>\n'
               '<link rel="stylesheet" href="/assets/fonts.css?v=1">\n', s, count=1)
    if '/assets/fonts.css' not in s:
        s = s.replace('<link rel="stylesheet" href="/assets/site.css', '<link rel="stylesheet" href="/assets/fonts.css?v=1">\n<link rel="stylesheet" href="/assets/site.css', 1)
    return ICON_RE.sub(_icon, s)

# ---------------------------------------------------------------- english
TOKEN = re.compile(r'[^<>"\'`{}\n]*[А-Яа-яЁё][^<>"\'`{}\n]*')
KEEP = {'🆕 Заявка с сайта Voriq (форма, EN)\\n\\n👤 Имя: $', '\\n📱 Контакт: $', '\\n📂 Тип: $', '\\n📝 Задача: $', '💬 Написать клиенту'}

def to_english(s):
    # RU-only service pages: no links to them from the English page
    s = re.sub(r'\n      <a href="/[a-z-]+/" class="svc-more[\s\S]*?</a>', '', s)
    s = re.sub(r'    <div class="svc-footer[^\n]*\n', '', s)
    s = s.replace('🆕 Заявка с сайта Voriq (форма)', '🆕 Заявка с сайта Voriq (форма, EN)')
    missing = set()
    def swap(m):
        raw = m.group(0); t = raw.strip()
        if t in KEEP: return raw
        if t not in EN:
            missing.add(t); return raw
        lead = raw[:len(raw) - len(raw.lstrip())]; tail = raw[len(raw.rstrip()):]
        return lead + EN[t].replace("'", '’') + tail
    s = TOKEN.sub(swap, s)
    if missing:
        raise SystemExit('No English for:\n  ' + '\n  '.join(sorted(missing)))
    s = s.replace('<html lang="ru">', '<html lang="en">', 1)
    s = s.replace('href="/privacy/"', 'href="/en/privacy/"').replace('href="/blog/', 'href="/en/blog/')
    s = s.replace('<div data-current-lang="ru"', '<div data-current-lang="en"', 1)
    s = s.replace('?start=site', '?start=site_en')
    s = s.replace('<link rel="canonical" href="https://voriq.ru/">', '<link rel="canonical" href="https://voriq.ru/en/">')
    s = s.replace('<meta property="og:locale" content="ru_RU">', '<meta property="og:locale" content="en_US">')
    s = s.replace('<meta property="og:url" content="https://voriq.ru/">', '<meta property="og:url" content="https://voriq.ru/en/">')
    s = s.replace('/media/og-ru.jpg', '/media/og-en.jpg')
    return s

# ---------------------------------------------------------------- structured data
def _plain(h):
    h = re.sub(r'<[^>]+>', '', h)
    return re.sub(r'\s+', ' ', h.replace('&nbsp;', ' ')).strip()

def jsonld(html, lang):
    en = lang == 'en'
    home = SITE + ('/en/' if en else '/')
    faq = []
    for q, a in re.findall(r'<summary[^>]*>(.*?)<svg[\s\S]*?</summary><p[^>]*>([\s\S]*?)</p>', html):
        faq.append({'@type': 'Question', 'name': _plain(q), 'acceptedAnswer': {'@type': 'Answer', 'text': _plain(a)}})
    services = (['Websites and landing pages', 'Telegram & MAX bots', 'AI agents', 'Process automation', 'Custom software', 'Support and growth'] if en else
                ['Разработка сайтов и лендингов', 'Боты для Telegram и MAX', 'ИИ-агенты', 'Автоматизация процессов', 'Кастомный софт', 'Поддержка и развитие'])
    graph = [
        {'@type': 'ProfessionalService', '@id': SITE + '/#org', 'name': 'Voriq', 'url': SITE + '/',
         'logo': SITE + '/media/logo.png', 'image': SITE + f'/media/og-{lang}.jpg',
         'description': ('Voriq builds websites, Telegram bots, AI agents and business automation, turnkey.' if en else
                         'Voriq — разработка сайтов, ботов для Telegram и MAX, ИИ-агентов и автоматизации бизнеса под ключ.'),
         'telephone': '+7-967-045-03-39', 'areaServed': ['RU', 'Worldwide'] if en else 'RU',
         'sameAs': ['https://t.me/rydr3', 'https://t.me/voriq_applicationsBot', 'https://max.ru/u/f9LHodD0cOI2tlgtGSDxYNm3lBYSskgV4OjiwH2SbofnAP5cFvRZjvrQSvo'],
         'contactPoint': {'@type': 'ContactPoint', 'contactType': 'sales', 'telephone': '+7-967-045-03-39', 'availableLanguage': ['Russian', 'English']},
         'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Services' if en else 'Услуги',
                             'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': n}} for n in services]}},
        {'@type': 'WebSite', '@id': home + '#site', 'url': home, 'name': 'Voriq', 'inLanguage': lang, 'publisher': {'@id': SITE + '/#org'}},
    ]
    if faq:
        graph.append({'@type': 'FAQPage', '@id': home + '#faq', 'mainEntity': faq})
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False)
    return html.replace('<!--JSONLD-->', f'<script type="application/ld+json">{data}</script>', 1)

# ---------------------------------------------------------------- build
def write(rel, html):
    out = R / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8')
    return rel

def main():
    pages = []  # (url, rel)
    ru = (S / 'index.html').read_text(encoding='utf-8')
    pages.append(('/', write('index.html', jsonld(localize_assets(ru), 'ru'))))
    pages.append(('/en/', write('en/index.html', jsonld(localize_assets(to_english(ru)), 'en'))))
    for rel, url in [('privacy/index.html', '/privacy/'), ('en/privacy/index.html', '/en/privacy/')]:
        pages.append((url, write(rel, localize_assets((S / rel).read_text(encoding='utf-8')))))
    if (S / '404.html').exists():
        write('404.html', localize_assets((S / '404.html').read_text(encoding='utf-8')))

    # optional blog step
    blog = S / 'blog_build.py'
    if blog.exists():
        sys.path.insert(0, str(S))
        import blog_build
        for url, rel, html in blog_build.render():
            pages.append((url, write(rel, localize_assets(html))))

    # service landing pages
    if (S / 'services_build.py').exists():
        import services_build
        for url, rel, html in services_build.render():
            pages.append((url, write(rel, localize_assets(html))))

    # tailwind
    built = [p for _, p in pages] + (['404.html'] if (R / '404.html').exists() else [])
    tw_in = S / 'tw.css'
    tw_in.write_text('@tailwind base;\n@tailwind components;\n@tailwind utilities;\n', encoding='utf-8')
    subprocess.run([str(NODE), str(TAILWIND), '-i', str(tw_in), '-o', str(R / 'assets' / 'site.css'), '--minify',
                    '--content', ','.join(built)], cwd=R, check=True, capture_output=True)
    v = hashlib.md5((R / 'assets' / 'site.css').read_bytes()).hexdigest()[:8]
    for p in built:
        f = R / p; f.write_text(f.read_text(encoding='utf-8').replace('__CSSV__', v), encoding='utf-8')

    # sitemap + robots
    urls = sorted({u for u, _ in pages})
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        pr = '1.0' if u in ('/', '/en/') else ('0.3' if 'privacy' in u else ('0.6' if 'blog' in u else '0.9'))
        sm.append(f'  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>')
    sm.append('</urlset>')
    (R / 'sitemap.xml').write_text('\n'.join(sm) + '\n', encoding='utf-8')
    (R / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /_src/\n\nHost: https://voriq.ru\nSitemap: {SITE}/sitemap.xml\n', encoding='utf-8')
    if SCHEME == 'http':
        for p in built + ['sitemap.xml', 'robots.txt']:
            f = R / p; f.write_text(f.read_text(encoding='utf-8').replace('https://voriq.ru', 'http://voriq.ru'), encoding='utf-8')
    print(f'built {len(urls)} pages, css v={v}, {(R / "assets" / "site.css").stat().st_size // 1024} KB, scheme={SCHEME}')

if __name__ == '__main__':
    main()
