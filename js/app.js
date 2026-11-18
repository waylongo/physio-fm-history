/* 思想年谱：一条时间阅读流。展开、地址和历史记录保持同步；相关论文在点开后保持可见。 */
(function () {
  'use strict';

  const main = document.getElementById('main');
  const BY = Object.create(null);
  const OUT = Object.create(null);
  const QUESTION = ['apple-iclr24', 'lsm', 'ppg-bench', 'sensorwm'];
  let META = null;
  let selected = null;
  let total = 0;
  let syncing = false;
  const view = { track: '', q: '' };
  let countEl = null;
  let emptyEl = null;
  let allBtn = null;
  let searchEl = null;
  const trackBtns = [];

  function loadJson(url) {
    return fetch(url).then(r => {
      if (!r.ok) throw new Error(r.status + ' ' + r.url);
      return r.json().then(null, err => {
        throw new Error('JSON 无法解析 ' + r.url + ' (' + err.message + ')');
      });
    });
  }

  function showLoadError(err) {
    console.error(err);
    const p = document.createElement('p');
    p.className = 'error';
    p.textContent = '条目没有载入。' + (err && err.message ? err.message : '未知错误');
    if (main) main.replaceChildren(p);
  }

  Promise.all([
    loadJson('data/meta.json'),
    loadJson('data/entries.json')
  ]).then(([meta, data]) => {
    if (!meta || !Array.isArray(meta.tracks) || !Array.isArray(meta.eras)) throw new Error('meta.json 缺少 tracks 或 eras');
    if (!data || !Array.isArray(data.entries)) throw new Error('entries.json 缺少 entries');
    META = meta;
    data.entries.forEach(e => { BY[e.id] = e; });
    data.entries.forEach(e => (e.links || []).forEach(l => {
      (OUT[l.from] = OUT[l.from] || []).push({ to: e.id, type: l.type, note: l.note });
    }));
    render(data.entries);
    if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
    const id = entryFromHash();
    history.replaceState({ entry: id || null }, '', location.href);
    if (id) apply(id, { scroll: true, focus: false });
    window.addEventListener('popstate', onHistory);
    window.addEventListener('hashchange', onHistory);
  }).catch(showLoadError);

  function track(id) { return META.tracks.find(t => t.id === id) || { short: id, color: '#555' }; }
  function org(id) { return (META.orgs[id] || { label: id }).label; }
  function typeLabel(id) { return (META.types.find(t => t.id === id) || {}).label || id; }
  function when(e) { return e.date.slice(0, 7).replace('-', '.'); }
  function sorted(list) { return list.slice().sort((a, b) => a.date < b.date ? -1 : a.date > b.date ? 1 : 0); }

  function appendRich(parent, text) {
    const re = /<b>([\s\S]*?)<\/b>/g;
    let last = 0;
    let m;
    while ((m = re.exec(text))) {
      parent.append(text.slice(last, m.index));
      const b = document.createElement('b');
      b.textContent = m[1];
      parent.append(b);
      last = re.lastIndex;
    }
    parent.append(text.slice(last));
  }

  function requireEl(id) {
    const el = document.getElementById(id);
    if (!el) throw new Error('页面缺少 #' + id);
    return el;
  }

  function render(entries) {
    total = entries.length;
    const jumps = requireEl('jumps');
    META.eras.forEach(era => {
      const a = document.createElement('a');
      a.href = '#era-' + era.id;
      a.textContent = era.no;
      jumps.append(a);
    });

    main.replaceChildren();
    main.append(essaySection(), toolsSection());

    const byEra = new Map(META.eras.map(era => [era.id, []]));
    sorted(entries).forEach(e => { if (byEra.has(e.era)) byEra.get(e.era).push(e); });
    META.eras.forEach(era => {
      const sec = document.createElement('section');
      sec.className = 'era';
      sec.id = 'era-' + era.id;
      const h = document.createElement('h2');
      const no = document.createElement('span');
      no.className = 'no';
      no.textContent = era.no;
      h.append(no, era.title);
      const thesis = document.createElement('p');
      thesis.className = 'thesis';
      thesis.textContent = era.thesis;
      sec.append(h, thesis);
      byEra.get(era.id).forEach(e => sec.append(entryArticle(e)));
      main.append(sec);
    });

    const foot = requireEl('foot');
    foot.textContent = '共 ' + entries.length + ' 项，核对至 ' + META.updated + '。关系与“意义”含编者解读。点开一条后，相关论文会留在页面上，直到换一条或关闭。';
    document.addEventListener('keydown', onKey);
  }

  function essaySection() {
    const essay = document.createElement('section');
    essay.className = 'essay';
    const eh = document.createElement('h2');
    eh.textContent = '这段历史';
    essay.append(eh);

    const bits = (META.essay[0] || '').split('→').map(s => s.trim());
    const cut = bits[0].indexOf('</b>');
    const leadHtml = cut >= 0 ? bits[0].slice(0, cut + 4) : '';
    const lead = document.createElement('p');
    appendRich(lead, leadHtml || bits[0]);
    essay.append(lead);

    const questions = [bits[0].slice(leadHtml.length).trim(), ...bits.slice(1)].filter(Boolean);
    const ol = document.createElement('ol');
    ol.className = 'questions';
    questions.forEach((text, i) => {
      const li = document.createElement('li');
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = text;
      const id = QUESTION[i];
      if (BY[id]) b.addEventListener('click', () => openEntry(id, { toggle: false }));
      li.append(b);
      ol.append(li);
    });
    essay.append(ol);

    const more = document.createElement('details');
    more.className = 'more';
    const sum = document.createElement('summary');
    sum.textContent = '导读';
    more.append(sum);
    META.essay.slice(1).forEach(text => {
      const p = document.createElement('p');
      appendRich(p, text);
      more.append(p);
    });
    if (META.relationNote) {
      const note = document.createElement('p');
      note.className = 'note';
      note.textContent = META.relationNote;
      more.append(note);
    }
    essay.append(more);
    return essay;
  }

  function toolsSection() {
    const wrap = document.createElement('div');
    const box = document.createElement('div');
    box.className = 'tools';
    META.tracks.forEach(t => {
      const b = document.createElement('button');
      b.type = 'button';
      b.dataset.track = t.id;
      b.textContent = t.short;
      b.style.color = t.color;
      b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', () => {
        view.track = view.track === t.id ? '' : t.id;
        paintFilter();
      });
      trackBtns.push(b);
      box.append(b);
    });
    allBtn = document.createElement('button');
    allBtn.type = 'button';
    allBtn.textContent = '全部';
    allBtn.hidden = true;
    allBtn.addEventListener('click', () => {
      view.track = '';
      view.q = '';
      if (searchEl) searchEl.value = '';
      paintFilter();
    });
    box.append(allBtn);
    searchEl = document.createElement('input');
    searchEl.type = 'search';
    searchEl.placeholder = '搜索';
    searchEl.setAttribute('aria-label', '搜索');
    searchEl.addEventListener('input', () => {
      view.q = searchEl.value.trim().toLowerCase();
      paintFilter();
    });
    box.append(searchEl);
    countEl = document.createElement('span');
    countEl.className = 'count';
    countEl.textContent = total + ' / ' + total;
    box.append(countEl);
    emptyEl = document.createElement('p');
    emptyEl.className = 'empty';
    emptyEl.hidden = true;
    emptyEl.textContent = '没有匹配。';
    wrap.append(box, emptyEl);
    return wrap;
  }

  function blob(e) {
    const bits = [e.title, e.short, e.q, e.how, e.shift];
    (e.links || []).forEach(l => {
      bits.push(l.note, l.type);
      const o = BY[l.from];
      if (o) bits.push(o.short, o.title);
    });
    (OUT[e.id] || []).forEach(o => {
      bits.push(o.note, o.type);
      const t = BY[o.to];
      if (t) bits.push(t.short, t.title);
    });
    return bits.filter(Boolean).join('\n').toLowerCase();
  }

  function hit(e) {
    if (view.track && e.track !== view.track) return false;
    if (view.q && blob(e).indexOf(view.q) === -1) return false;
    return true;
  }

  function paintFilter() {
    let n = 0;
    document.querySelectorAll('article.entry').forEach(art => {
      const show = hit(BY[art.id]);
      art.hidden = !show;
      if (show) n++;
    });
    document.querySelectorAll('section.era').forEach(sec => {
      sec.hidden = !sec.querySelector('article.entry:not([hidden])');
    });
    if (countEl) countEl.textContent = n + ' / ' + total;
    if (emptyEl) emptyEl.hidden = n !== 0;
    if (allBtn) allBtn.hidden = !view.track && !view.q;
    trackBtns.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.track === view.track && !!view.track)));
    if (selected) {
      const art = document.getElementById(selected);
      if (art && art.hidden) {
        setOpen(selected, false);
        selected = null;
        history.replaceState({ entry: null }, '', location.pathname + location.search);
      }
    }
  }

  function ensureShown(id) {
    const art = document.getElementById(id);
    if (!art || !art.hidden) return;
    view.track = '';
    view.q = '';
    if (searchEl) searchEl.value = '';
    paintFilter();
  }

  function entryArticle(e) {
    const t = track(e.track);
    const art = document.createElement('article');
    art.className = 'entry' + (e.start ? ' start' : '');
    art.id = e.id;
    art.style.setProperty('--c', t.color);

    const h = document.createElement('h3');
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.id = 'btn-' + e.id;
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-controls', 'panel-' + e.id);
    const whenEl = document.createElement('span');
    whenEl.className = 'when';
    whenEl.textContent = when(e);
    const name = document.createElement('span');
    name.className = 'name';
    if (e.start) {
      const tag = document.createElement('span');
      tag.className = 'tag';
      tag.textContent = '起点';
      name.append(tag);
    }
    name.append(e.short);
    const meta = document.createElement('span');
    meta.className = 'meta';
    meta.textContent = org(e.org) + ' · ' + typeLabel(e.type) + ' · ' + t.short;
    btn.append(whenEl, name, meta);
    btn.addEventListener('click', () => openEntry(e.id, { toggle: true, anchor: selected ? 'btn-' + selected : '' }));
    h.append(btn);

    const panel = document.createElement('div');
    panel.className = 'panel';
    panel.id = 'panel-' + e.id;
    panel.hidden = true;
    panel.setAttribute('role', 'region');
    panel.setAttribute('aria-labelledby', btn.id);
    fillPanel(panel, e);
    art.append(h, panel);
    return art;
  }

  function fillPanel(panel, e) {
    const t = track(e.track);
    const title = document.createElement('p');
    title.className = 'title';
    title.textContent = e.title;
    const who = document.createElement('p');
    who.className = 'who';
    who.textContent = org(e.org) + (e.orgNote ? '（' + e.orgNote + '）' : '') + ' · ' + typeLabel(e.type) + ' · ' + t.short + ' · ' + e.dateLabel;
    const facts = document.createElement('dl');
    facts.className = 'facts';
    [['问题', e.q], ['做法', e.how], ['意义', e.shift]].forEach(([k, v]) => {
      const wrap = document.createElement('div');
      const dt = document.createElement('dt');
      dt.textContent = k;
      const dd = document.createElement('dd');
      dd.textContent = v;
      wrap.append(dt, dd);
      facts.append(wrap);
    });
    panel.append(title, who, facts, sourceList(e), relations(e), dismissButton());
  }

  function sourceList(e) {
    const ul = document.createElement('ul');
    ul.className = 'links';
    const primary = document.createElement('li');
    primary.append(extLink(e.url, '原文', true));
    ul.append(primary);
    (e.sources || []).forEach(s => {
      if (!s.url || s.url === e.url) return;
      const li = document.createElement('li');
      li.append(extLink(s.url, s.label || '来源', false));
      ul.append(li);
    });
    return ul;
  }

  function extLink(url, label, primary) {
    const a = document.createElement('a');
    a.href = url;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    a.textContent = label;
    if (primary) a.className = 'primary';
    return a;
  }

  function relations(e) {
    const box = document.createElement('div');
    box.className = 'rels';
    const inc = (e.links || []).map(l => ({ type: l.type, note: l.note, other: BY[l.from] })).filter(x => x.other);
    const out = (OUT[e.id] || []).map(o => ({ type: o.type, note: o.note, other: BY[o.to] })).filter(x => x.other);
    inc.sort((a, b) => a.other.date < b.other.date ? -1 : 1);
    out.sort((a, b) => a.other.date < b.other.date ? -1 : 1);
    if (!inc.length && !out.length) return box;
    if (inc.length) box.append(relGroup(e.id, 'in', '承接', inc));
    if (out.length) box.append(relGroup(e.id, 'out', '后续', out));
    return box;
  }

  function relGroup(host, dir, label, items) {
    const wrap = document.createElement('div');
    const h = document.createElement('h4');
    h.textContent = label;
    const ul = document.createElement('ul');
    ul.className = 'rel';
    items.forEach((item, i) => {
      const li = document.createElement('li');
      const row = document.createElement('div');
      row.className = 'row';
      const kind = document.createElement('span');
      kind.className = 'kind';
      kind.textContent = item.type;
      const jump = document.createElement('button');
      jump.type = 'button';
      jump.className = 'jump';
      jump.id = 'rel-' + host + '-' + dir + '-' + item.other.id + '-' + i;
      jump.textContent = item.other.short;
      jump.addEventListener('click', () => openEntry(item.other.id, { toggle: false, anchor: jump.id }));
      row.append(kind, jump, extLink(item.other.url, '原文', false));
      li.append(row);
      if (item.note) {
        const why = document.createElement('p');
        why.className = 'why';
        why.textContent = item.note;
        li.append(why);
      }
      ul.append(li);
    });
    wrap.append(h, ul);
    return wrap;
  }

  function dismissButton() {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'dismiss';
    b.textContent = '关闭';
    b.addEventListener('click', () => { if (selected) push('', { anchor: 'btn-' + selected }); });
    return b;
  }

  function entryFromHash() {
    const id = decodeURIComponent((location.hash || '').replace(/^#/, ''));
    return BY[id] ? id : '';
  }

  function urlFor(id) {
    return location.pathname + location.search + (id ? '#' + id : '');
  }

  function openEntry(id, opts) {
    opts = opts || {};
    if (!BY[id]) return;
    if (selected === id) {
      if (opts.toggle) push('', { anchor: opts.anchor || ('btn-' + id) });
      return;
    }
    push(id, opts);
  }

  function push(id, opts) {
    opts = opts || {};
    syncing = true;
    if (opts.anchor && selected) history.replaceState({ entry: selected, anchor: opts.anchor }, '', location.href);
    history.pushState({ entry: id || null }, '', urlFor(id));
    apply(id, { scroll: opts.scroll !== false, focus: opts.focus });
    syncing = false;
  }

  function onHistory() {
    if (syncing) return;
    const id = entryFromHash();
    const anchor = history.state && history.state.anchor;
    apply(id, { anchor: anchor || '', scroll: true, focus: false });
    if (!id) {
      const raw = decodeURIComponent((location.hash || '').replace(/^#/, ''));
      const era = raw && document.getElementById(raw);
      if (era) requestAnimationFrame(() => era.scrollIntoView({ block: 'start' }));
    }
  }

  function apply(id, opts) {
    opts = opts || {};
    if (id) ensureShown(id);
    const prev = selected;
    if (selected && selected !== id) setOpen(selected, false);
    if (!id) {
      if (selected) setOpen(selected, false);
      selected = null;
      if (opts.focus !== false && prev) {
        const b = document.getElementById('btn-' + prev);
        if (b) b.focus();
      }
      return;
    }
    selected = id;
    setOpen(id, true);
    if (opts.focus !== false) {
      const b = document.getElementById('btn-' + id);
      if (b) b.focus({ preventScroll: true });
    }
    if (opts.scroll === false) return;
    const anchorEl = opts.anchor ? document.getElementById(opts.anchor) : null;
    const target = anchorEl || document.getElementById(id);
    if (!target) return;
    requestAnimationFrame(() => target.scrollIntoView({ block: anchorEl ? 'center' : 'start' }));
  }

  function setOpen(id, on) {
    const art = document.getElementById(id);
    const btn = document.getElementById('btn-' + id);
    const panel = document.getElementById('panel-' + id);
    if (!art || !btn || !panel) return;
    art.classList.toggle('open', on);
    btn.setAttribute('aria-expanded', String(on));
    panel.hidden = !on;
  }

  function onKey(ev) {
    if (ev.key === 'Escape' && selected) {
      ev.preventDefault();
      push('', { anchor: 'btn-' + selected });
      return;
    }
    if (ev.key !== 'ArrowDown' && ev.key !== 'ArrowUp') return;
    const buttons = Array.from(document.querySelectorAll('.entry > h3 > button')).filter(b => !b.closest('article').hidden);
    const i = buttons.indexOf(document.activeElement);
    if (i < 0) return;
    const next = buttons[i + (ev.key === 'ArrowDown' ? 1 : -1)];
    if (!next) return;
    ev.preventDefault();
    next.focus();
  }
})();
