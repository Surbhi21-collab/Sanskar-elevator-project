/* ============================================================
   SANSKAR ELEVATOR — Site interactions
   Vanilla JS, no dependencies. Each block is self-contained
   and fails silently if its markup is absent.
   ============================================================ */
(function () {
  'use strict';

  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1. PRELOADER ---------- */
  window.addEventListener('load', function () {
    var pre = $('#preloader');
    if (!pre) return;
    setTimeout(function () {
      pre.classList.add('is-done');
      setTimeout(function () { pre.remove(); }, 600);
    }, reduceMotion ? 0 : 450);
  });

  /* ---------- 2. THEME TOGGLE (persisted) ---------- */
  (function themeInit() {
    var root   = document.documentElement;
    var toggle = $('#themeToggle');
    var stored = null;
    try { stored = localStorage.getItem('se-theme'); } catch (e) {}

    var theme = stored || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    apply(theme);

    function apply(t) {
      root.setAttribute('data-theme', t);
      if (toggle) toggle.setAttribute('aria-label', t === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
      var meta = document.querySelector('meta[name="theme-color"]');
      if (meta) meta.setAttribute('content', t === 'dark' ? '#0B1120' : '#0F172A');
    }

    if (toggle) {
      toggle.addEventListener('click', function () {
        var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        apply(next);
        try { localStorage.setItem('se-theme', next); } catch (e) {}
      });
    }
  }());

  /* ---------- 3. STICKY HEADER + SCROLL PROGRESS + BACK TO TOP ---------- */
  (function scrollUI() {
    var header   = $('#header');
    var progress = $('#scrollProgress');
    var toTop    = $('#backToTop');
    var ticking  = false;

    function update() {
      var y      = window.scrollY || window.pageYOffset;
      var height = document.documentElement.scrollHeight - window.innerHeight;

      if (header) header.classList.toggle('is-stuck', y > 40);
      if (progress) progress.style.width = (height > 0 ? (y / height) * 100 : 0) + '%';
      if (toTop) toTop.classList.toggle('is-visible', y > 600);
      ticking = false;
    }

    window.addEventListener('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();

    if (toTop) {
      toTop.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
      });
    }
  }());

  /* ---------- 4. MOBILE NAVIGATION ---------- */
  (function mobileNav() {
    var burger  = $('#burger');
    var nav     = $('#nav');
    var overlay = $('#navOverlay');
    if (!burger || !nav) return;

    function setOpen(open) {
      nav.classList.toggle('is-open', open);
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      document.body.style.overflow = open ? 'hidden' : '';
      if (overlay) overlay.hidden = !open;
    }

    burger.addEventListener('click', function () {
      setOpen(burger.getAttribute('aria-expanded') !== 'true');
    });
    if (overlay) overlay.addEventListener('click', function () { setOpen(false); });
    $$('.nav__link', nav).forEach(function (link) {
      link.addEventListener('click', function () { setOpen(false); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });
  }());

  /* ---------- 5. SCROLL REVEAL + COUNTERS ---------- */
  (function revealAndCount() {
    var items = $$('.reveal');

    function runCounter(el) {
      var target   = parseFloat(el.getAttribute('data-target')) || 0;
      var duration = 1600;
      var start    = null;

      if (reduceMotion) { el.textContent = String(target); return; }

      function step(ts) {
        if (start === null) start = ts;
        var p = Math.min((ts - start) / duration, 1);
        var eased = 1 - Math.pow(1 - p, 3);          // easeOutCubic
        el.textContent = Math.round(target * eased).toString();
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }

    if (!('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-visible'); });
      $$('.counter').forEach(runCounter);
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        $$('.counter', entry.target).forEach(function (c) {
          if (!c.dataset.done) { c.dataset.done = '1'; runCounter(c); }
        });
        io.unobserve(entry.target);
      });
    }, { threshold: 0.14, rootMargin: '0px 0px -60px 0px' });

    items.forEach(function (el) { io.observe(el); });
  }());

  /* ---------- 6. ACTIVE NAV LINK ON SCROLL ---------- */
  (function scrollSpy() {
    // Only same-page hash links participate. Page links such as "about.html"
    // are NOT valid CSS selectors and would throw inside querySelector.
    var links = $$('.nav__link').filter(function (l) {
      var h = l.getAttribute('href') || '';
      return h.charAt(0) === '#' && h.length > 1;
    });
    var sections = links
      .map(function (l) { return document.querySelector(l.getAttribute('href')); })
      .filter(Boolean);
    if (!sections.length || !('IntersectionObserver' in window)) return;

    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (l) {
          l.classList.toggle('is-active', l.getAttribute('href') === '#' + entry.target.id);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });

    sections.forEach(function (s) { spy.observe(s); });
  }());

  /* ---------- 7. HERO PARALLAX ---------- */
  (function parallax() {
    var layer = $('[data-parallax]');
    if (!layer || reduceMotion) return;
    var ticking = false;

    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var y = window.scrollY;
        if (y < window.innerHeight * 1.2) {
          // 2D translateY at whole pixels. translate3d() would force a
          // permanent compositing layer; fractional offsets resample the image.
          layer.style.transform = 'translateY(' + Math.round(y * 0.28) + 'px)';
        }
        ticking = false;
      });
    }, { passive: true });
  }());

  /* ---------- 8. GALLERY FILTERS + LIGHTBOX ---------- */
  (function gallery() {
    var filters = $$('.filter');
    var tiles   = $$('.tile');

    filters.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var cat = btn.getAttribute('data-filter');
        filters.forEach(function (b) {
          var on = b === btn;
          b.classList.toggle('is-active', on);
          b.setAttribute('aria-selected', String(on));
        });
        tiles.forEach(function (t) {
          t.classList.toggle('is-hidden', cat !== 'all' && t.getAttribute('data-cat') !== cat);
        });
      });
    });

    // --- Lightbox ---
    var box   = $('#lightbox');
    if (!box) return;
    var imgEl = $('#lbImg');
    var capEl = $('#lbCap');
    var index = 0;
    var lastFocus = null;

    function visibleTiles() {
      return tiles.filter(function (t) { return !t.classList.contains('is-hidden'); });
    }

    // The tiles are ~700px crops. Blown up to 78vh in the lightbox they would
    // look soft, so request a proportionally larger source for the viewer.
    function hiRes(src, scale) {
      return src.replace(/\bw=(\d+)/, function (_, w) {
        return 'w=' + Math.round(w * scale);
      }).replace(/\bh=(\d+)/, function (_, h) {
        return 'h=' + Math.round(h * scale);
      });
    }

    function show(i) {
      var list = visibleTiles();
      if (!list.length) return;
      index = (i + list.length) % list.length;
      var tile = list[index];
      var img  = $('img', tile);
      var cap  = $('figcaption', tile);
      imgEl.src = hiRes(img.currentSrc || img.src, 2.5);
      imgEl.alt = img.alt;
      capEl.textContent = cap ? cap.textContent : '';
    }

    function open(tile) {
      lastFocus = document.activeElement;
      show(visibleTiles().indexOf(tile));
      box.hidden = false;
      requestAnimationFrame(function () { box.classList.add('is-open'); });
      document.body.style.overflow = 'hidden';
      $('#lbClose').focus();
    }

    function close() {
      box.classList.remove('is-open');
      document.body.style.overflow = '';
      setTimeout(function () { box.hidden = true; imgEl.src = ''; }, 300);
      if (lastFocus) lastFocus.focus();
    }

    tiles.forEach(function (tile) {
      tile.setAttribute('tabindex', '0');
      tile.setAttribute('role', 'button');
      tile.addEventListener('click', function () { open(tile); });
      tile.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(tile); }
      });
    });

    $('#lbClose').addEventListener('click', close);
    $('#lbPrev').addEventListener('click', function () { show(index - 1); });
    $('#lbNext').addEventListener('click', function () { show(index + 1); });
    box.addEventListener('click', function (e) { if (e.target === box) close(); });

    document.addEventListener('keydown', function (e) {
      if (box.hidden) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(index - 1);
      if (e.key === 'ArrowRight') show(index + 1);
    });
  }());

  /* ---------- 9. TESTIMONIAL SLIDER (auto + manual) ---------- */
  (function slider() {
    var track = $('#sliderTrack');
    var dots  = $('#sliderDots');
    if (!track) return;

    var slides  = $$('.quote', track);
    var pos     = 0;
    var timer   = null;
    var perView = 1;

    function calcPerView() {
      return window.innerWidth > 1100 ? 3 : window.innerWidth > 640 ? 2 : 1;
    }
    function maxPos() { return Math.max(0, slides.length - perView); }

    function render() {
      if (!slides.length) return;
      var slideW = slides[0].getBoundingClientRect().width;
      var gap    = parseFloat(getComputedStyle(slides[0]).marginRight) || 0;
      // Round to whole pixels — a fractional translateX lands text on a
      // half-pixel grid and renders every visible slide blurry.
      var offset = Math.round(pos * (slideW + gap));
      track.style.transform = 'translateX(-' + offset + 'px)';
      $$('button', dots).forEach(function (d, i) { d.classList.toggle('is-active', i === pos); });
    }

    function buildDots() {
      dots.innerHTML = '';
      for (var i = 0; i <= maxPos(); i++) {
        (function (i) {
          var b = document.createElement('button');
          b.type = 'button';
          b.setAttribute('aria-label', 'Go to testimonial group ' + (i + 1));
          b.addEventListener('click', function () { pos = i; render(); restart(); });
          dots.appendChild(b);
        }(i));
      }
    }

    function go(step) { pos = (pos + step + maxPos() + 1) % (maxPos() + 1); render(); }
    function restart() { stop(); start(); }
    function start() { if (!reduceMotion) timer = setInterval(function () { go(1); }, 5000); }
    function stop() { clearInterval(timer); }

    function layout() {
      var next = calcPerView();
      if (next !== perView) { perView = next; pos = Math.min(pos, maxPos()); buildDots(); }
      render();
    }

    perView = calcPerView();
    buildDots();
    render();
    start();

    $('#nextSlide').addEventListener('click', function () { go(1); restart(); });
    $('#prevSlide').addEventListener('click', function () { go(-1); restart(); });
    $('#slider').addEventListener('mouseenter', stop);
    $('#slider').addEventListener('mouseleave', start);
    $('#slider').addEventListener('focusin', stop);

    var rt;
    window.addEventListener('resize', function () {
      clearTimeout(rt);
      rt = setTimeout(layout, 150);
    });
  }());

  /* ---------- 10. FAQ ACCORDION ---------- */
  (function accordion() {
    $$('.acc').forEach(function (item) {
      var btn   = $('.acc__btn', item);
      var panel = $('.acc__panel', item);
      if (!btn || !panel) return;

      btn.addEventListener('click', function () {
        var isOpen = item.classList.contains('is-open');

        // Close siblings for a clean single-open accordion
        $$('.acc.is-open').forEach(function (other) {
          other.classList.remove('is-open');
          $('.acc__btn', other).setAttribute('aria-expanded', 'false');
          $('.acc__panel', other).style.maxHeight = null;
        });

        if (!isOpen) {
          item.classList.add('is-open');
          btn.setAttribute('aria-expanded', 'true');
          panel.style.maxHeight = panel.scrollHeight + 'px';
        }
      });
    });
  }());

  /* ---------- 11. QUOTE MODAL ---------- */
  (function quoteModal() {
    var modal = $('#quoteModal');
    if (!modal) return;
    var lastFocus = null;

    function open() {
      lastFocus = document.activeElement;
      modal.hidden = false;
      requestAnimationFrame(function () { modal.classList.add('is-open'); });
      document.body.style.overflow = 'hidden';
      var first = $('input', modal);
      if (first) first.focus();
    }
    function close() {
      modal.classList.remove('is-open');
      document.body.style.overflow = '';
      setTimeout(function () { modal.hidden = true; }, 350);
      if (lastFocus) lastFocus.focus();
    }

    $$('[data-open-quote]').forEach(function (b) { b.addEventListener('click', open); });
    $$('[data-close-quote]').forEach(function (b) { b.addEventListener('click', close); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !modal.hidden) close();
    });

    // Trap focus inside the dialog
    modal.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab') return;
      var focusables = $$('button, input, select, textarea, a[href]', modal)
        .filter(function (el) { return el.offsetParent !== null; });
      if (!focusables.length) return;
      var first = focusables[0], last = focusables[focusables.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }());

  /* ---------- 12. FORM VALIDATION ---------- */
  (function forms() {
    var MESSAGES = {
      valueMissing:  'This field is required.',
      typeMismatch:  'Please enter a valid value.',
      tooShort:      'Please enter a little more detail.',
      patternMismatch:'Please enter a valid phone number.'
    };

    function messageFor(input) {
      var v = input.validity;
      if (v.valueMissing)    return MESSAGES.valueMissing;
      if (v.typeMismatch)    return input.type === 'email' ? 'Please enter a valid email address.' : MESSAGES.typeMismatch;
      if (v.patternMismatch) return MESSAGES.patternMismatch;
      if (v.tooShort)        return MESSAGES.tooShort;
      return 'Please check this field.';
    }

    function validate(input) {
      var field = input.closest('.field');
      var slot  = field ? $('[data-error-for="' + input.id + '"]', field) : null;
      var ok    = input.checkValidity();
      if (field) field.classList.toggle('has-error', !ok);
      if (slot)  slot.textContent = ok ? '' : messageFor(input);
      input.setAttribute('aria-invalid', String(!ok));
      return ok;
    }

    function wire(formId, statusId, successText) {
      var form = $('#' + formId);
      if (!form) return;
      var status = $('#' + statusId);
      var fields = $$('input, textarea, select', form);

      fields.forEach(function (input) {
        input.addEventListener('blur', function () { validate(input); });
        input.addEventListener('input', function () {
          if (input.closest('.field') && input.closest('.field').classList.contains('has-error')) validate(input);
        });
      });

      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var allOk = fields.map(validate).every(Boolean);

        if (!allOk) {
          if (status) { status.textContent = 'Please correct the highlighted fields.'; status.className = 'form-status is-bad'; }
          var firstBad = $('.has-error input, .has-error textarea', form);
          if (firstBad) firstBad.focus();
          return;
        }

        // ---- Submission hook -------------------------------------------
        // Replace this block with a fetch() to your backend / form service:
        //   fetch('/api/enquiry', { method:'POST', body:new FormData(form) })
        // ----------------------------------------------------------------
        var btn = $('button[type="submit"]', form);
        var label = btn ? btn.innerHTML : '';
        if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }

        setTimeout(function () {
          if (btn) { btn.disabled = false; btn.innerHTML = label; }
          form.reset();
          $$('.field', form).forEach(function (f) { f.classList.remove('has-error'); });
          $$('.error', form).forEach(function (s) { s.textContent = ''; });
          if (status) { status.textContent = successText; status.className = 'form-status is-ok'; }
        }, 900);
      });
    }

    // Wire every enquiry form on the page, whatever its id.
    $$('form.contact__form').forEach(function (form) {
      wire(form.id, form.id + 'Status',
        'Thank you — your enquiry has been received. Our team will contact you shortly.');
    });
  }());

  /* ---------- 12b. SERVICES SUBMENU ---------- */
  (function submenu() {
    $$('.has-sub').forEach(function (item) {
      var toggle = $('.sub-toggle', item);
      if (!toggle) return;

      toggle.addEventListener('click', function (e) {
        e.preventDefault();
        var open = item.classList.toggle('is-open');
        toggle.setAttribute('aria-expanded', String(open));
      });
    });

    // Close any open submenu on Escape or on an outside click.
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      $$('.has-sub.is-open').forEach(function (i) {
        i.classList.remove('is-open');
        $('.sub-toggle', i).setAttribute('aria-expanded', 'false');
      });
    });
    document.addEventListener('click', function (e) {
      $$('.has-sub.is-open').forEach(function (i) {
        if (!i.contains(e.target)) {
          i.classList.remove('is-open');
          $('.sub-toggle', i).setAttribute('aria-expanded', 'false');
        }
      });
    });
  }());

  /* ---------- 13. COOKIE CONSENT ---------- */
  (function cookies() {
    var bar = $('#cookieBar');
    if (!bar) return;
    var choice = null;
    try { choice = localStorage.getItem('se-cookies'); } catch (e) {}
    if (choice) return;

    bar.hidden = false;
    setTimeout(function () { bar.classList.add('is-visible'); }, 1400);

    function decide(value) {
      try { localStorage.setItem('se-cookies', value); } catch (e) {}
      bar.classList.remove('is-visible');
      setTimeout(function () { bar.hidden = true; }, 500);
    }
    $('#cookieAccept').addEventListener('click', function () { decide('accepted'); });
    $('#cookieDecline').addEventListener('click', function () { decide('declined'); });
  }());

  /* ---------- 14. MISC ---------- */
  var yearEl = $('#year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Offset smooth-scroll so the sticky header never covers a heading
  $$('a[href^="#"]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      var id = link.getAttribute('href');
      if (id === '#' || id.length < 2) return;
      var target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      var top = target.getBoundingClientRect().top + window.scrollY - 78;
      window.scrollTo({ top: top, behavior: reduceMotion ? 'auto' : 'smooth' });
    });
  });

}());
