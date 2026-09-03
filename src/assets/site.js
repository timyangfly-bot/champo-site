const button=document.querySelector('.menu-button');
const nav=document.querySelector('#site-nav');
button?.addEventListener('click',()=>{const open=button.getAttribute('aria-expanded')==='true';button.setAttribute('aria-expanded',String(!open));nav.classList.toggle('open',!open)});
document.querySelectorAll('#site-nav a').forEach(a=>a.addEventListener('click',()=>{button?.setAttribute('aria-expanded','false');nav?.classList.remove('open')}));
