#!/usr/bin/env python3
"""Exploración NO certificada de Schur con una traslación prima activa.

No modifica la prueba de R=1/9. Cuadratura Gauss finita sin cota intervalar:
sus números sólo orientan una certificación posterior. Los ceros no entran.
"""
from pathlib import Path
import json
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--coarse",type=int,default=9)
parser.add_argument("--fine",type=int,default=81)
parser.add_argument("--order",type=int,default=32)
args = parser.parse_args()
root=Path(__file__).resolve().parent
rec=json.loads((root/"CERTIFICADO_SCHUR_R_UN_NOVENO.json").read_text())
c=float(rec["c_gamma"]["lower"])
from fractions import Fraction
pi=float(Fraction(rec["pi_publication"]["exact_lower"]))
L=float(Fraction(rec["log2_exact_bounds"][0]))
R=7/10
M=args.coarse
K=args.fine
if K%M: raise ValueError("non-nested partitions")
w=L/np.sqrt(2)
end=np.linspace(-R/2,R/2,K+1)
breaks=np.unique(np.concatenate((end,np.clip(end+L,-R/2,R/2),np.clip(end-L,-R/2,R/2))))
breaks=breaks[np.concatenate(([True],np.diff(breaks)>1e-14))]
nodes,ww=np.polynomial.legendre.leggauss(args.order)
x=((breaks[:-1,None]+breaks[1:,None])/2+(breaks[1:,None]-breaks[:-1,None])*nodes/2).ravel()
weights=((breaks[1:,None]-breaks[:-1,None])*ww/2).ravel()
h=R/K
aa=end[:-1][None,:];bb=end[1:][None,:];xx=x[:,None]
inside=(xx>aa)&(xx<bb)
Y=inside/np.sqrt(h)
tail=lambda y:np.arctanh(np.exp(-y/2))+np.arctan(np.exp(-y/2))
left=tail(np.abs(xx-aa));right=tail(np.abs(xx-bb))
Lg=np.where(inside,left+right,np.where(xx<aa,-left+right,-right+left))/np.sqrt(h)
Lp=-(w/np.sqrt(h))*(((xx-L>aa)&(xx-L<bb)).astype(float)+((xx+L>aa)&(xx+L<bb)).astype(float))
Lpol=4*(np.sinh((xx-aa)/2)-np.sinh((xx-bb)/2))/np.sqrt(h)
Lu=Lg+c*Y+Lp+Lpol
G=Y.T@(weights[:,None]*Lu)
G=(G+G.T)/2
block=K//M
C=np.zeros((K,M))
for j in range(M):C[j*block:(j+1)*block,j]=1/np.sqrt(block)
# Orthogonal new details on each coarse cell.
v=np.ones(block)/np.sqrt(block)
e=np.zeros(block);e[0]=1
hv=(e-v)/np.linalg.norm(e-v)
house=np.eye(block)-2*np.outer(hv,hv)
E=np.zeros((K,K-M))
for j in range(M): E[j*block:(j+1)*block,j*(block-1):(j+1)*(block-1)]=house[:,1:]
A=C.T@G@C
D=E.T@G@E
B=E.T@G@C
z=E@np.linalg.solve(D,B)
Sz=A-B.T@np.linalg.solve(D,B)
F=Lu@(C-z)
Yc=Y@C
res=F-Yc@(Yc.T@(weights[:,None]*F))
errorGram=res.T@(weights[:,None]*res)
hc=R/M
NN=range(1,int(pi/(2*hc))+3)
eta,N=max((4*sum(1/(4*n+1) for n in range(q+1))-hc*hc*(q+1)*(2*q+1)/(pi*pi)+c-2*w-(2*np.sinh(R/2)-R),q) for q in NN)
lower=Sz-errorGram/eta
print(json.dumps({"status":"EXPLORATION_NOT_CERTIFIED","R":"7/10","active_prime_clock":"log(2)","coarse":M,"fine":K,"gauss_order":args.order,"points":len(x),"detail_eta_candidate":eta,"N":N,"mean_min_eigenvalue":float(np.linalg.eigvalsh(A)[0]),"galerkin_detail_min":float(np.linalg.eigvalsh(D)[0]),"schur_upper_candidate":float(np.linalg.eigvalsh(Sz)[0]),"residual_gram_norm":float(np.linalg.eigvalsh(errorGram)[-1]),"schur_lower_candidate":float(np.linalg.eigvalsh(lower)[0]),"limitations":["no interval enclosure of quadrature","no tail bound for quadrature","no universal positivity assertion"]},indent=2))
