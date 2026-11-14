/* Шапка, мобильное меню, появление секций, FAQ, cookie, ссылки проектов. */
(() => {
  const $ = id => document.getElementById(id);
  const root = document.documentElement;
  const reduce = /[?&]static/.test(location.search);   // анимации всегда, как на v3; ?static=1 — без них

  /* шапка: фон после начала прокрутки */
  const hdr = $('hdr');
  const onScroll = () => hdr.classList.toggle('scrolled', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* мобильное меню */
  const burger = $('burger'), mnav = $('mnav');
  mnav.hidden = false;
  mnav.setAttribute('aria-hidden', 'true'); mnav.inert = true;
  let lockY = 0;
  const links = [...mnav.querySelectorAll('a.ml, .btn')];
  const setMenu = open => {
    if (open === root.classList.contains('menu-open')) return;
    if (open) { lockY = scrollY; document.body.style.cssText += `;position:fixed;top:${-lockY}px;left:0;right:0;width:100%`; }
    else { document.body.style.position = document.body.style.top = document.body.style.left = document.body.style.right = document.body.style.width = ''; scrollTo({ top: lockY, behavior: 'instant' }); }
    links.forEach((el, i) => el.style.transitionDelay = open ? (0.06 + i * 0.045) + 's' : '0s');
    root.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', String(open));
    const en = root.lang === 'en';
    burger.setAttribute('aria-label', open ? (en ? 'Close menu' : 'Закрыть меню') : (en ? 'Open menu' : 'Открыть меню'));
    mnav.setAttribute('aria-hidden', String(!open)); mnav.inert = !open;
  };
  const dim = $('mnavDim'); if (dim) dim.addEventListener('click', () => setMenu(false));
  burger.addEventListener('click', () => setMenu(!root.classList.contains('menu-open')));
  mnav.addEventListener('click', e => {
    const a = e.target.closest('a'); if (!a) return;
    const url = new URL(a.href, location.href);
    if (url.pathname === location.pathname && url.hash) {          // якорь на этой же странице: закрыть меню и доехать
      e.preventDefault(); setMenu(false);
      const el = document.querySelector(url.hash);
      if (el) requestAnimationFrame(() => { scrollTo({ top: el.getBoundingClientRect().top + scrollY - 80, behavior: 'smooth' }); history.replaceState(null, '', url.hash); });
    } else setMenu(false);
  });
  addEventListener('keydown', e => { if (e.key === 'Escape' && root.classList.contains('menu-open')) { setMenu(false); burger.focus(); } });
  matchMedia('(min-width: 1280px)').addEventListener('change', e => { if (e.matches) setMenu(false); });

  /* появление при прокрутке */
  const els = document.querySelectorAll('.rv');
  if (reduce || !('IntersectionObserver' in window)) els.forEach(el => el.classList.add('in'));
  else {
    const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }), { rootMargin: innerWidth < 760 ? '0px 0px 15% 0px' : '0px 0px -8% 0px', threshold: innerWidth < 760 ? 0 : .08 });
    els.forEach(el => io.observe(el));
    window.__rvObserve = el => io.observe(el);
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
    anim(q('.hero .dot'), [{ scale: 0 }, { scale: 1 }], 520, 1080, EXPO);
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
    const sync = () => v.play().catch(() => {});
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

  /* карточка «Пример автоматизации»: шаги появляются по очереди один раз */
  const feed = $('feed');
  if (feed && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const evs = [...feed.children];
    feed.classList.add('seq'); evs.forEach(e => e.classList.remove('on'));
    const t0 = root.classList.contains('pre') ? 2200 : 500;
    evs.forEach((e, i) => setTimeout(() => e.classList.add('on'), t0 + i * 1100));
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

/* ===== анимации как на v3: инерционное колесо, плавные якоря, прогресс, заголовки по словам ===== */
(() => {
  const reduce = /[?&]static/.test(location.search);   // анимации всегда, как на v3; ?static=1 — без них
  const HDR = 88;

  /* прогресс прокрутки */
  const prog = document.getElementById('progress');
  if (prog) { const on = () => { const m = document.documentElement.scrollHeight - innerHeight; prog.style.transform = `scaleX(${m > 0 ? scrollY / m : 0})`; };
    addEventListener('scroll', on, { passive: true }); addEventListener('resize', on); on(); }

  /* заголовки секций появляются по словам */
  document.querySelectorAll('main .h2').forEach(h => {
    if (reduce || h.closest('.hero')) return;
    let wi = 0;
    const walk = node => [...node.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(part => {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
          const w = document.createElement('span'); w.className = 'w';
          const i = document.createElement('span'); i.textContent = part; i.style.setProperty('--wd', (wi++ * 0.06) + 's');
          w.appendChild(i); frag.appendChild(w);
        });
        n.replaceWith(frag);
      } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
    });
    walk(h); h.classList.add('words');
    if (!h.classList.contains('rv')) { h.classList.add('rv'); window.__rvObserve && window.__rvObserve(h); }
  });

  if (reduce) return;

  /* инерционная прокрутка колесом (мышь на компьютере) */
  let wTarget = scrollY, wCur = scrollY, wRunning = false;
  const wheelStop = () => { wRunning = false; };
  const maxY = () => document.documentElement.scrollHeight - innerHeight;
  const glide = () => {
    if (!wRunning) return;
    if (Math.abs(scrollY - Math.round(wCur)) > 3) { wRunning = false; return; }   // прокрутили иначе — отдаём управление
    wCur += (wTarget - wCur) * .09;
    if (Math.abs(wTarget - wCur) < .5) { wCur = wTarget; wRunning = false; }
    scrollTo({ top: wCur, behavior: 'instant' });
    if (wRunning) requestAnimationFrame(glide);
  };
  addEventListener('wheel', e => {
    if (e.ctrlKey || Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
    if (document.documentElement.classList.contains('menu-open')) return;
    if (e.target.closest && e.target.closest('textarea,.tbl,.mnav')) return;
    e.preventDefault();
    if (!wRunning) wTarget = wCur = scrollY;
    wTarget = Math.max(0, Math.min(maxY(), wTarget + e.deltaY * (e.deltaMode === 1 ? 40 : 1)));
    if (!wRunning) { wRunning = true; requestAnimationFrame(glide); }
  }, { passive: false });
  addEventListener('keydown', wheelStop); addEventListener('pointerdown', wheelStop);

  /* якоря плавно доезжают до секции; колесо/касание прерывает */
  let run = 0;
  const easeIO = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  ['wheel', 'touchstart'].forEach(ev => addEventListener(ev, () => { run++; }, { passive: true }));
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href]'); if (!a || e.defaultPrevented) return;
    const url = new URL(a.href, location.href);
    if (url.pathname !== location.pathname || !url.hash || a.target === '_blank') return;
    const el = document.querySelector(url.hash); if (!el) return;
    e.preventDefault(); wheelStop();
    const off = el.id === 'main' ? 0 : HDR - 8, target = () => el.getBoundingClientRect().top + scrollY - off;
    const from = scrollY, d0 = target() - from;
    const dur = Math.min(1600, 650 + Math.abs(d0) * .2), t0 = performance.now(), my = ++run;
    // цель пересчитывается каждый кадр: пока едем, ниже могут догрузиться картинки и сдвинуть секцию
    const step = now => { if (my !== run) return; const k = Math.min(1, (now - t0) / dur);
      scrollTo({ top: from + (target() - from) * easeIO(k), behavior: 'instant' });
      if (k < 1) requestAnimationFrame(step); else setTimeout(() => { if (my === run && Math.abs(target() - scrollY) > 2) scrollTo({ top: target(), behavior: 'instant' }); }, 250); };
    requestAnimationFrame(step);
    history.replaceState(null, '', url.hash);
  });
})();

/* ===== просмотр фото (лайтбокс) на «Наших работах» и в карточках проектов ===== */
(() => {
  const sel = '.bshot-ph img, .wshot img, .ishots img, #sites .pf-shot img';
  const imgs = [...document.querySelectorAll(sel)];
  if (!imgs.length) return;
  const en = document.documentElement.lang === 'en';
  const lb = document.createElement('div');
  lb.className = 'lb'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', en ? 'Image viewer' : 'Просмотр изображения');
  lb.innerHTML = `<div class="lb-stage"><img alt=""></div>
    <button class="lb-btn lb-x" type="button" aria-label="${en ? 'Close' : 'Закрыть'}">✕</button>
    <button class="lb-btn lb-prev" type="button" aria-label="${en ? 'Previous' : 'Предыдущее'}">‹</button>
    <button class="lb-btn lb-next" type="button" aria-label="${en ? 'Next' : 'Следующее'}">›</button>
    <div class="lb-cap"><span class="lb-n"></span><span class="lb-t"></span><span class="lb-hint">${en ? 'Tap the image to zoom' : 'Нажмите на фото, чтобы приблизить'}</span></div>`;
  document.body.appendChild(lb);
  const stage = lb.querySelector('.lb-stage'), big = stage.querySelector('img');
  let i = 0, lastFocus = null;
  const caption = el => {
    const c = el.closest('figure')?.querySelector('figcaption');
    if (!c) return el.alt || '';
    const parts = [...c.children].filter(x => !x.classList.contains('bshot-n')).map(x => x.textContent.trim()).filter(Boolean);
    return parts.length ? parts.join(' · ') : c.textContent.trim();
  };
  const unzoom = () => { lb.classList.remove('z'); big.style.width = ''; };
  const show = k => {
    i = (k + imgs.length) % imgs.length; unzoom();
    big.src = imgs[i].currentSrc || imgs[i].src; big.alt = imgs[i].alt;
    lb.querySelector('.lb-n').textContent = (i + 1) + ' / ' + imgs.length;
    lb.querySelector('.lb-t').textContent = caption(imgs[i]);
    lb.querySelectorAll('.lb-prev,.lb-next').forEach(b => b.hidden = imgs.length < 2);
  };
  const open = k => { lastFocus = document.activeElement; show(k); lb.classList.add('on'); document.documentElement.classList.add('lb-open'); lb.querySelector('.lb-x').focus(); };
  const close = () => { lb.classList.remove('on'); document.documentElement.classList.remove('lb-open'); unzoom(); if (lastFocus) lastFocus.focus(); };
  imgs.forEach((el, k) => {
    el.classList.add('zoomable'); el.tabIndex = 0; el.setAttribute('role', 'button');
    el.setAttribute('aria-label', (en ? 'Open image: ' : 'Открыть фото: ') + (el.alt || ''));
    el.addEventListener('click', e => { e.preventDefault(); e.stopPropagation(); open(k); });
    el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(k); } });
  });
  // приближение: по клику фото увеличивается, точка под пальцем/курсором остаётся на месте
  big.addEventListener('click', e => {
    e.stopPropagation();
    if (lb.classList.contains('z')) { unzoom(); return; }
    const r = big.getBoundingClientRect(), fx = (e.clientX - r.left) / r.width, fy = (e.clientY - r.top) / r.height;
    const w = Math.max(big.naturalWidth, r.width * 2.2);
    lb.classList.add('z'); big.style.width = w + 'px';
    requestAnimationFrame(() => { stage.scrollLeft = w * fx - innerWidth / 2; stage.scrollTop = big.offsetHeight * fy - innerHeight / 2; });
  });
  stage.addEventListener('click', e => { if (e.target === stage) close(); });
  lb.querySelector('.lb-x').addEventListener('click', close);
  lb.querySelector('.lb-prev').addEventListener('click', e => { e.stopPropagation(); show(i - 1); });
  lb.querySelector('.lb-next').addEventListener('click', e => { e.stopPropagation(); show(i + 1); });
  addEventListener('keydown', e => {
    if (!lb.classList.contains('on')) return;
    if (e.key === 'Escape') close(); else if (e.key === 'ArrowLeft') show(i - 1); else if (e.key === 'ArrowRight') show(i + 1);
  });
  // свайп влево/вправо, когда фото не приближено
  let sx = 0, sy = 0;
  stage.addEventListener('touchstart', e => { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
  stage.addEventListener('touchend', e => {
    if (lb.classList.contains('z')) return;
    const dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) show(i + (dx < 0 ? 1 : -1));
  }, { passive: true });
})();
