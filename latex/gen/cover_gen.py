import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
# loss landscape: rotated elongated valley + a gentle bump, minimum near (0,0)
th=np.deg2rad(-25); R=np.array([[np.cos(th),-np.sin(th)],[np.sin(th),np.cos(th)]])
A=np.diag([0.12,1.6])
def f(p):
    q=R.T@p
    return 0.5*q@A@q + 0.35*np.exp(-((p[0]+3.2)**2+(p[1]-1.2)**2)/1.5)
def grad(p,h=1e-5):
    return np.array([(f(p+[h,0])-f(p-[h,0]))/(2*h),(f(p+[0,h])-f(p-[0,h]))/(2*h)])
x0=np.array([-8.4,-0.6]); rng=np.random.default_rng(11)
def run(kind,n=140):
    x=x0.copy(); P=[x.copy()]; v=np.zeros(2); s=np.zeros(2)
    for t in range(1,n+1):
        g=grad(x)
        if kind=='gd': x=x-1.05*g
        elif kind=='sgd': x=x-0.35*(g+rng.normal(0,0.9,2))
        elif kind=='mom': v=0.9*v+g; x=x-0.09*v
        elif kind=='nest':
            gl=grad(x-0.09*0.9*v); v=0.9*v+gl; x=x-0.09*v
        elif kind=='rms': s=0.9*s+0.1*g*g; x=x-0.3*g/(np.sqrt(s)+1e-8)
        elif kind=='adam':
            v=0.9*v+0.1*g; s=0.999*s+0.001*g*g; vh=v/(1-0.9**t); sh=s/(1-0.999**t); x=x-0.35*vh/(np.sqrt(sh)+1e-8)
        P.append(x.copy())
    return np.array(P)
T={k:run(k) for k in ['gd','sgd','mom','nest','rms','adam']}
for k,v in T.items(): print(k, v[-1].round(3), f(v[-1]).round(4))
X,Y=np.meshgrid(np.linspace(-11,11,400),np.linspace(-6,6,260))
Z=np.vectorize(lambda a,b: f(np.array([a,b])))(X,Y)
levels=[0.05,0.2,0.5,1,1.8,2.9,4.3,6,8,10.5,13.5]
cs=plt.contour(X,Y,Z,levels=levels)
np.save('Z.npy',Z)
import pickle; pickle.dump({'T':T,'segs':cs.allsegs,'levels':levels},open('cover.pkl','wb'))
plt.figure(figsize=(8,4.5))
plt.contour(X,Y,Z,levels=levels,colors='gray')
cols=dict(gd='g',sgd='b',mom='orange',nest='r',rms='purple',adam='gold')
for k,v in T.items(): plt.plot(v[:,0],v[:,1],color=cols[k],label=k)
plt.legend(); plt.gca().set_aspect('equal'); plt.savefig('/tmp/coverprev.png',dpi=90)
