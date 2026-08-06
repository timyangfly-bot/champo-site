// Get current category from URL
function getCurrentCategory() {
  const path = window.location.pathname;
  const match = path.match(/\/products\/([^\/]+)/);
  return match ? match[1] : "seat-hanging-bag";
}

const category = getCurrentCategory();
const perPage = 9;
let currentPage = 1;

const grid = document.getElementById("productGrid");
const pagination = document.getElementById("pagination");

const productDescriptions = {
  "HB-01": "Seat back organizer with tablet holder and cup pockets, ideal for family travel and backseat storage.",
  "hb-02": "Foldable tray style seat hanging organizer with tissue pocket and multiple storage compartments.",
  "HB-03": "Multi-pocket car seat organizer with bottle holders and mesh storage for everyday vehicle essentials.",

  "ps-01": "Premium waterproof pet seat cover with non-slip backing and side pockets for pet accessories.",
  "ps-02": "Heavy-duty pet seat protector with scratch-resistant surface and adjustable straps.",
  "ps-03": "Breathable mesh pet seat cover with hammock design for full seat protection."
};

// Loading state
if (grid) {
  grid.innerHTML = '<div class="loading">Loading products...</div>';
}

// ✅ 关键：读取 JSON
fetch("/products.json")
  .then(res => {
    if (!res.ok) throw new Error(`Failed to load products: ${res.status}`);
    return res.json();
  })
  .then(data => {
    const products = data[category] || [];

    if (products.length === 0) {
      grid.innerHTML = '<div class="no-products">No products found.</div>';
      return;
    }

    renderProducts(products);
    renderPagination(products);
  })
  .catch(error => {
    console.error("Error:", error);
    grid.innerHTML = '<div class="error">Failed to load products.</div>';
  });

function renderProducts(products) {
  if (!grid) return;

  grid.innerHTML = "";

  const start = (currentPage - 1) * perPage;
  const end = start + perPage;

  products.slice(start, end).forEach(item => {

    // ✅ ✅ 核心修复：支持 folder
    let code, folder, desc;

    if (typeof item === "string") {
      code = item;
      folder = item; // 兼容旧数据
      desc = productDescriptions[code] || defaultDesc();
    } else {
      folder = item.folder;
      code = item.code || item.folder;
      desc = item.desc || productDescriptions[code] || defaultDesc();
    }

   const path = `https://champoauto.com/images/products/${category}/${folder}`;

    const card = document.createElement("div");
    card.className = "product-card";

    card.innerHTML = `
      <div class="product-image">
        <div class="zoom-container">
          <img src="${path}/main.jpg"
               class="main-img"
               loading="lazy"
               alt="${formatName(code)}"
               onerror="this.onerror=null;this.src='${path}/main.webp'">
        </div>
        <div class="thumbs">
          <img src="${path}/main_thumb.webp"
               onerror="this.style.display='none'">
          <img src="${path}/variant1_thumb.webp"
               onerror="this.style.display='none'">
          <img src="${path}/variant2_thumb.webp"
               onerror="this.style.display='none'">
        </div>
      </div>

      <div class="product-info">
        <h3 class="product-title">${formatName(code)}</h3>
        <p class="product-desc">${desc}</p>

        <div class="product-actions">
          <a href="/products/${category}/${code}.html" class="product-btn">
            View Details
          </a>
          <a href="/#inquiry?product=${code}" class="quick-inquiry">
            Quick Inquiry
          </a>
        </div>
      </div>
    `;

    grid.appendChild(card);
  });

  setTimeout(() => {
    initThumbHover();
    initZoom();
    initImageLightbox();
  }, 0);
}

function renderPagination(products) {
  if (!pagination) return;

  pagination.innerHTML = "";
  const pages = Math.ceil(products.length / perPage);

  for (let i = 1; i <= pages; i++) {
    const btn = document.createElement("button");
    btn.innerText = i;

    if (i === currentPage) btn.classList.add("active");

    btn.onclick = () => {
      currentPage = i;
      renderProducts(products);
      renderPagination(products);
      window.scrollTo({ top: 0, behavior: "smooth" });
    };

    pagination.appendChild(btn);
  }
}

// Thumbnail hover
function initThumbHover() {
  document.querySelectorAll(".product-card").forEach(card => {
    const main = card.querySelector(".main-img");
    const thumbs = card.querySelectorAll(".thumbs img");

    thumbs.forEach(img => {
      img.addEventListener("mouseover", function () {
        let full = this.src.replace("_thumb.webp", ".jpg");
        main.src = full;
      });
    });
  });
}

// Zoom
function initZoom() {
  document.querySelectorAll(".zoom-container").forEach(container => {
    const img = container.querySelector(".main-img");

    container.addEventListener("mousemove", (e) => {
      const rect = container.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width * 100;
      const y = (e.clientY - rect.top) / rect.height * 100;

      img.style.transformOrigin = `${x}% ${y}%`;
      img.style.transform = "scale(1.8)";
    });

    container.addEventListener("mouseleave", () => {
      img.style.transform = "scale(1)";
    });
  });
}

// Lightbox
function initImageLightbox() {
  document.querySelectorAll(".main-img").forEach(img => {
    img.addEventListener("click", () => {
      openLightbox(img.src);
    });
  });
}

function openLightbox(src) {
  let lightbox = document.createElement("div");
  lightbox.className = "image-lightbox";
  lightbox.innerHTML = `
    <div class="lightbox-content">
      <img src="${src}">
    </div>
  `;
  lightbox.onclick = () => lightbox.remove();
  document.body.appendChild(lightbox);
}

function formatName(code) {
  if (!code) return "";
  return code.replace(/[-_]/g, " ").toUpperCase();
}

function defaultDesc() {
  const defaultDescriptions = {
    "seat-hanging-bag": "Durable car seat hanging organizer.",
    "pet-seat-cover": "Premium pet seat cover for protection.",
    "storage-box": "Vehicle storage solution.",
    "tool-kit": "Automotive tool kit.",
    "trunk-mat": "Protective trunk mat.",
    "child-seat-protection-pad": "Child seat protector."
  };

  return defaultDescriptions[category] || "High-quality automotive accessory.";
}
