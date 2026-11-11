"""Service landing pages (RU) for build.py: /razrabotka-sajtov/ etc."""
import json, html
from blog_build import HEAD, FOOT, switch, cta, L, load, card

SITE = 'https://voriq.ru'
BOT = 'https://t.me/voriq_applicationsBot'

CASES = {
    'maing': ('MAING', 'Сайт производителя вывесок, боты для заявок, рассылки', '/media/cases/maing.jpg', 'https://maing.ru/'),
    'velion': ('Velion', 'Сайт агентства ИИ-агентов на двух языках', '/media/cases/velion.jpg', 'https://velionagency.ru/'),
    'nohassle': ('NoHassle', 'Сайт агентства и бот заявок 24/7', '/media/cases/nohassle.jpg', 'https://nohassle.ru/'),
    'apolline': ('Apolline', 'Сайт на 8 языках с блогом и ботом заявок', '/media/cases/apolline.jpg', 'https://apolline.site/'),
}

SERVICES = [
    dict(slug='razrabotka-sajtov', img='web', short='Сайты и лендинги',
         title='Разработка сайтов и лендингов под ключ',
         meta_title='Разработка сайтов и лендингов под ключ — Voriq',
         desc='Делаем лендинги, корпоративные сайты и интернет-магазины под ключ: дизайн, адаптив, формы заявок, интеграции, запуск и поддержка. План и сроки — до старта.',
         lead='Лендинги, корпоративные сайты и интернет-магазины, которые быстро открываются с телефона и приводят заявки. Делаем всё сами — от структуры и дизайна до домена и запуска.',
         what=[('Лендинг', 'Одна сильная страница под услугу или рекламную кампанию — с понятным оффером и формой заявки.'),
               ('Корпоративный сайт', 'Разделы услуг, кейсы, команда, документы — витрина компании для клиентов и партнёров.'),
               ('Интернет-магазин', 'Каталог, корзина, промокоды, оплата и админка, где удобно вести товары и заказы.'),
               ('Редизайн', 'Обновляем устаревший сайт: современный вид, скорость, мобильная версия, понятная структура.'),
               ('Многоязычный сайт', 'Русская и английская версии (или больше), правильная разметка для поиска в разных странах.'),
               ('SEO-основа', 'Заголовки, описания, разметка, sitemap и скорость — чтобы сайт находили в Яндексе и Google.')],
         who=['Бизнесу, которому нужны заявки из рекламы и поиска', 'Компаниям со старым сайтом, который стыдно показывать', 'Экспертам и студиям, которым нужна понятная витрина услуг', 'Тем, кто запускает новое направление и хочет быстро проверить спрос'],
         cases=['maing', 'apolline', 'nohassle'], posts=['skolko-vremeni-razrabotka-sajta', 'lending-ili-mnogostranichnyj-sajt', 'kak-podgotovit-tz-na-sajt-ili-bota'],
         faq=[('Сколько времени занимает разработка сайта?', 'Лендинг — около недели, корпоративный сайт — две-три недели, интернет-магазин — от трёх недель. Точный срок называем в плане до начала работ.'),
              ('Сайт будет удобен с телефона?', 'Да. Большинство клиентов приходят со смартфонов, поэтому мобильную версию проектируем с самого начала, а не подгоняем в конце.'),
              ('Поможете с текстами и фото?', 'Да. Подскажем структуру, напишем тексты и подберём изображения, если своих материалов пока нет.'),
              ('Кому принадлежит сайт после запуска?', 'Вам. Домен, хостинг, исходный код и доступы оформляются на вас.')]),
    dict(slug='telegram-boty', img='bots', short='Боты Telegram и MAX',
         title='Разработка ботов для Telegram и MAX',
         meta_title='Разработка ботов для Telegram и MAX под ключ — Voriq',
         desc='Делаем ботов для Telegram и MAX: для заявок, записи, оплаты, рассылок и поддержки. Админка с заявками, интеграция с CRM и таблицами, запуск на сервере под ключ.',
         lead='Боты в Telegram и MAX, которые принимают заявки, записывают клиентов, принимают оплату и отвечают на вопросы круглосуточно. Вы получаете готовые заявки, а не переписку в чатах.',
         what=[('Бот заявок', 'Короткая анкета в 4–6 вопросов, проверка контактов и аккуратная карточка заявки вам в Telegram.'),
               ('Запись и бронирование', 'Выбор услуги, даты и времени, напоминания клиенту перед визитом.'),
               ('Приём оплаты', 'Оплата прямо в чате и автоматическое подтверждение заказа.'),
               ('Рассылки', 'Сообщения тем, кто уже писал боту: акции, новости, напоминания.'),
               ('Админка и CRM', 'Статусы заявок, поиск, выгрузка, связь с CRM и Google-таблицами.'),
               ('Поддержка клиентов', 'Ответы на частые вопросы и передача сложных случаев сотруднику.')],
         who=['Салонам, клиникам, студиям и мастерским с записью клиентов', 'Бизнесу, который теряет заявки ночью и в выходные', 'Магазинам, которым нужен каталог и заказ в мессенджере', 'Командам, которые вручную переносят заявки из чатов в таблицы'],
         cases=['maing', 'nohassle', 'apolline'], posts=['telegram-bot-dlya-biznesa', 'avtomatizaciya-zayavok-sajt-bot-crm', 'kak-podgotovit-tz-na-sajt-ili-bota'],
         faq=[('Сколько времени занимает разработка бота?', 'Бот заявок запускается примерно за неделю. Боты с оплатой, записью и интеграциями — от двух недель.'),
              ('Где будет работать бот?', 'На сервере, круглосуточно. Настраиваем размещение сами и следим, чтобы бот не падал.'),
              ('Можно посмотреть, как работает ваш бот?', 'Да — напишите нашему боту @voriq_applicationsBot: он сделан так же, как боты для клиентов.'),
              ('Делаете ботов для MAX?', 'Да. Делаем ботов и для Telegram, и для мессенджера MAX — можно один сценарий сразу в обоих, чтобы клиенты писали туда, где им удобнее.'),
              ('Бот сможет передавать заявки в CRM?', 'Да: amoCRM, Битрикс24, Google-таблицы и другие системы — подключаем при разработке.')]),
    dict(slug='ii-agenty', img='ai', short='ИИ-агенты',
         title='ИИ-агенты и ИИ-ассистенты для бизнеса',
         meta_title='ИИ-агенты для бизнеса: внедрение ИИ-ассистентов — Voriq',
         desc='Внедряем ИИ-агентов: ответы клиентам 24/7, разбор заявок, работа с документами и базой знаний, интеграция с Telegram, сайтом и CRM.',
         lead='ИИ-ассистенты, которые понимают вопросы клиентов своими словами, опираются на ваши документы и сами выполняют действия: отвечают, раскладывают заявки, заполняют CRM.',
         what=[('ИИ-консультант', 'Отвечает клиентам на сайте и в Telegram по вашей базе знаний, круглосуточно.'),
               ('Разбор входящих заявок', 'Читает обращения, определяет задачу и передаёт нужному сотруднику.'),
               ('Работа с документами', 'Находит ответы в регламентах, договорах и инструкциях за секунды.'),
               ('Квалификация лидов', 'Уточняет задачу, сроки и контакты до того, как подключится менеджер.'),
               ('Интеграции', 'Подключаем агента к Telegram, сайту, CRM и таблицам.'),
               ('Контроль качества', 'Смотрим реальные диалоги и дорабатываем ответы, оставляем путь к живому человеку.')],
         who=['Бизнесу с большим потоком однотипных вопросов', 'Командам, где сотрудники тонут в документах и регламентах', 'Отделам продаж, которым нужны уже квалифицированные заявки', 'Тем, кто хочет внедрить ИИ без хайпа и с понятным результатом'],
         cases=['velion', 'apolline', 'nohassle'], posts=['ii-agent-dlya-biznesa', 'telegram-bot-dlya-biznesa', 'avtomatizaciya-zayavok-sajt-bot-crm'],
         faq=[('Чем ИИ-агент отличается от обычного бота?', 'Обычный бот работает по кнопкам и сценарию. ИИ-агент понимает свободный текст, опирается на ваши документы и сам выполняет действия.'),
              ('Агент не будет выдумывать ответы?', 'Ограничиваем его вашей базой знаний и тестируем на реальных вопросах. Если ответа нет — агент передаёт диалог сотруднику.'),
              ('С чего начать внедрение?', 'С одной задачи, обычно с ответов на частые вопросы. Когда она работает, добавляем следующие.'),
              ('Данные клиентов в безопасности?', 'Обсуждаем, какие данные агенту можно видеть, и настраиваем доступы под ваши требования.')]),
    dict(slug='avtomatizaciya-biznesa', img='auto', short='Автоматизация',
         title='Автоматизация бизнес-процессов',
         meta_title='Автоматизация бизнес-процессов и заявок — Voriq',
         desc='Связываем сайт, ботов в Telegram и MAX, CRM, таблицы и оплату в один поток: заявки, уведомления, рассылки и отчёты без ручной работы.',
         lead='Связываем ваши сервисы в одну систему: заявки сами попадают в CRM, клиенту уходит ответ, команда получает уведомление, а отчёты собираются без ручного копирования.',
         what=[('Автоматизация заявок', 'Сайт, бот и мессенджеры собирают обращения в одно место.'),
               ('Интеграция с CRM', 'amoCRM, Битрикс24 или Google-таблицы — заявки со статусами и ответственными.'),
               ('Уведомления', 'Команда сразу узнаёт о новой заявке, оплате или задаче в Telegram.'),
               ('Оплата и документы', 'Счета, ссылки на оплату и подтверждения уходят автоматически.'),
               ('Парсеры и выгрузки', 'Собираем данные с сайтов и сервисов в таблицы по расписанию.'),
               ('Отчёты', 'Сколько заявок пришло, из каких каналов и что с ними стало.')],
         who=['Бизнесу, где заявки теряются между почтой, директом и мессенджерами', 'Командам, которые тратят часы на копирование данных', 'Руководителям, которым нужна понятная картина по заявкам', 'Тем, у кого уже есть CRM, но она живёт отдельно от сайта и бота'],
         cases=['maing', 'nohassle', 'apolline'], posts=['avtomatizaciya-zayavok-sajt-bot-crm', 'telegram-bot-dlya-biznesa', 'kak-podgotovit-tz-na-sajt-ili-bota'],
         faq=[('С чего начинается автоматизация?', 'С короткого разбора: куда приходят клиенты и что дальше происходит с заявкой. Обычно сразу видно, где теряется больше всего.'),
              ('Нужно ли менять CRM?', 'Нет. Подключаемся к той системе, что уже есть, или предлагаем простую — например, Google-таблицу.'),
              ('Что если какой-то сервис не поддерживает интеграцию?', 'Ищем обходной путь: выгрузки, парсеры, вебхуки. Если надёжного способа нет — говорим об этом честно.'),
              ('Кто будет поддерживать автоматизацию?', 'Мы остаёмся на связи после запуска, а все доступы и описание схемы передаём вам.')]),
    dict(slug='razrabotka-po', img='soft', short='Кастомный софт',
         title='Разработка программного обеспечения на заказ',
         meta_title='Разработка ПО на заказ: кабинеты, дашборды, парсеры — Voriq',
         desc='Пишем внутренние сервисы под задачи бизнеса: личные кабинеты, дашборды, админки, парсеры и интеграции по API. Код и доступы — ваши.',
         lead='Внутренние сервисы, которых нет в готовых решениях: личные кабинеты, админки, дашборды, парсеры и интеграции по API — под ваши процессы, а не наоборот.',
         what=[('Личные кабинеты', 'Кабинеты клиентов и партнёров: заказы, статусы, документы, оплаты.'),
               ('Админки', 'Удобное управление товарами, заявками, контентом и пользователями.'),
               ('Дашборды', 'Ключевые показатели бизнеса на одном экране, с обновлением в реальном времени.'),
               ('Парсеры', 'Сбор данных с сайтов, маркетплейсов и сервисов по расписанию.'),
               ('Интеграции по API', 'Связываем сервисы, у которых нет готовой интеграции между собой.'),
               ('Доработка существующего', 'Разбираемся в текущем коде и добавляем нужные функции.')],
         who=['Бизнесу, который перерос таблицы и готовые сервисы', 'Компаниям с уникальным процессом, под который нет коробки', 'Командам, которым нужна своя админка или кабинет клиента', 'Тем, кому нужно регулярно собирать и обрабатывать данные'],
         cases=['apolline', 'velion', 'maing'], posts=['avtomatizaciya-zayavok-sajt-bot-crm', 'kak-podgotovit-tz-na-sajt-ili-bota', 'ii-agent-dlya-biznesa'],
         faq=[('Как оценивается срок разработки?', 'После короткого созвона описываем функции по этапам и называем срок каждого этапа до начала работ.'),
              ('Можно начать с минимальной версии?', 'Да, и мы это рекомендуем: сначала главная функция, потом — остальное по мере использования.'),
              ('На чём пишете?', 'Подбираем технологии под задачу: Python, JavaScript/Node.js, React, PostgreSQL и другие проверенные инструменты.'),
              ('Кому принадлежит код?', 'Вам: исходники, репозиторий и доступы к серверу передаём заказчику.')]),
    dict(slug='podderzhka-sajtov', img='support', short='Поддержка и развитие',
         title='Поддержка и развитие сайтов и ботов',
         meta_title='Техническая поддержка и развитие сайтов и ботов — Voriq',
         desc='Поддерживаем сайты, ботов в Telegram и MAX и сервисы после запуска: доработки, обновления, мониторинг, исправление ошибок и аналитика.',
         lead='Запуск — это только начало. Следим, чтобы сайт и бот работали без сбоев, вносим правки, добавляем новые функции и показываем, что приносит заявки.',
         what=[('Доработки', 'Новые страницы, разделы, функции бота и интеграции по мере роста бизнеса.'),
               ('Мониторинг', 'Следим, что сайт открывается, а бот отвечает, и быстро реагируем на сбои.'),
               ('Обновления', 'Обновляем зависимости, хостинг и сертификаты, чтобы всё работало безопасно.'),
               ('Исправление ошибок', 'Разбираемся, что сломалось, и чиним — в том числе в чужом коде.'),
               ('Аналитика', 'Подключаем счётчики и показываем, сколько заявок приносят сайт и бот.'),
               ('Контент', 'Помогаем обновлять тексты, кейсы и статьи для блога.')],
         who=['Владельцам сайтов и ботов, у которых нет своего разработчика', 'Бизнесу, у которого подрядчик пропал после запуска', 'Тем, кто хочет развивать проект постепенно', 'Командам, которым нужен человек «на связи», а не разовая работа'],
         cases=['nohassle', 'apolline', 'maing'], posts=['skolko-vremeni-razrabotka-sajta', 'avtomatizaciya-zayavok-sajt-bot-crm', 'telegram-bot-dlya-biznesa'],
         faq=[('Берёте на поддержку проекты, сделанные не вами?', 'Да. Сначала смотрим код и инфраструктуру и честно говорим, что можно поддерживать, а что лучше переделать.'),
              ('Как быстро исправляете ошибки?', 'Срочные сбои — в приоритете. Сроки реакции обсуждаем и фиксируем заранее.'),
              ('Можно обращаться разово?', 'Да, можно с отдельной задачей, а можно договориться о регулярной поддержке.'),
              ('Как общаемся?', 'Один чат в Telegram для всех вопросов и понятный отчёт о сделанном.')]),
]

ICON = {'arrow': '<iconify-icon icon="solar:arrow-right-linear" width="18" class="transition-transform duration-500 group-hover:translate-x-1"></iconify-icon>'}


def service_url(slug):
    return f'/{slug}/'


def render():
    c = L['ru']
    posts = {p['slug']: p for p in load('ru')}
    pages = []
    for k, sv in enumerate(SERVICES):
        url = SITE + service_url(sv['slug'])
        faq_ld = [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in sv['faq']]
        ld = json.dumps({'@context': 'https://schema.org', '@graph': [
            {'@type': 'Service', 'name': sv['title'], 'description': sv['desc'], 'serviceType': sv['short'], 'url': url,
             'areaServed': 'RU', 'provider': {'@type': 'ProfessionalService', 'name': 'Voriq', 'url': SITE + '/', '@id': SITE + '/#org'}},
            {'@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Voriq', 'item': SITE + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Услуги', 'item': SITE + '/#assets'},
                {'@type': 'ListItem', 'position': 3, 'name': sv['short'], 'item': url}]},
            {'@type': 'FAQPage', 'mainEntity': faq_ld}]}, ensure_ascii=False)
        h = HEAD.format(lang='ru', title=html.escape(sv['meta_title']), desc=html.escape(sv['desc']), url=url,
                        alts=f'<link rel="alternate" hreflang="ru" href="{url}">', ogtype='website', locale='ru_RU', site=SITE, ld=ld,
                        home='/', base='/blog/', blog='Блог', switch=switch('ru', service_url(sv['slug']), '/en/'), cta_b='Оставить заявку')
        what = ''.join(f'''<div class="reveal rounded-[22px] bg-white border border-[#132a24]/10 p-6" style="--d:{i * 0.05:.2f}s"><h3 class="text-[19px] font-medium tracking-[-0.01em]">{html.escape(t)}</h3><p class="mt-2 text-[15px] text-[#879f98] leading-relaxed">{html.escape(d)}</p></div>''' for i, (t, d) in enumerate(sv['what']))
        who = ''.join(f'<li class="flex gap-3 py-3 border-b border-[#132a24]/10"><span class="mt-2 w-1.5 h-1.5 rounded-full bg-[#78A184] shrink-0"></span><span>{html.escape(x)}</span></li>' for x in sv['who'])
        steps = [('01', 'Задача', 'Пишете в Telegram или оставляете заявку — пары слов достаточно.'), ('02', 'План и сроки', 'Присылаем план работ и сроки до старта.'),
                 ('03', 'Разработка', 'Показываем промежуточные версии и вносим правки по ходу.'), ('04', 'Запуск', 'Запускаем, передаём доступы и остаёмся на связи.')]
        steps_h = ''.join(f'<div class="reveal border-t border-[#132a24]/15 pt-5" style="--d:{i * 0.06:.2f}s"><span class="text-[13px] font-medium text-[#78A184]">{n}</span><h3 class="mt-3 text-[19px] font-medium">{t}</h3><p class="mt-1.5 text-[15px] text-[#879f98] leading-relaxed">{d}</p></div>' for i, (n, t, d) in enumerate(steps))
        cases = ''.join(f'''<a href="{CASES[x][3]}" target="_blank" rel="noopener" class="reveal group block rounded-[22px] bg-white border border-[#132a24]/10 overflow-hidden transition-[transform,box-shadow] duration-700 hover:-translate-y-1 hover:shadow-[0_30px_60px_-30px_rgba(19,42,36,.35)]" style="--d:{i * 0.06:.2f}s"><div class="aspect-[1.5/1] overflow-hidden bg-[#e4ebe8]"><img src="{CASES[x][2]}" alt="Сайт {CASES[x][0]}" loading="lazy" class="w-full h-full object-cover object-top transition-transform duration-[1200ms] group-hover:scale-105"></div><div class="p-5"><h3 class="text-[18px] font-medium">{CASES[x][0]}</h3><p class="mt-1 text-[14px] text-[#879f98]">{CASES[x][1]}</p></div></a>''' for i, x in enumerate(sv['cases']))
        faq = ''.join(f'<details class="group py-4 border-b border-[#132a24]/10"><summary class="flex cursor-pointer list-none items-center justify-between gap-4 text-[17px] font-medium">{html.escape(q)}<iconify-icon icon="solar:add-circle-linear" width="20" class="shrink-0 transition-transform duration-500 group-open:rotate-45"></iconify-icon></summary><p class="mt-2 text-[15px] text-[#879f98] leading-relaxed">{html.escape(a)}</p></details>' for q, a in sv['faq'])
        rel_posts = ''.join(card(posts[s], c, 'ru', i) for i, s in enumerate(sv['posts']) if s in posts)
        others = ''.join(f'<a href="{service_url(o["slug"])}" class="inline-flex items-center rounded-full border border-[#132a24]/15 bg-white/70 px-4 h-10 text-[14px] font-medium hover:bg-[#132a24] hover:text-white transition-colors duration-500">{html.escape(o["short"])}</a>' for o in SERVICES if o['slug'] != sv['slug'])
        h += f'''<main>
<section class="relative overflow-hidden">
  <div class="absolute inset-0 -z-10 bg-[radial-gradient(600px_500px_at_5%_0%,#b9d3c2_0%,transparent_70%),radial-gradient(700px_600px_at_95%_30%,#cfe0d6_0%,transparent_70%)]"></div>
  <div class="max-w-6xl mx-auto px-5 sm:px-8 pt-10 sm:pt-14 pb-16 grid lg:grid-cols-[1.1fr_.9fr] gap-8 items-center">
    <div>
      <nav class="reveal text-[14px] text-[#879f98]" aria-label="breadcrumbs"><a href="/" class="hover:text-[#132a24]">Voriq</a> <span class="mx-1.5">/</span> <a href="/#assets" class="hover:text-[#132a24]">Услуги</a> <span class="mx-1.5">/</span> <span>{html.escape(sv["short"])}</span></nav>
      <h1 class="reveal mt-6 text-4xl sm:text-5xl lg:text-[60px] font-medium tracking-[-0.035em] leading-[1.03]" style="--d:.06s">{html.escape(sv["title"])}</h1>
      <p class="reveal mt-6 text-[18px] text-[#4b625b] leading-relaxed max-w-xl" style="--d:.12s">{html.escape(sv["lead"])}</p>
      <div class="reveal mt-8 flex flex-wrap gap-3" style="--d:.18s">
        <a href="/#contact" class="group inline-flex items-center gap-2 rounded-full bg-[#132a24] text-white text-[15px] font-medium px-7 h-14 hover:bg-[#274f44] transition-colors duration-500">Обсудить проект {ICON["arrow"]}</a>
        <a href="{BOT}?start={sv["slug"]}" target="_blank" rel="noopener" class="inline-flex items-center gap-2 rounded-full border border-[#132a24]/20 text-[15px] font-medium px-7 h-14 hover:bg-[#132a24] hover:text-white transition-colors duration-500"><iconify-icon icon="simple-icons:telegram" width="16"></iconify-icon>Написать боту</a>
      </div>
    </div>
    <img src="/media/services/{sv["img"]}.webp" alt="{html.escape(sv["short"])} — иллюстрация" width="820" height="615" class="reveal w-full max-w-[520px] mx-auto" style="--d:.2s">
  </div>
</section>
<section class="max-w-6xl mx-auto px-5 sm:px-8 py-16">
  <h2 class="reveal text-3xl sm:text-4xl font-medium tracking-[-0.03em]">Что делаем</h2>
  <div class="mt-8 grid sm:grid-cols-2 lg:grid-cols-3 gap-4">{what}</div>
</section>
<section class="max-w-6xl mx-auto px-5 sm:px-8 py-10 grid lg:grid-cols-2 gap-12">
  <div><h2 class="reveal text-3xl sm:text-4xl font-medium tracking-[-0.03em]">Кому подходит</h2><ul class="reveal mt-6 text-[17px] text-[#3f5a52]">{who}</ul></div>
  <div><h2 class="reveal text-3xl sm:text-4xl font-medium tracking-[-0.03em]">Как работаем</h2><div class="mt-6 grid sm:grid-cols-2 gap-x-8 gap-y-6">{steps_h}</div></div>
</section>
<section class="max-w-6xl mx-auto px-5 sm:px-8 py-16">
  <h2 class="reveal text-3xl sm:text-4xl font-medium tracking-[-0.03em]">Примеры работ</h2>
  <div class="mt-8 grid sm:grid-cols-2 lg:grid-cols-3 gap-5">{cases}</div>
</section>
<section class="max-w-6xl mx-auto px-5 sm:px-8 py-10">
  <h2 class="reveal text-3xl sm:text-4xl font-medium tracking-[-0.03em]">Частые вопросы</h2>
  <div class="mt-6 border-t border-[#132a24]/10 grid md:grid-cols-2 gap-x-10">{faq}</div>
</section>
<section class="max-w-6xl mx-auto px-5 sm:px-8">
  {cta("ru", c)}
  <h2 class="mt-20 text-[28px] font-medium tracking-[-0.02em]">Полезно почитать</h2>
  <div class="mt-6 grid sm:grid-cols-2 lg:grid-cols-3 gap-5">{rel_posts}</div>
  <h2 class="mt-16 text-[22px] font-medium tracking-[-0.02em]">Другие услуги</h2>
  <div class="mt-5 mb-24 flex flex-wrap gap-2">{others}</div>
</section>
</main>''' + FOOT.format(home='/', privacy='/privacy/', privacy_t='Политика конфиденциальности')
        pages.append((service_url(sv['slug']), f'{sv["slug"]}/index.html', h))
    return pages
