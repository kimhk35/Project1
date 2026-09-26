import numpy as np, wave, sys
SR=44100; T=float(sys.argv[1]); starts=[float(x) for x in sys.argv[2].split(',')]
n=int(SR*T); out=np.zeros((n,2))
bpm=84; beat=60/bpm; bar=4*beat
def mtof(m): return 440*2**((m-69)/12)
chords=[[48,55,64,71],[45,52,60,67],[41,48,57,64],[43,50,59,65]]  # Cmaj7 Am7 Fmaj7 G7sus-ish
bass=[36,33,29,31]
rng=np.random.default_rng(7)
def add(sig,t0,pan=0.5,g=1.0):
    i=int(t0*SR); j=min(n,i+len(sig))
    if i>=n: return
    s=sig[:j-i]*g; out[i:j,0]+=s*(1-pan)*1.4; out[i:j,1]+=s*pan*1.4
def ep(f,dur,vel=0.2):
    t=np.arange(int(dur*SR))/SR
    env=np.exp(-t*2.2)*(1-np.exp(-t*200))
    s=np.sin(2*np.pi*f*t)+0.35*np.sin(2*np.pi*2*f*t)*np.exp(-t*4)+0.12*np.sin(2*np.pi*3*f*t)*np.exp(-t*6)
    trem=1+0.15*np.sin(2*np.pi*4.5*t)
    return s*env*trem*vel
def pluck(f,dur,vel=0.12):
    t=np.arange(int(dur*SR))/SR
    return (np.sin(2*np.pi*f*t)+0.3*np.sin(2*np.pi*4*f*t)*np.exp(-t*10))*np.exp(-t*5)*vel
def kick():
    t=np.arange(int(0.35*SR))/SR; f=50+90*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)*0.55
def hat(v=0.05):
    t=np.arange(int(0.06*SR))/SR; return rng.standard_normal(len(t))*np.exp(-t*70)*v
def snare():
    t=np.arange(int(0.25*SR))/SR; return (rng.standard_normal(len(t))*0.5+np.sin(2*np.pi*190*t))*np.exp(-t*18)*0.16
melody=[76,74,72,74,76,79,76,74, 72,69,72,74,72,69,67,69, 69,72,74,72,69,67,65,67, 67,71,74,72,71,67,71,74]
t=0.0; k=0
while t<T:
    c=k%4; ch=chords[c]
    for m in ch: add(ep(mtof(m),bar*1.05,0.075),t+rng.uniform(0,0.02),pan=rng.uniform(.3,.7))
    add(ep(mtof(bass[c]),bar*0.9,0.22)*1.0,t,0.5)
    add(ep(mtof(bass[c]),beat*1.2,0.16),t+2.5*beat,0.5)
    for b in range(4):
        if k>=1 and T-t>bar:
            add(kick(),t+b*beat) if b in (0,2) else add(snare(),t+b*beat,0.55)
            if b==2: add(kick()*0.6,t+b*beat+beat*0.75)
        for h in range(2):
            add(hat(0.04 if h else 0.06),t+b*beat+h*beat/2*1.08,pan=0.65)
    if k>=2 and (k//8)%2==0:
        for q in range(8):
            m=melody[(k%4)*8+q]
            if rng.random()<0.8: add(pluck(mtof(m),beat*0.9),t+q*beat/2,pan=0.4)
    t+=bar; k+=1
# lowpass-ish smoothing (lofi)
from numpy.fft import rfft, irfft
for ch in range(2):
    x=out[:,ch]; a=0.25; y=np.empty_like(x); acc=0
    # one-pole filter vectorised via lfilter-free approach
    import math
    y=np.convolve(x,np.ones(6)/6,mode='same'); out[:,ch]=y
# vinyl noise
out+=rng.standard_normal(out.shape)*0.0025
# whoosh at scene changes
for s in starts[1:]:
    L=int(0.7*SR); tt=np.arange(L)/SR
    nz=rng.standard_normal(L); nz=np.convolve(nz,np.ones(12)/12,mode='same')
    env=np.sin(np.pi*tt/0.7)**2*0.25
    add(nz*env,s-0.45,pan=0.5)
# fades
fi=int(2*SR); fo=int(4*SR)
out[:fi]*=np.linspace(0,1,fi)[:,None]; out[-fo:]*=np.linspace(1,0,fo)[:,None]
out/=np.max(np.abs(out))/0.6
w=wave.open('bgm.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
print('ok',T)
