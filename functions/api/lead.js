// Cloudflare Pages Function: POST /api/lead -> Telegram bot.
// Secrets (Pages → Settings → Variables and Secrets): TG_BOT_TOKEN, TG_CHAT_ID.
const clip = (v, n) => String(v ?? '').trim().slice(0, n);

export async function onRequestPost({ request, env }) {
  let data;
  try { data = await request.json(); } catch { return json({ ok: false, error: 'bad_json' }, 400); }

  if (data.website) return json({ ok: true }); // honeypot: bots fill hidden field
  const name = clip(data.name, 100), contact = clip(data.contact, 120);
  const type = clip(data.type, 60) || '—', msg = clip(data.msg, 2000) || '—', page = clip(data.page, 200);
  if (!name || !contact) return json({ ok: false, error: 'required' }, 400);
  if (!env.TG_BOT_TOKEN || !env.TG_CHAT_ID) return json({ ok: false, error: 'not_configured' }, 500);

  const text = `🆕 Заявка с сайта Voriq\n\n👤 Имя: ${name}\n📱 Контакт: ${contact}\n📂 Тип: ${type}\n📝 Задача: ${msg}\n\n🌐 ${page}`;
  const r = await fetch(`https://api.telegram.org/bot${env.TG_BOT_TOKEN}/sendMessage`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ chat_id: env.TG_CHAT_ID, text, disable_web_page_preview: true }),
  });
  const j = await r.json().catch(() => ({}));
  return j.ok ? json({ ok: true }) : json({ ok: false, error: 'telegram' }, 502);
}

export const onRequest = () => json({ ok: false, error: 'method' }, 405);

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { 'content-type': 'application/json; charset=utf-8' } });
}
