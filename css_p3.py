CSS3 = """
.domains-header{max-width:600px;margin-bottom:36px}
.domains-header p{color:var(--text-secondary);font-size:.95rem}
.domain-tabs{display:flex;gap:8px;margin-bottom:28px;overflow-x:auto;
  padding-bottom:4px;scrollbar-width:thin;flex-wrap:nowrap}
.domain-tab{flex:0 0 auto;padding:10px 20px;border-radius:100px;
  border:1.5px solid rgba(27,42,74,.12);background:var(--white);
  font-size:.88rem;font-weight:600;color:var(--text-secondary);
  cursor:pointer;transition:all var(--transition);
  display:flex;align-items:center;gap:8px;white-space:nowrap}
.domain-tab:hover{border-color:var(--navy-600);color:var(--navy-800)}
.domain-tab.active{background:var(--navy-800);border-color:var(--navy-800);color:var(--white)}
.domain-tab .tab-icon{font-size:1.1rem}
.domain-panel{min-height:300px;background:var(--white);
  border:1px solid rgba(27,42,74,.08);border-radius:var(--radius-lg);
  padding:36px;box-shadow:var(--shadow-sm);transition:opacity var(--transition)}
.domain-panel.loading{opacity:0}
.domain-panel-header{display:flex;align-items:flex-start;gap:20px;
  margin-bottom:28px;padding-bottom:24px;
  border-bottom:1px solid rgba(27,42,74,.08)}
.domain-panel-icon{font-size:2.4rem;flex-shrink:0;line-height:1}
.domain-panel-title-group{flex:1}
.domain-panel-number{font-size:.72rem;font-weight:700;color:var(--gold-500);
  letter-spacing:.08em;text-transform:uppercase;margin-bottom:4px}
.domain-panel-title{font-size:1.4rem;font-family:var(--font-serif);
  color:var(--navy-800);margin-bottom:6px}
.domain-panel-desc{color:var(--text-secondary);font-size:.92rem;line-height:1.65}
.domain-subsections{display:flex;flex-direction:column;gap:12px}
.domain-subsec{padding:16px 20px;background:var(--cream);
  border-left:3px solid var(--gold-500);
  border-radius:0 var(--radius-sm) var(--radius-sm) 0;
  transition:background var(--transition)}
.domain-subsec:hover{background:var(--cream-2)}
.domain-subsec-head{display:flex;align-items:center;gap:10px;margin-bottom:6px}
.domain-subsec-name{font-weight:700;font-size:.95rem;color:var(--navy-800)}
.domain-subsec-icon{font-size:1rem;flex-shrink:0}
.domain-subsec-body{display:flex;gap:20px;flex-wrap:wrap}
.domain-subsec-item{flex:1;min-width:160px}
.domain-subsec-item-label{font-size:.7rem;font-weight:600;color:var(--text-muted);
  letter-spacing:.05em;text-transform:uppercase;margin-bottom:4px}
.domain-subsec-item-value{font-size:.85rem;color:var(--text-secondary);line-height:1.5}

.flow-grid{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:start}
.flow-text{max-width:480px}
.flow-text p{color:var(--text-secondary);line-height:1.8}
.flow-eradec{display:flex;flex-direction:column;gap:10px;margin-top:28px}
.era-card{display:flex;gap:16px;padding:16px 20px;background:var(--white);
  border:1px solid rgba(27,42,74,.08);border-radius:var(--radius-md);
  transition:box-shadow var(--transition),transform var(--transition);
  cursor:pointer;align-items:flex-start}
.era-card:hover{box-shadow:var(--shadow-md);transform:translateX(4px)}
.era-year{font-family:var(--font-serif);font-weight:700;font-size:.85rem;
  color:var(--gold-500);flex-shrink:0;min-width:90px;padding-top:2px}
.era-title{font-weight:700;font-size:.95rem;color:var(--navy-800);margin-bottom:4px}
.era-desc{font-size:.83rem;color:var(--text-muted);line-height:1.5}
.flow-visual{background:var(--white);border:1px solid rgba(27,42,74,.08);
  border-radius:var(--radius-lg);padding:24px;box-shadow:var(--shadow-sm);
  min-height:340px;display:flex;align-items:center;justify-content:center}
.flow-visual svg{width:100%;max-width:420px;height:auto}

.refs-grid{display:grid;grid-template-columns:1fr 1fr;gap:40px}
.refs-heading{font-size:1.15rem;margin-bottom:20px;padding-bottom:12px;
  border-bottom:2px solid var(--gold-500);display:inline-block}
.refs-list{list-style:none;counter-reset:ref-counter}
.refs-list li{counter-increment:ref-counter;padding:14px 16px;margin-bottom:8px;
  background:var(--white);border:1px solid rgba(27,42,74,.07);
  border-radius:var(--radius-sm);font-size:.83rem;color:var(--text-secondary);
  line-height:1.6;transition:background var(--transition),box-shadow var(--transition);
  display:flex;gap:10px}
.refs-list li:hover{background:var(--cream);box-shadow:var(--shadow-sm)}
.refs-list li::before{content:counter(ref-counter);
  font-family:var(--font-serif);font-weight:700;font-size:.75rem;color:var(--coral);
  background:var(--cream-2);border:1px solid rgba(212,168,83,.2);
  border-radius:100px;padding:2px 8px;flex-shrink:0;
  align-self:flex-start;margin-top:2px}

.site-footer{background:var(--navy-900);color:rgba(255,255,255,.7);padding:56px 0 32px}
.footer-inner{display:flex;flex-wrap:wrap;gap:32px;align-items:flex-start}
.footer-brand{display:flex;gap:12px;align-items:flex-start;flex-shrink:0}
.footer-brand .logo-icon{font-size:1.8rem;color:var(--gold-500)}
.footer-title{font-family:var(--font-serif);font-weight:700;
  font-size:1rem;color:var(--white);margin-bottom:2px}
.footer-subtitle{font-size:.72rem;color:rgba(255,255,255,.45);letter-spacing:.03em}
.footer-nav{flex:1;display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center}
.footer-label{font-size:.75rem;font-weight:600;color:rgba(255,255,255,.4);
  letter-spacing:.06em;text-transform:uppercase;margin-right:4px}
.footer-nav a{font-size:.85rem;color:rgba(255,255,255,.65);transition:color var(--transition)}
.footer-nav a:hover{color:var(--gold-300)}
.footer-note{width:100%;font-size:.75rem;color:rgba(255,255,255,.35);
  line-height:1.6;padding-top:20px;border-top:1px solid rgba(255,255,255,.08);margin-top:8px}
"""
with open("c:/upstage/style.css","a",encoding="utf-8") as f:
    f.write(CSS3)
print("style.css part3 완료")
