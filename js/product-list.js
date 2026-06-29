const category="seat-hanging-bag"

const products = [
"HB-01","hb-02","HB-03","hb-04","hb-05",
"hb-06","hb-07","hb-08","hb-09","hb-10",
"hb-11","hb-12","hb-13","hb-14","hb-15",
"hb-16","hb-17","hb-18","hb-19",
"hb-21","hb-22","hb-23","hb-24","hb-25",
"hb-26","hb-27","hb-28","hb-29","hb-30",
"sh001","sh002"
];

const perPage=9
let currentPage=1

const grid=document.getElementById("productGrid")
const pagination=document.getElementById("pagination")

function renderProducts(){

grid.innerHTML=""

const start=(currentPage-1)*perPage
const end=start+perPage

products.slice(start,end).forEach(code=>{

const path=/images/products/${category}/${code}

const card=document.createElement("div")
card.className="product-card"

card.innerHTML=`

<picture> <source srcset="${path}/main.webp" type="image/webp"> <img src="${path}/main.jpg" class="main-img" loading="lazy"> </picture> <div class="thumbs"> <img src="${path}/main_thumb.webp">
<img src="${path}/variant1_thumb.webp" onerror="this.style.display='none'">

<img src="${path}/variant2_thumb.webp" onerror="this.style.display='none'">

</div> <h4>${code}</h4>
`

grid.appendChild(card)

})

initThumbSwitch()

}

function renderPagination(){

pagination.innerHTML=""

const pages=Math.ceil(products.length/perPage)

for(let i=1;i<=pages;i++){

const btn=document.createElement("button")

btn.innerText=i

if(i===currentPage) btn.classList.add("active")

btn.onclick=()=>{

currentPage=i
renderProducts()
renderPagination()

}

pagination.appendChild(btn)

}

}

function initThumbSwitch(){

document.querySelectorAll(".product-card").forEach(card=>{

const main=card.querySelector(".main-img")

const thumbs=card.querySelectorAll(".thumbs img")

thumbs.forEach(img=>{

img.onclick=()=>{

main.src=img.src.replace("_thumb","")

}

})

})

}

renderProducts()
renderPagination()
