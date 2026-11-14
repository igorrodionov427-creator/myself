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
  const LOADED = Date.now(); let LAST = 0, SENT = 0;   // антиспам, только в памяти страницы
  const isEN = document.documentElement.lang === 'en';
  const L = (ru, en) => isEN ? en : ru;            // тексты для английской версии

  /* способ связи: подсказка, клавиатура и проверка зависят от выбора */
  const ctype = () => (form.querySelector('input[name=ctype]:checked') || {}).value || 'Telegram';
  const CT = {
    Telegram: [L('@ваш_ник или номер телефона', '@username or phone number'), 'text', L('Ваш ник в Telegram', 'Your Telegram username')],
    'Телефон': [L('+7 900 123-45-67', '+1 555 123 4567'), 'tel', L('Ваш номер телефона', 'Your phone number')],
    WhatsApp: [L('+7 900 123-45-67', '+1 555 123 4567'), 'tel', L('Номер в WhatsApp', 'Your WhatsApp number')],
    MAX: [L('Номер или ссылка на профиль', 'Phone or profile link'), 'text', L('Ваш контакт в MAX', 'Your MAX contact')],
    Email: [L('name@example.ru', 'name@example.com'), 'email', L('Ваш email', 'Your email')],
    'Другое': [L('Например: VK — vk.com/ivan, или «звоните после 18:00»', 'E.g. LinkedIn, Signal, or “call after 6 pm”'), 'text', L('Где с вами связаться', 'Where to reach you')],
  };
  const applyCtype = () => {
    const [ph, mode, lbl] = CT[ctype()], inp = form.elements.contact;
    inp.placeholder = ph; inp.inputMode = mode === 'tel' ? 'tel' : mode === 'email' ? 'email' : 'text';
    inp.autocomplete = mode === 'tel' ? 'tel' : mode === 'email' ? 'email' : 'off';
    document.getElementById('l-contact').textContent = lbl;
    if (form.querySelector('[data-f="contact"]').classList.contains('bad') && inp.value) check('contact');
  };
  form.querySelectorAll('input[name=ctype]').forEach(r => r.addEventListener('change', () => { applyCtype(); form.elements.contact.focus(); }));

  const rules = {
    name: v => v.trim().length >= 2 || L('Напишите, как к вам обращаться', 'Please enter your name'),
    contact: v => {
      const s = v.trim(), t = ctype();
      if (!s) return L('Оставьте контакт, чтобы мы могли ответить', 'Leave a contact so we can reply');
      const phone = s.replace(/[^\d]/g, '').length >= 10 && /^[\d\s()+-]+$/.test(s);
      if (t === 'Telegram') return /^@?[A-Za-z0-9_]{5,32}$/.test(s) || phone || L('Укажите ник в Telegram (например, @ivan_petrov) или номер', 'Enter a Telegram username (e.g. @john_smith) or phone');
      if (t === 'Телефон' || t === 'WhatsApp') return phone || L('Укажите номер телефона, например +7 900 123-45-67', 'Enter a phone number with country code');
      if (t === 'Email') return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s) || L('Похоже, в адресе почты ошибка', 'That email address looks wrong');
      if (t === 'MAX') return phone || s.length >= 3 || L('Укажите номер или ссылку на профиль в MAX', 'Enter a phone or MAX profile link');
      return s.length >= 3 || L('Напишите, где и как с вами связаться', 'Tell us where and how to reach you');
    },
    consent: (_, el) => el.checked || L('Нужно согласие на обработку данных', 'Please agree to data processing'),
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
    const text = `🆕 Заявка с сайта Voriq (форма)\n\n👤 Имя: ${lead.name}\n📱 Связь: ${lead.ctype} — ${lead.contact}\n📂 Тип: ${lead.type}\n📝 Задача: ${lead.msg}${isEN ? '\n🌍 Язык сайта: EN' : ''}\n\n🌐 ${lead.page}`;
    const tg = lead.ctype === 'Telegram' && /^@?[A-Za-z0-9_]{5,32}$/.test(lead.contact);
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
    const now = Date.now();
    if (now - LOADED < 3000) return;                   // слишком быстро для человека — спам-бот
    if (SENT >= 3) { status.className = 'form-status bad'; status.textContent = L('Вы уже отправили несколько заявок. Мы скоро ответим — или напишите нам в Telegram.', 'You have already sent a few requests. We’ll reply soon — or message us on Telegram.'); return; }
    if (now - LAST < 60000) { status.className = 'form-status bad'; status.textContent = L('Подождите минуту перед следующей заявкой.', 'Please wait a minute before sending another request.'); return; }
    const bad = Object.keys(rules).filter(n => !check(n));
    if (bad.length) { status.className = 'form-status bad'; status.textContent = L('Проверьте отмеченные поля', 'Please check the highlighted fields'); form.elements[bad[0]].focus(); return; }

    const lead = {
      name: form.elements.name.value.trim().slice(0, 100),
      contact: form.elements.contact.value.trim().slice(0, 120),
      ctype: ctype(),
      type: (form.querySelector('input[name=type]:checked') || {}).value || '—',
      msg: form.elements.msg.value.trim().slice(0, 2000) || '—',
      page: location.href,
    };
    busy = true; btn.disabled = true; btn.setAttribute('aria-busy', 'true');
    const prevIcon = btn.querySelector('svg'); prevIcon.style.display = 'none';
    const sp = document.createElement('span'); sp.className = 'spin'; sp.setAttribute('aria-hidden', 'true'); btn.appendChild(sp);
    btnLabel.textContent = L('Отправляем…', 'Sending…'); status.className = 'form-status'; status.textContent = '';
    try {
      if (cfg.endpoint) await sendToServer(lead);
      else if (cfg.telegramFallback) await sendToTelegram(lead);
      else throw new Error('нет способа отправки');
      LAST = Date.now(); SENT++;
      form.reset(); applyCtype();
      form.classList.add('sent');
      okBox.focus();
    } catch (err) {
      status.className = 'form-status bad';
      status.innerHTML = L('Не получилось отправить. Напишите нам в', 'Couldn’t send. Please message us on') + ' <a href="https://t.me/rydr3" target="_blank" rel="noopener">Telegram</a>' + L(' — ответим там.', ' — we’ll reply there.');
    } finally {
      busy = false; btn.disabled = false; btn.removeAttribute('aria-busy');
      sp.remove(); prevIcon.style.display = ''; btnLabel.textContent = L('Отправить заявку', 'Send request');
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
