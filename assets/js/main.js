/* Шапка, мобильное меню, появление секций, FAQ, cookie, ссылки проектов. */
(() => {
  const $ = id => document.getElementById(id);
  const root = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* шапка: фон после начала прокрутки */
  const hdr = $('hdr');
  const onScroll = () => hdr.classList.toggle('scrolled', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* мобильное меню */
  const burger = $('burger'), mnav = $('mnav');
  mnav.hidden = false;
  mnav.setAttribute('aria-hidden', 'true'); mnav.inert = true;
  const setMenu = open => {
    root.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
    mnav.setAttribute('aria-hidden', String(!open)); mnav.inert = !open;
    if (open) mnav.querySelector('a').focus({ preventScroll: true });
  };
  burger.addEventListener('click', () => setMenu(!root.classList.contains('menu-open')));
  mnav.addEventListener('click', e => { if (e.target.closest('a')) setMenu(false); });
  addEventListener('keydown', e => { if (e.key === 'Escape' && root.classList.contains('menu-open')) { setMenu(false); burger.focus(); } });
  matchMedia('(min-width: 960px)').addEventListener('change', e => { if (e.matches) setMenu(false); });

  /* появление при прокрутке */
  const els = document.querySelectorAll('.rv');
  if (reduce || !('IntersectionObserver' in window)) els.forEach(el => el.classList.add('in'));
  else {
    const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }), { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    els.forEach(el => io.observe(el));
  }

  /* hero: вход один раз (WAAPI), затем стили возвращаются к авторскому CSS */
  (() => {
    if (!root.classList.contains('pre')) return;
    const q = sel => document.querySelector(sel), qa = sel => [...document.querySelectorAll(sel)];
    const EXPO = 'cubic-bezier(.16,1,.3,1)', SOFT = 'cubic-bezier(.22,.7,.25,1)', GLASS = 'cubic-bezier(.2,.75,.28,1)';
    const s = matchMedia('(max-width: 640px)').matches ? .86 : 1;
    const running = [];
    const anim = (el, kf, dur, delay, easing) => { if (el) running.push(el.animate(kf, { duration: dur * s, delay: delay * s, easing, fill: 'both' })); };
    const rise = (el, delay, dur) => anim(el, [{ clipPath: 'inset(100% 0 -14% 0)', translate: '0 .16em' }, { clipPath: 'inset(-18% 0 -14% 0)', translate: '0 0' }], dur, delay, EXPO);
    const lift = (el, delay, dist = '.7em', dur = 560) => anim(el, [{ opacity: 0, translate: '0 ' + dist }, { opacity: 1, translate: '0 0' }], dur, delay, SOFT);
    const settle = (el, delay, dur = 760, from = .985, dist = '1.1em') => anim(el, [{ opacity: 0, scale: from, translate: '0 ' + dist }, { opacity: 1, scale: 1, translate: '0 0' }], dur, delay, GLASS);
    lift(q('.hdr'), 60, '-.4em', 600);
    lift(q('.hero .eyebrow'), 300, '.8em', 520);
    qa('.hero h1 .ln').forEach((l, i) => rise(l, 380 + i * 90, 980));
    settle(q('.hero .play'), 720, 640, .88, '.3em');
    lift(q('.hero .tag'), 770, '.7em', 560);
    settle(q('.hero .panel'), 800, 880, .982, '1.4em');
    qa('.hero .ev').forEach((e, i) => settle(e, 1000 + i * 90, 640, .97, '.5em'));
    anim(q('.hero .dot'), [{ scale: 0 }, { scale: 1 }], 520, 1080, EXPO);
    anim(q('.hero .track i'), [{ scale: '0 1' }, { scale: '1 1' }], 820, 1120, EXPO);
    qa('.hero .num').forEach((n, i) => rise(n, 920 + i * 70, 860));
    qa('.hero .lbl').forEach((l, i) => lift(l, 1030 + i * 45, '.6em', 520));
    anim(q('.hero .slash'), [{ scale: '1 0' }, { scale: '1 1' }], 700, 1010, EXPO);
    settle(q('.hero .meet'), 1140, 820, .985, '1.2em');
    Promise.all(running.map(a => a.finished.catch(() => {}))).then(() => {
      root.classList.remove('pre'); running.forEach(a => a.cancel()); running.length = 0;
    });
  })();

  /* фон-видео: при reduced-motion стоит на первом кадре; фоновая вкладка подхватывает воспроизведение при показе */
  (() => {
    const v = document.querySelector('.hero video.bg'); if (!v) return;
    const mq = matchMedia('(prefers-reduced-motion: reduce)');
    const sync = () => { if (mq.matches) { v.pause(); v.currentTime = 0; } else v.play().catch(() => {}); };
    mq.addEventListener('change', sync);
    document.addEventListener('visibilitychange', () => { if (!document.hidden) sync(); });
    v.addEventListener('canplay', sync); sync();
  })();

  /* этапы: шкала и номера заполняются при появлении */
  const steps = $('steps');
  if (steps) {
    const items = steps.querySelectorAll('.step');
    const run = () => { steps.classList.add('on'); items.forEach((s, i) => setTimeout(() => s.classList.add('on'), reduce ? 0 : 250 + i * 300)); };
    if (reduce || !('IntersectionObserver' in window)) run();
    else { const so = new IntersectionObserver(es => { if (es[0].isIntersecting) { run(); so.disconnect(); } }, { threshold: .35 }); so.observe(steps); }
  }

  /* FAQ-аккордеон: одна открытая панель, стрелки ↑↓ между вопросами */
  const acc = $('acc');
  if (acc) {
    const btns = [...acc.querySelectorAll('.acc-btn')];
    const toggle = (b, open) => { b.setAttribute('aria-expanded', String(open)); b.closest('.acc-item').classList.toggle('open', open); };
    btns.forEach((b, i) => {
      b.addEventListener('click', () => { const open = b.getAttribute('aria-expanded') !== 'true'; btns.forEach(o => o !== b && toggle(o, false)); toggle(b, open); });
      b.addEventListener('keydown', e => {
        const k = { ArrowDown: i + 1, ArrowUp: i - 1, Home: 0, End: btns.length - 1 }[e.key];
        if (k !== undefined) { e.preventDefault(); btns[(k + btns.length) % btns.length].focus(); }
      });
    });
    toggle(btns[0], true);
  }

  /* ссылки проектов, адрес которых не хранится в разметке */
  document.querySelectorAll('[data-go]').forEach(a => a.addEventListener('click', e => {
    e.preventDefault();
    const g = a.dataset.go.split(',');
    window.open('https://' + g[2] + g[1] + '.' + g[0] + '/', '_blank', 'noopener');
  }));

  /* hero-виджет: заявка → бот → CRM, строки появляются по очереди и повторяются */
  const feed = $('feed');
  if (feed && !reduce) {
    const evs = [...feed.children], bar = feed.parentElement.querySelector('.track i');
    let step = 0, timer = 0;
    const tick = () => {
      if (step === 0) { evs.forEach(e => e.classList.remove('on')); bar.style.transform = 'scaleX(0)'; }
      else if (step <= evs.length) { evs[step - 1].classList.add('on'); bar.style.transform = `scaleX(${step / evs.length})`; }
      step = step > evs.length + 2 ? 0 : step + 1;           // после последней строки — пауза, затем заново
      timer = setTimeout(tick, step === 1 ? 500 : 1300);
    };
    const start = () => { clearTimeout(timer); feed.classList.add('cycling'); step = 0; tick(); };
    setTimeout(start, root.classList.contains('pre') ? 2600 : 600);
    document.addEventListener('visibilitychange', () => { if (document.hidden) clearTimeout(timer); else start(); });
  }

  /* блик на карточке основателя следует за курсором */
  const ph = document.querySelector('.ph');
  if (ph && !reduce && matchMedia('(hover: hover)').matches) ph.addEventListener('pointermove', e => {
    const r = ph.getBoundingClientRect();
    ph.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100) + '%'); ph.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100) + '%');
  });

  /* cookie: показываем при каждом заходе, ничего не сохраняем */
  const ck = $('cookie');
  if (ck) { setTimeout(() => ck.classList.add('on'), 900); $('cookieOk').addEventListener('click', () => ck.classList.remove('on')); }
})();
