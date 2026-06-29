const category = "seat-hanging-bag";

const perPage = 9;
let currentPage = 1;

const grid = document.getElementById("productGrid");
const pagination = document.getElementById("pagination");

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

const card = document.createElement("div");
card.className = "product-card";

card.innerHTML = `

<picture>
<source srcset="${path}/main.webp" type="image/webp">
<img src="${path}/main.jpg" class="main-img" loading="lazy">
</picture>

<div class="thumbs">

<img src="${path}/main_thumb.webp">

<img src="${path}/variant1_thumb.webp"
onerror="this.style.display='none'">

<img src="${path}/variant2_thumb.webp"
onerror="this.style.display='none'">

</div>

<h4>${code}</h4>

`;

grid.appendChild(card);

});

initThumbSwitch();

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

};

pagination.appendChild(btn);

}

}

function initThumbSwitch(){

document.querySelectorAll(".product-card").forEach(card=>{

const main=card.querySelector(".main-img");
const thumbs=card.querySelectorAll(".thumbs img");

thumbs.forEach(img=>{

img.onclick=()=>{

main.src=img.src.replace("_thumb","");

};

});

});

}
