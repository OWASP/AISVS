/* AISVS Requirements Visualizer — D3.js v7 force-directed graph */

// ── Config ──────────────────────────────────────────────────────────────────

const COLOR = {
  root:         '#c9d1d9',
  chapter:      '#58a6ff',
  section:      '#bc8cff',
  'control-l1': '#3fb950',
  'control-l2': '#d29922',
  'control-l3': '#f78166',
};

const RADIUS = {
  root:         18,
  chapter:      13,
  section:       6,
  'control-l1':  3.5,
  'control-l2':  3.5,
  'control-l3':  3.5,
};

// Which filter chip key corresponds to which node types
const FILTER_TYPES = {
  l1:      ['control-l1'],
  l2:      ['control-l2'],
  l3:      ['control-l3'],
  section: ['section'],
};

// ── State ───────────────────────────────────────────────────────────────────

let allNodes = [];
let allLinks = [];
let simulation;
let gNode, gLink;
let activeNode = null;
let activeFilters = new Set(['l1', 'l2', 'l3', 'section']);
let searchTerm = '';

// Map nodeId -> node object for fast lookup
const nodeById = new Map();

// ── Graph building ───────────────────────────────────────────────────────────

function buildGraph(root) {
  allNodes = [];
  allLinks = [];
  nodeById.clear();

  function walk(node, parent, depth, sectorIndex, totalSectors) {
    const n = {
      id:          node.name,
      name:        node.name,
      title:       node.title || node.name,
      type:        node.type,
      level:       node.level || null,
      description: node.description || '',
      depth,
      sectorIndex,
      totalSectors,
      children:    node.children || [],
      // Will be set by D3
      x: undefined,
      y: undefined,
    };
    allNodes.push(n);
    nodeById.set(n.id, n);

    if (parent) {
      allLinks.push({ source: parent.id, target: n.id, depth });
    }

    const kids = node.children || [];
    kids.forEach((child, i) => walk(child, n, depth + 1, sectorIndex, totalSectors));
  }

  // Root
  walk(root, null, 0, 0, 1);
}

// ── Pre-position nodes in a radial layout by chapter sector ─────────────────

function prePosition(width, height) {
  const cx = width / 2;
  const cy = height / 2;

  const chapters = allNodes.filter(n => n.type === 'chapter');
  const numChapters = chapters.length;

  allNodes.forEach(n => {
    if (n.type === 'root') {
      n.x = cx;
      n.y = cy;
      return;
    }

    // Find which chapter this node belongs to
    const chapterIndex = findChapterIndex(n, chapters);
    const angle = (chapterIndex / numChapters) * 2 * Math.PI - Math.PI / 2;

    let r;
    if (n.type === 'chapter')      r = 160;
    else if (n.type === 'section') r = 280;
    else                           r = 380 + Math.random() * 60;

    n.x = cx + r * Math.cos(angle) + (Math.random() - 0.5) * 30;
    n.y = cy + r * Math.sin(angle) + (Math.random() - 0.5) * 30;
    n._angle = angle;
    n._chapterIndex = chapterIndex;
  });
}

function findChapterIndex(node, chapters) {
  // For chapter nodes
  if (node.type === 'chapter') {
    return chapters.findIndex(c => c.id === node.id);
  }
  // For section/control: chapter prefix is first part of id
  const prefix = node.id.split('.')[0];  // e.g. "1" from "1.1.2"
  const chNum = prefix.replace('C', ''); // normalise "C1" -> "1"
  const idx = chapters.findIndex(c => {
    const cn = c.id.match(/\d+/)?.[0];
    return cn === chNum;
  });
  return idx >= 0 ? idx : 0;
}

// ── Force simulation ─────────────────────────────────────────────────────────

function initSimulation(width, height) {
  const cx = width / 2;
  const cy = height / 2;
  const chapters = allNodes.filter(n => n.type === 'chapter');
  const numChapters = chapters.length;

  // Compute sector center targets
  const sectorTargets = new Map();
  chapters.forEach((c, i) => {
    const angle = (i / numChapters) * 2 * Math.PI - Math.PI / 2;
    sectorTargets.set(i, {
      x: cx + 270 * Math.cos(angle),
      y: cy + 270 * Math.sin(angle),
    });
  });

  simulation = d3.forceSimulation(allNodes)
    .force('link', d3.forceLink(allLinks)
      .id(d => d.id)
      .distance(d => {
        if (d.depth === 1) return 130;
        if (d.depth === 2) return 70;
        return 28;
      })
      .strength(d => {
        if (d.depth === 1) return 0.6;
        if (d.depth === 2) return 0.5;
        return 0.7;
      })
    )
    .force('charge', d3.forceManyBody()
      .strength(d => {
        if (d.type === 'root')    return -600;
        if (d.type === 'chapter') return -200;
        if (d.type === 'section') return -60;
        return -8;
      })
    )
    .force('collide', d3.forceCollide()
      .radius(d => RADIUS[d.type] + 2)
      .strength(0.5)
    )
    .force('sector', alpha => {
      // Pull controls and sections toward their chapter sector center
      allNodes.forEach(n => {
        if (n.type === 'root' || n.type === 'chapter') return;
        const idx = n._chapterIndex ?? findChapterIndex(n, chapters);
        n._chapterIndex = idx;
        const target = sectorTargets.get(idx);
        if (!target) return;
        const strength = n.type === 'section' ? 0.04 : 0.015;
        n.vx += (target.x - n.x) * strength * alpha;
        n.vy += (target.y - n.y) * strength * alpha;
      });
    })
    .alphaDecay(0.02)
    .velocityDecay(0.4)
    .on('tick', ticked);
}

// ── Render ───────────────────────────────────────────────────────────────────

function render(svg, width, height) {
  svg.selectAll('*').remove();

  const g = svg.append('g').attr('class', 'zoom-g');

  // Zoom
  const zoom = d3.zoom()
    .scaleExtent([0.1, 8])
    .on('zoom', e => g.attr('transform', e.transform));
  svg.call(zoom);

  // Initial zoom to fit
  const initialScale = Math.min(width, height) < 700 ? 0.55 : 0.7;
  svg.call(zoom.transform, d3.zoomIdentity
    .translate(width / 2, height / 2)
    .scale(initialScale)
    .translate(-width / 2, -height / 2));

  // Links
  gLink = g.append('g').attr('class', 'links')
    .selectAll('line')
    .data(allLinks)
    .join('line')
    .attr('class', 'link')
    .attr('stroke-width', d => d.depth <= 1 ? 1.2 : 0.5);

  // Nodes
  gNode = g.append('g').attr('class', 'nodes')
    .selectAll('g')
    .data(allNodes)
    .join('g')
    .attr('class', d => `node ${d.type}`)
    .call(d3.drag()
      .on('start', dragStart)
      .on('drag',  dragged)
      .on('end',   dragEnd)
    )
    .on('click', (event, d) => {
      event.stopPropagation();
      selectNode(d);
    })
    .on('mouseenter', (event, d) => showTooltip(event, d))
    .on('mouseleave', hideTooltip);

  // Circle
  gNode.append('circle')
    .attr('r', d => RADIUS[d.type] || 4)
    .attr('fill', d => COLOR[d.type] || '#888')
    .attr('stroke', d => d3.color(COLOR[d.type] || '#888').darker(0.8))
    .attr('stroke-width', 1.2);

  // Labels for chapters only
  gNode.filter(d => d.type === 'chapter')
    .append('text')
    .attr('dy', -RADIUS.chapter - 4)
    .attr('text-anchor', 'middle')
    .attr('font-size', 9)
    .attr('fill', '#8b949e')
    .text(d => d.id);

  // Dismiss on background click
  svg.on('click', () => deselectNode());

  applyVisibility();
}

function ticked() {
  if (!gLink || !gNode) return;

  gLink
    .attr('x1', d => d.source.x)
    .attr('y1', d => d.source.y)
    .attr('x2', d => d.target.x)
    .attr('y2', d => d.target.y);

  gNode.attr('transform', d => `translate(${d.x},${d.y})`);
}

// ── Drag ─────────────────────────────────────────────────────────────────────

function dragStart(event, d) {
  if (!event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}
function dragged(event, d) {
  d.fx = event.x;
  d.fy = event.y;
}
function dragEnd(event, d) {
  if (!event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

// ── Visibility (filters + search) ────────────────────────────────────────────

function isVisible(n) {
  // Root and chapters always visible
  if (n.type === 'root' || n.type === 'chapter') return true;

  // Section filter
  if (n.type === 'section' && !activeFilters.has('section')) return false;

  // Level filters
  if (n.type === 'control-l1' && !activeFilters.has('l1')) return false;
  if (n.type === 'control-l2' && !activeFilters.has('l2')) return false;
  if (n.type === 'control-l3' && !activeFilters.has('l3')) return false;

  // Search
  if (searchTerm) {
    const hay = `${n.id} ${n.title} ${n.description}`.toLowerCase();
    if (!hay.includes(searchTerm)) return false;
  }

  return true;
}

function applyVisibility() {
  if (!gNode || !gLink) return;

  gNode.style('display', d => isVisible(d) ? null : 'none');

  gLink.style('display', d => {
    const src = typeof d.source === 'object' ? d.source : nodeById.get(d.source);
    const tgt = typeof d.target === 'object' ? d.target : nodeById.get(d.target);
    return (src && tgt && isVisible(src) && isVisible(tgt)) ? null : 'none';
  });
}

// ── Selection & detail panel ──────────────────────────────────────────────────

function selectNode(d) {
  // Clear previous active
  if (activeNode) {
    gNode.filter(n => n.id === activeNode.id)
      .classed('active', false)
      .select('circle')
      .attr('stroke-width', 1.2);
  }

  activeNode = d;

  gNode.filter(n => n.id === d.id)
    .classed('active', true)
    .select('circle')
    .attr('stroke-width', 3);

  showDetail(d);
}

function deselectNode() {
  if (activeNode) {
    gNode.filter(n => n.id === activeNode.id)
      .classed('active', false)
      .select('circle')
      .attr('stroke-width', 1.2);
    activeNode = null;
  }
  hideDetail();
}

function showDetail(d) {
  const panel = document.getElementById('detail-panel');
  const badge = document.getElementById('detail-badge');
  const title = document.getElementById('detail-title');
  const desc  = document.getElementById('detail-desc');
  const meta  = document.getElementById('detail-meta');
  const list  = document.getElementById('detail-children');

  // Badge
  const badgeLabels = {
    root: 'Standard', chapter: 'Chapter',
    section: 'Section',
    'control-l1': 'L1 Control',
    'control-l2': 'L2 Control',
    'control-l3': 'L3 Control',
  };
  badge.textContent = badgeLabels[d.type] || d.type;
  badge.className = d.type;

  // Title
  title.textContent = d.type === 'chapter'
    ? d.title || d.id
    : d.type === 'section'
    ? `${d.id} — ${d.title || ''}`
    : d.id;

  // Description
  desc.textContent = d.description || '';

  // Meta
  meta.innerHTML = '';
  if (d.level) {
    const t = document.createElement('span');
    t.className = 'meta-tag';
    t.textContent = `Level ${d.level}`;
    meta.appendChild(t);
  }
  if (d.type === 'chapter' || d.type === 'section') {
    const count = d.children.length;
    if (count) {
      const t = document.createElement('span');
      t.className = 'meta-tag';
      t.textContent = `${count} ${d.type === 'chapter' ? 'sections' : 'controls'}`;
      meta.appendChild(t);
    }
  }

  // Children list
  list.innerHTML = '';
  if (d.children && d.children.length) {
    d.children.forEach(child => {
      const li = document.createElement('li');
      const idSpan = document.createElement('span');
      idSpan.className = 'child-id';
      idSpan.textContent = child.name;
      li.appendChild(idSpan);
      if (child.type === 'section' && child.title) {
        li.appendChild(document.createTextNode(child.title));
      } else if (child.description) {
        const short = child.description.length > 120
          ? child.description.slice(0, 120) + '…'
          : child.description;
        li.appendChild(document.createTextNode(short));
      }
      li.addEventListener('click', () => {
        const n = nodeById.get(child.name);
        if (n) selectNode(n);
      });
      list.appendChild(li);
    });
  }

  panel.removeAttribute('hidden');
}

function hideDetail() {
  document.getElementById('detail-panel').setAttribute('hidden', '');
}

// ── Tooltip ───────────────────────────────────────────────────────────────────

const tooltip = document.getElementById('tooltip');

function showTooltip(event, d) {
  let text = d.id;
  if (d.type === 'section' && d.title) text = `${d.id} — ${d.title}`;
  else if (d.type === 'chapter' && d.name) text = d.name;
  else if (d.description) {
    text = d.description.length > 100 ? d.description.slice(0, 100) + '…' : d.description;
  }
  tooltip.textContent = text;
  tooltip.removeAttribute('hidden');
  moveTooltip(event);
}

function hideTooltip() {
  tooltip.setAttribute('hidden', '');
}

function moveTooltip(event) {
  const pad = 12;
  let x = event.clientX + pad;
  let y = event.clientY + pad;
  const tw = tooltip.offsetWidth;
  const th = tooltip.offsetHeight;
  if (x + tw > window.innerWidth)  x = event.clientX - tw - pad;
  if (y + th > window.innerHeight) y = event.clientY - th - pad;
  tooltip.style.left = x + 'px';
  tooltip.style.top  = y + 'px';
}

document.addEventListener('mousemove', e => {
  if (!tooltip.hasAttribute('hidden')) moveTooltip(e);
});

// ── Filter chips ──────────────────────────────────────────────────────────────

document.querySelectorAll('.chip').forEach(chip => {
  chip.addEventListener('click', () => {
    const f = chip.dataset.filter;
    if (activeFilters.has(f)) {
      activeFilters.delete(f);
      chip.classList.remove('active');
    } else {
      activeFilters.add(f);
      chip.classList.add('active');
    }
    applyVisibility();
    if (simulation) simulation.alpha(0.1).restart();
  });
});

// ── Search ────────────────────────────────────────────────────────────────────

const searchInput = document.getElementById('search');
let searchDebounce;
searchInput.addEventListener('input', () => {
  clearTimeout(searchDebounce);
  searchDebounce = setTimeout(() => {
    searchTerm = searchInput.value.trim().toLowerCase();
    applyVisibility();
    if (simulation) simulation.alpha(0.1).restart();
  }, 180);
});

// ── Close detail panel ────────────────────────────────────────────────────────

document.getElementById('close-detail').addEventListener('click', deselectNode);

// ── Resize ────────────────────────────────────────────────────────────────────

let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    if (simulation) simulation.alpha(0.2).restart();
  }, 200);
});

// ── Bootstrap ─────────────────────────────────────────────────────────────────

const svgEl = document.getElementById('graph');
const loading = document.getElementById('loading');

fetch('./data.json')
  .then(r => r.json())
  .then(data => {
    const svg = d3.select(svgEl);
    const w = svgEl.clientWidth  || window.innerWidth;
    const h = svgEl.clientHeight || window.innerHeight - 60;

    buildGraph(data);
    prePosition(w, h);
    initSimulation(w, h);
    render(svg, w, h);

    loading.classList.add('hidden');
    setTimeout(() => loading.remove(), 400);
  })
  .catch(err => {
    loading.innerHTML = `<span style="color:#f78166">Failed to load data.json: ${err.message}</span>`;
  });
