// 从URL获取当前分类
function getCurrentCategory() {
  const path = window.location.pathname;
  // 匹配 /products/seat-hanging-bag/ 这样的路径
  const match = path.match(/\/products\/([^\/]+)/);
  return match ? match[1] : "seat-hanging-bag";
}

const category = getCurrentCategory();
const perPage = 9;
let currentPage = 1;

const grid = document.getElementById("productGrid");
const pagination = document.getElementById("pagination");

const productDescriptions = {
  // Seat Hanging Bags
  "hb-01": "Seat back organizer with tablet holder and cup pockets, ideal for family travel and backseat storage.",
  "hb-02": "Foldable tray style seat hanging organizer with tissue pocket and multiple storage compartments.",
  "hb-03": "Multi-pocket car seat organizer with bottle holders and mesh storage for everyday vehicle essentials.",
  
  // Pet Seat Covers
  "ps-01": "Premium waterproof pet seat cover with non-slip backing and side pockets for pet accessories.",
  "ps-02": "Heavy-duty pet seat protector with scratch-resistant surface and adjustable straps.",
  "ps-03": "Breathable mesh pet seat cover with hammock design for full seat protection.",
  
  // Storage Boxes
  "sb-01": "Collapsible trunk organizer with multiple compartments and waterproof lining.",
  "sb-02": "Heavy-duty storage box with reinforced handles and durable construction.",
  "sb-03": "Multi-functional car storage organizer with removable dividers and tool compartments.",
  
  // Tool Kits
  "tk-01": "Basic car emergency tool kit with essential tools and roadside assistance items.",
  "tk-02": "Professional automotive tool set with comprehensive tools for common repairs.",
  "tk-03": "Premium emergency roadside kit with advanced tools and safety equipment.",
  
  // Trunk Mats
  "tm-01": "Custom-fit all-weather trunk mat with deep ridges to contain spills and dirt.",
  "tm-02": "Premium carpet trunk liner with non-slip backing and precise vehicle fit.",
  "tm-03": "Heavy-duty rubber trunk mat with raised edges for maximum protection.",
  
  // Child Seat Protection Pads
  "cp-01": "Standard child seat protector with thick padding and non-slip surface.",
  "cp-02": "Premium seat protection pad with waterproof layer and storage pocket.",
  "cp-03": "Extra large child seat protector for SUVs and larger vehicle seats."
};

// 添加加载状态
grid.innerHTML = '<div class="loading">Loading products...</div>';

fetch("/products.json")
  .then(res => {
    if (!res.ok) {
      throw new Error(`Failed to load products: ${res.status}`);
    }
    return res.json();
  })
  .then(data => {
    const products = data[category] || [];
    
    if (products.length === 0) {
      grid.innerHTML = '<div class="no-products">No products found in this category.</div>';
      return;
    }
    
    renderProducts(products);
    renderPagination(products);
  })
  .catch(error => {
    console.error("Error:", error);
    grid.innerHTML = '<div class="error">Failed to load products. Please try again later.</div>';
  });

function renderProducts(products) {
  grid.innerHTML = "";

  const start = (currentPage - 1) * perPage;
  const end = start + perPage;

  products.slice(start, end).forEach(item => {
    let code, desc;

    if (typeof item === "string") {
      code = item;
      desc = productDescriptions[code] || defaultDesc();
    } else {
      code = item.code;
      desc = item.desc || productDescriptions[code] || defaultDesc();
    }

    const path = `/images/products/${category}/${code}`;

    const card = document.createElement("div");
    card.className = "product-card";

    card.innerHTML = `
      <div class="product-image">
        <div class="zoom-container">
          <img src="${path}/main.jpg"
               class="main-img"
               loading="lazy"
               alt="${formatName(code)}"
               onerror="this.src='/images/placeholder.jpg'">
        </div>
        <div class="thumbs">
          <img src="${path}/main_thumb.webp" 
               alt="Thumbnail 1"
               onerror="this.style.display='none'">
          <img src="${path}/variant1_thumb.webp"
               onerror="this.style.display='none'"
               alt="Thumbnail 2">
          <img src="${path}/variant2_thumb.webp"
               onerror="this.style.display='none'"
               alt="Thumbnail 3">
        </div>
      </div>
      <div class="product-info">
        <h3 class="product-title">
          ${formatName(code)}
        </h3>
        <p class="product-desc">
          ${desc}
        </p>
        <div class="product-actions">
          <a href="/products/${category}/${code}.html"
             class="product-btn">
            View Details
          </a>
          <a href="/#inquiry?product=${code}"
             class="quick-inquiry">
            Quick Inquiry
          </a>
        </div>
      </div>
    `;

    grid.appendChild(card);
  });

  // 使用 setTimeout 确保DOM更新后再初始化事件
  setTimeout(() => {
    initThumbHover();
    initZoom();
    initImageLightbox();
  }, 0);
}

function renderPagination(products) {
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
      window.scrollTo({
        top: 0,
        behavior: "smooth"
      });
    };

    pagination.appendChild(btn);
  }
}

/* hover 缩略图切换 */
function initThumbHover() {
  document.querySelectorAll(".product-card").forEach(card => {
    const main = card.querySelector(".main-img");
    const thumbs = card.querySelectorAll(".thumbs img");

    thumbs.forEach(img => {
      img.addEventListener("mouseover", function() {
        // 修复路径转换：将 _thumb.webp 替换为 .jpg
        let full = this.src.replace("_thumb.webp", ".jpg");
        main.src = full;

        thumbs.forEach(t => t.classList.remove("active"));
        this.classList.add("active");
      });
    });
  });
}

/* 主图hover放大 */
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

/* 点击主图放大 */
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
      <img src="${src}" alt="Enlarged view">
    </div>
  `;
  lightbox.onclick = () => lightbox.remove();
  document.body.appendChild(lightbox);
}

function formatName(code) {
  if (!code) return "";
  return code
    .replace(/-/g, " ")
    .replace(/\b\w/g, l => l.toUpperCase());
}

function defaultDesc() {
  const defaultDescriptions = {
    "seat-hanging-bag": "Durable car seat hanging organizer designed for storage and seat back protection.",
    "pet-seat-cover": "Premium pet seat cover designed to protect your car seats from pet hair and scratches.",
    "storage-box": "Organized storage solution for your vehicle trunk with durable construction.",
    "tool-kit": "Comprehensive automotive tool kit for emergency repairs and maintenance.",
    "trunk-mat": "Protective trunk mat designed to keep your vehicle clean and damage-free.",
    "child-seat-protection-pad": "Child seat protection pad to prevent indentations and wear on car seats."
  };
  
  return defaultDescriptions[category] || "High-quality automotive accessory designed for durability and functionality.";
}