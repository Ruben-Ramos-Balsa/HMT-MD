\ ILP model for K_{R12} (HMT N32 referee closeout)
Minimize
 obj: 0
Subject To
 c1_1:  k1 + k4 + k7 + k10 = 2378
 c1_2:  k1 + k4 - k7 - k10 = -452
 c1_3:  k1 - k4 + k7 - k10 = -668
 c1_4:  k1 - k4 - k7 + k10 = -322
 c2_1:  k2 + k5 + k8 + k11 = 1406
 c2_2:  k2 + k5 - k8 - k11 = 998
 c2_3:  k2 - k5 + k8 - k11 = -204
 c2_4:  k2 - k5 - k8 + k11 = -28
 c3_1:  k3 + k6 + k9 + k12 = 2479
 c3_2:  k3 + k6 - k9 - k12 = -551
 c3_3:  k3 - k6 + k9 - k12 = -371
 c3_4:  k3 - k6 - k9 + k12 = -997
Bounds
 0 <= k1 <= 999
 0 <= k2 <= 999
 0 <= k3 <= 999
 0 <= k4 <= 999
 0 <= k5 <= 999
 0 <= k6 <= 999
 0 <= k7 <= 999
 0 <= k8 <= 999
 0 <= k9 <= 999
 0 <= k10 <= 999
 0 <= k11 <= 999
 0 <= k12 <= 999
Generals
 k1 k2 k3 k4 k5 k6 k7 k8 k9 k10 k11 k12
End
