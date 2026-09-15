const button=document.querySelector('.menu-button');
const nav=document.querySelector('#site-nav');
button?.addEventListener('click',()=>{const open=button.getAttribute('aria-expanded')==='true';button.setAttribute('aria-expanded',String(!open));nav.classList.toggle('open',!open)});
document.querySelectorAll('#site-nav a').forEach(a=>a.addEventListener('click',()=>{button?.setAttribute('aria-expanded','false');nav?.classList.remove('open')}));

const slides=[...document.querySelectorAll('.hero-slide')];
const dots=[...document.querySelectorAll('.slider-dots button')];
let slideIndex=0;
let slideTimer;
const showSlide=index=>{
  if(!slides.length)return;
  slideIndex=(index+slides.length)%slides.length;
  slides.forEach((slide,i)=>slide.classList.toggle('active',i===slideIndex));
  dots.forEach((dot,i)=>dot.classList.toggle('active',i===slideIndex));
};
const restartSlider=()=>{
  clearInterval(slideTimer);
  slideTimer=setInterval(()=>showSlide(slideIndex+1),6000);
};
dots.forEach((dot,i)=>dot.addEventListener('click',()=>{showSlide(i);restartSlider()}));
document.querySelector('.slider-prev')?.addEventListener('click',()=>{showSlide(slideIndex-1);restartSlider()});
document.querySelector('.slider-next')?.addEventListener('click',()=>{showSlide(slideIndex+1);restartSlider()});
if(slides.length>1)restartSlider();

const filterSearch=document.querySelector('[data-filter-search]');
const filterType=document.querySelector('[data-filter-type]');
const filterMaterial=document.querySelector('[data-filter-material]');
const filterSort=document.querySelector('[data-filter-sort]');
const filterReset=document.querySelector('[data-filter-reset]');
const filterCount=document.querySelector('[data-filter-count]');
const filterEmpty=document.querySelector('[data-filter-empty]');
const productCards=[...document.querySelectorAll('.product-card[data-name]')];
const productGrid=document.querySelector('[data-product-grid]');
const applyProductFilters=()=>{
  const query=(filterSearch?.value||'').trim().toLowerCase();
  const type=filterType?.value||'';
  const material=filterMaterial?.value||'';
  let visible=0;
  productCards.forEach(card=>{
    const match=(!query||card.dataset.name.includes(query))&&(!type||card.dataset.type===type)&&(!material||card.dataset.material===material);
    card.hidden=!match;
    if(match)visible+=1;
  });
  const sorted=[...productCards];
  if(filterSort?.value==='name')sorted.sort((a,b)=>a.dataset.name.localeCompare(b.dataset.name));
  if(filterSort?.value==='sku')sorted.sort((a,b)=>a.dataset.sku.localeCompare(b.dataset.sku,undefined,{numeric:true}));
  if(filterSort?.value==='default')sorted.sort((a,b)=>productCards.indexOf(a)-productCards.indexOf(b));
  sorted.forEach(card=>productGrid?.insertBefore(card,filterEmpty));
  if(filterCount)filterCount.textContent=String(visible);
  if(filterEmpty)filterEmpty.hidden=visible!==0;
};
[filterSearch,filterType,filterMaterial,filterSort].forEach(control=>control?.addEventListener('input',applyProductFilters));
filterReset?.addEventListener('click',()=>{
  if(filterSearch)filterSearch.value='';
  if(filterType)filterType.value='';
  if(filterMaterial)filterMaterial.value='';
  if(filterSort)filterSort.value='default';
  applyProductFilters();
  filterSearch?.focus();
});

document.querySelector('[data-print-spec]')?.addEventListener('click',()=>window.print());

document.querySelectorAll('[data-rfq-form]').forEach(form=>form.addEventListener('submit',()=>{
  if(form.checkValidity())sessionStorage.setItem('champo_rfq_pending','1');
}));

const wechatToggle=document.querySelector('[data-wechat-toggle]');
const wechatCard=document.querySelector('[data-wechat-card]');
const closeWechat=()=>{if(!wechatCard||!wechatToggle)return;wechatCard.hidden=true;wechatToggle.setAttribute('aria-expanded','false')};
wechatToggle?.addEventListener('click',()=>{const willOpen=wechatCard.hidden;wechatCard.hidden=!willOpen;wechatToggle.setAttribute('aria-expanded',String(willOpen));if(willOpen)window.dataLayer?.push({event:'contact_click',contact_method:'wechat'})});
document.querySelector('[data-wechat-close]')?.addEventListener('click',closeWechat);
document.addEventListener('keydown',event=>{if(event.key==='Escape')closeWechat()});
document.querySelector('[data-wechat-copy]')?.addEventListener('click',async event=>{const button=event.currentTarget;try{await navigator.clipboard.writeText(button.dataset.wechatValue);button.textContent='Copied';setTimeout(()=>button.textContent='Copy number',1800)}catch{button.textContent='Select & copy the number above'}});
document.querySelector('[data-contact-channel="whatsapp"]')?.addEventListener('click',()=>window.dataLayer?.push({event:'contact_click',contact_method:'whatsapp'}));
