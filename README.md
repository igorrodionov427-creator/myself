# Voriq — voriq.ru

Сайт агентства: сайты, боты, автоматизация. Статика (`index.html`, `media/`) + Cloudflare Pages Function `functions/api/lead.js` (заявки с формы → Telegram-бот).

## Cloudflare Pages
- Build command: пусто, output directory: `/`
- Variables and Secrets (Production): `TG_BOT_TOKEN` (secret), `TG_CHAT_ID`
- Custom domain: `voriq.ru`
