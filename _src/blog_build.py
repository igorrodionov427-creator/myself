"""Blog pages for build.py: _src/blog/{ru,en}/*.md -> blog/<slug>/, en/blog/<slug>/ + index pages."""
import re, json, html, pathlib, datetime

S = pathlib.Path(__file__).parent
SITE = 'https://voriq.ru'
BOT = 'https://t.me/voriq_applicationsBot'

L = {
    'ru': dict(base='/blog/', home='/', other='/en/blog/', lang_ru='RU', blog='Блог', back='На главную', cta_h='Обсудим ваш проект?',
               cta_p='Опишите задачу в паре предложений — пришлём план и сроки. Первая консультация бесплатно.',
               cta_b='Оставить заявку', cta_bot='Написать боту', more='Ещё статьи', read='Читать',
               index_title='Блог Voriq — сайты, боты, ИИ и автоматизация', index_h='Блог.',
               index_p='Пишем простым языком о сайтах, Telegram-ботах, ИИ-агентах и автоматизации бизнеса.',
               index_desc='Статьи Voriq о разработке сайтов, Telegram-ботов, ИИ-агентов и автоматизации бизнеса — простым языком.',
               months=['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'],
               locale='ru_RU', start='blog', privacy='/privacy/', privacy_t='Политика конфиденциальности'),
    'en': dict(base='/en/blog/', home='/en/', other='/blog/', blog='Blog', back='Home', cta_h='Let’s talk about your project',
               cta_p='Describe the task in a couple of sentences — we’ll send a plan and timeline. The first consultation is free.',
               cta_b='Send a request', cta_bot='Message the bot', more='More articles', read='Read',
               index_title='Voriq Blog — websites, bots, AI and automation', index_h='Blog.',
               index_p='Plain-language notes on websites, Telegram bots, AI agents and business automation.',
               index_desc='Voriq articles on building websites, Telegram bots, AI agents and business automation — in plain language.',
               months=None, locale='en_US', start='blog_en', privacy='/en/privacy/', privacy_t='Privacy policy'),
}

def fmt_date(d, lang):
    if lang == 'ru':
        return f'{d.day} {L["ru"]["months"][d.month - 1]} {d.year}'
    return d.strftime('%B %-d, %Y') if hasattr(d, 'strftime') and False else f'{d.strftime("%B")} {d.day}, {d.year}'

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<a href="{m.group(2)}"' + (' target="_blank" rel="noopener"' if m.group(2).startswith('http') else '') + f'>{m.group(1)}</a>', t)
    return t

def md(src):
    out, lines, i = [], src.strip().split('\n'), 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip(): i += 1; continue
        if ln.startswith('## '):
            out.append(f'<h2>{inline(ln[3:])}</h2>'); i += 1; continue
        if ln.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                if not re.match(r'^\|[\s\-|]+\|$', lines[i]): rows.append([c.strip() for c in lines[i].strip('|').split('|')])
                i += 1
            head, body = rows[0], rows[1:]
            out.append('<div class="tbl"><table><thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in head) + '</tr></thead><tbody>' +
                       ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in body) + '</tbody></table></div>')
            continue
        if re.match(r'^(- |\d+\. )', ln):
            tag = 'ol' if re.match(r'^\d+\. ', ln) else 'ul'; items = []
            while i < len(lines) and re.match(r'^(- |\d+\. )', lines[i]):
                items.append(re.sub(r'^(- |\d+\. )', '', lines[i])); i += 1
            out.append(f'<{tag}>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + f'</{tag}>'); continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r'^(## |- |\d+\. |\|)', lines[i]):
            para.append(lines[i]); i += 1
        out.append(f'<p>{inline(" ".join(para))}</p>')
    return '\n'.join(out)

def load(lang):
    posts = []
    for f in sorted((S / 'blog' / lang).glob('*.md')):
        raw = f.read_text(encoding='utf-8')
        m = re.match(r'---\n([\s\S]*?)\n---\n([\s\S]*)', raw)
        meta = dict(re.findall(r'^(\w+):\s*(.+)$', m.group(1), re.M))
        meta['slug'] = f.stem; meta['body'] = md(m.group(2))
        meta['d'] = datetime.date.fromisoformat(meta['date'])
        words = len(re.sub(r'<[^>]+>', ' ', meta['body']).split())
        meta['min'] = max(2, round(words / 180))
        posts.append(meta)
    return posts

HEAD = '''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#132a24">
<link rel="canonical" href="{url}">
{alts}
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="Voriq">
<meta property="og:locale" content="{locale}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{site}/media/og-{lang}.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/media/favicon.png">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope">
<script src="https://cdn.tailwindcss.com/3.4.17"></script>
<script type="application/ld+json">{ld}</script>
<style>
  body{{font-family:'Satoshi','Manrope',sans-serif}}
  ::selection{{background:#132a24;color:#fff}}
  .prose h2{{font-size:clamp(24px,3vw,30px);font-weight:500;letter-spacing:-.02em;line-height:1.2;margin:48px 0 14px}}
  .prose p,.prose li{{color:#3f5a52;font-size:18px;line-height:1.75}}
  .prose p{{margin:16px 0}}
  .prose ul,.prose ol{{margin:14px 0;padding-left:22px}}
  .prose ul{{list-style:disc}} .prose ol{{list-style:decimal}}
  .prose li{{margin:8px 0}} .prose li::marker{{color:#78A184}}
  .prose strong{{color:#132a24;font-weight:600}}
  .prose a{{color:#132a24;text-decoration:underline;text-decoration-color:#78A184;text-underline-offset:3px}}
  .prose .tbl{{overflow-x:auto;margin:24px 0;border:1px solid rgba(19,42,36,.1);border-radius:18px;background:#fff}}
  .prose table{{width:100%;border-collapse:collapse;font-size:15px}}
  .prose th,.prose td{{text-align:left;padding:14px 16px;border-bottom:1px solid rgba(19,42,36,.08);vertical-align:top}}
  .prose th{{font-weight:600;background:#f1f5f3}}
  .prose tr:last-child td{{border-bottom:0}}
  .reveal{{opacity:0;transform:translateY(24px);animation:in 1s cubic-bezier(.22,1,.36,1) forwards;animation-delay:var(--d,0s)}}
  @keyframes in{{to{{opacity:1;transform:none}}}}
</style>
</head>
<body class="bg-[#f5f7f6] text-[#132a24] antialiased">
<header class="sticky top-0 z-50 backdrop-blur-md bg-[#f5f7f6]/90 border-b border-[#132a24]/5">
  <div class="max-w-6xl mx-auto px-5 sm:px-8 h-20 flex items-center justify-between">
    <a href="{home}" class="text-[22px] font-bold tracking-tight">voriq</a>
    <div class="flex items-center gap-2">
      <a href="{base}" class="hidden sm:inline text-[15px] font-medium px-3">{blog}</a>
      <div class="flex items-center rounded-full border border-[#132a24]/15 bg-white/60 p-0.5 text-[12px] font-medium">{switch}</div>
      <a href="{home}#contact" class="group inline-flex items-center gap-2 rounded-full bg-[#132a24] text-white text-[14px] font-medium pl-5 pr-4 h-11 hover:bg-[#274f44] transition-colors duration-500">{cta_b}<iconify-icon icon="solar:arrow-right-linear" width="18" class="transition-transform duration-500 group-hover:translate-x-1"></iconify-icon></a>
    </div>
  </div>
</header>
'''

FOOT = '''
<footer class="bg-[#132a24] text-[#879f98]">
  <div class="max-w-6xl mx-auto px-5 sm:px-8 py-10 flex flex-col sm:flex-row gap-4 justify-between text-[14px]">
    <a href="{home}" class="text-white font-bold text-[18px]">voriq</a>
    <a href="{privacy}" class="hover:text-white transition-colors">{privacy_t}</a>
    <span>© 2026 Voriq</span>
  </div>
</footer>
</body>
</html>
'''

def switch(lang, ru_url, en_url):
    on = 'rounded-full px-2.5 py-1 bg-[#132a24] text-white'; off = 'rounded-full px-2.5 py-1 text-[#879f98] hover:text-[#132a24]'
    return (f'<a href="{ru_url}" hreflang="ru" class="{on if lang == "ru" else off}">RU</a>'
            f'<a href="{en_url}" hreflang="en" class="{on if lang == "en" else off}">EN</a>')

def cta(lang, c):
    return f'''
  <section class="reveal mt-16 rounded-[28px] bg-[#132a24] text-white p-8 sm:p-10 relative overflow-hidden">
    <div class="absolute -right-20 -top-20 w-72 h-72 rounded-full bg-[radial-gradient(circle,#78A184_0%,transparent_70%)] opacity-40 blur-2xl"></div>
    <h2 class="relative text-[28px] sm:text-[34px] font-medium tracking-[-0.02em] leading-tight">{c["cta_h"]}</h2>
    <p class="relative mt-3 text-[#b7c9c2] max-w-xl leading-relaxed">{c["cta_p"]}</p>
    <div class="relative mt-6 flex flex-wrap gap-3">
      <a href="{c["home"]}#contact" class="group inline-flex items-center gap-2 rounded-full bg-white text-[#132a24] font-medium px-6 h-12 hover:bg-[#78A184] hover:text-white transition-colors duration-500">{c["cta_b"]}<iconify-icon icon="solar:arrow-right-linear" width="18" class="transition-transform duration-500 group-hover:translate-x-1"></iconify-icon></a>
      <a href="{BOT}?start={c["start"]}" target="_blank" rel="noopener" class="inline-flex items-center gap-2 rounded-full border border-white/20 px-6 h-12 hover:bg-white hover:text-[#132a24] transition-colors duration-500"><iconify-icon icon="simple-icons:telegram" width="16"></iconify-icon>{c["cta_bot"]}</a>
    </div>
  </section>'''

def card(p, c, lang, k):
    return f'''<a href="{c["base"]}{p["slug"]}/" class="reveal group flex flex-col justify-between rounded-[24px] bg-white border border-[#132a24]/10 p-7 min-h-[220px] transition-[transform,box-shadow] duration-700 hover:-translate-y-1 hover:shadow-[0_30px_60px_-30px_rgba(19,42,36,.35)]" style="--d:{k * 0.06:.2f}s">
      <div class="flex items-center justify-between text-[13px] text-[#879f98]"><span class="rounded-full bg-[#e4ebe8] text-[#274f44] px-3 py-1 font-medium">{p["tag"]}</span><span>{p["min"]} {"мин" if lang == "ru" else "min"}</span></div>
      <div><h3 class="mt-6 text-[22px] font-medium tracking-[-0.02em] leading-snug">{html.escape(p["title"])}</h3>
      <p class="mt-2 text-[15px] text-[#879f98] leading-relaxed">{html.escape(p["description"])}</p>
      <span class="mt-5 inline-flex items-center gap-2 text-[14px] font-medium">{c["read"]}<iconify-icon icon="solar:arrow-right-linear" width="16" class="transition-transform duration-500 group-hover:translate-x-1"></iconify-icon></span></div>
    </a>'''

def render():
    pages = []
    posts = {lang: load(lang) for lang in L}
    for lang, c in L.items():
        ps = posts[lang]
        # index
        url = SITE + c['base']
        ld = json.dumps({'@context': 'https://schema.org', '@type': 'Blog', 'name': 'Voriq ' + c['blog'], 'url': url, 'inLanguage': lang,
                         'blogPost': [{'@type': 'BlogPosting', 'headline': p['title'], 'url': url + p['slug'] + '/', 'datePublished': p['date']} for p in ps]},
                        ensure_ascii=False)
        alts = (f'<link rel="alternate" hreflang="ru" href="{SITE}/blog/">\n<link rel="alternate" hreflang="en" href="{SITE}/en/blog/">')
        h = HEAD.format(lang=lang, title=c['index_title'], desc=c['index_desc'], url=url, alts=alts, ogtype='website', locale=c['locale'], site=SITE, ld=ld,
                        home=c['home'], base=c['base'], blog=c['blog'], switch=switch(lang, '/blog/', '/en/blog/'), cta_b=c['cta_b'])
        h += f'''<main class="max-w-6xl mx-auto px-5 sm:px-8 pt-16 sm:pt-24 pb-24">
  <p class="reveal text-[13px] font-medium uppercase tracking-[0.18em] text-[#879f98]">Voriq</p>
  <h1 class="reveal mt-4 text-5xl sm:text-6xl lg:text-[72px] font-medium tracking-[-0.035em] leading-[1.02]" style="--d:.08s">{c["index_h"]}</h1>
  <p class="reveal mt-5 text-[18px] text-[#879f98] max-w-2xl leading-relaxed" style="--d:.16s">{c["index_p"]}</p>
  <div class="mt-14 grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
    {"".join(card(p, c, lang, k) for k, p in enumerate(ps))}
  </div>
  {cta(lang, c)}
</main>''' + FOOT.format(home=c['home'], privacy=c['privacy'], privacy_t=c['privacy_t'])
        pages.append((c['base'], c['base'].strip('/') + '/index.html', h))
        # posts
        for p in ps:
            purl = url + p['slug'] + '/'
            ld = json.dumps({'@context': 'https://schema.org', '@graph': [
                {'@type': 'BlogPosting', 'headline': p['title'], 'description': p['description'], 'datePublished': p['date'], 'dateModified': p['date'],
                 'inLanguage': lang, 'mainEntityOfPage': purl, 'image': f'{SITE}/media/og-{lang}.jpg',
                 'author': {'@type': 'Organization', 'name': 'Voriq', 'url': SITE + '/'}, 'publisher': {'@type': 'Organization', 'name': 'Voriq', 'logo': {'@type': 'ImageObject', 'url': SITE + '/media/logo.png'}}},
                {'@type': 'BreadcrumbList', 'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Voriq', 'item': SITE + c['home']},
                    {'@type': 'ListItem', 'position': 2, 'name': c['blog'], 'item': url},
                    {'@type': 'ListItem', 'position': 3, 'name': p['title'], 'item': purl}]}]}, ensure_ascii=False)
            alts = f'<link rel="alternate" hreflang="{lang}" href="{purl}">'
            h = HEAD.format(lang=lang, title=html.escape(p['title']) + ' — Voriq', desc=html.escape(p['description']), url=purl, alts=alts, ogtype='article',
                            locale=c['locale'], site=SITE, ld=ld, home=c['home'], base=c['base'], blog=c['blog'],
                            switch=switch(lang, '/blog/', '/en/blog/'), cta_b=c['cta_b'])
            others = [o for o in ps if o['slug'] != p['slug']][:3]
            h += f'''<main class="max-w-6xl mx-auto px-5 sm:px-8 pt-12 sm:pt-16 pb-24">
  <nav class="reveal text-[14px] text-[#879f98]" aria-label="breadcrumbs"><a href="{c["home"]}" class="hover:text-[#132a24]">Voriq</a> <span class="mx-1.5">/</span> <a href="{c["base"]}" class="hover:text-[#132a24]">{c["blog"]}</a></nav>
  <article class="max-w-3xl">
    <div class="reveal mt-8 flex flex-wrap items-center gap-3 text-[14px] text-[#879f98]" style="--d:.05s"><span class="rounded-full bg-[#e4ebe8] text-[#274f44] px-3 py-1 font-medium">{p["tag"]}</span><time datetime="{p["date"]}">{fmt_date(p["d"], lang)}</time><span>·</span><span>{p["min"]} {"мин чтения" if lang == "ru" else "min read"}</span></div>
    <h1 class="reveal mt-5 text-4xl sm:text-5xl lg:text-[56px] font-medium tracking-[-0.035em] leading-[1.05]" style="--d:.1s">{html.escape(p["title"])}</h1>
    <p class="reveal mt-6 text-[20px] text-[#4b625b] leading-relaxed" style="--d:.15s">{html.escape(p["description"])}</p>
    <div class="prose reveal mt-8" style="--d:.2s">
{p["body"]}
    </div>
  </article>
  {cta(lang, c)}
  <h2 class="mt-20 text-[28px] font-medium tracking-[-0.02em]">{c["more"]}</h2>
  <div class="mt-6 grid sm:grid-cols-2 lg:grid-cols-3 gap-5">{"".join(card(o, c, lang, k) for k, o in enumerate(others))}</div>
</main>''' + FOOT.format(home=c['home'], privacy=c['privacy'], privacy_t=c['privacy_t'])
            rel = c['base'].strip('/') + f'/{p["slug"]}/index.html'
            pages.append((c['base'] + p['slug'] + '/', rel, h))
    return pages
