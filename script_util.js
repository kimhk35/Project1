// ── DOM 헬퍼 ──
const $=s=>document.querySelector(s);
const $$=s=>[...document.querySelectorAll(s)];

// ── 헤더 / 모바일 메뉴 ──
const header=document.getElementById('header');
const menuToggle=document.getElementById('menuToggle');
const mainNav=document.getElementById('mainNav');

window.addEventListener('scroll',()=>{
  header.classList.toggle('scrolled',window.scrollY>20);
},{passive:true});

menuToggle.addEventListener('click',()=>{
  const o=!mainNav.classList.toggle('open');
  menuToggle.classList.toggle('open',o);
  menuToggle.setAttribute('aria-expanded',o);
});

$$('.nav-link').forEach(l=>l.addEventListener('click',()=>{
  mainNav.classList.remove('open');
  menuToggle.classList.remove('open');
  menuToggle.setAttribute('aria-expanded','false');
}));

// ── Hero 카운트 ──
function animateCounters(){
  $$('.stat-number').forEach(el=>{
    const t=parseInt(el.dataset.count,10),d=1800,s=performance.now();
    (function f(n){const p=Math.min((n-s)/d,1),e=1-Math.pow(1-p,3);
      el.textContent=Math.round(t*e);p<1&&requestAnimationFrame(f);})(s);
  });
}
const ho=new IntersectionObserver(es=>{
  es.forEach(e=>{if(e.isIntersecting){animateCounters();ho.disconnect();}});
},{threshold:0.4});
ho.observe(document.querySelector('.hero'));

// ── 프레임워크 타임라인 ──
function renderTimeline(){
  const c=document.getElementById('frameworkTimeline');
  const track=document.createElement('div');
  track.className='timeline-track';
  FRAMEWORK.forEach(item=>{
    const el=document.createElement('div');
    el.className='timeline-item';
    el.setAttribute('role','button');
    el.setAttribute('tabindex','0');
    el.innerHTML=`<span class="timeline-order">${item.order}</span>
      <h3>${item.title}</h3><p>${item.desc}</p>
      <div class="tli-tags">${item.tags.map(t=>`<span class="tli-tag">${t}</span>`).join('')}</div>`;
    el.addEventListener('click',()=>el.classList.toggle('active'));
    track.appendChild(el);
  });
  c.appendChild(track);
}

// ── 스크롤 리빌 ──
function observeReveals(){
  const els=$$('.timeline-item,.era-card,.mini-card,.refs-list li');
  els.forEach(el=>el.classList.add('reveal'));
  const ob=new IntersectionObserver(es=>{
    es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');ob.unobserve(e.target);}});
  },{threshold:0.15});
  els.forEach(el=>ob.observe(el));
}

// ── 초기화 ──
document.addEventListener('DOMContentLoaded',()=>{
  renderTimeline();
  renderTabs();
  renderPanel(activeDomain,false);
  renderRefs();
  observeReveals();
});
