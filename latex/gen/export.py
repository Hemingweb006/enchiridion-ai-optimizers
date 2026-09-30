import pickle, numpy as np
d=pickle.load(open('cover.pkl','rb'))
sc=0.955; cx,cy=10.5,10.4
def P(x,y): return (cx+sc*x, cy+sc*y)
out=[]
lv=d['levels']; n=len(lv)
for i,segs in enumerate(d['segs']):
    frac=i/(n-1)
    col=f"cyanglow!{int(75-60*frac)}!nightlight"
    op=0.95-0.5*frac
    for seg in segs:
        seg=seg[::2] if len(seg)>200 else seg
        pts=" -- ".join("(%.3f,%.3f)"%P(*p) for p in seg)
        out.append(r"\draw[%s,line width=%.2fpt,opacity=%.2f] %s;"%(col,0.9-0.3*frac,op,pts))
open('cover-contours.tex','w').write("\n".join(out))
cols=dict(gd='greenglow',sgd='cyanglow',mom='copper',nest='redglow',rms='violetglow',adam='goldleaf')
lw=dict(gd=1.1,sgd=0.8,mom=1.1,nest=1.1,rms=1.1,adam=1.8)
out=[]
for k in ['sgd','gd','rms','nest','mom','adam']:
    T=d['T'][k]
    # cut once converged
    keep=len(T)
    for i in range(len(T)):
        if np.linalg.norm(T[i])<0.05: keep=i+1; break
    T=T[:keep]
    pts=" -- ".join("(%.3f,%.3f)"%P(*p) for p in T)
    out.append(r"\draw[%s,line width=%.1fpt,opacity=0.18,line join=round] %s;"%(cols[k],lw[k]*4,pts))
    out.append(r"\draw[%s,line width=%.1fpt,line join=round] %s;"%(cols[k],lw[k],pts))
    for p in T[:min(25,len(T))][::1] if k in ('gd','mom','adam') else []:
        out.append(r"\fill[%s] (%.3f,%.3f) circle (0.9pt);"%((cols[k],)+P(*p)))
x0=d['T']['gd'][0]
out.append(r"\fill[white,opacity=0.25] (%.3f,%.3f) circle (0.28);\fill[white] (%.3f,%.3f) circle (0.09);"%(P(*x0)+P(*x0)))
out.append(r"\node[white,font=\small\itshape,anchor=east] at (%.3f,%.3f) {$x_0$};"%(P(*x0)[0]-0.2,P(*x0)[1]))
m=P(0,0)
for r,o in [(0.55,0.10),(0.38,0.18),(0.24,0.35)]:
    out.append(r"\fill[goldleaf,opacity=%.2f] (%.3f,%.3f) circle (%.2f);"%(o,m[0],m[1],r))
out.append(r"\fill[goldpale] (%.3f,%.3f) circle (0.11);"%m)
out.append(r"\node[goldpale,font=\small\itshape,anchor=west] at (%.3f,%.3f) {$x^*$};"%(m[0]+0.25,m[1]-0.35))
open('cover-paths.tex','w').write("\n".join(out))
print(len(open('cover-contours.tex').read())//1000,'kB')
