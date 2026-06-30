const category = "seat-hanging-bag";

const perPage = 9;
let currentPage = 1;

const grid = document.getElementById("productGrid");
const pagination = document.getElementById("pagination");

/* 每个产品独立描述 */
const productDescriptions = {
"hb-01": "Seat back organizer with tablet holder and cup pockets, ideal for family travel and backseat storage.",
"hb-02": "Foldable tray style seat hanging organizer with tissue pocket and multiple storage compartments.",
"hb-03": "Multi-pocket car seat organizer with bottle holders and mesh storage for everyday vehicle essentials."
};

fetch("/products.json")
.then(res => res.json())
.then(data => {

const products = data[category];

renderProducts(products);
renderPagination(products);

});


function renderProducts(products){

grid.innerHTML = "";

const start = (currentPage-1)*perPage;
const end = start + perPage;

products.slice(start,end).forEach(code=>{

const path = `/images/products/${category}/${code}`;
const desc = productDescriptions[code] || "Durable car seat hanging organizer designed for storage and seat back protection.";

const card = document.createElement("div");
card.className = "product-card";

card.innerHTML = `

<div class="product-image">

<picture>
<source srcset="${path}/main.webp" type="image/webp">
<img src="${path}/main.jpg" class="main-img" loading="lazy">
</picture>

<div class="thumbs">

<img src="${path}/main_thumb.webp" data-full="${path}/main.jpg">

<img src="${path}/variant1_thumb.webp"
data-full="${path}/variant1.jpg"
onerror="this.style.display='none'">

<img src="${path}/variant2_thumb.webp"
data-full="${path}/variant2.jpg"
onerror="this.style.display='none'">

</div>

</div>

<div class="product-info">

<h3 class="product-title">${formatName(code)}</h3>

<p class="product-desc">
${desc}
</p>

<a href="/products/${category}/${code}.html" class="product-btn">
View Details
</a>

</div>

`;

grid.appendChild(card);

});

initThumbSwitch();
initImageZoom();

}


function renderPagination(products){

pagination.innerHTML="";

const pages = Math.ceil(products.length/perPage);

for(let i=1;i<=pages;i++){

const btn=document.createElement("button");

btn.innerText=i;

if(i===currentPage) btn.classList.add("active");

btn.onclick=()=>{

currentPage=i;

renderProducts(products);
renderPagination(products);

window.scrollTo({
top:0,
behavior:"smooth"
});

};

pagination.appendChild(btn);

}

}


/* 小图切换主图 */

function initThumbSwitch(){

document.querySelectorAll(".product-card").forEach(card=>{

const main=card.querySelector(".main-img");
const thumbs=card.querySelectorAll(".thumbs img");

thumbs.forEach(img=>{

img.onclick=()=>{

main.src=img.dataset.full;

};

});

});

}


/* 图片放大预览 */

function initImageZoom(){

document.querySelectorAll(".thumbs img").forEach(img=>{

img.addEventListener("dblclick",()=>{

openLightbox(img.dataset.full);

});

});

}


function openLightbox(src){

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


function formatName(code){

return code
.replace(/-/g," ")
.replace(/\b\w/g,l=>l.toUpperCase());

}
