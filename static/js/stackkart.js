function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function formatPrice(value) {
  const number = Number(value || 0);
  return `$${number.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

/* Cart Panel */
const cartOverlay = document.getElementById('cartOverlay');
const cartPanel = document.getElementById('cartPanel');
const cartOpenBtn = document.getElementById('cartOpenBtn');
const cartCloseBtn = document.getElementById('cartCloseBtn');

function openCartPanel() {
  if (cartOverlay && cartPanel) {
    cartOverlay.classList.add('open');
    cartPanel.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
}

function closeCartPanel() {
  if (cartOverlay && cartPanel) {
    cartOverlay.classList.remove('open');
    cartPanel.classList.remove('open');
    document.body.style.overflow = '';
  }
}

if (cartOpenBtn) cartOpenBtn.addEventListener('click', openCartPanel);
if (cartCloseBtn) cartCloseBtn.addEventListener('click', closeCartPanel);
if (cartOverlay) cartOverlay.addEventListener('click', closeCartPanel);

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeCartPanel();
    closeWishlistPanel();
    closeQuickView();
  }
});

/* Cart Panel Rendering (slide-out panel) */
function updateCartPanel(cart) {
  const items = cart.items || [];
  const totalQuantity = items.reduce((sum, item) => sum + Number(item.quantity || 0), 0);

  const cartCounts = document.querySelectorAll('.cart-count');
  cartCounts.forEach(el => el.textContent = totalQuantity);

  const panelCount = document.getElementById('cartPanelCount');
  if (panelCount) panelCount.textContent = `${totalQuantity} item${totalQuantity !== 1 ? 's' : ''}`;

  const latestImg = document.getElementById('cartLatestImg');
  const latestPlaceholder = document.getElementById('cartLatestPlaceholder');
  const latestName = document.getElementById('cartLatestName');
  const latestMeta = document.getElementById('cartLatestMeta');
  const latestPrice = document.getElementById('cartLatestPrice');

  if (!items.length) {
    if (latestName) latestName.textContent = 'Your cart is empty';
    if (latestMeta) latestMeta.textContent = 'Add a product to get started';
    if (latestPrice) latestPrice.textContent = '$0.00';
    if (latestImg) { latestImg.style.display = 'none'; latestImg.src = ''; }
    if (latestPlaceholder) { latestPlaceholder.style.display = 'grid'; latestPlaceholder.textContent = '🛒'; }
  } else {
    const latest = items[items.length - 1];
    const product = latest.product || {};
    if (latestName) latestName.textContent = product.name || 'Cart item';
    if (latestMeta) latestMeta.textContent = product.subtitle || product.category?.name || 'Product';
    if (latestPrice) latestPrice.textContent = formatPrice(latest.line_total || product.price || 0);
    if (product.image_url) {
      if (latestImg) { latestImg.style.display = 'block'; latestImg.src = product.image_url; }
      if (latestPlaceholder) latestPlaceholder.style.display = 'none';
    } else {
      if (latestImg) latestImg.style.display = 'none';
      if (latestPlaceholder) { latestPlaceholder.style.display = 'grid'; latestPlaceholder.textContent = (product.name || '?')[0]; }
    }
  }

  const miniList = document.getElementById('cartMiniList');
  if (miniList) {
    if (!items.length) {
      miniList.innerHTML = '<p style="color:var(--muted);font-size:0.9rem;text-align:center;padding:20px 0;">Your cart is empty.</p>';
    } else {
      miniList.innerHTML = items.map(item => renderMiniItem(item)).join('');
    }
  }

  const subtotalEl = document.getElementById('cartSubtotal');
  if (subtotalEl) subtotalEl.textContent = formatPrice(cart.total || 0);
}

/* Render a single mini cart item HTML */
function renderMiniItem(item) {
  const product = item.product || {};
  const img = product.image_url
    ? `<img src="${product.image_url}" alt="${product.name}" loading="lazy">`
    : `<div class="placeholder">${(product.name || '?')[0]}</div>`;
  return `
    <div class="cart-mini-item" data-item-id="${item.id}">
      ${img}
      <div class="cart-mini-info">
        <h4>${product.name || 'Item'}</h4>
        <div class="cart-mini-price">${formatPrice(item.line_total || product.price || 0)}</div>
      </div>
      <div class="cart-mini-actions">
        <button class="qty-btn" data-qty-change="${item.id}" data-delta="-1">-</button>
        <span class="qty-value">${item.quantity}</span>
        <button class="qty-btn" data-qty-change="${item.id}" data-delta="1">+</button>
        <button class="cart-mini-remove" data-remove="${item.id}" aria-label="Remove item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
        </button>
      </div>
    </div>
  `;
}

/* Homepage Sidebar Update — NO page reloads */
function updateSidebar(cart) {
  const sidebar = document.querySelector('.cart-sidebar');
  if (!sidebar) return;

  const items = cart.items || [];
  const totalQuantity = items.reduce((sum, item) => sum + Number(item.quantity || 0), 0);

  // Update header count
  const headerCount = sidebar.querySelector('.cart-sidebar-header .cart-item-count');
  if (headerCount) headerCount.textContent = `${totalQuantity} item${totalQuantity !== 1 ? 's' : ''}`;

  // Rebuild body
  const body = sidebar.querySelector('.cart-sidebar-body');
  if (!body) return;

  if (!items.length) {
    body.innerHTML = `
      <div class="cart-latest-label">Latest added item</div>
      <div class="cart-latest-item">
        <div class="placeholder">🛒</div>
        <div class="cart-latest-info">
          <h4>Your cart is empty</h4>
          <p>Add a product to get started</p>
          <div class="cart-latest-price">$0.00</div>
        </div>
      </div>
      <p style="color:var(--muted);font-size:0.9rem;text-align:center;padding:20px 0;">Your cart is empty.</p>
    `;
  } else {
    const latest = items[items.length - 1];
    const latestProduct = latest.product || {};
    const latestImg = latestProduct.image_url
      ? `<img src="${latestProduct.image_url}" alt="${latestProduct.name}">`
      : `<div class="placeholder">${(latestProduct.name || '?')[0]}</div>`;

    body.innerHTML = `
      <div class="cart-latest-label">Latest added item</div>
      <div class="cart-latest-item">
        ${latestImg}
        <div class="cart-latest-info">
          <h4>${latestProduct.name || 'Cart item'}</h4>
          <p>${latestProduct.subtitle || latestProduct.category?.name || 'Product'}</p>
          <div class="cart-latest-price">${formatPrice(latest.line_total || latestProduct.price || 0)}</div>
        </div>
      </div>
      <div class="cart-list-mini">
        ${items.map(item => renderMiniItem(item)).join('')}
      </div>
    `;
  }

  // Update footer subtotal
  const subtotal = sidebar.querySelector('.cart-sidebar-footer .cart-subtotal-line strong');
  if (subtotal) subtotal.textContent = formatPrice(cart.total || 0);
}

async function refreshCart() {
  try {
    const res = await fetch('/api/v1/cart/');
    if (!res.ok) throw new Error('Cart fetch failed');
    const cart = await res.json();
    updateCartPanel(cart);
    updateSidebar(cart);
    return cart;
  } catch (e) {
    console.warn('Cart refresh error:', e);
  }
}

/* Add to cart */
document.addEventListener('click', async (event) => {
  const button = event.target.closest('[data-add-cart]');
  if (!button) return;
  button.disabled = true;
  const oldText = button.innerHTML;
  button.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
  try {
    const res = await fetch('/api/v1/cart/add/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') || '' },
      body: JSON.stringify({ product_id: button.dataset.addCart, quantity: 1 })
    });
    if (!res.ok) throw new Error('Cart request failed');
    const cart = await res.json();
    updateCartPanel(cart);
    updateSidebar(cart);
    button.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
    setTimeout(() => button.innerHTML = oldText, 1400);
  } catch (err) {
    button.innerHTML = '!';
    setTimeout(() => button.innerHTML = oldText, 1400);
  } finally {
    button.disabled = false;
  }
});

/* Cart panel / sidebar interactions (quantity + remove) */
document.addEventListener('click', async (event) => {
  const qtyBtn = event.target.closest('[data-qty-change]');
  const removeBtn = event.target.closest('[data-remove]');

  if (qtyBtn) {
    const itemId = qtyBtn.dataset.qtyChange;
    const delta = parseInt(qtyBtn.dataset.delta, 10);
    const qtyValue = qtyBtn.parentElement.querySelector('.qty-value');
    const currentQty = parseInt(qtyValue.textContent, 10);
    const newQty = currentQty + delta;
    if (newQty < 1) return;

    try {
      const res = await fetch(`/api/v1/cart/item/${itemId}/`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') || '' },
        body: JSON.stringify({ quantity: newQty })
      });
      if (!res.ok) throw new Error('Update failed');
      const cart = await res.json();
      updateCartPanel(cart);
      updateSidebar(cart);
    } catch (e) {
      console.warn('Qty update failed:', e);
    }
  }

  if (removeBtn) {
    const itemId = removeBtn.dataset.remove;
    try {
      const res = await fetch(`/api/v1/cart/item/${itemId}/`, {
        method: 'DELETE',
        headers: { 'X-CSRFToken': getCookie('csrftoken') || '' }
      });
      if (!res.ok) throw new Error('Remove failed');
      await refreshCart();
    } catch (e) {
      console.warn('Remove failed:', e);
    }
  }
});

/* Theme toggle with icon switching */
const themeToggle = document.getElementById('themeToggle');
const darkIcon = document.querySelector('.theme-icon-dark');
const lightIcon = document.querySelector('.theme-icon-light');

function updateThemeIcons() {
  const isLight = document.documentElement.classList.contains('light');
  if (darkIcon) darkIcon.style.display = isLight ? 'none' : 'inline';
  if (lightIcon) lightIcon.style.display = isLight ? 'inline' : 'none';
}

if (themeToggle) {
  updateThemeIcons();
  themeToggle.addEventListener('click', () => {
    document.documentElement.classList.toggle('light');
    const isLight = document.documentElement.classList.contains('light');
    localStorage.setItem('stackkart-theme', isLight ? 'light' : 'dark');
    updateThemeIcons();
  });
}

/* Search shortcut (⌘K / Ctrl+K) */
document.addEventListener('keydown', (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault();
    const searchInput = document.querySelector('.nav-search input');
    if (searchInput) searchInput.focus();
  }
});

/* Mobile nav toggle */
const mobileToggle = document.getElementById('mobileToggle');
const mobileNav = document.getElementById('mobileNav');
if (mobileToggle && mobileNav) {
  mobileToggle.addEventListener('click', () => {
    mobileNav.classList.toggle('open');
  });
}

/* Initialize */
refreshCart();

/* ============================
   WISHLIST
   ============================ */

const WISHLIST_GUEST_KEY = 'stackkart-wishlist-guest';
const WISHLIST_GUEST_DATA_KEY = 'stackkart-wishlist-guest-data';

function getGuestWishlist() {
  try {
    return JSON.parse(localStorage.getItem(WISHLIST_GUEST_KEY) || '[]');
  } catch { return []; }
}

function setGuestWishlist(ids) {
  localStorage.setItem(WISHLIST_GUEST_KEY, JSON.stringify(ids));
}

function getGuestWishlistData() {
  try {
    return JSON.parse(localStorage.getItem(WISHLIST_GUEST_DATA_KEY) || '{}');
  } catch { return {}; }
}

function setGuestWishlistData(data) {
  localStorage.setItem(WISHLIST_GUEST_DATA_KEY, JSON.stringify(data));
}

function updateWishlistUI(activeIds) {
  const idSet = new Set(activeIds.map(String));
  document.querySelectorAll('[data-wishlist-id]').forEach(btn => {
    const pid = btn.dataset.wishlistId;
    const isActive = idSet.has(pid);
    btn.classList.toggle('active', isActive);
    const svg = btn.querySelector('svg');
    if (svg) svg.setAttribute('fill', isActive ? 'currentColor' : 'none');
    const label = btn.querySelector('.wishlist-label');
    if (label) label.textContent = isActive ? 'Saved' : 'Save';
  });
  const badge = document.getElementById('wishlistCount');
  if (badge) {
    badge.textContent = activeIds.length;
    badge.style.display = activeIds.length > 0 ? 'grid' : 'none';
  }
}

async function toggleWishlist(productId, button) {
  const isAuthenticated = document.body.dataset.authenticated === 'true';
  if (!isAuthenticated) {
    const ids = getGuestWishlist();
    const data = getGuestWishlistData();
    const idx = ids.indexOf(productId);
    if (idx > -1) {
      ids.splice(idx, 1);
      delete data[productId];
    } else {
      ids.push(productId);
      const raw = button.dataset.wishlistData;
      if (raw) {
        try { data[productId] = JSON.parse(raw); }
        catch (e) { data[productId] = { id: productId, name: 'Product', price: 0, slug: '' }; }
      }
    }
    setGuestWishlist(ids);
    setGuestWishlistData(data);
    updateWishlistUI(ids);
    return;
  }
  button.disabled = true;
  try {
    const res = await fetch('/api/v1/wishlist/toggle/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') || '' },
      body: JSON.stringify({ product_id: productId })
    });
    if (!res.ok) throw new Error('Wishlist toggle failed');
    const listRes = await fetch('/api/v1/wishlist/');
    const list = await listRes.json();
    updateWishlistUI(list.map(i => i.product.id));
  } catch (e) {
    console.warn('Wishlist toggle error:', e);
  } finally {
    button.disabled = false;
  }
}

async function syncGuestWishlist() {
  const guestIds = getGuestWishlist();
  if (!guestIds.length) return;
  try {
    const res = await fetch('/api/v1/wishlist/sync/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') || '' },
      body: JSON.stringify({ product_ids: guestIds })
    });
    if (res.ok) {
      localStorage.removeItem(WISHLIST_GUEST_KEY);
      localStorage.removeItem(WISHLIST_GUEST_DATA_KEY);
      const listRes = await fetch('/api/v1/wishlist/');
      const list = await listRes.json();
      updateWishlistUI(list.map(i => i.product.id));
    }
  } catch (e) {
    console.warn('Wishlist sync error:', e);
  }
}

async function loadWishlist() {
  const isAuthenticated = document.body.dataset.authenticated === 'true';
  if (isAuthenticated) {
    await syncGuestWishlist();
    try {
      const res = await fetch('/api/v1/wishlist/');
      if (!res.ok) throw new Error('Failed to load wishlist');
      const list = await res.json();
      updateWishlistUI(list.map(i => i.product.id));
    } catch (e) {
      console.warn('Wishlist load error:', e);
    }
  } else {
    updateWishlistUI(getGuestWishlist());
  }
}

document.addEventListener('click', (e) => {
  const btn = e.target.closest('[data-wishlist-id]');
  if (!btn) return;
  e.preventDefault();
  e.stopPropagation();
  toggleWishlist(btn.dataset.wishlistId, btn);
});

/* Wishlist Panel */
const wishlistOverlay = document.getElementById('wishlistOverlay');
const wishlistPanel = document.getElementById('wishlistPanel');
const wishlistOpenBtn = document.getElementById('wishlistOpenBtn');
const wishlistCloseBtn = document.getElementById('wishlistCloseBtn');

function openWishlistPanel() {
  if (wishlistOverlay && wishlistPanel) {
    renderWishlistPanel();
    wishlistOverlay.classList.add('open');
    wishlistPanel.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
}

function closeWishlistPanel() {
  if (wishlistOverlay && wishlistPanel) {
    wishlistOverlay.classList.remove('open');
    wishlistPanel.classList.remove('open');
    document.body.style.overflow = '';
  }
}

if (wishlistOpenBtn) wishlistOpenBtn.addEventListener('click', openWishlistPanel);
if (wishlistCloseBtn) wishlistCloseBtn.addEventListener('click', closeWishlistPanel);
if (wishlistOverlay) wishlistOverlay.addEventListener('click', closeWishlistPanel);

async function renderWishlistPanel() {
  const body = document.getElementById('wishlistBody');
  const count = document.getElementById('wishlistPanelCount');
  const isAuthenticated = document.body.dataset.authenticated === 'true';
  let items = [];

  if (isAuthenticated) {
    try {
      const res = await fetch('/api/v1/wishlist/');
      if (!res.ok) throw new Error();
      items = await res.json();
    } catch (e) {
      if (body) body.innerHTML = '<p style="color:var(--muted);text-align:center;padding:40px 0;">Failed to load wishlist.</p>';
      return;
    }
  } else {
    const data = getGuestWishlistData();
    items = Object.values(data);
  }

  if (count) count.textContent = `${items.length} item${items.length !== 1 ? 's' : ''}`;

  if (!items.length) {
    if (body) {
      body.innerHTML = '<p style="color:var(--muted);text-align:center;padding:40px 0;">Your wishlist is empty. Save items you love to find them here.</p>';
    }
    return;
  }

  if (body) {
    body.innerHTML = items.map(item => {
      const p = item.product || item;
      const img = p.image_url
        ? `<img src="${p.image_url}" alt="${p.name}" loading="lazy">`
        : `<div class="placeholder">${(p.name || '?')[0]}</div>`;
      return `
        <div class="wishlist-item">
          <a href="/products/${p.slug}/" class="wishlist-thumb">${img}</a>
          <div class="wishlist-info">
            <h4>${p.name}</h4>
            <p>${p.subtitle || ''}</p>
            <div class="wishlist-price">${formatPrice(p.price)}</div>
          </div>
          <div class="wishlist-actions">
            <button class="btn-cart" data-add-cart="${p.id}" aria-label="Add to cart">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>
            </button>
            <button class="wishlist-remove" data-wishlist-remove="${p.id}" aria-label="Remove from wishlist">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
            </button>
          </div>
        </div>
      `;
    }).join('');
  }
}

/* Remove from wishlist via panel */
document.addEventListener('click', (e) => {
  const btn = e.target.closest('[data-wishlist-remove]');
  if (!btn) return;
  const pid = btn.dataset.wishlistRemove;
  const heartBtn = document.querySelector(`[data-wishlist-id="${pid}"]`);
  if (heartBtn) {
    toggleWishlist(pid, heartBtn).then(() => renderWishlistPanel());
  } else {
    toggleWishlist(pid, btn).then(() => renderWishlistPanel());
  }
});

/* ============================
   QUICK VIEW MODAL
   ============================ */

const qvOverlay = document.getElementById('quickViewOverlay');
const qvClose = document.getElementById('quickViewClose');
const qvContent = document.getElementById('quickViewContent');

function openQuickView(productId) {
  if (!qvOverlay || !qvContent) return;
  qvOverlay.style.display = 'flex';
  // small delay to allow display:flex before adding opacity class
  requestAnimationFrame(() => qvOverlay.classList.add('open'));
  document.body.style.overflow = 'hidden';

  qvContent.innerHTML = `
    <div class="modal-media skeletonPulse" style="background:var(--surface);display:grid;place-items:center;">
      <div class="modal-skeleton" style="width:80%;height:80%;"></div>
    </div>
    <div class="modal-info">
      <div class="modal-skeleton" style="width:60px;height:16px;margin-bottom:12px;"></div>
      <div class="modal-skeleton" style="width:80%;height:28px;margin-bottom:12px;"></div>
      <div class="modal-skeleton" style="width:100%;height:80px;margin-bottom:20px;"></div>
      <div class="modal-skeleton" style="width:100px;height:24px;margin-bottom:20px;"></div>
      <div class="modal-skeleton" style="width:100%;height:44px;"></div>
    </div>
  `;

  fetch(`/api/v1/products/${productId}/`)
    .then(r => r.ok ? r.json() : Promise.reject())
    .then(p => {
      const img = p.image_url
        ? `<img src="${p.image_url}" alt="${p.name}">`
        : `<div class="placeholder-img" style="width:100%;aspect-ratio:1;display:grid;place-items:center;font-size:5rem;font-weight:900;color:var(--accent);background:linear-gradient(135deg,#111827,#0d1117);">${p.name[0]}</div>`;
      const badge = p.tag
        ? `<span class="card-badge ${p.tag}" style="position:absolute;top:12px;left:12px;">${p.tag === 'sale' && p.discount_percent ? '-' + p.discount_percent + '%' : p.tag}</span>`
        : '';
      qvContent.innerHTML = `
        <div class="modal-media" style="position:relative;">
          ${img}
          ${badge}
        </div>
        <div class="modal-info">
          <p class="eyebrow">${p.category?.name || 'Product'}</p>
          <h2>${p.name}</h2>
          <p class="desc">${p.description}</p>
          <div class="price" style="font-size:1.5rem;color:var(--accent);font-weight:700;margin-bottom:20px;">
            $${Number(p.price).toFixed(2)}
            ${p.original_price ? `<span style="text-decoration:line-through;color:var(--muted-dark);font-size:1rem;margin-left:10px;">$${Number(p.original_price).toFixed(2)}</span>` : ''}
          </div>
          <div class="actions">
            <button class="btn-primary" data-add-cart="${p.id}">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>
              Add to Cart
            </button>
            <a href="/products/${p.slug}/" class="btn-secondary">View Details</a>
          </div>
        </div>
      `;
    })
    .catch(() => {
      qvContent.innerHTML = `<div style="padding:40px;text-align:center;color:var(--muted);">Failed to load product.</div>`;
    });
}

function closeQuickView() {
  if (!qvOverlay) return;
  qvOverlay.classList.remove('open');
  setTimeout(() => {
    qvOverlay.style.display = 'none';
    document.body.style.overflow = '';
    if (qvContent) qvContent.innerHTML = '';
  }, 300);
}

if (qvClose) qvClose.addEventListener('click', closeQuickView);
if (qvOverlay) qvOverlay.addEventListener('click', (e) => { if (e.target === qvOverlay) closeQuickView(); });

document.addEventListener('click', (e) => {
  const trigger = e.target.closest('.quick-view-trigger');
  if (!trigger) return;
  const card = trigger.closest('[data-quick-view]');
  if (!card) return;
  // Don't open if clicking wishlist or cart button inside the card
  if (e.target.closest('[data-wishlist-id]') || e.target.closest('[data-add-cart]')) return;
  e.preventDefault();
  openQuickView(card.dataset.quickView);
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeQuickView();
    closeCartPanel();
  }
});

/* ============================
   STOCK ALERT
   ============================ */

const stockAlertForm = document.getElementById('stockAlertForm');
if (stockAlertForm) {
  stockAlertForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const btn = form.querySelector('button[type="submit"]');
    const msg = document.getElementById('stockAlertMsg');
    const data = Object.fromEntries(new FormData(form).entries());
    btn.disabled = true;
    try {
      const res = await fetch('/api/v1/stock-alert/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') || '' },
        body: JSON.stringify(data)
      });
      const result = await res.json();
      if (msg) {
        msg.style.display = 'block';
        msg.style.color = res.ok ? 'var(--accent)' : 'var(--danger)';
        msg.textContent = result.detail || 'Submitted.';
      }
      if (res.ok) form.reset();
    } catch (err) {
      if (msg) {
        msg.style.display = 'block';
        msg.style.color = 'var(--danger)';
        msg.textContent = 'Something went wrong. Please try again.';
      }
    } finally {
      btn.disabled = false;
    }
  });
}

/* ============================
   CATEGORY BAR SCROLL FADE
   ============================ */

(function initCategoryScroll() {
  const bar = document.querySelector('.category-bar');
  const wrap = document.querySelector('.category-bar-wrap');
  if (!bar || !wrap) return;

  function updateFade() {
    const scrollLeft = bar.scrollLeft;
    const maxScroll = bar.scrollWidth - bar.clientWidth;
    wrap.style.setProperty('--show-left', scrollLeft > 5 ? '1' : '0');
    wrap.style.setProperty('--show-right', scrollLeft < maxScroll - 5 ? '1' : '0');
  }

  // CSS will read these custom properties for opacity of pseudo-elements
  // We inject a small style block to handle dynamic opacity
  const style = document.createElement('style');
  style.textContent = `
    .category-bar-wrap::before { opacity: var(--show-left, 0); }
    .category-bar-wrap::after { opacity: var(--show-right, 0); }
  `;
  document.head.appendChild(style);

  bar.addEventListener('scroll', updateFade, { passive: true });
  window.addEventListener('resize', updateFade);
  updateFade();
})();

/* ============================
   FILTER SIDEBAR TOGGLE (mobile)
   ============================ */

const filterToggle = document.getElementById('filterToggle');
const filterSidebar = document.getElementById('filterSidebar');
if (filterToggle && filterSidebar) {
  filterToggle.addEventListener('click', () => {
    filterSidebar.classList.toggle('open');
  });
}

/* ============================
   AUTH FLAG & WISHLIST BOOT
   ============================ */

(function() {
  const userMeta = document.querySelector('meta[name="user-authenticated"]');
  document.body.dataset.authenticated = userMeta ? userMeta.content : 'false';
  loadWishlist();
})();
