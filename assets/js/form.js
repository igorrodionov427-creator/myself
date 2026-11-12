/* Форма заявки: проверка полей, отправка, состояния. */
(() => {
  const form = document.getElementById('form');
  if (!form) return;
  const cfg = window.VORIQ_FORM || {};
  const btn = document.getElementById('formBtn');
  const status = document.getElementById('formStatus');
  const okBox = document.getElementById('formOk');
  const btnLabel = btn.querySelector('.lbl-t');
  let busy = false;

  const rules = {
    name: v => v.trim().length >= 2 || 'Напишите, как к вам обращаться',
    contact: v => {
      const s = v.trim();
      if (!s) return 'Оставьте контакт, чтобы мы могли ответить';
      const tg = /^@?[A-Za-z0-9_]{5,32}$/.test(s);
      const phone = s.replace(/[^\d]/g, '').length >= 10 && /^[\d\s()+-]+$/.test(s);
      const mail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);
      return tg || phone || mail || 'Укажите @ник в Telegram, телефон или email';
    },
    consent: (_, el) => el.checked || 'Нужно согласие на обработку данных',
  };

  const setErr = (name, msg) => {
    const fld = form.querySelector(`[data-f="${name}"]`);
    const el = form.elements[name];
    fld.classList.toggle('bad', !!msg);
    el.setAttribute('aria-invalid', msg ? 'true' : 'false');
    document.getElementById('e-' + name).textContent = msg || '';
  };
  const check = name => {
    const el = form.elements[name];
    const r = rules[name](el.value, el);
    setErr(name, r === true ? '' : r);
    return r === true;
  };
  Object.keys(rules).forEach(n => {
    const el = form.elements[n];
    el.addEventListener(el.type === 'checkbox' ? 'change' : 'blur', () => { if (el.value || el.type === 'checkbox') check(n); });
    el.addEventListener('input', () => { if (form.querySelector(`[data-f="${n}"]`).classList.contains('bad')) check(n); });
  });

  /* ---- транспорт: свой сервер или прежний бот ---- */
  const _k = [55, 97, 91, 248, 205, 65, 75, 241, 153];
  const _p = [[139, 244, 9, 10, 176, 163, 1, 88, 110, 200, 252, 116, 115, 192, 168, 14], [126, 9, 16, 169, 168, 57, 42, 195, 160, 98, 85, 62, 141, 189, 34], [30, 162, 227, 127, 37, 30, 190, 248, 23, 32, 158, 172, 127, 20, 31]];
  const _o = [1, 2, 0];
  const _c = [6, 82, 108, 206, 245, 117, 121, 199, 174, 2];
  const _d = arr => arr.map((n, i) => String.fromCharCode(n ^ _k[i % _k.length])).join('');
  const _t = () => _d(_o.flatMap(i => _p[i])).split('').reverse().join('');

  async function sendToServer(lead) {
    const r = await fetch(cfg.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(lead) });
    if (!r.ok) throw new Error('HTTP ' + r.status);
  }
  async function sendToTelegram(lead) {
    const text = `🆕 Заявка с сайта Voriq (форма)\n\n👤 Имя: ${lead.name}\n📱 Контакт: ${lead.contact}\n📂 Тип: ${lead.type}\n📝 Задача: ${lead.msg}\n\n🌐 ${lead.page}`;
    const tg = /^@?[A-Za-z0-9_]{5,32}$/.test(lead.contact);
    const body = new URLSearchParams({ chat_id: _d(_c), text, disable_web_page_preview: 'true' });
    if (tg) body.set('reply_markup', JSON.stringify({ inline_keyboard: [[{ text: '💬 Написать клиенту', url: 'https://t.me/' + lead.contact.replace('@', '') }]] }));
    const r = await fetch('https://api.telegram.org/bot' + _t() + '/sendMessage', { method: 'POST', body });
    const j = await r.json();
    if (!j.ok) throw new Error(j.description || 'telegram error');
  }

  form.addEventListener('submit', async e => {
    e.preventDefault();
    if (busy) return;                                  // защита от повторной отправки
    if (form.elements.website.value) return;           // ловушка для ботов
    const bad = Object.keys(rules).filter(n => !check(n));
    if (bad.length) { status.className = 'form-status bad'; status.textContent = 'Проверьте отмеченные поля'; form.elements[bad[0]].focus(); return; }

    const lead = {
      name: form.elements.name.value.trim().slice(0, 100),
      contact: form.elements.contact.value.trim().slice(0, 120),
      type: (form.querySelector('input[name=type]:checked') || {}).value || '—',
      msg: form.elements.msg.value.trim().slice(0, 2000) || '—',
      page: location.href,
    };
    busy = true; btn.disabled = true; btn.setAttribute('aria-busy', 'true');
    const prevIcon = btn.querySelector('svg'); prevIcon.style.display = 'none';
    const sp = document.createElement('span'); sp.className = 'spin'; sp.setAttribute('aria-hidden', 'true'); btn.appendChild(sp);
    btnLabel.textContent = 'Отправляем…'; status.className = 'form-status'; status.textContent = '';
    try {
      if (cfg.endpoint) await sendToServer(lead);
      else if (cfg.telegramFallback) await sendToTelegram(lead);
      else throw new Error('нет способа отправки');
      form.reset();
      form.classList.add('sent');
      okBox.focus();
    } catch (err) {
      status.className = 'form-status bad';
      status.innerHTML = 'Не получилось отправить. Напишите нам в <a href="https://t.me/rydr3" target="_blank" rel="noopener">Telegram</a> — ответим там.';
    } finally {
      busy = false; btn.disabled = false; btn.removeAttribute('aria-busy');
      sp.remove(); prevIcon.style.display = ''; btnLabel.textContent = 'Отправить заявку';
    }
  });

  document.getElementById('formAgain').addEventListener('click', () => {
    form.classList.remove('sent'); status.textContent = '';
    form.elements.name.focus();
  });

  /* карточки услуг выбирают тип проекта в форме */
  document.querySelectorAll('[data-type]').forEach(a => a.addEventListener('click', () => {
    const r = form.querySelector(`input[name=type][value="${a.dataset.type}"]`);
    if (r) r.checked = true;
  }));
})();
