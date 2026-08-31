/**
 * 拾物档案 · 顶级在线小说阅读子站与免登录段落共读批注引擎
 */

const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000/api/novel'
  : 'https://api.shide.app/api/novel';

const VINTAGE_PERSONAS = [
  "修表客_08", "站台旅客_93", "古道掌柜_42", "拾物学徒_17", 
  "白马少年_55", "平汉工匠_19", "铜匠老罗_66", "夜班检票员_03",
  "钟表学徒_24", "海鸥表友_88", "车厢听客_37", "奉命出馆人_09"
];

// State
let catalog = [];
let currentEpisodeId = 'e1';
let currentEpisodeData = null;
let currentAnnotations = [];
let activeParagraphId = null;
let selectedStamp = null;

// DOM Elements
const bodyEl = document.body;
const progressBar = document.getElementById('readProgressBar');
const currentChapterLabel = document.getElementById('currentChapterLabel');
const btnTocToggle = document.getElementById('btnTocToggle');
const btnCloseToc = document.getElementById('btnCloseToc');
const tocDrawer = document.getElementById('tocDrawer');
const tocOverlay = document.getElementById('tocOverlay');
const tocList = document.getElementById('tocList');
const btnOpenTocBottom = document.getElementById('btnOpenTocBottom');

const btnSettingsToggle = document.getElementById('btnSettingsToggle');
const settingsPopup = document.getElementById('settingsPopup');
const btnFontSmaller = document.getElementById('btnFontSmaller');
const btnFontLarger = document.getElementById('btnFontLarger');
const fontSizeDisplay = document.getElementById('fontSizeDisplay');
const chkShowAnnotations = document.getElementById('chkShowAnnotations');

const episodeTitleEl = document.getElementById('episodeTitle');
const epMetaWordsEl = document.getElementById('epMetaWords');
const episodeBodyEl = document.getElementById('episodeBody');
const btnPrevChapter = document.getElementById('btnPrevChapter');
const btnNextChapter = document.getElementById('btnNextChapter');

const annotationOverlay = document.getElementById('annotationOverlay');
const annotationDrawer = document.getElementById('annotationDrawer');
const btnCloseAnnotation = document.getElementById('btnCloseAnnotation');
const annParagraphIdEl = document.getElementById('annParagraphId');
const annQuotePreviewEl = document.getElementById('annQuotePreview');
const annListContainer = document.getElementById('annListContainer');
const annForm = document.getElementById('annForm');
const inputNickname = document.getElementById('inputNickname');
const btnRandomizeNickname = document.getElementById('btnRandomizeNickname');
const inputComment = document.getElementById('inputComment');
const stampButtons = document.querySelectorAll('.stamp-btn');

const btnShareNovel = document.getElementById('btnShareNovel');
const quoteCardModal = document.getElementById('quoteCardModal');
const btnCloseQuoteModal = document.getElementById('btnCloseQuoteModal');
const cardQuoteText = document.getElementById('cardQuoteText');
const cardChapterMeta = document.getElementById('cardChapterMeta');
const btnCopyQuoteText = document.getElementById('btnCopyQuoteText');

// --- Init Application ---
async function init() {
  loadSettings();
  initNickname();
  initEventListeners();
  
  try {
    const res = await fetch('./data/catalog.json');
    catalog = await res.json();
    renderTOC();
    
    // Determine start chapter from Hash or localStorage
    const hash = window.location.hash.replace('#', '').toLowerCase();
    const validEp = catalog.find(c => c.id.toLowerCase() === hash);
    if (validEp) {
      currentEpisodeId = validEp.id.toLowerCase();
    } else {
      const savedEp = localStorage.getItem('shide_novel_last_ep');
      if (savedEp && catalog.some(c => c.id.toLowerCase() === savedEp)) {
        currentEpisodeId = savedEp;
      }
    }
    
    loadEpisode(currentEpisodeId);
  } catch (err) {
    console.error('Failed to load catalog:', err);
  }
}

// --- Load Episode ---
async function loadEpisode(epId) {
  currentEpisodeId = epId.toLowerCase();
  localStorage.setItem('shide_novel_last_ep', currentEpisodeId);
  window.location.hash = currentEpisodeId;
  
  episodeBodyEl.innerHTML = '<div class="loading-spinner">正在展开卷轴...</div>';
  window.scrollTo({ top: 0, behavior: 'smooth' });
  
  try {
    const res = await fetch(`./data/${currentEpisodeId}.json`);
    currentEpisodeData = await res.json();
    
    // Update Header and Metadata
    currentChapterLabel.textContent = `${currentEpisodeData.label} · ${currentEpisodeData.title}`;
    episodeTitleEl.textContent = `${currentEpisodeData.label} · 《${currentEpisodeData.title}》`;
    epMetaWordsEl.textContent = `全篇 ${currentEpisodeData.char_count.toLocaleString()} 字`;
    document.title = `${currentEpisodeData.label} 《${currentEpisodeData.title}》 · 拾物档案 | 拾得 Ensō`;
    
    // Render Content
    renderParagraphs(currentEpisodeData.paragraphs);
    updateTOCActiveState();
    updateNavigationButtons();
    
    // Fetch Annotations
    fetchAnnotations(currentEpisodeId);
  } catch (err) {
    episodeBodyEl.innerHTML = '<div class="loading-spinner">正文加载失败，请刷新重试。</div>';
    console.error(err);
  }
}

// --- Render Paragraphs ---
function renderParagraphs(paragraphs) {
  episodeBodyEl.innerHTML = '';
  
  paragraphs.forEach(p => {
    if (p.is_subhead) {
      const h = document.createElement('h2');
      h.className = 'prose-subhead';
      h.textContent = p.text.replace(/^#+\s*/, '');
      episodeBodyEl.appendChild(h);
    } else {
      const pEl = document.createElement('p');
      pEl.className = 'prose-p';
      pEl.id = `p-${p.pid}`;
      pEl.dataset.pid = p.pid;
      pEl.textContent = p.text;
      
      // Annotation pill on the right
      const pill = document.createElement('span');
      pill.className = 'ann-pill';
      pill.dataset.pid = p.pid;
      pill.title = '点击查看/添加此段批注';
      pill.innerHTML = `<span class="pill-icon">💬</span><span class="ann-count" id="count-p-${p.pid}"></span>`;
      
      pill.addEventListener('click', (e) => {
        e.stopPropagation();
        openAnnotationDrawer(p.pid, p.text);
      });
      
      pEl.appendChild(pill);
      
      pEl.addEventListener('click', () => {
        openAnnotationDrawer(p.pid, p.text);
      });
      
      episodeBodyEl.appendChild(pEl);
    }
  });
}

// --- Annotations System ---
async function fetchAnnotations(epId) {
  try {
    const res = await fetch(`${API_BASE}/annotations?novel_id=shiwu-s1&chapter_id=${epId}`);
    if (res.ok) {
      const data = await res.json();
      currentAnnotations = data.annotations || [];
      updateParagraphPills();
    }
  } catch (e) {
    console.warn('Backend offline or unreachable, using local storage fallback');
    loadLocalAnnotations();
  }
}

function loadLocalAnnotations() {
  const local = JSON.parse(localStorage.getItem(`shide_ann_${currentEpisodeId}`) || '[]');
  currentAnnotations = local;
  updateParagraphPills();
}

function updateParagraphPills() {
  // Count by pid
  const counts = {};
  currentAnnotations.forEach(a => {
    if (!a.parent_id) {
      counts[a.paragraph_id] = (counts[a.paragraph_id] || 0) + 1;
    }
  });
  
  document.querySelectorAll('.ann-pill').forEach(pill => {
    const pid = parseInt(pill.dataset.pid);
    const count = counts[pid] || 0;
    const countEl = pill.querySelector('.ann-count');
    if (count > 0) {
      pill.classList.add('has-comments');
      countEl.textContent = ` ${count}`;
    } else {
      pill.classList.remove('has-comments');
      countEl.textContent = '';
    }
  });
}

function openAnnotationDrawer(pid, quoteText) {
  activeParagraphId = pid;
  
  // Highlight paragraph
  document.querySelectorAll('.prose-p').forEach(p => p.classList.remove('highlighted'));
  const pEl = document.getElementById(`p-${pid}`);
  if (pEl) pEl.classList.add('highlighted');
  
  annParagraphIdEl.textContent = `第 ${pid} 段`;
  annQuotePreviewEl.textContent = `“${quoteText}”`;
  
  renderDrawerAnnotations(pid);
  
  annotationOverlay.classList.remove('hidden');
  annotationDrawer.classList.remove('hidden');
}

function closeAnnotationDrawer() {
  annotationOverlay.classList.add('hidden');
  annotationDrawer.classList.add('hidden');
  document.querySelectorAll('.prose-p').forEach(p => p.classList.remove('highlighted'));
  activeParagraphId = null;
}

function renderDrawerAnnotations(pid) {
  annListContainer.innerHTML = '';
  const paraAnnotations = currentAnnotations.filter(a => a.paragraph_id === pid && !a.parent_id);
  
  if (paraAnnotations.length === 0) {
    annListContainer.innerHTML = `
      <div class="empty-ann-state">
        <p>这一段暂无读者批注</p>
        <span>成为第一个在此段留下洞察与推测的读者吧！</span>
      </div>
    `;
    return;
  }
  
  paraAnnotations.forEach(ann => {
    const card = document.createElement('div');
    card.className = 'ann-card';
    
    const timeStr = formatRelativeTime(ann.created_at);
    const stampHtml = ann.stamp ? `<span class="ann-stamp-pill">${ann.stamp}</span>` : '';
    
    // Find replies
    const replies = currentAnnotations.filter(a => a.parent_id === ann.id);
    let repliesHtml = '';
    if (replies.length > 0) {
      repliesHtml = `
        <div class="nested-replies-box">
          ${replies.map(r => `
            <div class="nested-reply-item">
              <span class="nested-author">${escapeHtml(r.nickname)}：</span>
              <span class="nested-text">${escapeHtml(r.content)}</span>
            </div>
          `).join('')}
        </div>
      `;
    }
    
    card.innerHTML = `
      <div class="ann-card-header">
        <div class="ann-author-badge">
          <span>${escapeHtml(ann.nickname)}</span>
          ${stampHtml}
        </div>
        <span class="ann-time-label">${timeStr}</span>
      </div>
      <div class="ann-content-body">${escapeHtml(ann.content)}</div>
      <div class="ann-card-actions">
        <button class="ann-action-btn btn-like" data-id="${ann.id}">
          ❤️ <span class="like-count">${ann.likes || 0}</span>
        </button>
        <button class="ann-action-btn btn-reply" data-id="${ann.id}" data-author="${escapeHtml(ann.nickname)}">
          💬 回复
        </button>
        <button class="ann-action-btn btn-share-quote" data-quote="${escapeHtml(ann.quote_text || '')}" data-comment="${escapeHtml(ann.content)}" data-author="${escapeHtml(ann.nickname)}">
          📜 分享金句
        </button>
      </div>
      ${repliesHtml}
    `;
    
    // Bind Like Action
    card.querySelector('.btn-like').addEventListener('click', async function() {
      const id = this.dataset.id;
      const countEl = this.querySelector('.like-count');
      this.classList.add('liked');
      countEl.textContent = parseInt(countEl.textContent) + 1;
      
      try {
        await fetch(`${API_BASE}/annotations/${id}/like`, { method: 'POST' });
      } catch (e) {
        console.warn('Like stored locally');
      }
    });
    
    // Bind Reply Action
    card.querySelector('.btn-reply').addEventListener('click', function() {
      const author = this.dataset.author;
      inputComment.value = `@${author} `;
      inputComment.focus();
    });
    
    // Bind Share Quote Action
    card.querySelector('.btn-share-quote').addEventListener('click', function() {
      openQuoteModal(this.dataset.quote, this.dataset.comment, this.dataset.author);
    });
    
    annListContainer.appendChild(card);
  });
}

// --- Submit Annotation ---
annForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = inputComment.value.trim();
  const nickname = inputNickname.value.trim() || '拾得读者';
  if (!text || !activeParagraphId) return;
  
  const quoteText = annQuotePreviewEl.textContent.replace(/^“|”$/g, '');
  
  // Check if replying to someone
  let parentId = null;
  const replyMatch = text.match(/^@([^\s]+)\s+/);
  if (replyMatch) {
    const parentAnn = currentAnnotations.find(a => a.nickname === replyMatch[1] && a.paragraph_id === activeParagraphId);
    if (parentAnn) parentId = parentAnn.id;
  }
  
  const newAnn = {
    id: `local_${Date.now()}`,
    novel_id: 'shiwu-s1',
    chapter_id: currentEpisodeId,
    paragraph_id: activeParagraphId,
    quote_text: quoteText,
    nickname: nickname,
    content: text,
    stamp: selectedStamp,
    likes: 0,
    parent_id: parentId,
    created_at: Date.now() / 1000
  };
  
  // Optimistic UI Update
  currentAnnotations.push(newAnn);
  renderDrawerAnnotations(activeParagraphId);
  updateParagraphPills();
  inputComment.value = '';
  
  // Persist
  try {
    const res = await fetch(`${API_BASE}/annotations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        novel_id: 'shiwu-s1',
        chapter_id: currentEpisodeId,
        paragraph_id: activeParagraphId,
        quote_text: quoteText,
        nickname: nickname,
        content: text,
        stamp: selectedStamp,
        parent_id: parentId
      })
    });
    if (res.ok) {
      const data = await res.json();
      newAnn.id = data.annotation.id;
    }
  } catch (err) {
    // Save to localStorage as fallback
    localStorage.setItem(`shide_ann_${currentEpisodeId}`, JSON.stringify(currentAnnotations));
  }
});

// --- Quote Share Card Modal ---
function openQuoteModal(quote, comment, author) {
  cardQuoteText.textContent = `“${quote || annQuotePreviewEl.textContent.replace(/^“|”$/g, '')}”`;
  cardChapterMeta.textContent = `《拾物档案》· ${currentEpisodeData.label} 《${currentEpisodeData.title}》`;
  
  const commentBox = document.getElementById('cardUserComment');
  const userTag = document.getElementById('cardUserTag');
  const commentText = document.getElementById('cardCommentText');
  
  if (comment) {
    commentBox.style.display = 'block';
    userTag.textContent = `${author} 批注：`;
    commentText.textContent = comment;
  } else {
    commentBox.style.display = 'none';
  }
  
  quoteCardModal.classList.remove('hidden');
}

btnCopyQuoteText.addEventListener('click', () => {
  const text = `${cardQuoteText.textContent}\n\n—— 选自《拾物档案》${currentEpisodeData.label}《${currentEpisodeData.title}》\n在线共读：https://shide.app/novel/#${currentEpisodeId}`;
  navigator.clipboard.writeText(text);
  btnCopyQuoteText.textContent = '✅ 已复制金句';
  setTimeout(() => btnCopyQuoteText.textContent = '复制纯文本', 2000);
});

btnCloseQuoteModal.addEventListener('click', () => {
  quoteCardModal.classList.add('hidden');
});

// --- Settings & Themes ---
function loadSettings() {
  const theme = localStorage.getItem('shide_novel_theme') || 'theme-paper';
  setTheme(theme);
  
  const fontSize = parseInt(localStorage.getItem('shide_novel_fontsize') || '19');
  setFontSize(fontSize);
}

function setTheme(theme) {
  bodyEl.classList.remove('theme-paper', 'theme-dark', 'theme-bamboo');
  bodyEl.classList.add(theme);
  localStorage.setItem('shide_novel_theme', theme);
  document.querySelectorAll('.theme-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.theme === theme);
  });
}

function setFontSize(size) {
  const clamped = Math.max(16, Math.min(26, size));
  document.documentElement.style.setProperty('--base-font-size', `${clamped}px`);
  fontSizeDisplay.textContent = `${clamped}px`;
  localStorage.setItem('shide_novel_fontsize', clamped);
}

// --- TOC & Navigation ---
function renderTOC() {
  tocList.innerHTML = '';
  catalog.forEach(ep => {
    const li = document.createElement('li');
    li.className = 'toc-item';
    li.innerHTML = `
      <button class="toc-item-btn" data-id="${ep.id}">
        <div class="toc-item-num">${ep.label}</div>
        <div class="toc-item-title">《${ep.title}》</div>
        <div class="toc-item-meta">${ep.char_count.toLocaleString()} 字 · ${ep.paragraphs_count} 段</div>
      </button>
    `;
    li.querySelector('.toc-item-btn').addEventListener('click', () => {
      loadEpisode(ep.id);
      closeTOC();
    });
    tocList.appendChild(li);
  });
}

function updateTOCActiveState() {
  document.querySelectorAll('.toc-item-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.id.toLowerCase() === currentEpisodeId);
  });
}

function updateNavigationButtons() {
  const idx = catalog.findIndex(c => c.id.toLowerCase() === currentEpisodeId);
  btnPrevChapter.disabled = idx <= 0;
  btnNextChapter.disabled = idx >= catalog.length - 1;
  btnPrevChapter.style.opacity = idx <= 0 ? '0.4' : '1';
  btnNextChapter.style.opacity = idx >= catalog.length - 1 ? '0.4' : '1';
}

function openTOC() {
  tocOverlay.classList.remove('hidden');
  tocDrawer.classList.remove('hidden');
}

function closeTOC() {
  tocOverlay.classList.add('hidden');
  tocDrawer.classList.add('hidden');
}

// --- Nickname Randomizer ---
function initNickname() {
  const saved = localStorage.getItem('shide_novel_nickname');
  if (saved) {
    inputNickname.value = saved;
  } else {
    randomizeNickname();
  }
}

function randomizeNickname() {
  const r = VINTAGE_PERSONAS[Math.floor(Math.random() * VINTAGE_PERSONAS.length)];
  inputNickname.value = r;
  localStorage.setItem('shide_novel_nickname', r);
}

inputNickname.addEventListener('change', () => {
  localStorage.setItem('shide_novel_nickname', inputNickname.value.trim());
});

btnRandomizeNickname.addEventListener('click', randomizeNickname);

// --- Helpers ---
function formatRelativeTime(ts) {
  if (!ts) return '刚刚';
  const diff = Math.floor(Date.now() / 1000 - ts);
  if (diff < 60) return '刚刚';
  if (diff < 3600) return `${Math.floor(diff / 60)}分钟前`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}小时前`;
  return `${Math.floor(diff / 86400)}天前`;
}

function escapeHtml(str) {
  return (str || '').replace(/[&<>"']/g, m => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[m]));
}

// --- Event Listeners ---
function initEventListeners() {
  // TOC
  btnTocToggle.addEventListener('click', openTOC);
  btnCloseToc.addEventListener('click', closeTOC);
  tocOverlay.addEventListener('click', closeTOC);
  btnOpenTocBottom.addEventListener('click', openTOC);
  
  // Chapter Nav
  btnPrevChapter.addEventListener('click', () => {
    const idx = catalog.findIndex(c => c.id.toLowerCase() === currentEpisodeId);
    if (idx > 0) loadEpisode(catalog[idx - 1].id);
  });
  btnNextChapter.addEventListener('click', () => {
    const idx = catalog.findIndex(c => c.id.toLowerCase() === currentEpisodeId);
    if (idx < catalog.length - 1) loadEpisode(catalog[idx + 1].id);
  });
  
  // Settings
  btnSettingsToggle.addEventListener('click', () => {
    settingsPopup.classList.toggle('hidden');
  });
  document.addEventListener('click', (e) => {
    if (!settingsPopup.contains(e.target) && e.target !== btnSettingsToggle) {
      settingsPopup.classList.add('hidden');
    }
  });
  document.querySelectorAll('.theme-btn').forEach(btn => {
    btn.addEventListener('click', () => setTheme(btn.dataset.theme));
  });
  btnFontSmaller.addEventListener('click', () => {
    const current = parseInt(localStorage.getItem('shide_novel_fontsize') || '19');
    setFontSize(current - 1);
  });
  btnFontLarger.addEventListener('click', () => {
    const current = parseInt(localStorage.getItem('shide_novel_fontsize') || '19');
    setFontSize(current + 1);
  });
  chkShowAnnotations.addEventListener('change', (e) => {
    document.querySelectorAll('.ann-pill').forEach(pill => {
      pill.style.display = e.target.checked ? 'inline-flex' : 'none';
    });
  });
  
  // Drawer
  btnCloseAnnotation.addEventListener('click', closeAnnotationDrawer);
  annotationOverlay.addEventListener('click', closeAnnotationDrawer);
  
  // Stamps
  stampButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      if (btn.classList.contains('selected')) {
        btn.classList.remove('selected');
        selectedStamp = null;
      } else {
        stampButtons.forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        selectedStamp = btn.dataset.stamp;
      }
    });
  });
  
  // Share Novel
  btnShareNovel.addEventListener('click', () => {
    openQuoteModal('', '', '');
  });
  
  // Scroll Progress
  window.addEventListener('scroll', () => {
    const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    progressBar.style.width = `${scrolled}%`;
  });
}

// Start
init();
