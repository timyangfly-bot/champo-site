const category = "seat-hanging-bag";

const perPage = 9;
let currentPage = 1;

const grid = document.getElementById("productGrid");
const pagination = document.getElementById("pagination");

const productDescriptions = {

"hb-01":"Seat back organizer with tablet holder and cup pockets, ideal for family travel and backseat storage.",
"hb-02":"Foldable tray style seat hanging organizer with tissue pocket and multiple storage compartments.",
"hb-03":"Multi-pocket car seat organizer with bottle holders and mesh storage for everyday vehicle essentials."

};

fetch("/products.json")
.then(res=>res.json())
.then(data=>{

const products=data[category]||[];

renderProducts(products);
renderPagination(products);

});

function renderProducts(products){

grid.innerHTML="";

const start=(currentPage-1)*perPage;
const end=start+perPage;

products.slice(start,end).forEach(item=>{

let code,desc;

if(typeof item==="string"){

code=item;
desc=productDescriptions[code]||defaultDesc();

}else{

code=item.code;
desc=item.desc||productDescriptions[code]||defaultDesc();

}

const path=`/images/products/${category}/${code}`;

const card=document.createElement("div");
card.className="product-card";

card.innerHTML=`

<div class="product-image">

<div class="zoom-container">

<img src="${path}/main.jpg"
class="main-img"
loading="lazy">

</div>

<div class="thumbs">

<img src="${path}/main_thumb.webp">

<img src="${path}/variant1_thumb.webp"
onerror="this.style.display='none'">

<img src="${path}/variant2_thumb.webp"
onerror="this.style.display='none'">

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

initThumbHover();
initZoom();
initImageLightbox();

}

function renderPagination(products){

pagination.innerHTML="";

const pages=Math.ceil(products.length/perPage);

for(let i=1;i<=pages;i++){

const btn=document.createElement("button");

btn.innerText=i;

if(i===currentPage)btn.classList.add("active");

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

/* hover 缩略图切换 */

function initThumbHover(){

document.querySelectorAll(".product-card").forEach(card=>{

const main=card.querySelector(".main-img");
const thumbs=card.querySelectorAll(".thumbs img");

thumbs.forEach(img=>{

img.addEventListener("mouseover",function(){

let full=this.src.replace("_thumb.webp",".jpg");

main.src=full;

thumbs.forEach(t=>t.classList.remove("active"));
this.classList.add("active");

});

});

});

}

/* 主图hover放大 */

function initZoom(){

document.querySelectorAll(".zoom-container").forEach(container=>{

const img=container.querySelector(".main-img");

container.addEventListener("mousemove",(e)=>{

const rect=container.getBoundingClientRect();

const x=(e.clientX-rect.left)/rect.width*100;
const y=(e.clientY-rect.top)/rect.height*100;

img.style.transformOrigin=`${x}% ${y}%`;
img.style.transform="scale(1.8)";

});

container.addEventListener("mouseleave",()=>{

img.style.transform="scale(1)";

});

});

}

/* 点击主图放大 */

function initImageLightbox(){

document.querySelectorAll(".main-img").forEach(img=>{

img.addEventListener("click",()=>{

openLightbox(img.src);

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

function formatName(code){

if(!code)return"";

return code
.replace(/-/g," ")
.replace(/\b\w/g,l=>l.toUpperCase());

}

function defaultDesc(){

return"Durable car seat hanging organizer designed for storage and seat back protection.";

}
