CSS2 = """
.section{padding:96px 0}
.section-label{display:flex;align-items:center;gap:14px;margin-bottom:48px;
  font-size:.82rem;font-weight:600;color:var(--text-muted);
  letter-spacing:.06em;text-transform:uppercase}
.label-line{display:inline-block;width:36px;height:2px;background:var(--gold-500);flex-shrink:0}
.section-title{font-size:clamp(1.7rem,3.5vw,2.4rem);margin-bottom:16px;color:var(--navy-800)}

.overview-grid{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center}
.lead-paragraph{font-size:1.05rem;color:var(--text-secondary);line-height:1.85;margin-bottom:1.2rem}
.overview-text p{color:var(--text-secondary);line-height:1.85;margin-bottom:1rem}
.overview-cards-mini{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:28px}
.mini-card{display:flex;gap:12px;padding:14px 16px;background:var(--white);
  border:1px solid rgba(27,42,74,.08);border-radius:var(--radius-md);
  transition:box-shadow var(--transition),transform var(--transition)}
.mini-card:hover{box-shadow:var(--shadow-md);transform:translateY(-3px)}
.mini-card-icon{font-size:1.4rem;flex-shrink:0;margin-top:2px}
.mini-card-title{font-weight:700;font-size:.88rem;color:var(--navy-800);margin-bottom:2px}
.mini-card-desc{font-size:.78rem;color:var(--text-muted);line-height:1.4}

.overview-visual{display:flex;justify-content:center;align-items:center}
.venn-diagram{position:relative;width:340px;height:340px}
.venn-circle{position:absolute;width:180px;height:180px;border-radius:50%;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;
  transition:transform var(--transition),box-shadow var(--transition)}
.venn-a{background:radial-gradient(circle,rgba(212,168,83,.20) 0%,rgba(212,168,83,.06) 70%);
  border:2px solid rgba(212,168,83,.40)}
.venn-b{background:radial-gradient(circle,rgba(27,42,74,.18) 0%,rgba(27,42,74,.05) 70%);
  border:2px solid rgba(27,42,74,.35)}
.venn-c{background:radial-gradient(circle,rgba(224,122,95,.18) 0%,rgba(224,122,95,.05) 70%);
  border:2px solid rgba(224,122,95,.35)}
.venn-label{font-family:var(--font-serif);font-weight:700;font-size:1rem;color:var(--navy-800)}
.venn-sub{font-size:.7rem;color:var(--text-muted)}
.venn-circle:hover{transform:scale(1.08);box-shadow:0 0 0 4px rgba(212,168,83,.2)}
.venn-center{position:absolute;top:50%;left:50%;
  transform:translate(-50%,-50%);width:120px;height:120px;border-radius:50%;
  background:var(--navy-800);display:flex;align-items:center;justify-content:center;
  z-index:5;box-shadow:var(--shadow-lg)}
.venn-center-text{font-family:var(--font-serif);font-weight:700;font-size:.75rem;
  color:var(--white);text-align:center;line-height:1.3}

.framework-intro p{color:var(--text-secondary);font-size:1rem;line-height:1.8;max-width:640px}
.framework-timeline{position:relative;margin-top:48px}
.timeline-track{position:relative;padding-left:48px}
.timeline-track::before{content:'';position:absolute;left:22px;top:0;bottom:0;
  width:2px;background:linear-gradient(to bottom,var(--gold-500),var(--coral));border-radius:1px}
.timeline-item{position:relative;padding:24px 28px;margin-bottom:16px;
  background:var(--white);border:1px solid rgba(27,42,74,.08);
  border-radius:var(--radius-md);transition:box-shadow var(--transition),transform var(--transition);
  cursor:pointer}
.timeline-item:hover{box-shadow:var(--shadow-md);transform:translateX(4px)}
.timeline-item::before{content:'';position:absolute;left:-32px;top:30px;
  width:14px;height:14px;border-radius:50%;background:var(--white);
  border:2px solid var(--gold-500)}
.timeline-item.active::before{background:var(--gold-500);
  box-shadow:0 0 0 5px rgba(212,168,83,.2)}
.timeline-order{display:inline-block;padding:2px 10px;background:var(--soft-blue);
  color:var(--navy-700);border-radius:100px;font-size:.72rem;font-weight:700;
  letter-spacing:.05em;margin-bottom:10px}
.timeline-item h3{font-size:1.05rem;font-family:var(--font-serif);margin-bottom:6px}
.timeline-item p{font-size:.88rem;color:var(--text-muted);line-height:1.5}
.timeline-item .tli-tags{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}
.timeline-item .tli-tag{padding:3px 10px;background:var(--cream-2);
  border:1px solid rgba(27,42,74,.06);border-radius:100px;
  font-size:.72rem;color:var(--text-secondary);font-weight:500}
"""
with open("c:/upstage/style.css","a",encoding="utf-8") as f:
    f.write(CSS2)
print("style.css part2 완료")
