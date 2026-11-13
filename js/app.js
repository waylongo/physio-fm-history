/* 生理基础模型 · 思想年谱 —— 纯静态渲染脚本，无依赖
 * 数据：data/meta.json（纲、时期、脉络、公司、问题、机构、主叙事）与 data/entries.json（条目）
 * 视图：年谱（四列时间轴）/ 脉络（问题 → 做法 → 改变 → 解锁）/ 公司（数据 → 模型 → 产品）/ 问题（核心问题 × 时期）
 */
(function () {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const NARROW = '(max-width: 860px)';
  const narrow = () => window.matchMedia(NARROW).matches;

  let META, ENTRIES, EXTRA, BY_ID = {}, OUT = {};
  const VIEWS = ['chrono', 'threads', 'companies', 'questions'];
  const state = { view: 'chrono', tracks: new Set(), groups: new Set(), types: new Set(), thread: '', prelude: true };
  let pinned = null, lastPointer = 'mouse';

  Promise.all([fetch('data/meta.json').then(r => r.json()), fetch('data/entries.json').then(r => r.json()), fetch('data/sources-extra.json').then(r => r.ok ? r.json() : { items: [], groups: [] }).catch(() => ({ items: [], groups: [] }))])
    .then(([m, e, x]) => { META = m; ENTRIES = e.entries; EXTRA = x; init(); })
    .catch(err => {
      $('#canvas').innerHTML = '<p style="padding:20px;color:#8c4a3f">数据加载失败。若直接用 file:// 打开，请改用本地服务预览（见 README）。<br>' + esc(err) + '</p>';
    });

  const trackOf = id => META.tracks.find(t => t.id === id);
  const orgOf = id => META.orgs[id] || { label: id, group: 'other' };
  const color = id => (trackOf(id) || {}).color || '#555';
  const relColor = t => (META.relations[t] || {}).color || '#4a4844';
  const typeLabel = t => (META.types.find(x => x.id === t) || {}).label || t;
  const ym = e => e.dateShort || e.date.slice(0, 7).replace('-', '.');
  const threadById = id => META.threads.find(t => t.id === id);

  function init() {
    ENTRIES.forEach(e => { BY_ID[e.id] = e; });
    ENTRIES.forEach(e => (e.links || []).forEach(l => { (OUT[l.from] = OUT[l.from] || []).push({ to: e.id, type: l.type, note: l.note }); }));
    META.tracks.forEach(t => state.tracks.add(t.id));
    META.orgGroups.forEach(g => state.groups.add(g.id));
    META.types.forEach(t => state.types.add(t.id));
    buildStats(); buildLegend(); buildControls(); buildThreads(); buildCompanies(); buildQuestions(); buildEssay(); buildSources();
    readHash(); syncControls();
    render();
    let rt, lastW = window.innerWidth;
    window.addEventListener('resize', () => { if (window.innerWidth === lastW) return; lastW = window.innerWidth; clearTimeout(rt); rt = setTimeout(render, 120); });
    window.addEventListener('hashchange', () => { readHash(); syncControls(); render(); });
    document.addEventListener('click', ev => { if (!ev.target.closest('[data-eid]') && !ev.target.closest('.card')) hideCard(true); });
    document.addEventListener('keydown', ev => { lastPointer = 'mouse'; if (ev.key === 'Escape') hideCard(true); });
    $('#card').addEventListener('click', ev => { if (ev.target.closest('.cx')) hideCard(true); });
    $('#card').addEventListener('mouseleave', () => { if (lastPointer === 'mouse') hideCard(false); });
  }

  /* ---------- 统计、图例与控件 ---------- */
  function buildStats() {
    const n = k => ENTRIES.filter(e => e.type === k).length;
    const orgs = new Set(ENTRIES.map(e => e.org)).size;
    $('#stats').innerHTML = `收录 <b>${ENTRIES.length}</b> 项：论文 ${n('paper')} · 开源 ${n('open')} · 产品 ${n('product')} · 宣布/收购/在建 ${n('announce')}；来自 ${orgs} 家机构，${META.threads.length} 条思想脉络。核对至 ${esc(META.updated)}。`;
  }
  function buildLegend() {
    const ul = $('#legendTracks');
    META.tracks.forEach(t => ul.appendChild(el('li', null, `<span class="sw" style="background:${t.color}"></span><div><b>${esc(t.name)}</b><span class="d">${esc(t.desc)}</span></div>`)));
    const heads = $('#laneHeads');
    heads.appendChild(el('div', null, ''));
    META.tracks.forEach(t => heads.appendChild(el('div', null, `<span style="color:${t.color}">●</span> ${esc(t.name)}<small>${esc(t.en)}</small>`)));
    const rl = $('#legendRels');
    Object.entries(META.relations).forEach(([k, v]) => rl.appendChild(el('span', null, `<i style="background:${v.color}"></i><b>${esc(k)}</b> ${esc(v.desc)}`)));
  }
  function chip(parent, label, onToggle, sw) {
    const b = el('button', 'chip', (sw ? `<span class="sw" style="background:${sw}"></span>` : '') + esc(label));
    b.type = 'button'; b.setAttribute('aria-pressed', 'true');
    b.addEventListener('click', () => { const v = b.getAttribute('aria-pressed') !== 'true'; b.setAttribute('aria-pressed', String(v)); onToggle(v); render(); writeHash(); });
    parent.appendChild(b); return b;
  }
  function buildControls() {
    $$('.views button[data-view]').forEach(b => b.addEventListener('click', () => { state.view = b.dataset.view; syncControls(); render(); writeHash(); window.scrollTo({ top: Math.min(window.scrollY, $('#views').offsetTop), behavior: 'auto' }); }));
    META.tracks.forEach(t => chip($('#fTracks'), t.short, v => v ? state.tracks.add(t.id) : state.tracks.delete(t.id), t.color));
    META.orgGroups.forEach(g => chip($('#fOrgs'), g.label, v => v ? state.groups.add(g.id) : state.groups.delete(g.id)));
    META.types.forEach(t => chip($('#fTypes'), t.label, v => v ? state.types.add(t.id) : state.types.delete(t.id)));
    const sel = $('#fThread');
    META.threads.forEach(th => { const o = el('option', null, esc(th.name)); o.value = th.id; sel.appendChild(o); });
    sel.addEventListener('change', () => { state.thread = sel.value; render(); writeHash(); });
    $('#fPrelude').addEventListener('change', e => { state.prelude = e.target.checked; render(); writeHash(); });
    $('#fReset').addEventListener('click', () => {
      META.tracks.forEach(t => state.tracks.add(t.id)); META.orgGroups.forEach(g => state.groups.add(g.id)); META.types.forEach(t => state.types.add(t.id));
      state.thread = ''; state.prelude = true; syncControls(); render(); writeHash();
    });
    $('#fToggle').addEventListener('click', () => { const f = $('#filters'); const on = !f.classList.contains('open'); f.classList.toggle('open', on); $('#fToggle').setAttribute('aria-expanded', String(on)); });
  }
  function syncControls() {
    const set = (box, arr, s) => $$('.chip', box).forEach((b, i) => b.setAttribute('aria-pressed', String(s.has(arr[i].id))));
    set($('#fTracks'), META.tracks, state.tracks); set($('#fOrgs'), META.orgGroups, state.groups); set($('#fTypes'), META.types, state.types);
    $('#fThread').value = state.thread; $('#fPrelude').checked = state.prelude;
    $$('.views button[data-view]').forEach(b => b.setAttribute('aria-selected', String(b.dataset.view === state.view)));
    document.body.dataset.view = state.view;
    const nOff = (META.tracks.length - state.tracks.size) + (META.orgGroups.length - state.groups.size) + (META.types.length - state.types.size) + (state.thread ? 1 : 0) + (state.prelude ? 0 : 1);
    $('#fToggle').textContent = nOff ? `筛选（${nOff}）` : '筛选';
  }
  function writeHash() {
    const p = [];
    if (state.view !== 'chrono') p.push('view=' + state.view);
    if (state.view === 'chrono' && state.thread) p.push('thread=' + state.thread);
    const h = p.length ? '#' + p.join('&') : '';
    if (location.hash !== h) history.replaceState(null, '', h || location.pathname + location.search);
  }
  function readHash() {
    const q = new URLSearchParams(location.hash.slice(1));
    const v = q.get('view'); state.view = VIEWS.includes(v) ? v : 'chrono';
    const t = q.get('thread'); state.thread = t && threadById(t) ? t : '';
  }

  function visible(e) {
    return state.tracks.has(e.track) && state.types.has(e.type) && state.groups.has(orgOf(e.org).group) && !(e.prelude && !state.prelude);
  }
  function sorted(list) { const ti = id => META.tracks.findIndex(t => t.id === id); return list.slice().sort((a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : ti(a.track) - ti(b.track))); }
  function threadSet() { const th = threadById(state.thread); return th ? new Set(th.steps.map(s => s.id)) : null; }

  /* ---------- 渲染 ---------- */
  function render() {
    hideCard(true);
    VIEWS.forEach(v => { $('#v-' + v).hidden = v !== state.view; });
    if (state.view !== 'chrono') return;
    renderNote();
    if (narrow()) renderList(); else renderChrono();
  }
  function renderNote() {
    const box = $('#threadNote');
    const th = threadById(state.thread);
    if (!th) { box.className = 'thread-note'; box.innerHTML = ''; return; }
    box.innerHTML = `<h3>脉络 · ${esc(th.name)}</h3><p class="tq">${esc(th.question)}</p>
      <p><b>问题</b> ${esc(th.problem)} <b>做法</b> ${esc(th.approach)}</p>
      <p><a href="#view=threads" data-goto-thread="${th.id}">在“脉络”视图中查看每一步的作用 →</a></p>`;
    box.className = 'thread-note on';
    box.querySelector('[data-goto-thread]').addEventListener('click', ev => { ev.preventDefault(); gotoThread(th.id); });
  }
  function gotoThread(id) {
    state.view = 'threads'; syncControls(); render(); writeHash();
    const t = $('#th-' + id); if (t) t.scrollIntoView({ block: 'start' });
  }

  function renderChrono() {
    const canvas = $('#canvas'), svg = $('#edges');
    $$('.node,.year,.era,.lane-rule,.startline', canvas).forEach(n => n.remove());
    const W = canvas.clientWidth, G = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--gutter')) || 84;
    const laneW = (W - G) / 4, laneX = i => G + i * laneW + 14;
    const list = sorted(ENTRIES.filter(visible));
    const ths = threadSet();
    canvas.parentElement.classList.toggle('dim', !!ths);
    META.tracks.forEach((t, i) => { const r = el('div', 'lane-rule'); r.style.left = laneX(i) + 'px'; canvas.appendChild(r); });

    const nodes = list.map(e => {
      const ti = META.tracks.findIndex(t => t.id === e.track);
      const a = el('a', `node t-${e.type}${e.prelude ? ' prelude' : ''}${e.start ? ' start' : ''}${ths && ths.has(e.id) ? ' on' : ''}`);
      a.href = e.url; a.target = '_blank'; a.rel = 'noopener'; a.dataset.eid = e.id;
      a.style.setProperty('--c', color(e.track));
      a.style.left = laneX(ti) + 'px'; a.style.width = (laneW - 22) + 'px'; a.style.top = '0px';
      a.innerHTML = `<span class="dot"></span><span class="tt">${e.start ? '<span class="tag">起点</span>' : ''}${esc(e.short)}</span><span class="mm">${esc(orgOf(e.org).label)} · ${esc(typeLabel(e.type))} · ${esc(ym(e))}</span>`;
      a.setAttribute('aria-label', `${e.short}，${orgOf(e.org).label}，${e.dateLabel}`);
      bindHover(a, e);
      canvas.appendChild(a);
      return { e, a, ti };
    });

    // 纵向布局：分段时间刻度 + 同列避让 + 全局单调；新年份开始前清空所有列，年份线不会穿过上一年的条目
    const t0 = new Date('2019-01-01').getTime(), split = new Date('2023-06-01').getTime(), MONTH = 2629800000;
    const scale = d => { const t = new Date(d.length === 7 ? d + '-15' : d).getTime(); return t < split ? (t - t0) / MONTH * 6 : (split - t0) / MONTH * 6 + (t - split) / MONTH * 22; };
    const laneLast = [-1e9, -1e9, -1e9, -1e9];
    let prevY = 0, curEra = null, curYear = null, offset = 0, firstScaled = null;
    const GAP = 14, YEAR_PAD = 22;
    nodes.forEach((n, idx) => {
      const e = n.e;
      if (e.era !== curEra) {
        curEra = e.era;
        const era = META.eras.find(x => x.id === e.era);
        const band = el('div', 'era' + (era.prelude ? ' prelude' : ''), `<div class="no">${esc(era.no)}</div><h2>${esc(era.title)}</h2><p>${esc(era.thesis)}</p>`);
        canvas.appendChild(band);
        const top = idx === 0 ? 0 : Math.max(prevY + 40, Math.max(...laneLast) + 26);
        band.style.top = top + 'px';
        const bh = band.offsetHeight + 26;
        const s = scale(e.date);
        if (firstScaled === null) firstScaled = s;
        offset = top + bh - (s - firstScaled);
        prevY = top + bh; for (let i = 0; i < 4; i++) laneLast[i] = top + bh - GAP;
        curYear = null;
      }
      let y = Math.max(scale(e.date) - firstScaled + offset, prevY, laneLast[n.ti] + GAP);
      const yr = e.date.slice(0, 4);
      if (yr !== curYear) {
        const fresh = curYear === null;
        curYear = yr;
        if (!fresh) y = Math.max(y, Math.max(...laneLast) + YEAR_PAD);
        const yl = el('div', 'year' + (fresh ? ' noline' : ''), `<span>${yr}</span>`); yl.style.top = (y - 10) + 'px'; canvas.appendChild(yl);
      }
      n.a.style.top = y + 'px'; n.y = y;
      laneLast[n.ti] = y + n.a.offsetHeight;
      prevY = y;
      if (e.start) { const sl = el('div', 'startline'); sl.style.top = (y - 8) + 'px'; canvas.appendChild(sl); }
    });
    const H = Math.max(...laneLast, prevY) + 60;
    canvas.style.height = H + 'px';
    svg.setAttribute('width', W); svg.setAttribute('height', H); svg.style.width = W + 'px'; svg.style.height = H + 'px';
    canvas._nodes = {}; nodes.forEach(n => { canvas._nodes[n.e.id] = n; });
    drawEdges(null);
  }

  const dotPos = n => ({ x: parseFloat(n.a.style.left), y: n.y + 12 });

  function drawEdges(focusId) {
    const svg = $('#edges'), canvas = $('#canvas'); if (!canvas._nodes || state.view !== 'chrono' || narrow()) { if (svg) svg.innerHTML = ''; return; }
    const N = canvas._nodes; let html = defs();
    const pairs = [];
    const th = threadById(state.thread);
    if (focusId) {
      if (!N[focusId]) { svg.innerHTML = html; return; }
      const e = BY_ID[focusId];
      (e.links || []).forEach(l => pairs.push({ from: l.from, to: e.id, type: l.type, inc: true }));
      (OUT[focusId] || []).forEach(o => pairs.push({ from: focusId, to: o.to, type: o.type, inc: false }));
    } else if (th) {
      const st = th.steps.map(s => s.id).filter(id => N[id]);
      for (let i = 1; i < st.length; i++) {
        const to = BY_ID[st[i]]; const l = (to.links || []).find(x => x.from === st[i - 1]);
        pairs.push({ from: st[i - 1], to: st[i], type: l ? l.type : null, inc: true });
      }
    }
    const crowded = pairs.filter(p => N[p.from] && N[p.to]).length > 6;
    pairs.forEach(p => {
      const a = N[p.from], b = N[p.to]; if (!a || !b) return;
      const A = dotPos(a), B = dotPos(b);
      const c = p.type ? relColor(p.type) : '#9a958b';
      const dy = Math.max(30, (B.y - A.y) * 0.5);
      const d = A.x === B.x ? `M${A.x},${A.y} C${A.x - 46},${A.y + dy} ${B.x - 46},${B.y - dy} ${B.x},${B.y}` : `M${A.x},${A.y} C${A.x},${A.y + dy} ${B.x},${B.y - dy} ${B.x},${B.y}`;
      const dash = p.type === '并行' || !p.type ? ' stroke-dasharray="4 4"' : '';
      const faint = crowded && !p.inc;
      html += `<path d="${d}" stroke="${c}"${dash} marker-end="url(#ar-${(META.relations[p.type] || {}).key || 'none'})" opacity="${faint ? .4 : .9}" stroke-width="${faint ? .9 : 1.2}"/>`;
      if (p.type && !faint) {
        const mx = A.x === B.x ? A.x - 36 : (A.x + B.x) / 2, my = (A.y + B.y) / 2;
        html += `<text x="${mx}" y="${my}" fill="${c}" text-anchor="middle">${esc(p.type)}</text>`;
      }
    });
    svg.innerHTML = html;
  }
  function defs() {
    const ks = Object.values(META.relations).map(v => [v.key, v.color]).concat([['none', '#9a958b']]);
    return '<defs>' + ks.map(([k, c]) => `<marker id="ar-${k}" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z" fill="${c}"/></marker>`).join('') + '</defs>';
  }

  /* ---------- 浮层卡片 ---------- */
  function relHTML(e) {
    const inc = (e.links || []).map(l => { const s = BY_ID[l.from]; return s ? `<div class="ri"><span class="rt" style="background:${relColor(l.type)}">${esc(l.type)}</span><b>${esc(s.short)}</b><span class="rn">${l.note ? esc(l.note) : ''}</span></div>` : ''; }).join('');
    const out = (OUT[e.id] || []).map(o => ({ o, t: BY_ID[o.to] })).filter(x => x.t);
    let outHTML = '';
    if (out.length) {
      const byType = {}; out.forEach(x => { (byType[x.o.type] = byType[x.o.type] || []).push(x.t); });
      const sum = Object.entries(byType).map(([k, v]) => `<span style="color:${relColor(k)}">${esc(k)} ${v.length}</span>`).join(' · ');
      const names = out.slice(0, 4).map(x => esc(x.t.short)).join('；') + (out.length > 4 ? ` 等 ${out.length} 项` : '');
      outHTML = `<div class="ro"><span class="lab">后续</span>${sum}<div class="rn">${names}</div></div>`;
    }
    if (!inc && !outHTML) return '';
    return `<div class="rel">${inc ? '<span class="lab">承接</span>' + inc : ''}${outHTML}</div>`;
  }
  function cardHTML(e, withLink) {
    return `${withLink ? '<button type="button" class="cx" aria-label="关闭">×</button>' : ''}<div class="ct">${esc(e.title)}</div>
      <div class="cm"><span class="ty" style="border-color:${color(e.track)};color:${color(e.track)}">${esc(trackOf(e.track).short)}</span><span class="ty">${esc(typeLabel(e.type))}</span>${esc(orgOf(e.org).label)}${e.orgNote ? '（' + esc(e.orgNote) + '）' : ''} · ${esc(e.dateLabel)}</div>
      <dl><dt>问题</dt><dd>${esc(e.q)}</dd><dt>做法</dt><dd>${esc(e.how)}</dd><dt>意义</dt><dd>${esc(e.shift)}</dd></dl>
      ${relHTML(e)}
      <div class="cf">${withLink ? `<a class="go" href="${esc(e.url)}" target="_blank" rel="noopener">打开原文 ↗</a>` : '<span class="hint">点击打开原文 ↗</span>'}<span class="fn">“意义”与关系线含编者解读</span></div>`;
  }
  function showCard(a, e, pin) {
    const card = $('#card');
    card.innerHTML = cardHTML(e, pin || lastPointer !== 'mouse');
    card.classList.add('on'); card.scrollTop = 0;
    if (!narrow()) {
      const r = a.getBoundingClientRect(), sx = window.scrollX, sy = window.scrollY;
      const cw = card.offsetWidth, ch = card.offsetHeight, vw = document.documentElement.clientWidth, vh = window.innerHeight;
      let left = r.right + 12; if (left + cw > vw - 10) left = r.left - cw - 12; if (left < 10) left = Math.max(10, Math.min(vw - cw - 10, r.left));
      let top = r.top - 8; if (top + ch > vh - 10) top = Math.max(10, vh - ch - 10);
      card.style.left = (left + sx) + 'px'; card.style.top = (top + sy) + 'px';
    } else { card.style.left = ''; card.style.top = ''; }
    $$('.active[data-eid]').forEach(n => n.classList.remove('active')); a.classList.add('active');
    drawEdges(e.id);
    if (pin) pinned = e.id;
  }
  function hideCard(force) {
    if (pinned && !force) return;
    pinned = null; const card = $('#card'); if (card) card.classList.remove('on');
    $$('.active[data-eid]').forEach(n => n.classList.remove('active'));
    if (META) drawEdges(null);
  }
  let hideT;
  function bindHover(a, e) {
    a.addEventListener('pointerdown', ev => { lastPointer = ev.pointerType || 'mouse'; });
    a.addEventListener('mouseenter', () => { clearTimeout(hideT); if (lastPointer === 'mouse' && !pinned) showCard(a, e, false); });
    a.addEventListener('mouseleave', ev => { if (lastPointer !== 'mouse') return; if (ev.relatedTarget && ev.relatedTarget.closest && ev.relatedTarget.closest('.card')) return; hideT = setTimeout(() => hideCard(false), 60); });
    a.addEventListener('focus', () => { if (!pinned && lastPointer !== 'touch' && lastPointer !== 'pen') showCard(a, e, false); });
    a.addEventListener('blur', () => { if (lastPointer !== 'touch') hideCard(false); });
    a.addEventListener('click', ev => { if (lastPointer !== 'mouse' && pinned !== e.id) { ev.preventDefault(); showCard(a, e, true); } });
  }
  /* 视图中引用条目的小标签：悬停看卡片，点击打开原文（触屏：先显示卡片） */
  function ref(id, extra) {
    const e = BY_ID[id]; if (!e) return '';
    return `<a class="ref${e.start ? ' start' : ''}" data-eid="${e.id}" href="${esc(e.url)}" target="_blank" rel="noopener" style="--c:${color(e.track)}">${esc(e.short)}<span class="rm">${esc(orgOf(e.org).label)} · ${esc(ym(e))}</span>${extra || ''}</a>`;
  }
  function bindRefs(root) { $$('a[data-eid]', root).forEach(a => bindHover(a, BY_ID[a.dataset.eid])); }

  /* ---------- 窄屏年谱列表 ---------- */
  function renderList() {
    const box = $('#list'); box.innerHTML = '';
    const ths = threadSet(); box.classList.toggle('dim', !!ths);
    let era = null, yr = null;
    sorted(ENTRIES.filter(visible)).forEach(e => {
      if (e.era !== era) { era = e.era; const E = META.eras.find(x => x.id === era); box.appendChild(el('details', 'eh', `<summary><span class="no">${esc(E.no)}</span><h2>${esc(E.title)}</h2></summary><p>${esc(E.thesis)}</p>`)); yr = null; }
      if (e.date.slice(0, 4) !== yr) { yr = e.date.slice(0, 4); box.appendChild(el('div', 'yr', yr)); }
      const t = trackOf(e.track);
      const d = el('div', 'li' + (ths && ths.has(e.id) ? ' on' : '') + (e.start ? ' start' : ''));
      d.style.setProperty('--c', t.color);
      d.innerHTML = `<button type="button" class="lh" aria-expanded="false"><span class="tt">${e.start ? '<span class="tag">起点</span>' : ''}${esc(e.short)}</span><span class="mm"><span class="lt">${esc(t.short)}</span>${esc(orgOf(e.org).label)} · ${esc(typeLabel(e.type))} · ${esc(ym(e))}</span></button><div class="det">${cardHTML(e, true)}</div>`;
      d.querySelector('.lh').addEventListener('click', () => { const on = d.classList.toggle('open'); d.querySelector('.lh').setAttribute('aria-expanded', String(on)); });
      box.appendChild(d);
    });
  }

  /* ---------- 脉络视图 ---------- */
  function buildThreads() {
    const root = $('#v-threads');
    const toc = el('nav', 'toc', `<span class="lab">${META.threads.length} 条脉络</span>` + META.threads.map((t, i) => `<a href="#th-${t.id}" data-th="${t.id}"><span class="n">${i + 1}</span>${esc(t.name.split('：')[0])}</a>`).join(''));
    root.appendChild(el('p', 'vlead', '每条脉络对应一个持续被改写的问题。上方是编者对这条线的概括（问题 → 做法 → 改变了什么 → 解锁了什么 → 仍未解决），下方按时间列出关键工作及其在这条线中的作用；两步之间若有明确的承接关系，会标出关系类型。'));
    root.appendChild(toc);
    toc.addEventListener('click', ev => { const a = ev.target.closest('a[data-th]'); if (!a) return; ev.preventDefault(); const t = $('#th-' + a.dataset.th); if (t) t.scrollIntoView({ block: 'start' }); });
    META.threads.forEach((t, i) => {
      const sec = el('section', 'thread', '');
      sec.id = 'th-' + t.id;
      const steps = t.steps.map((s, k) => {
        const e = BY_ID[s.id]; if (!e) return '';
        const prevIds = t.steps.slice(0, k).map(x => x.id);
        const l = (e.links || []).filter(x => prevIds.includes(x.from)).pop();
        const rel = l ? `<span class="srel" style="color:${relColor(l.type)}">${esc(l.type)}自「${esc(BY_ID[l.from].short)}」</span>` : '';
        return `<li style="--c:${color(e.track)}" class="${e.start ? 'start' : ''}"><span class="sd">${esc(e.date.slice(0, 7).replace('-', '.'))}</span><div class="sb">${ref(e.id)}<div class="role">${esc(s.role)}</div>${rel}</div></li>`;
      }).join('');
      sec.innerHTML = `<header><span class="tn">${i + 1}</span><div><h3>${esc(t.name)}</h3><p class="tq">${esc(t.question)}</p></div></header>
        <div class="logic">
          <div><span class="k">问题</span>${esc(t.problem)}</div>
          <div><span class="k">做法</span>${esc(t.approach)}</div>
          <div><span class="k">改变了什么</span>${esc(t.changed)}</div>
          <div><span class="k">解锁了什么</span>${esc(t.unlocked)}</div>
          <div class="open"><span class="k">仍未解决</span>${esc(t.open)}</div>
        </div>
        <ol class="steps">${steps}</ol>
        <p class="tfoot"><a href="#thread=${t.id}" data-hl="${t.id}">在年谱中高亮这条脉络 →</a></p>`;
      sec.querySelector('[data-hl]').addEventListener('click', ev => { ev.preventDefault(); state.view = 'chrono'; state.thread = t.id; syncControls(); render(); writeHash(); $('#views').scrollIntoView({ block: 'start' }); });
      root.appendChild(sec);
    });
    bindRefs(root);
  }

  /* ---------- 公司视图 ---------- */
  function buildCompanies() {
    const root = $('#v-companies');
    root.appendChild(el('p', 'vlead', '同一个问题，各家走的路径不同。每张卡片按“数据资产 → 模型 → 产品与 Agent”排列已核实的公开工作；底部是编者判断。未见公开材料的环节如实标注为空。'));
    const grid = el('div', 'cgrid');
    META.companies.forEach(c => {
      const isGroup = META.orgGroups.some(g => g.id === c.org) && !META.orgs[c.org];
      const n = ENTRIES.filter(e => isGroup ? orgOf(e.org).group === c.org : e.org === c.org).length;
      const row = (k, lab) => `<div class="crow"><div class="ck">${lab}</div><div><p>${esc(c[k].text)}</p><div class="refs">${c[k].ids.map(id => ref(id)).join('')}</div></div></div>`;
      grid.appendChild(el('article', 'co', `<header><h3>${esc(c.name)}</h3><span class="cn">收录 ${n} 项</span></header><p class="path">${esc(c.path)}</p>${row('data', '数据资产')}${row('model', '模型')}${row('product', '产品与 Agent')}<p class="note"><span>编者判断</span>${esc(c.note)}</p>`));
    });
    root.appendChild(grid);
    bindRefs(root);
  }

  /* ---------- 问题视图 ---------- */
  function buildQuestions() {
    const root = $('#v-questions');
    root.appendChild(el('p', 'vlead', '把整段历史压缩成五个反复被回答的问题。横向读，是同一个问题的答案如何随时期改写；纵向读，是每个时期的整体立场。格子里的概括为编者解读，标签指向支撑它的条目。'));
    const tbl = el('div', 'qgrid');
    tbl.style.setProperty('--cols', META.eras.length);
    tbl.appendChild(el('div', 'qh corner', '问题 ＼ 时期'));
    META.eras.forEach(e => tbl.appendChild(el('div', 'qh', `<span class="no">${esc(e.no)}</span><b>${esc(e.title)}</b>`)));
    META.questions.forEach(q => {
      tbl.appendChild(el('div', 'qq', esc(q.q)));
      q.cells.forEach(c => {
        const era = META.eras.find(x => x.id === c.era);
        tbl.appendChild(el('div', 'qc', `<span class="qe">${esc(era.no)}</span><p>${esc(c.text)}</p><div class="refs">${c.ids.map(id => ref(id)).join('')}</div>`));
      });
    });
    root.appendChild(tbl);
    bindRefs(root);
  }

  /* ---------- 主叙事与来源 ---------- */
  function buildEssay() { $('#essayBody').innerHTML = META.essay.map(p => `<p>${p}</p>`).join(''); }
  function buildSources() {
    const ul = $('#srcList'), xl = $('#srcExtra');
    const nx = (EXTRA.items || []).length;
    $('#srcCount').textContent = `（${ENTRIES.length + nx} 项）`;
    $('#srcMainH').textContent = `年谱条目（${ENTRIES.length} 项，含补充链接）`;
    sorted(ENTRIES).forEach(e => {
      const extra = (e.sources || []).map(s => ` · <a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.label)}</a>`).join('');
      const li = el('li', null, `<a href="${esc(e.url)}" target="_blank" rel="noopener">${esc(e.title)}</a> <span class="d">— ${esc(orgOf(e.org).label)}${e.orgNote ? '（' + esc(e.orgNote) + '）' : ''}，${esc(e.dateLabel)}</span>${extra}`);
      li.style.setProperty('--c', color(e.track)); li.dataset.q = (e.title + e.short + orgOf(e.org).label + e.dateLabel).toLowerCase();
      ul.appendChild(li);
    });
    if (!nx) { $('#srcExtraWrap').hidden = true; } else {
      $('#srcExtraH').textContent = `相关但未上年谱（${nx} 项）`;
      (EXTRA.groups || []).forEach(g => {
        const its = EXTRA.items.filter(x => x.group === g.id).sort((a, b) => a.date < b.date ? -1 : 1);
        if (!its.length) return;
        xl.appendChild(el('li', 'gh', `${esc(g.label)}（${its.length}）`));
        its.forEach(x => {
          const li = el('li', null, `<a href="${esc(x.url)}" target="_blank" rel="noopener">${esc(x.title)}</a> <span class="d">— ${esc(x.org)}，${esc(x.dateLabel || x.date)}</span><div class="why">${x.track ? '<span class="lt">' + esc((trackOf(x.track) || {}).short || '') + '</span>' : ''}${esc(x.reason)}</div>`);
          li.style.setProperty('--c', x.track ? color(x.track) : '#bbb'); li.dataset.q = (x.title + x.org + (x.dateLabel || x.date) + x.reason).toLowerCase();
          xl.appendChild(li);
        });
      });
    }
    $('#srcFilter').addEventListener('input', ev => {
      const q = ev.target.value.trim().toLowerCase();
      $$('#srcList li, #srcExtra li').forEach(li => { if (li.classList.contains('gh')) return; li.hidden = !!q && !(li.dataset.q || '').includes(q); });
    });
  }
})();

// 让泳道表头紧贴在控制条下方（控制条高度随换行变化）
(function () {
  const c = document.querySelector('.controls'); if (!c) return;
  const set = () => document.documentElement.style.setProperty('--ctl-h', c.offsetHeight + 'px');
  set(); if (window.ResizeObserver) new ResizeObserver(set).observe(c); else window.addEventListener('resize', set);
})();
