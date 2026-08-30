let activeDomain=0;

// ── 도메인 탭 ──
function renderTabs(){
  const tabs=document.getElementById('domainTabs');
  DOMAINS.forEach((d,i)=>{
    const btn=document.createElement('button');
    btn.className='domain-tab'+(i===activeDomain?' active':'');
    btn.setAttribute('role','tab');
    btn.setAttribute('aria-selected',i===activeDomain?'true':'false');
    btn.setAttribute('aria-controls','domainPanel');
    btn.innerHTML=`<span class="tab-icon">${d[1]}</span>${d[2]}`;
    btn.addEventListener('click',()=>selectDomain(i));
    tabs.appendChild(btn);
  });
}

// ── 도메인 패널 ──
function renderPanel(i,animate=true){
  const panel=document.getElementById('domainPanel');
  const d=DOMAINS[i]; if(!d) return;
  if(animate) panel.classList.add('loading');
  panel.innerHTML=
    `<div class="domain-panel-header">
      <div class="domain-panel-icon">${d[1]}</div>
      <div class="domain-panel-title-group">
        <div class="domain-panel-number">${d[0]}</div>
        <div class="domain-panel-title">${d[2]}</div>
        <div class="domain-panel-desc">${d[3]}</div>
      </div></div>
      <div class="domain-subsections">
        ${d[4].map(s=>`<div class="domain-subsec">
          <div class="domain-subsec-head">
            <span class="domain-subsec-icon">${s[1]}</span>
            <span class="domain-subsec-name">${s[0]}</span>
          </div>
          <div class="domain-subsec-body">
            <div class="domain-subsec-item">
              <div class="domain-subsec-item-label">주요 연구 질문</div>
              <div class="domain-subsec-item-value">${s[2]}</div>
            </div>
            <div class="domain-subsec-item">
              <div class="domain-subsec-item-label">대표 방법론</div>
              <div class="domain-subsec-item-value">${s[3]}</div>
            </div>
          </div></div>`).join('')}
      </div>`+(animate?'':'');
  if(animate) requestAnimationFrame(()=>panel.classList.remove('loading'));
}

function selectDomain(i){
  if(i===activeDomain) return;
  activeDomain=i;
  $$('.domain-tab').forEach((tab,idx)=>{
    const isActive=idx===i;
    tab.classList.toggle('active',isActive);
    tab.setAttribute('aria-selected',isActive?'true':'false');
  });
  renderPanel(i);
}

// ── 연구 흐름 SVG ──
function renderFlowVisual(){
  const c=document.getElementById('flowVisual');
  const N=[
    ['태동기','1900-1950',30,250],
    ['구조주의','1960-1970',120,190],
    ['구성주의','1980-1990',220,130],
    ['사회문화','2000-2010',320,80],
    ['융합·실천','2010-현',380,30]
  ];
  const L=[[0,1],[1,2],[2,3],[3,4]];
  let S=`<svg viewBox="0 0 420 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="수학교육 연구 흐름 다이어그램"><defs><linearGradient id="g1" x1="0" y1="1" x2="1" y2="0"><stop offset="0%" stop-color="#D4A853"/><stop offset="50%" stop-color="#E07A5F"/><stop offset="100%" stop-color="#1B2A4A"/></linearGradient><filter id="f1"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#1B2A4A" flood-opacity="0.2"/></filter></defs><rect width="420" height="300" fill="#FAF7F2" rx="12"/>`;
  L.forEach(([a,b])=>{const x=N[a],y=N[b];
    const cx1=x[2]+(y[2]-x[2])*0.5,cy1=x[3],cx2=y[2]-(y[2]-x[2])*0.5,cy2=y[3];
    S+=`<path d="M${x[2]},${x[3]} C${cx1},${cy1} ${cx2},${cy2} ${y[2]},${y[3]}" fill="none" stroke="url(#g1)" stroke-width="2.5" stroke-linecap="round" opacity="0.6"/>`;});
  N.forEach((n,i)=>{
    const r=24+(i===4?8:0);
    const fill=i===4?'#1B2A4A':(i===0?'#D4A853':'#fff');
    const stroke=i===4?'#D4A853':'#1B2A4A';
    const tf=i===4?'#fff':'#1B2A4A';
    S+=`<g filter="url(#f1)"><circle cx="${n[2]}" cy="${n[3]}" r="${r}" fill="${fill}" stroke="${stroke}" stroke-width="2.5"/><text x="${n[2]}" y="${n[3]-5}" text-anchor="middle" font-family="Noto Serif KR,serif" font-size="9" font-weight="700" fill="${tf}">${n[0]}</text><text x="${n[2]}" y="${n[3]+12}" text-anchor="middle" font-family="Noto Sans KR,sans-serif" font-size="7" fill="${tf}" opacity="0.7">${n[1]}</text></g>`});
  [1900,1930,1960,1990,2020].forEach((y,i)=>{
    const x=30+i*85;
    S+=`<line x1="${x}" y1="285" x2="${x}" y2="291" stroke="#D4A853" stroke-width="1.5" opacity="0.5"/><text x="${x}" y="297" text-anchor="middle" font-family="Noto Sans KR,sans-serif" font-size="7.5" fill="#7a7a8a" font-weight="500">${y}</text>`});
  S+='</svg>';
  c.innerHTML=S;
}

// ── 참고문헌 ──
function renderRefs(){
  document.getElementById('refsInternational').innerHTML=
    INT_REFS.map(r=>`<li>${r}</li>`).join('');
  document.getElementById('refsDomestic').innerHTML=
    DOM_REFS.map(r=>`<li>${r}</li>`).join('');
}
