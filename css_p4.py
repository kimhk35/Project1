CSS4 = """
@media (max-width:1024px){
  .overview-grid,.flow-grid{grid-template-columns:1fr;gap:40px}
  .overview-visual{order:-1}
  .venn-diagram{width:280px;height:280px}
  .refs-grid{grid-template-columns:1fr;gap:28px}
}
@media (max-width:768px){
  .container{padding:0 16px}
  .section{padding:64px 0}
  .main-nav{position:fixed;top:72px;left:0;right:0;
    background:rgba(250,247,242,.97);
    backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);
    border-bottom:1px solid rgba(27,42,74,.08);
    padding:16px 24px;flex-direction:column;align-items:flex-start;
    gap:4px;transform:translateY(-120%);opacity:0;
    transition:transform .3s ease,opacity .3s ease;z-index:999}
  .main-nav.open{transform:translateY(0);opacity:1}
  .nav-list{flex-direction:column;width:100%;gap:2px}
  .nav-link{padding:10px 16px;font-size:.95rem;
    border-radius:var(--radius-sm);width:100%}
  .menu-toggle{display:flex}
  .menu-toggle.open span:nth-child(1){transform:rotate(45deg) translate(5px,5px)}
  .menu-toggle.open span:nth-child(2){opacity:0}
  .menu-toggle.open span:nth-child(3){transform:rotate(-45deg) translate(5px,-5px)}
  .hero-stats{flex-wrap:wrap;justify-content:center;gap:14px;padding:16px 20px}
  .stat-divider{display:none}
  .hero-actions{flex-direction:column;align-items:flex-start}
  .overview-cards-mini{grid-template-columns:1fr}
  .venn-diagram{width:260px;height:260px}
  .domain-tabs{gap:6px}
  .domain-tab{padding:8px 14px;font-size:.82rem}
  .domain-panel{padding:20px}
}
@media (max-width:480px){
  .hero-title{font-size:2.4rem}
  .hero-subtitle{font-size:.92rem}
  .btn{padding:12px 22px;font-size:.88rem;width:100%;justify-content:center}
  .hero-actions{flex-direction:column}
  .venn-diagram{width:220px;height:220px}
  .venn-circle{width:140px;height:140px}
  .venn-center{width:90px;height:90px}
  .venn-center-text{font-size:.65rem}
}

.reveal{opacity:0;transform:translateY(24px);
  transition:opacity .6s ease,transform .6s ease}
.reveal.visible{opacity:1;transform:translateY(0)}
"""
with open("c:/upstage/style.css","a",encoding="utf-8") as f:
    f.write(CSS4)
print("style.css part4 완료")
