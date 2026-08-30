CSS = """
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --navy-900:#0f1a2e; --navy-800:#1B2A4A; --navy-700:#253a63;
  --navy-600:#35507d; --gold-500:#D4A853; --gold-300:#f0cd8a;
  --cream:#FAF7F2; --cream-2:#F5F0E6; --soft-blue:#E8EFF7;
  --coral:#E07A5F; --text-primary:#1a1a2e; --text-secondary:#4a4a5a;
  --text-muted:#7a7a8a; --white:#fff;
  --shadow-sm:0 1px 3px rgba(15,26,46,.08);
  --shadow-md:0 4px 16px rgba(15,26,46,.10);
  --shadow-lg:0 12px 40px rgba(15,26,46,.14);
  --radius-sm:6px; --radius-md:12px; --radius-lg:20px;
  --font-serif:'Noto Serif KR','Nanum Myeongjo',serif;
  --font-sans:'Noto Sans KR','Nanum Gothic',sans-serif;
  --transition:.25s cubic-bezier(.4,0,.2,1);
}
html{scroll-behavior:smooth}
body{font-family:var(--font-sans);color:var(--text-primary);
  background:var(--cream);line-height:1.7;overflow-x:hidden;
  -webkit-font-smoothing:antialiased}
h1,h2,h3,h4,h5{font-family:var(--font-serif);font-weight:700;
  line-height:1.35;color:var(--navy-800)}
p{margin-bottom:1rem}
a{color:inherit;text-decoration:none}
strong.highlight{color:var(--coral);font-weight:600}
.container{width:100%;max-width:1200px;margin:0 auto;padding:0 24px}

.site-header{position:fixed;top:0;left:0;right:0;z-index:1000;
  background:rgba(250,247,242,.88);
  backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);
  border-bottom:1px solid rgba(27,42,74,.07);
  transition:box-shadow var(--transition)}
.site-header.scrolled{box-shadow:var(--shadow-md)}
.header-inner{display:flex;align-items:center;justify-content:space-between;
  height:72px;gap:24px}
.logo{display:flex;align-items:center;gap:10px;
  font-family:var(--font-serif);font-weight:700;font-size:1.1rem;
  color:var(--navy-800);flex-shrink:0;transition:opacity var(--transition)}
.logo:hover{opacity:.75}
.logo-icon{font-size:1.6rem;color:var(--gold-500);line-height:1}
.main-nav{display:flex;align-items:center}
.nav-list{display:flex;list-style:none;gap:4px}
.nav-link{display:inline-block;padding:6px 14px;border-radius:var(--radius-sm);
  font-size:.9rem;font-weight:500;color:var(--text-secondary);
  transition:color var(--transition),background var(--transition);white-space:nowrap}
.nav-link:hover,.nav-link.active{color:var(--navy-800);background:var(--soft-blue)}
.menu-toggle{display:none;flex-direction:column;gap:5px;background:none;
  border:none;cursor:pointer;padding:6px}
.menu-toggle span{display:block;width:22px;height:2px;background:var(--navy-800);
  border-radius:2px;transition:transform var(--transition),opacity var(--transition)}

.hero{position:relative;min-height:100vh;display:flex;align-items:center;
  padding-top:72px;overflow:hidden;
  background:linear-gradient(160deg,var(--cream) 0%,var(--soft-blue) 50%,var(--cream-2) 100%)}
.hero-bg-grid{position:absolute;inset:0;pointer-events:none;
  background-image:linear-gradient(rgba(27,42,74,.03) 1px,transparent 1px),
    linear-gradient(90deg,rgba(27,42,74,.03) 1px,transparent 1px);
  background-size:60px 60px}
.hero-shape{position:absolute;border-radius:50%;pointer-events:none}
.hero-shape-1{width:500px;height:500px;
  background:radial-gradient(circle,rgba(212,168,83,.10) 0%,transparent 70%);
  top:-120px;right:-80px}
.hero-shape-2{width:300px;height:300px;
  background:radial-gradient(circle,rgba(27,42,74,.05) 0%,transparent 70%);
  bottom:80px;left:-60px}
.hero-content{position:relative;z-index:2;display:flex;
  flex-direction:column;align-items:flex-start;
  max-width:700px;padding-top:48px;padding-bottom:80px}
.hero-badge{display:inline-flex;align-items:center;gap:8px;
  padding:6px 16px;background:rgba(212,168,83,.12);
  border:1px solid rgba(212,168,83,.25);border-radius:100px;
  font-size:.8rem;font-weight:600;color:var(--gold-500);
  letter-spacing:.05em;text-transform:uppercase;margin-bottom:28px}
.badge-dot{display:inline-block;width:8px;height:8px;border-radius:50%;
  background:var(--gold-500);animation:pulse-dot 2s ease-in-out infinite}
@keyframes pulse-dot{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.5;transform:scale(.8)}}
.hero-title{font-size:clamp(2.8rem,6vw,4.5rem);font-weight:900;
  color:var(--navy-800);line-height:1.15;margin-bottom:20px;letter-spacing:-.02em}
.title-accent{color:var(--coral);display:inline-block;position:relative}
.title-accent::after{content:'';position:absolute;bottom:4px;left:0;right:0;
  height:4px;background:var(--gold-500);border-radius:2px;opacity:.6}
.hero-subtitle{font-size:clamp(1rem,2vw,1.15rem);color:var(--text-secondary);
  line-height:1.8;margin-bottom:40px;max-width:560px}
.hero-actions{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:64px}
.btn{display:inline-flex;align-items:center;gap:8px;
  padding:14px 28px;border-radius:100px;font-size:.95rem;font-weight:600;
  cursor:pointer;transition:all var(--transition);border:2px solid transparent}
.btn-primary{background:var(--navy-800);color:var(--white);border-color:var(--navy-800)}
.btn-primary:hover{background:var(--navy-700);border-color:var(--navy-700);
  transform:translateY(-2px);box-shadow:var(--shadow-md)}
.btn-outline{background:transparent;color:var(--navy-800);border-color:var(--navy-800)}
.btn-outline:hover{background:var(--navy-800);color:var(--white);transform:translateY(-2px)}
.hero-stats{display:flex;align-items:center;gap:24px;padding:20px 28px;
  background:rgba(255,255,255,.7);border:1px solid rgba(27,42,74,.10);
  border-radius:var(--radius-lg);box-shadow:var(--shadow-sm);
  backdrop-filter:blur(4px)}
.stat{display:flex;flex-direction:column;gap:2px}
.stat-number{font-family:var(--font-serif);font-size:1.8rem;
  font-weight:700;color:var(--navy-800)}
.stat-label{font-size:.78rem;color:var(--text-muted);font-weight:500;letter-spacing:.03em}
.stat-divider{width:1px;height:40px;background:rgba(27,42,74,.12)}
"""
with open("c:/upstage/style.css","w",encoding="utf-8") as f:
    f.write(CSS)
print("style.css part1 완료")
