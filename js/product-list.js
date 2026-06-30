/* 自动识别分类 */

const pathParts = window.location.pathname.split("/");
const category = pathParts[pathParts.length-2];

const perPage = 9;
let currentPage = 1;

const grid = document.getElementById("productGrid");
const pagination = document.getElementById("pagination");

fetch("/products.json")
.then(res => res.json())
.then(data => {

const products = data[category];

if(!products) return;

renderProducts(products);
renderPagination(products);

});



function renderProducts(products){

grid.innerHTML = "";

const start = (currentPage-1)*perPage;
const end = start + perPage;

products.slice(start,end).forEach(product=>{

const code = product.code;
const desc = product.desc;

const imgPath = `/images/products/${category}/${code}`;

const card = document.createElement("div");
card.className = "product-card";

card.innerHTML = `

<div class="product-image">

<picture>
<source srcset="${imgPath}/main.webp" type="image/webp">
<img src="${imgPath}/main.jpg" class="main-img" loading="lazy">
</picture>

<div class="thumbs">

<img src="${imgPath}/main_thumb.webp"
data-full="${imgPath}/main.jpg">

<img src="${imgPath}/variant1_thumb.webp"
data-full="${imgPath}/variant1.jpg"
onerror="this.style.display='none'">

<img src="${imgPath}/variant2_thumb.webp"
data-full="${imgPath}/variant2.jpg"
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



/* 小图切换 */

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



/* 图片放大 */

function initImageZoom(){

document.querySelectorAll(".thumbs img").forEach(img=>{

img.addEventListener("dblclick",()=>{

openLightbox(img.dataset.full);

});

});

}



function openLightbox(src){

let lightbox=document.createElement("div");
lightbox.className="image-lightbox";

lightbox.innerHTML=`
<div class="lightbox-content">
<img src="${src}">
</div>
`;

lightbox.onclick=()=>lightbox.remove();

document.body.appendChild(lightbox);

}



/* 产品名称格式化 */

function formatName(code){

return code
.replace(/-/g," ")
.replace(/\b\w/g,l=>l.toUpperCase());

}
