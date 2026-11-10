"""Build en/index.html from the Russian index.html.

Run after every change of index.html:  python build_en.py
Text tokens (between tags/quotes) are swapped by exact match from EN below;
the lead message sent to the owner's Telegram stays in Russian.
"""
import re, pathlib

ROOT = pathlib.Path(__file__).parent
EN = {
    "Voriq — сайты, боты и автоматизация": "Voriq — websites, bots and automation",
    "Voriq — студия разработки: сайты, Telegram-боты и автоматизация бизнеса под ключ.": "Voriq is a development studio: websites, Telegram bots and business automation, turnkey.",
    "Telegram-бот": "Telegram bot",
    "Telegram-боты": "Telegram bots",
    "под ключ": "turnkey",
    "под ключ.": "turnkey.",
    "Услуги": "Services",
    "Принципы": "Principles",
    "Гарантии": "Guarantees",
    "Проекты": "Projects",
    "Связаться": "Contact us",
    "Цифровая инфраструктура": "Digital infrastructure",
    "для реального бизнеса.": "for real business.",
    "Строим сайты, Telegram-ботов и автоматизацию, которые приводят заявки и снимают рутину. Под ключ — от идеи до запуска и поддержки.": "We build websites, Telegram bots and automation that bring in leads and take routine off your plate. Turnkey — from idea to launch and support.",
    "Смотреть услуги": "View services",
    "Частые вопросы": "FAQ",
    "Разработка": "Development",
    "Без лишних": "Without extra",
    "подрядчиков.": "contractors.",
    "Сайт и мобильная версия": "Website and mobile version",
    "Сайты и лендинги": "Websites & landings",
    "Лендинг": "Landing page",
    "Лендинги, корпоративные сайты и интернет-магазины. Быстрые, удобные с телефона и настроенные на заявки.": "Landing pages, company websites and online stores. Fast, mobile-friendly and built to generate leads.",
    "Корпоративный сайт": "Company website",
    "Магазин": "Online store",
    "Редизайн": "Redesign",
    "Чат-бот в телефоне": "Chatbot on a phone",
    "Боты для заявок, записи, оплаты и поддержки. Отвечают клиентам круглосуточно и передают заявки вам.": "Bots for leads, bookings, payments and support. They answer customers 24/7 and pass requests to you.",
    "Бот заявок": "Lead bot",
    "Приём оплаты": "Payments",
    "Рассылки": "Broadcasts",
    "Поддержка": "Support",
    "ИИ-ассистент со связанными сервисами": "AI assistant with connected services",
    "ИИ-агент": "AI agent",
    "ИИ-агенты": "AI agents",
    "Ассистенты на базе ИИ: отвечают на вопросы клиентов, разбирают входящие обращения и работают с вашими документами.": "AI-powered assistants: they answer customer questions, sort incoming requests and work with your documents.",
    "Консультант": "Consultant",
    "Разбор заявок": "Lead triage",
    "База знаний": "Knowledge base",
    "Работа с CRM": "CRM work",
    "Сервисы, связанные в один поток": "Services connected into one flow",
    "Автоматизация процессов": "Process automation",
    "Связываем CRM, мессенджеры, таблицы и оплаты в один поток — рутина делается сама, без ручной работы.": "We connect your CRM, messengers, spreadsheets and payments into one flow — routine runs itself, no manual work.",
    "Таблицы": "Spreadsheets",
    "Уведомления": "Notifications",
    "Отчёты": "Reports",
    "Дашборд и код": "Dashboard and code",
    "Кастомный софт": "Custom software",
    "Внутренние сервисы под задачи бизнеса: личные кабинеты, дашборды, парсеры и интеграции по API.": "Internal tools built around your business: client portals, dashboards, scrapers and API integrations.",
    "Кабинеты": "Portals",
    "Дашборды": "Dashboards",
    "Парсеры": "Scrapers",
    "Мониторинг и обновления": "Monitoring and updates",
    "Мониторинг": "Monitoring",
    "Поддержка и развитие": "Support & growth",
    "Доработки, обновления и мониторинг после запуска. Продукт продолжает расти вместе с бизнесом.": "Improvements, updates and monitoring after launch. Your product keeps growing with your business.",
    "Доработки": "Improvements",
    "Обновления": "Updates",
    "Аналитика": "Analytics",
    "Как мы работаем": "How we work",
    "Принципы, на которых держится каждый проект.": "The principles behind every project.",
    "Задача": "Task",
    "Задача — в двух словах": "Your task in a few words",
    "Пишете в Telegram голосом или текстом. Дальше разбираемся сами.": "Message us on Telegram by voice or text. We take it from there.",
    "План до старта": "A plan before we start",
    "Присылаем план и сроки. Вы заранее знаете, что и когда получите.": "We send a plan and timeline. You know upfront what you get and when.",
    "Показываем по ходу": "Progress you can see",
    "Промежуточные версии и правки — без долгих согласований.": "Interim versions and edits — no lengthy approvals.",
    "Запуск и поддержка": "Launch and support",
    "Подключаем домен и аналитику, остаёмся на связи. Код и доступы — ваши.": "We connect your domain and analytics and stay in touch. The code and access are yours.",
    "Код и доступы — ваши": "Your code, your access",
    "Технологии, с которыми работаем": "Technologies we work with",
    "Прозрачно на каждом этапе.": "Transparent at every stage.",
    "Щит с галочкой: код и доступы у клиента": "Shield with a check mark: code and access stay with the client",
    "Передаём исходники, домен, хостинг и админки на ваше имя. Никакой привязки к нам.": "We hand over the source code, domain, hosting and admin panels in your name. No lock-in.",
    "Договор с подписью": "Signed contract",
    "Работа по договору": "Work under contract",
    "Сроки и объём работ фиксируются письменно. Понятно, что и когда вы получите.": "Timeline and scope are fixed in writing. You know exactly what you get and when.",
    "Календарь, этапы проекта и часы": "Calendar, project stages and a clock",
    "Сроки по плану": "On schedule",
    "Делим проект на этапы и показываем результат после каждого. Всегда видно, на каком шаге работа.": "We split the project into stages and show results after each one. You always see where things stand.",
    "График роста заявок": "Lead growth chart",
    "Понятные отчёты": "Clear reports",
    "Подключаем аналитику и показываем, сколько заявок приносит сайт и бот — без воды.": "We set up analytics and show how many leads your site and bot bring in — no fluff.",
    "Наши работы.": "Our work.",
    "Обсудить": "Let's talk",
    "Обсудить ваш проект": "Discuss your project",
    "Частые вопросы.": "FAQ.",
    "Не нашли ответ? Напишите нам — ответим в течение дня.": "Didn't find an answer? Message us — we reply within a day.",
    "С чего начать?": "Where do we start?",
    "Напишите нам в Telegram, боту": "Message us on Telegram, write to the bot",
    "или оставьте заявку на сайте. Пары слов о задаче достаточно — дальше зададим уточняющие вопросы сами.": "or leave a request on the site. A couple of words about the task is enough — we'll ask the follow-up questions.",
    "Что нужно от меня для старта?": "What do you need from me to start?",
    "Коротко описать задачу и, если есть, показать примеры, которые нравятся. Тексты, фото и доступы можно прислать позже — подскажем, что именно нужно.": "A short description of the task and, if you have them, examples you like. Texts, photos and access can come later — we'll tell you exactly what's needed.",
    "Работаете по договору?": "Do you work under a contract?",
    "Да. Объём работ, сроки и этапы фиксируем письменно до начала, чтобы обе стороны понимали, что и когда будет готово.": "Yes. Scope, timeline and stages are fixed in writing before we start, so both sides know what will be ready and when.",
    "Кому принадлежат код и доступы?": "Who owns the code and access?",
    "Вам. Передаём исходники, домен, хостинг, админки и ботов на ваше имя — без привязки к нам.": "You do. We hand over the source code, domain, hosting, admin panels and bots in your name — no lock-in.",
    "Можно начать с небольшой задачи?": "Can we start with a small task?",
    "Да. Многие начинают с одного бота или лендинга, а потом добавляют автоматизацию. Так удобно проверить, как мы работаем.": "Yes. Many clients start with one bot or a landing page and add automation later. It's an easy way to see how we work.",
    "Доработаете мой текущий сайт или бота?": "Can you improve my existing website or bot?",
    "Да. Посмотрим, что уже есть, и скажем, что лучше доработать, а что проще переделать.": "Yes. We'll look at what you have and tell you what's worth improving and what's easier to rebuild.",
    "Как проходит работа и общение?": "How do work and communication go?",
    "Один чат в Telegram для всех вопросов. Показываем промежуточные версии, вносим правки по ходу — без долгих созвонов и согласований.": "One Telegram chat for everything. We show interim versions and make edits along the way — no long calls or approvals.",
    "Подключаете оплату, CRM и аналитику?": "Do you set up payments, CRM and analytics?",
    "Да: приём оплаты, CRM, Google-таблицы, рассылки, уведомления в Telegram и аналитику — всё связываем в одну систему.": "Yes: payments, CRM, Google Sheets, broadcasts, Telegram notifications and analytics — all connected into one system.",
    "Делаете сайты и ботов на английском?": "Do you build websites and bots in English?",
    "Да, на русском и английском. Работаем удалённо с клиентами из разных городов и стран.": "Yes, in English and Russian. We work remotely with clients from different cities and countries.",
    "Нужно ли разбираться в технике?": "Do I need to be technical?",
    "Нет. Хостинг, домен, интеграции и запуск берём на себя.": "No. We handle hosting, the domain, integrations and launch.",
    "Что после запуска?": "What happens after launch?",
    "Остаёмся на связи: правки, поддержка, обновления и доработки по мере роста бизнеса.": "We stay in touch: edits, support, updates and improvements as your business grows.",
    "Контакты": "Contact",
    "Расскажите задачу&nbsp;—": "Tell us the task&nbsp;—",
    "остальное на нас.": "we'll handle the rest.",
    "Первую консультацию проводим бесплатно. Ответим в течение дня.": "The first consultation is free. We reply within a day.",
    "Заявка через бота": "Request via bot",
    "· Telegram @rydr3 · WhatsApp и MAX по номеру +7 967 045-03-39": "· Telegram @rydr3 · WhatsApp and MAX: +7 967 045-03-39",
    "Имя": "Name",
    "Как к вам обращаться": "How should we call you",
    "Telegram или телефон": "Telegram or phone",
    "Тип запроса": "Request type",
    "Выберите направление": "Choose a service",
    "Сайт или лендинг": "Website or landing page",
    "Пока не знаю / другое": "Not sure yet / other",
    "Пара слов о проекте": "A few words about the project",
    "Отправить заявку": "Send request",
    "Бот заявок @voriq_applicationsBot": "Lead bot @voriq_applicationsBot",
    "Сайт + боты": "Website + bots",
    "Производитель вывесок: сайт, боты для заявок и рассылки по базе.": "Sign manufacturer: website, lead bots and customer broadcasts.",
    "Сайт + ИИ-агенты": "Website + AI agents",
    "Агентство сайтов, ботов и ИИ-агентов: сайт с двумя языками и ботами.": "Agency for websites, bots and AI agents: a bilingual website with bots.",
    "Интернет-магазин": "Online store",
    "Магазин спортивного питания: каталог, корзина, промокоды и админка.": "Sports nutrition store: catalog, cart, promo codes and admin panel.",
    "Сайт + бот заявок": "Website + lead bot",
    "Сайт агентства и бот, который принимает заявки 24/7.": "Agency website and a bot that takes requests 24/7.",
    "Сайт на 8 языках": "Website in 8 languages",
    "Сайт агентства для США и Европы с блогом и ботом заявок.": "Agency website for the US and Europe with a blog and a lead bot.",
    "Сайт $": "Website $",
    "Следующий": "Next",
    "Ваш проект —": "Your project —",
    "здесь.": "here.",
    "Расскажите задачу — пришлём план и сроки.": "Tell us the task — we'll send a plan and timeline.",
    "Заполните имя и контакт.": "Please fill in your name and contact.",
    "Отправляем…": "Sending…",
    "Спасибо! Заявка отправлена — скоро свяжемся.": "Thank you! Your request is sent — we'll be in touch soon.",
    "Не получилось отправить. Напишите нам в": "Couldn't send it. Message us on",
}

TOKEN = re.compile(r'[^<>"\'`{}\n]*[А-Яа-яЁё][^<>"\'`{}\n]*')

def build():
    s = (ROOT / 'index.html').read_text(encoding='utf-8')
    # owner-facing lead message: keep Russian, mark the language
    s = s.replace('🆕 Заявка с сайта Voriq (форма)', '🆕 Заявка с сайта Voriq (форма, EN)')
    keep = {'🆕 Заявка с сайта Voriq (форма, EN)\\n\\n👤 Имя: $', '\\n📱 Контакт: $', '\\n📂 Тип: $', '\\n📝 Задача: $', '💬 Написать клиенту'}
    missing = set()
    def swap(m):
        raw = m.group(0); t = raw.strip()
        if t in keep: return raw
        if t not in EN:
            missing.add(t); return raw
        lead = raw[:len(raw) - len(raw.lstrip())]; tail = raw[len(raw.rstrip()):]
        return lead + EN[t].replace("'", "’") + tail
    s = TOKEN.sub(swap, s)
    if missing:
        raise SystemExit('No translation for:\n  ' + '\n  '.join(sorted(missing)))
    s = s.replace('<html lang="ru">', '<html lang="en">', 1)
    s = s.replace('src="media/', 'src="../media/').replace("'media/", "'../media/").replace('href="media/', 'href="../media/')
    s = re.sub(r'(class="lang-ru-link[^"]*" href=")\./"', r'\1../"', s, count=1)
    s = re.sub(r'(class="lang-en-link[^"]*" href=")en/"', r'\1./"', s, count=1)
    s = s.replace('?start=site', '?start=site_en')
    s = s.replace('<link rel="canonical" href="https://voriq.ru/">', '<link rel="canonical" href="https://voriq.ru/en/">')
    s = s.replace('<div data-current-lang="ru"', '<div data-current-lang="en"', 1)
    out = ROOT / 'en' / 'index.html'
    out.parent.mkdir(exist_ok=True)
    out.write_text(s, encoding='utf-8')
    left = [t for t in TOKEN.findall(s) if t.strip() not in keep]
    print('en/index.html written; Cyrillic left outside the owner message:', len(left))

if __name__ == '__main__':
    build()
