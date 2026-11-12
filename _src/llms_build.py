"""llms.txt / llms-full.txt for AI assistants (https://llmstxt.org). Called by build.py."""
import re, html, pathlib
from services_build import SERVICES, CASES
from blog_build import load

SITE = 'https://voriq.ru'
R = pathlib.Path(__file__).parent.parent

ABOUT = ('Voriq — студия разработки из России: сайты и лендинги, боты для Telegram и MAX, ИИ-агенты, '
         'автоматизация бизнес-процессов, кастомный софт, поддержка и развитие проектов. Работаем под ключ и удалённо, '
         'с клиентами по всей России и за её пределами, на русском и английском языках.')
FACTS = [
    'Название: Voriq (сайт voriq.ru).',
    'Владелец и оператор персональных данных: самозанятый Родионов Игорь Романович, ИНН 773135398240.',
    'Формат работы: под ключ — от задачи и плана до запуска и поддержки; удалённо.',
    'Как работаем: 1) задача в Telegram; 2) план и сроки до старта; 3) разработка с промежуточными версиями; 4) запуск и поддержка.',
    'Гарантии: работа по договору; сроки и объём фиксируются письменно; код, домен, хостинг и доступы передаются клиенту.',
    'Цены на сайте не публикуются: стоимость называется после короткой консультации, первая консультация бесплатная.',
    'Языки: русский и английский (английская версия сайта — https://voriq.ru/en/).',
]
CONTACTS = [
    'Заявка через бота: https://t.me/voriq_applicationsBot',
    'Telegram: @rydr3 (https://t.me/rydr3)',
    'Телефон, WhatsApp: +7 967 045-03-39',
    'MAX: https://max.ru/u/f9LHodD0cOI2tlgtGSDxYNm3lBYSskgV4OjiwH2SbofnAP5cFvRZjvrQSvo',
    'Форма заявки: https://voriq.ru/#contact',
]


def _plain(h):
    h = re.sub(r'<[^>]+>', '', h)
    return html.unescape(re.sub(r'\s+', ' ', h.replace('&nbsp;', ' '))).strip()


def _faq(page_html):
    return [(_plain(q), _plain(a)) for q, a in re.findall(r'<summary[^>]*>(.*?)<svg[\s\S]*?</summary><p[^>]*>([\s\S]*?)</p>', page_html)]


def _md_body(md_html):
    t = re.sub(r'<h2>(.*?)</h2>', lambda m: '\n### ' + _plain(m.group(1)) + '\n', md_html)
    t = re.sub(r'<li>(.*?)</li>', lambda m: '- ' + _plain(m.group(1)) + '\n', t)
    t = re.sub(r'<tr>(.*?)</tr>', lambda m: '| ' + ' | '.join(_plain(c) for c in re.findall(r'<t[hd]>(.*?)</t[hd]>', m.group(1))) + ' |\n', t)
    t = re.sub(r'<p>(.*?)</p>', lambda m: _plain(m.group(1)) + '\n\n', t)
    t = re.sub(r'<[^>]+>', '', t)
    return html.unescape(re.sub(r'\n{3,}', '\n\n', t)).strip()


def render():
    home = (R / 'index.html').read_text(encoding='utf-8')
    posts_ru, posts_en = load('ru'), load('en')
    faq = _faq(home)

    s = [f'# Voriq\n\n> {ABOUT}\n']
    s.append('## Ключевые факты\n\n' + '\n'.join(f'- {f}' for f in FACTS) + '\n')
    s.append('## Услуги\n\n' + '\n'.join(
        f'- [{sv["title"]}]({SITE}/{sv["slug"]}/): {sv["desc"]}' for sv in SERVICES) + '\n')
    s.append('## Примеры работ\n\n' + '\n'.join(f'- [{n}]({u}): {d}' for n, d, _, u in CASES.values()) + '\n')
    s.append('## Блог\n\n' + '\n'.join(f'- [{p["title"]}]({SITE}/blog/{p["slug"]}/): {p["description"]}' for p in posts_ru) + '\n')
    s.append('## English\n\n- [Voriq in English](https://voriq.ru/en/)\n' + '\n'.join(
        f'- [{p["title"]}]({SITE}/en/blog/{p["slug"]}/): {p["description"]}' for p in posts_en) + '\n')
    s.append('## Контакты\n\n' + '\n'.join(f'- {c}' for c in CONTACTS) + '\n')
    s.append(f'## Документы\n\n- [Политика конфиденциальности]({SITE}/privacy/)\n- [Полная версия для ИИ (весь текст сайта)]({SITE}/llms-full.txt)\n- [Sitemap]({SITE}/sitemap.xml)\n')
    llms = '\n'.join(s)

    f = [llms, '\n---\n\n# Полный текст\n']
    if faq:
        f.append('## Частые вопросы\n\n' + '\n\n'.join(f'### {q}\n{a}' for q, a in faq) + '\n')
    for sv in SERVICES:
        block = [f'## {sv["title"]}\n', f'URL: {SITE}/{sv["slug"]}/\n', sv['lead'] + '\n', '### Что делаем']
        block += [f'- {t}: {d}' for t, d in sv['what']]
        block += ['\n### Кому подходит'] + [f'- {w}' for w in sv['who']]
        block += ['\n### Вопросы и ответы'] + [f'**{q}** {a}' for q, a in sv['faq']]
        f.append('\n'.join(block) + '\n')
    for p in posts_ru:
        f.append(f'## {p["title"]}\n\nURL: {SITE}/blog/{p["slug"]}/\n\n{p["description"]}\n\n{_md_body(p["body"])}\n')
    full = '\n'.join(f)
    return llms, full
