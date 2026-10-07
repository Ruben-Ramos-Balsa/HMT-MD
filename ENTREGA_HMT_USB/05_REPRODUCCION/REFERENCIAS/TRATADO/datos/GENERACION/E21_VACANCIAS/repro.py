import math, mpmath as mp
mp.mp.dps=80
eps=mp.log10(mp.mpf(10)/9)
rho=mp.log10(9)
alpha=mp.mpf('0.007297352569283800997285105472380663')
positions=[math.floor(n/float(eps)) for n in range(300)]
gaps=[positions[i+1]-positions[i] for i in range(len(positions)-1)]
short=[i for i,g in enumerate(gaps) if g==21]
returns=[short[i+1]-short[i] for i in range(len(short)-1)]
expr5=2*mp.pi*alpha-mp.mpf(7)/4*alpha**2+alpha**3/(2*mp.pi)+alpha**4/20-mp.mpf(2)/21*alpha**5
expr6=expr5-alpha**6/46
print('rho', rho)
print('epsilon', eps)
print('gaps', sorted(set(gaps[:200])))
print('short returns', sorted(set(returns[:100])))
print('res5', expr5-eps)
print('res6', expr6-eps)
