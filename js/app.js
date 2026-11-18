/* 思想年谱：一条时间阅读流。点开条目后相关论文保持可见，直到换一条或关闭。 */
(function () {
  'use strict';

  const main = document.getElementById('main');
  const BY = Object.create(null);
  const OUT = Object.create(null);
  let META = null;
  let selected = null;

  Promise.all([
    fetch('data/meta.json').then(r => r.json()),
    fetch('data/entries.json').then(r => r.json())
  ]).then(([meta, data]) => {
    META = meta;
    data.entries.forEach(e => { BY[e.id] = e; });
    data.entries.forEach(e => (e.links || []).forEach(l => {
      (OUT[l.from] = OUT[l.from] || []).push({ to: e.id, type: l.type, note: l.note });
    }));
    render(data.entries);
    const id = decodeURIComponent(location.hash.replace(/^#/, ''));
    if (BY[id]) openEntry(id, { toggle: false, focus: false });
  }).catch(() => {
    main.innerHTML = '<p class="error">无法读取数据。请用本地 HTTP 服务打开本页，不要直接双击文件。</p>';
  });

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

  function render(entries) {
    const tracks = document.getElementById('tracks');
    META.tracks.forEach(t => {
      const s = document.createElement('span');
      s.textContent = t.short;
      s.style.color = t.color;
      tracks.append(s);
    });

    const jumps = document.getElementById('jumps');
    META.eras.forEach(era => {
      const a = document.createElement('a');
      a.href = '#era-' + era.id;
      a.textContent = era.no;
      jumps.append(a);
    });

    main.replaceChildren();

    const essay = document.createElement('section');
    essay.className = 'essay';
    const eh = document.createElement('h2');
    eh.textContent = '这段历史';
    essay.append(eh);
    META.essay.forEach(text => {
      const p = document.createElement('p');
      appendRich(p, text);
      essay.append(p);
    });
    main.append(essay);

    if (META.relationNote) {
      const note = document.createElement('p');
      note.className = 'note';
      note.textContent = META.relationNote;
      main.append(note);
    }

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

    const foot = document.getElementById('foot');
    foot.textContent = '共 ' + entries.length + ' 项，核对至 ' + META.updated + '。关系与“意义”含编者解读。点开一条后，相关论文会留在页面上，直到换一条或关闭。';

    document.addEventListener('keydown', onKey);
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
    btn.addEventListener('click', () => openEntry(e.id, { toggle: true }));
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
    if (inc.length) box.append(relGroup('承接', inc));
    if (out.length) box.append(relGroup('后续', out));
    return box;
  }

  function relGroup(label, items) {
    const wrap = document.createElement('div');
    const h = document.createElement('h4');
    h.textContent = label;
    const ul = document.createElement('ul');
    ul.className = 'rel';
    items.forEach(item => {
      const li = document.createElement('li');
      const row = document.createElement('div');
      row.className = 'row';
      const kind = document.createElement('span');
      kind.className = 'kind';
      kind.textContent = item.type;
      const jump = document.createElement('button');
      jump.type = 'button';
      jump.className = 'jump';
      jump.textContent = item.other.short;
      jump.addEventListener('click', () => openEntry(item.other.id, { toggle: false }));
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
    b.addEventListener('click', () => dismiss({ restoreFocus: true }));
    return b;
  }

  function openEntry(id, opts) {
    if (!BY[id]) return;
    if (selected === id) {
      if (opts.toggle) dismiss({ restoreFocus: false });
      return;
    }
    if (selected) setOpen(selected, false);
    selected = id;
    setOpen(id, true);
    const art = document.getElementById(id);
    if (location.hash !== '#' + id) history.replaceState(null, '', '#' + id);
    if (opts.focus !== false) document.getElementById('btn-' + id).focus({ preventScroll: true });
    const panel = document.getElementById('panel-' + id);
    const rect = panel.getBoundingClientRect();
    if (rect.top < 0 || rect.bottom > window.innerHeight - 8) art.scrollIntoView({ block: 'start' });
  }

  function setOpen(id, on) {
    const art = document.getElementById(id);
    const btn = document.getElementById('btn-' + id);
    const panel = document.getElementById('panel-' + id);
    art.classList.toggle('open', on);
    btn.setAttribute('aria-expanded', String(on));
    panel.hidden = !on;
  }

  function dismiss(opts) {
    if (!selected) return;
    const id = selected;
    setOpen(id, false);
    selected = null;
    if (location.hash) history.replaceState(null, '', location.pathname + location.search);
    if (opts.restoreFocus) document.getElementById('btn-' + id).focus();
  }

  function onKey(ev) {
    if (ev.key === 'Escape' && selected) {
      ev.preventDefault();
      dismiss({ restoreFocus: true });
      return;
    }
    if (ev.key !== 'ArrowDown' && ev.key !== 'ArrowUp') return;
    const buttons = Array.from(document.querySelectorAll('.entry > h3 > button'));
    const i = buttons.indexOf(document.activeElement);
    if (i < 0) return;
    const next = buttons[i + (ev.key === 'ArrowDown' ? 1 : -1)];
    if (!next) return;
    ev.preventDefault();
    next.focus();
  }
})();
