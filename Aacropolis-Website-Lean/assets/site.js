/* Shared navigation, accessible photo viewer, and community map. No dependencies. */
const menuButton=document.querySelector('.menu-toggle');
const nav=document.querySelector('#site-navigation');
menuButton?.addEventListener('click',()=>{const open=menuButton.getAttribute('aria-expanded')!=='true';menuButton.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open)});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){document.querySelectorAll('details[open]').forEach(d=>d.open=false);menuButton?.setAttribute('aria-expanded','false');nav?.classList.remove('open')}});
document.addEventListener('click',e=>{document.querySelectorAll('.more-nav[open]').forEach(d=>{if(!d.contains(e.target))d.open=false})});
const viewer=document.querySelector('#lightbox');
const viewerImage=document.querySelector('#lightbox-image');
let photoTrigger;
document.querySelectorAll('[data-lightbox]').forEach(a=>a.addEventListener('click',e=>{if(!viewer?.showModal)return;e.preventDefault();photoTrigger=a;viewerImage.src=a.href;viewerImage.alt=a.querySelector('img')?.alt||'Aacropolis home';document.querySelector('#lightbox-caption').textContent=viewerImage.alt;viewer.showModal();document.body.classList.add('lightbox-open')}));
function closeViewer(){viewer?.close()}
document.querySelector('#lightbox-close')?.addEventListener('click',closeViewer);
viewer?.addEventListener('click',e=>{if(e.target===viewer)closeViewer()});
viewer?.addEventListener('close',()=>{document.body.classList.remove('lightbox-open');photoTrigger?.focus()});
document.querySelectorAll('.place').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('.place').forEach(b=>{b.classList.remove('active');b.setAttribute('aria-pressed','false')});button.classList.add('active');button.setAttribute('aria-pressed','true');const {lat,lon,title}=button.dataset;const q=encodeURIComponent(`${lat},${lon}`);const map=document.querySelector('#community-map');map.src=`https://maps.google.com/maps?q=${q}&z=12&output=embed`;map.title=`Map of ${title}`;document.querySelector('#map-title').textContent=title;document.querySelector('#map-link').href=`https://www.google.com/maps/search/?api=1&query=${q}`}));
