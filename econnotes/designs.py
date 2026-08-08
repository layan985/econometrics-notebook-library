"""Transparent reference implementations for the Econometrics Notebook Library."""
from __future__ import annotations
from itertools import combinations
from math import comb
from typing import Iterable
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.optimize import minimize

def shift_share_instrument(shares: np.ndarray, shocks: np.ndarray) -> np.ndarray:
    shares = np.asarray(shares, float); shocks = np.asarray(shocks, float); return shares @ shocks

def iv_ratio(y: np.ndarray, x: np.ndarray, z: np.ndarray) -> float:
    y=np.asarray(y,float); x=np.asarray(x,float); z=np.asarray(z,float); return float(z@y/(z@x))

def shock_level_iv_equivalent(y: np.ndarray, x: np.ndarray, shares: np.ndarray, shocks: np.ndarray) -> float:
    exposure=shares.sum(axis=0); ybar=shares.T@y/exposure; xbar=shares.T@x/exposure
    return float(np.sum(exposure*shocks*ybar)/np.sum(exposure*shocks*xbar))

def effective_number_of_shocks(shares: np.ndarray) -> float:
    exposure=np.asarray(shares,float).sum(axis=0); w=exposure/exposure.sum(); return float(1.0/np.sum(w**2))

def simulate_shift_share(n_regions:int=180,n_sectors:int=25,beta:float=1.5,seed:int=202)->dict:
    rng=np.random.default_rng(seed); concentration=rng.uniform(.4,2.0,size=n_sectors); shares=rng.dirichlet(concentration,size=n_regions); shocks=rng.normal(size=n_sectors); z=shares@shocks; first_stage_noise=rng.normal(scale=.8,size=n_regions); x=1.2*z+first_stage_noise; structural_error=.4*first_stage_noise+rng.normal(scale=1.0,size=n_regions); y=beta*x+structural_error
    return {'shares':shares,'shocks':shocks,'z':z,'x':x,'y':y,'beta':beta}

def _project_simplex(v:np.ndarray)->np.ndarray:
    v=np.asarray(v,float); u=np.sort(v)[::-1]; cssv=np.cumsum(u)-1.0; ind=np.arange(1,len(v)+1); cond=u-cssv/ind>0; rho=np.where(cond)[0][-1]; theta=cssv[rho]/(rho+1.0); return np.maximum(v-theta,0.0)

def synthetic_control_weights(y1_pre:np.ndarray,Y0_pre:np.ndarray,ridge:float=0.0)->np.ndarray:
    y1_pre=np.asarray(y1_pre,float); Y0_pre=np.asarray(Y0_pre,float); J=Y0_pre.shape[1]
    def objective(w):
        gap=y1_pre-Y0_pre@w; return float(gap@gap+ridge*(w@w))
    cons=({'type':'eq','fun':lambda w:np.sum(w)-1.0},); bounds=[(0.0,1.0)]*J; w0=np.ones(J)/J
    res=minimize(objective,w0,method='SLSQP',bounds=bounds,constraints=cons,options={'ftol':1e-10,'maxiter':1000})
    if res.success and np.all(np.isfinite(res.x)): return _project_simplex(res.x)
    w=w0.copy(); L=2.0*(np.linalg.norm(Y0_pre,2)**2+ridge); step=1.0/max(L,1e-12)
    for _ in range(20000):
        grad=2.0*(Y0_pre.T@(Y0_pre@w-y1_pre)+ridge*w); w_new=_project_simplex(w-step*grad)
        if np.max(np.abs(w_new-w))<1e-9: w=w_new; break
        w=w_new
    return w

def simulate_synthetic_control(n_donors:int=18,t_pre:int=20,t_post:int=10,tau:float=-2.0,seed:int=101)->dict:
    rng=np.random.default_rng(seed); T=t_pre+t_post; f1=np.sin(np.arange(T)/4.0); f2=np.linspace(-1,1,T); donor_loadings=rng.normal(size=(n_donors,2)); donors=donor_loadings[:,0,None]*f1+donor_loadings[:,1,None]*f2+rng.normal(scale=.25,size=(n_donors,T)); true_w=rng.dirichlet(np.ones(n_donors)); treated0=true_w@donors+rng.normal(scale=.12,size=T); treated=treated0.copy(); treated[t_pre:]+=tau
    return {'treated':treated,'treated0':treated0,'donors':donors,'t_pre':t_pre,'tau':tau}

def scm_placebo_rmspe_ratios(treated:np.ndarray,donors:np.ndarray,t_pre:int)->tuple[float,np.ndarray]:
    panel=np.vstack([treated[None,:],donors]); ratios=[]
    for i in range(panel.shape[0]):
        y1=panel[i]; Y0=np.delete(panel,i,axis=0).T; w=synthetic_control_weights(y1[:t_pre],Y0[:t_pre]); synth=Y0@w; pre=np.sqrt(np.mean((y1[:t_pre]-synth[:t_pre])**2)); post=np.sqrt(np.mean((y1[t_pre:]-synth[t_pre:])**2)); ratios.append(post/max(pre,1e-8))
    ratios=np.asarray(ratios); return float(ratios[0]),ratios[1:]

def difference_in_means(y:np.ndarray,z:np.ndarray)->float:
    y=np.asarray(y,float); z=np.asarray(z,int); return float(y[z==1].mean()-y[z==0].mean())

def randomization_inference_complete(y:np.ndarray,z:np.ndarray,tau_null:float=0.0,B:int=5000,seed:int=44)->dict:
    rng=np.random.default_rng(seed); y=np.asarray(y,float); z=np.asarray(z,int); n=len(y); n1=int(z.sum()); y_uniform=y-tau_null*z; obs=difference_in_means(y_uniform,z); total_assignments=comb(n,n1); stats=[]
    if total_assignments<=B:
        for idx in combinations(range(n),n1):
            z_star=np.zeros(n,dtype=int); z_star[list(idx)]=1; stats.append(difference_in_means(y_uniform,z_star))
    else:
        for _ in range(B):
            treated_idx=rng.choice(n,size=n1,replace=False); z_star=np.zeros(n,dtype=int); z_star[treated_idx]=1; stats.append(difference_in_means(y_uniform,z_star))
    stats=np.asarray(stats); p=float((1+np.sum(np.abs(stats)>=abs(obs)))/(len(stats)+1)); return {'stat_obs':float(obs),'p_value':p,'null_distribution':stats}

def simulate_randomized_experiment(n:int=80,n_treated:int=40,tau:float=.6,seed:int=55)->dict:
    rng=np.random.default_rng(seed); y0=rng.normal(size=n); z=np.zeros(n,dtype=int); z[rng.choice(n,size=n_treated,replace=False)]=1; y=y0+tau*z; return {'y':y,'z':z,'y0':y0,'tau':tau}

def simulate_local_projection_series(T:int=500,rho:float=.72,theta:float=.8,seed:int=808)->pd.DataFrame:
    rng=np.random.default_rng(seed); shock=rng.normal(size=T); eps=rng.normal(scale=.8,size=T); y=np.zeros(T)
    for t in range(1,T): y[t]=rho*y[t-1]+theta*shock[t]+eps[t]
    return pd.DataFrame({'time':np.arange(T),'y':y,'shock':shock})

def local_projections(df:pd.DataFrame,horizons:Iterable[int]=range(0,13),lags:int=2)->pd.DataFrame:
    d=df.copy()
    for L in range(1,lags+1): d[f'y_l{L}']=d['y'].shift(L); d[f'shock_l{L}']=d['shock'].shift(L)
    rows=[]; controls=[f'y_l{L}' for L in range(1,lags+1)]+[f'shock_l{L}' for L in range(1,lags+1)]
    for h in horizons:
        tmp=d.copy(); tmp['y_lead']=tmp['y'].shift(-h); use=tmp.dropna(subset=['y_lead','shock']+controls); X=sm.add_constant(use[['shock']+controls]); fit=sm.OLS(use['y_lead'],X).fit(cov_type='HAC',cov_kwds={'maxlags':max(h+1,lags)}); rows.append({'horizon':int(h),'estimate':float(fit.params['shock']),'se':float(fit.bse['shock'])})
    return pd.DataFrame(rows)
