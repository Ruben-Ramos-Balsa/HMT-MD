# N57 - Bockstein-Hensel carry final closure

## What is closed

The carries c_t and h_t are not free objects and not P_m. They are canonical Bockstein/Hensel cocycles induced by the digit section F3 -> {0,1,2}.

Local formulas:
q=(p+e+f) mod 3
c=(p+e+f-q)/3
a=(p+e-f) mod 3
h=(p+e-f-a)/3

Decomposition:
c=kappa(p,e)+kappa((p+e) mod3,f)
h=kappa(p,e)+beta((p+e) mod3,f)

kappa 2-cocycle identity pass: True

## Nonlinearity

q and a are affine over F3.
c and h are not affine; they are the nonlinear obstruction.

Polynomial c terms:
['2ef', '2ef^2', '2e^2f', '2pf', '2pf^2', '2pe', 'pef', '2pe^2', '2p^2f', '2p^2e']

Polynomial h terms:
['2f^2', 'ef', '2ef^2', 'e^2f', 'pf', '2pf^2', '2pe', '2pef', '2pe^2', 'p^2f', '2p^2e']

## Terminal

T rows: ['021020', '001220', '100210']
q=122120
c=000110
a=222000
h integer=-1 0 0 0 1 0
row charges=221

## Remaining yellow

The 180-layer pass is an external certificate from LIFT-CELDA-15 unless the raw x_t,u_t arrays are supplied.
The final remaining mathematical target is APP/TPK -> channel states/lifts x_t^pi,e,phi, not carry.
