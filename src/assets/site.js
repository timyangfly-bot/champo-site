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
