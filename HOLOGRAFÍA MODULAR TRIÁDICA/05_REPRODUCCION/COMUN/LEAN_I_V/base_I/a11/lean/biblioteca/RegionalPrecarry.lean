import RegionalPublicationComposition
import KSelectedLattice

/-! Twelve pre-carry blocks computed from rational regional enclosures.
No real constant or target expansion enters the definitions. -/
noncomputable section
namespace HMT.I.RegionalPrecarry

open HMT.I.RegionalPublicationComposition
open HMT.I.KMarkedIncidence HMT.IncidenceRegister
open HMT.I.KSelectedLattice HMT.II.CKM.Incidence
open HMT.IV.CoxeterNeighbor HMT.IV.GlueDuality
open HMT.IV.NeighborSpan HMT.IV.NeighborLattice HMT.IV.NeighborDuality

set_option maxHeartbeats 12000000
set_option maxRecDepth 10000

def scale : Nat := 10 ^ 36
def index : Channel → Nat
  | .closure => 15
  | .propagation => 40
  | .autoscale => 100
def generatedPrefix (c : Channel) : Int :=
  RadixCellSelection.first (lower c (index c)) scale

theorem closure_cell_computation :
    RadixCellSelection.first (lower .closure 15) scale = 3141592653589793238462643383279502884 ∧
    RadixCellSelection.last (upper .closure 15) scale = 3141592653589793238462643383279502884 := by
  norm_num [lower, upper, scale, RadixCellSelection.first, RadixCellSelection.last,
    ClosureAnalytic.lowerQ, ClosureAnalytic.upperQ,
    ClosureAnalytic.quarterCount, ClosureAnalytic.companionCount,
    ClosureAnalytic.primitive_slope_value, ClosureAnalytic.compensator_slope_value,
    ClosureAnalytic.arctanPartialQ, ClosureAnalytic.magnitudeQ, Finset.sum_range_succ]

theorem propagation_cell_computation :
    RadixCellSelection.first (lower .propagation 40) scale = 2718281828459045235360287471352662497 ∧
    RadixCellSelection.last (upper .propagation 40) scale = 2718281828459045235360287471352662497 := by
  norm_num [lower, upper, scale, RadixCellSelection.first, RadixCellSelection.last,
    PropagationLimit.partialQ, PropagationLimit.upperQ, PropagationLimit.tailQ,
    PropagationLimit.coefficient, Finset.sum_range_succ]

theorem autoscale_pairs_computation :
    AutoscaleBrackets.cursorPair 100 = (573147844013817084101,927372692193078999176) ∧
    AutoscaleBrackets.cursorPair 101 = (927372692193078999176,1500520536206896083277) := by
  have h0 := AutoscaleBrackets.cursorPair_zero
  have h1 : AutoscaleBrackets.cursorPair 1 = (1,2) := by
    have h := AutoscaleBrackets.cursorPair_next 0
    rw [h0] at h
    norm_num at h
    exact h
  have h2 : AutoscaleBrackets.cursorPair 2 = (2,3) := by
    have h := AutoscaleBrackets.cursorPair_next 1
    rw [h1] at h
    norm_num at h
    exact h
  have h3 : AutoscaleBrackets.cursorPair 3 = (3,5) := by
    have h := AutoscaleBrackets.cursorPair_next 2
    rw [h2] at h
    norm_num at h
    exact h
  have h4 : AutoscaleBrackets.cursorPair 4 = (5,8) := by
    have h := AutoscaleBrackets.cursorPair_next 3
    rw [h3] at h
    norm_num at h
    exact h
  have h5 : AutoscaleBrackets.cursorPair 5 = (8,13) := by
    have h := AutoscaleBrackets.cursorPair_next 4
    rw [h4] at h
    norm_num at h
    exact h
  have h6 : AutoscaleBrackets.cursorPair 6 = (13,21) := by
    have h := AutoscaleBrackets.cursorPair_next 5
    rw [h5] at h
    norm_num at h
    exact h
  have h7 : AutoscaleBrackets.cursorPair 7 = (21,34) := by
    have h := AutoscaleBrackets.cursorPair_next 6
    rw [h6] at h
    norm_num at h
    exact h
  have h8 : AutoscaleBrackets.cursorPair 8 = (34,55) := by
    have h := AutoscaleBrackets.cursorPair_next 7
    rw [h7] at h
    norm_num at h
    exact h
  have h9 : AutoscaleBrackets.cursorPair 9 = (55,89) := by
    have h := AutoscaleBrackets.cursorPair_next 8
    rw [h8] at h
    norm_num at h
    exact h
  have h10 : AutoscaleBrackets.cursorPair 10 = (89,144) := by
    have h := AutoscaleBrackets.cursorPair_next 9
    rw [h9] at h
    norm_num at h
    exact h
  have h11 : AutoscaleBrackets.cursorPair 11 = (144,233) := by
    have h := AutoscaleBrackets.cursorPair_next 10
    rw [h10] at h
    norm_num at h
    exact h
  have h12 : AutoscaleBrackets.cursorPair 12 = (233,377) := by
    have h := AutoscaleBrackets.cursorPair_next 11
    rw [h11] at h
    norm_num at h
    exact h
  have h13 : AutoscaleBrackets.cursorPair 13 = (377,610) := by
    have h := AutoscaleBrackets.cursorPair_next 12
    rw [h12] at h
    norm_num at h
    exact h
  have h14 : AutoscaleBrackets.cursorPair 14 = (610,987) := by
    have h := AutoscaleBrackets.cursorPair_next 13
    rw [h13] at h
    norm_num at h
    exact h
  have h15 : AutoscaleBrackets.cursorPair 15 = (987,1597) := by
    have h := AutoscaleBrackets.cursorPair_next 14
    rw [h14] at h
    norm_num at h
    exact h
  have h16 : AutoscaleBrackets.cursorPair 16 = (1597,2584) := by
    have h := AutoscaleBrackets.cursorPair_next 15
    rw [h15] at h
    norm_num at h
    exact h
  have h17 : AutoscaleBrackets.cursorPair 17 = (2584,4181) := by
    have h := AutoscaleBrackets.cursorPair_next 16
    rw [h16] at h
    norm_num at h
    exact h
  have h18 : AutoscaleBrackets.cursorPair 18 = (4181,6765) := by
    have h := AutoscaleBrackets.cursorPair_next 17
    rw [h17] at h
    norm_num at h
    exact h
  have h19 : AutoscaleBrackets.cursorPair 19 = (6765,10946) := by
    have h := AutoscaleBrackets.cursorPair_next 18
    rw [h18] at h
    norm_num at h
    exact h
  have h20 : AutoscaleBrackets.cursorPair 20 = (10946,17711) := by
    have h := AutoscaleBrackets.cursorPair_next 19
    rw [h19] at h
    norm_num at h
    exact h
  have h21 : AutoscaleBrackets.cursorPair 21 = (17711,28657) := by
    have h := AutoscaleBrackets.cursorPair_next 20
    rw [h20] at h
    norm_num at h
    exact h
  have h22 : AutoscaleBrackets.cursorPair 22 = (28657,46368) := by
    have h := AutoscaleBrackets.cursorPair_next 21
    rw [h21] at h
    norm_num at h
    exact h
  have h23 : AutoscaleBrackets.cursorPair 23 = (46368,75025) := by
    have h := AutoscaleBrackets.cursorPair_next 22
    rw [h22] at h
    norm_num at h
    exact h
  have h24 : AutoscaleBrackets.cursorPair 24 = (75025,121393) := by
    have h := AutoscaleBrackets.cursorPair_next 23
    rw [h23] at h
    norm_num at h
    exact h
  have h25 : AutoscaleBrackets.cursorPair 25 = (121393,196418) := by
    have h := AutoscaleBrackets.cursorPair_next 24
    rw [h24] at h
    norm_num at h
    exact h
  have h26 : AutoscaleBrackets.cursorPair 26 = (196418,317811) := by
    have h := AutoscaleBrackets.cursorPair_next 25
    rw [h25] at h
    norm_num at h
    exact h
  have h27 : AutoscaleBrackets.cursorPair 27 = (317811,514229) := by
    have h := AutoscaleBrackets.cursorPair_next 26
    rw [h26] at h
    norm_num at h
    exact h
  have h28 : AutoscaleBrackets.cursorPair 28 = (514229,832040) := by
    have h := AutoscaleBrackets.cursorPair_next 27
    rw [h27] at h
    norm_num at h
    exact h
  have h29 : AutoscaleBrackets.cursorPair 29 = (832040,1346269) := by
    have h := AutoscaleBrackets.cursorPair_next 28
    rw [h28] at h
    norm_num at h
    exact h
  have h30 : AutoscaleBrackets.cursorPair 30 = (1346269,2178309) := by
    have h := AutoscaleBrackets.cursorPair_next 29
    rw [h29] at h
    norm_num at h
    exact h
  have h31 : AutoscaleBrackets.cursorPair 31 = (2178309,3524578) := by
    have h := AutoscaleBrackets.cursorPair_next 30
    rw [h30] at h
    norm_num at h
    exact h
  have h32 : AutoscaleBrackets.cursorPair 32 = (3524578,5702887) := by
    have h := AutoscaleBrackets.cursorPair_next 31
    rw [h31] at h
    norm_num at h
    exact h
  have h33 : AutoscaleBrackets.cursorPair 33 = (5702887,9227465) := by
    have h := AutoscaleBrackets.cursorPair_next 32
    rw [h32] at h
    norm_num at h
    exact h
  have h34 : AutoscaleBrackets.cursorPair 34 = (9227465,14930352) := by
    have h := AutoscaleBrackets.cursorPair_next 33
    rw [h33] at h
    norm_num at h
    exact h
  have h35 : AutoscaleBrackets.cursorPair 35 = (14930352,24157817) := by
    have h := AutoscaleBrackets.cursorPair_next 34
    rw [h34] at h
    norm_num at h
    exact h
  have h36 : AutoscaleBrackets.cursorPair 36 = (24157817,39088169) := by
    have h := AutoscaleBrackets.cursorPair_next 35
    rw [h35] at h
    norm_num at h
    exact h
  have h37 : AutoscaleBrackets.cursorPair 37 = (39088169,63245986) := by
    have h := AutoscaleBrackets.cursorPair_next 36
    rw [h36] at h
    norm_num at h
    exact h
  have h38 : AutoscaleBrackets.cursorPair 38 = (63245986,102334155) := by
    have h := AutoscaleBrackets.cursorPair_next 37
    rw [h37] at h
    norm_num at h
    exact h
  have h39 : AutoscaleBrackets.cursorPair 39 = (102334155,165580141) := by
    have h := AutoscaleBrackets.cursorPair_next 38
    rw [h38] at h
    norm_num at h
    exact h
  have h40 : AutoscaleBrackets.cursorPair 40 = (165580141,267914296) := by
    have h := AutoscaleBrackets.cursorPair_next 39
    rw [h39] at h
    norm_num at h
    exact h
  have h41 : AutoscaleBrackets.cursorPair 41 = (267914296,433494437) := by
    have h := AutoscaleBrackets.cursorPair_next 40
    rw [h40] at h
    norm_num at h
    exact h
  have h42 : AutoscaleBrackets.cursorPair 42 = (433494437,701408733) := by
    have h := AutoscaleBrackets.cursorPair_next 41
    rw [h41] at h
    norm_num at h
    exact h
  have h43 : AutoscaleBrackets.cursorPair 43 = (701408733,1134903170) := by
    have h := AutoscaleBrackets.cursorPair_next 42
    rw [h42] at h
    norm_num at h
    exact h
  have h44 : AutoscaleBrackets.cursorPair 44 = (1134903170,1836311903) := by
    have h := AutoscaleBrackets.cursorPair_next 43
    rw [h43] at h
    norm_num at h
    exact h
  have h45 : AutoscaleBrackets.cursorPair 45 = (1836311903,2971215073) := by
    have h := AutoscaleBrackets.cursorPair_next 44
    rw [h44] at h
    norm_num at h
    exact h
  have h46 : AutoscaleBrackets.cursorPair 46 = (2971215073,4807526976) := by
    have h := AutoscaleBrackets.cursorPair_next 45
    rw [h45] at h
    norm_num at h
    exact h
  have h47 : AutoscaleBrackets.cursorPair 47 = (4807526976,7778742049) := by
    have h := AutoscaleBrackets.cursorPair_next 46
    rw [h46] at h
    norm_num at h
    exact h
  have h48 : AutoscaleBrackets.cursorPair 48 = (7778742049,12586269025) := by
    have h := AutoscaleBrackets.cursorPair_next 47
    rw [h47] at h
    norm_num at h
    exact h
  have h49 : AutoscaleBrackets.cursorPair 49 = (12586269025,20365011074) := by
    have h := AutoscaleBrackets.cursorPair_next 48
    rw [h48] at h
    norm_num at h
    exact h
  have h50 : AutoscaleBrackets.cursorPair 50 = (20365011074,32951280099) := by
    have h := AutoscaleBrackets.cursorPair_next 49
    rw [h49] at h
    norm_num at h
    exact h
  have h51 : AutoscaleBrackets.cursorPair 51 = (32951280099,53316291173) := by
    have h := AutoscaleBrackets.cursorPair_next 50
    rw [h50] at h
    norm_num at h
    exact h
  have h52 : AutoscaleBrackets.cursorPair 52 = (53316291173,86267571272) := by
    have h := AutoscaleBrackets.cursorPair_next 51
    rw [h51] at h
    norm_num at h
    exact h
  have h53 : AutoscaleBrackets.cursorPair 53 = (86267571272,139583862445) := by
    have h := AutoscaleBrackets.cursorPair_next 52
    rw [h52] at h
    norm_num at h
    exact h
  have h54 : AutoscaleBrackets.cursorPair 54 = (139583862445,225851433717) := by
    have h := AutoscaleBrackets.cursorPair_next 53
    rw [h53] at h
    norm_num at h
    exact h
  have h55 : AutoscaleBrackets.cursorPair 55 = (225851433717,365435296162) := by
    have h := AutoscaleBrackets.cursorPair_next 54
    rw [h54] at h
    norm_num at h
    exact h
  have h56 : AutoscaleBrackets.cursorPair 56 = (365435296162,591286729879) := by
    have h := AutoscaleBrackets.cursorPair_next 55
    rw [h55] at h
    norm_num at h
    exact h
  have h57 : AutoscaleBrackets.cursorPair 57 = (591286729879,956722026041) := by
    have h := AutoscaleBrackets.cursorPair_next 56
    rw [h56] at h
    norm_num at h
    exact h
  have h58 : AutoscaleBrackets.cursorPair 58 = (956722026041,1548008755920) := by
    have h := AutoscaleBrackets.cursorPair_next 57
    rw [h57] at h
    norm_num at h
    exact h
  have h59 : AutoscaleBrackets.cursorPair 59 = (1548008755920,2504730781961) := by
    have h := AutoscaleBrackets.cursorPair_next 58
    rw [h58] at h
    norm_num at h
    exact h
  have h60 : AutoscaleBrackets.cursorPair 60 = (2504730781961,4052739537881) := by
    have h := AutoscaleBrackets.cursorPair_next 59
    rw [h59] at h
    norm_num at h
    exact h
  have h61 : AutoscaleBrackets.cursorPair 61 = (4052739537881,6557470319842) := by
    have h := AutoscaleBrackets.cursorPair_next 60
    rw [h60] at h
    norm_num at h
    exact h
  have h62 : AutoscaleBrackets.cursorPair 62 = (6557470319842,10610209857723) := by
    have h := AutoscaleBrackets.cursorPair_next 61
    rw [h61] at h
    norm_num at h
    exact h
  have h63 : AutoscaleBrackets.cursorPair 63 = (10610209857723,17167680177565) := by
    have h := AutoscaleBrackets.cursorPair_next 62
    rw [h62] at h
    norm_num at h
    exact h
  have h64 : AutoscaleBrackets.cursorPair 64 = (17167680177565,27777890035288) := by
    have h := AutoscaleBrackets.cursorPair_next 63
    rw [h63] at h
    norm_num at h
    exact h
  have h65 : AutoscaleBrackets.cursorPair 65 = (27777890035288,44945570212853) := by
    have h := AutoscaleBrackets.cursorPair_next 64
    rw [h64] at h
    norm_num at h
    exact h
  have h66 : AutoscaleBrackets.cursorPair 66 = (44945570212853,72723460248141) := by
    have h := AutoscaleBrackets.cursorPair_next 65
    rw [h65] at h
    norm_num at h
    exact h
  have h67 : AutoscaleBrackets.cursorPair 67 = (72723460248141,117669030460994) := by
    have h := AutoscaleBrackets.cursorPair_next 66
    rw [h66] at h
    norm_num at h
    exact h
  have h68 : AutoscaleBrackets.cursorPair 68 = (117669030460994,190392490709135) := by
    have h := AutoscaleBrackets.cursorPair_next 67
    rw [h67] at h
    norm_num at h
    exact h
  have h69 : AutoscaleBrackets.cursorPair 69 = (190392490709135,308061521170129) := by
    have h := AutoscaleBrackets.cursorPair_next 68
    rw [h68] at h
    norm_num at h
    exact h
  have h70 : AutoscaleBrackets.cursorPair 70 = (308061521170129,498454011879264) := by
    have h := AutoscaleBrackets.cursorPair_next 69
    rw [h69] at h
    norm_num at h
    exact h
  have h71 : AutoscaleBrackets.cursorPair 71 = (498454011879264,806515533049393) := by
    have h := AutoscaleBrackets.cursorPair_next 70
    rw [h70] at h
    norm_num at h
    exact h
  have h72 : AutoscaleBrackets.cursorPair 72 = (806515533049393,1304969544928657) := by
    have h := AutoscaleBrackets.cursorPair_next 71
    rw [h71] at h
    norm_num at h
    exact h
  have h73 : AutoscaleBrackets.cursorPair 73 = (1304969544928657,2111485077978050) := by
    have h := AutoscaleBrackets.cursorPair_next 72
    rw [h72] at h
    norm_num at h
    exact h
  have h74 : AutoscaleBrackets.cursorPair 74 = (2111485077978050,3416454622906707) := by
    have h := AutoscaleBrackets.cursorPair_next 73
    rw [h73] at h
    norm_num at h
    exact h
  have h75 : AutoscaleBrackets.cursorPair 75 = (3416454622906707,5527939700884757) := by
    have h := AutoscaleBrackets.cursorPair_next 74
    rw [h74] at h
    norm_num at h
    exact h
  have h76 : AutoscaleBrackets.cursorPair 76 = (5527939700884757,8944394323791464) := by
    have h := AutoscaleBrackets.cursorPair_next 75
    rw [h75] at h
    norm_num at h
    exact h
  have h77 : AutoscaleBrackets.cursorPair 77 = (8944394323791464,14472334024676221) := by
    have h := AutoscaleBrackets.cursorPair_next 76
    rw [h76] at h
    norm_num at h
    exact h
  have h78 : AutoscaleBrackets.cursorPair 78 = (14472334024676221,23416728348467685) := by
    have h := AutoscaleBrackets.cursorPair_next 77
    rw [h77] at h
    norm_num at h
    exact h
  have h79 : AutoscaleBrackets.cursorPair 79 = (23416728348467685,37889062373143906) := by
    have h := AutoscaleBrackets.cursorPair_next 78
    rw [h78] at h
    norm_num at h
    exact h
  have h80 : AutoscaleBrackets.cursorPair 80 = (37889062373143906,61305790721611591) := by
    have h := AutoscaleBrackets.cursorPair_next 79
    rw [h79] at h
    norm_num at h
    exact h
  have h81 : AutoscaleBrackets.cursorPair 81 = (61305790721611591,99194853094755497) := by
    have h := AutoscaleBrackets.cursorPair_next 80
    rw [h80] at h
    norm_num at h
    exact h
  have h82 : AutoscaleBrackets.cursorPair 82 = (99194853094755497,160500643816367088) := by
    have h := AutoscaleBrackets.cursorPair_next 81
    rw [h81] at h
    norm_num at h
    exact h
  have h83 : AutoscaleBrackets.cursorPair 83 = (160500643816367088,259695496911122585) := by
    have h := AutoscaleBrackets.cursorPair_next 82
    rw [h82] at h
    norm_num at h
    exact h
  have h84 : AutoscaleBrackets.cursorPair 84 = (259695496911122585,420196140727489673) := by
    have h := AutoscaleBrackets.cursorPair_next 83
    rw [h83] at h
    norm_num at h
    exact h
  have h85 : AutoscaleBrackets.cursorPair 85 = (420196140727489673,679891637638612258) := by
    have h := AutoscaleBrackets.cursorPair_next 84
    rw [h84] at h
    norm_num at h
    exact h
  have h86 : AutoscaleBrackets.cursorPair 86 = (679891637638612258,1100087778366101931) := by
    have h := AutoscaleBrackets.cursorPair_next 85
    rw [h85] at h
    norm_num at h
    exact h
  have h87 : AutoscaleBrackets.cursorPair 87 = (1100087778366101931,1779979416004714189) := by
    have h := AutoscaleBrackets.cursorPair_next 86
    rw [h86] at h
    norm_num at h
    exact h
  have h88 : AutoscaleBrackets.cursorPair 88 = (1779979416004714189,2880067194370816120) := by
    have h := AutoscaleBrackets.cursorPair_next 87
    rw [h87] at h
    norm_num at h
    exact h
  have h89 : AutoscaleBrackets.cursorPair 89 = (2880067194370816120,4660046610375530309) := by
    have h := AutoscaleBrackets.cursorPair_next 88
    rw [h88] at h
    norm_num at h
    exact h
  have h90 : AutoscaleBrackets.cursorPair 90 = (4660046610375530309,7540113804746346429) := by
    have h := AutoscaleBrackets.cursorPair_next 89
    rw [h89] at h
    norm_num at h
    exact h
  have h91 : AutoscaleBrackets.cursorPair 91 = (7540113804746346429,12200160415121876738) := by
    have h := AutoscaleBrackets.cursorPair_next 90
    rw [h90] at h
    norm_num at h
    exact h
  have h92 : AutoscaleBrackets.cursorPair 92 = (12200160415121876738,19740274219868223167) := by
    have h := AutoscaleBrackets.cursorPair_next 91
    rw [h91] at h
    norm_num at h
    exact h
  have h93 : AutoscaleBrackets.cursorPair 93 = (19740274219868223167,31940434634990099905) := by
    have h := AutoscaleBrackets.cursorPair_next 92
    rw [h92] at h
    norm_num at h
    exact h
  have h94 : AutoscaleBrackets.cursorPair 94 = (31940434634990099905,51680708854858323072) := by
    have h := AutoscaleBrackets.cursorPair_next 93
    rw [h93] at h
    norm_num at h
    exact h
  have h95 : AutoscaleBrackets.cursorPair 95 = (51680708854858323072,83621143489848422977) := by
    have h := AutoscaleBrackets.cursorPair_next 94
    rw [h94] at h
    norm_num at h
    exact h
  have h96 : AutoscaleBrackets.cursorPair 96 = (83621143489848422977,135301852344706746049) := by
    have h := AutoscaleBrackets.cursorPair_next 95
    rw [h95] at h
    norm_num at h
    exact h
  have h97 : AutoscaleBrackets.cursorPair 97 = (135301852344706746049,218922995834555169026) := by
    have h := AutoscaleBrackets.cursorPair_next 96
    rw [h96] at h
    norm_num at h
    exact h
  have h98 : AutoscaleBrackets.cursorPair 98 = (218922995834555169026,354224848179261915075) := by
    have h := AutoscaleBrackets.cursorPair_next 97
    rw [h97] at h
    norm_num at h
    exact h
  have h99 : AutoscaleBrackets.cursorPair 99 = (354224848179261915075,573147844013817084101) := by
    have h := AutoscaleBrackets.cursorPair_next 98
    rw [h98] at h
    norm_num at h
    exact h
  have h100 : AutoscaleBrackets.cursorPair 100 = (573147844013817084101,927372692193078999176) := by
    have h := AutoscaleBrackets.cursorPair_next 99
    rw [h99] at h
    norm_num at h
    exact h
  have h101 : AutoscaleBrackets.cursorPair 101 = (927372692193078999176,1500520536206896083277) := by
    have h := AutoscaleBrackets.cursorPair_next 100
    rw [h100] at h
    norm_num at h
    exact h
  exact ⟨h100,h101⟩

theorem autoscale_cell_computation :
    RadixCellSelection.first (lower .autoscale 100) scale = 1618033988749894848204586834365638117 ∧
    RadixCellSelection.last (upper .autoscale 100) scale = 1618033988749894848204586834365638117 := by
  norm_num [lower, upper, scale, RadixCellSelection.first, RadixCellSelection.last,
    AutoscaleBrackets.lowerQ, AutoscaleBrackets.upperQ, AutoscaleBrackets.ratioQ,
    autoscale_pairs_computation.1, autoscale_pairs_computation.2]

theorem selected_depth_stops (c : Channel) : Stops c scale (index c) := by
  cases c with
  | closure => exact closure_cell_computation.1.trans closure_cell_computation.2.symm
  | propagation => exact propagation_cell_computation.1.trans propagation_cell_computation.2.symm
  | autoscale => exact autoscale_cell_computation.1.trans autoscale_cell_computation.2.symm

theorem prefix_is_regional_cell (c : Channel) :
    generatedPrefix c = RadixCellSelection.cell (value c) scale :=
  stopped_cell_correct c scale (index c) (by norm_num [scale]) (selected_depth_stops c)

theorem generated_prefix_evaluates :
    generatedPrefix .closure = 3141592653589793238462643383279502884 ∧
    generatedPrefix .propagation = 2718281828459045235360287471352662497 ∧
    generatedPrefix .autoscale = 1618033988749894848204586834365638117 :=
  ⟨closure_cell_computation.1, propagation_cell_computation.1, autoscale_cell_computation.1⟩

def regionalBlock (c : Channel) (i : Fin 12) : Int :=
  generatedPrefix c / (1000 : Int) ^ (11 - i.val) % 1000

theorem regional_block_is_cell_readout (c : Channel) (i : Fin 12) :
    regionalBlock c i =
      RadixCellSelection.cell (value c) scale / (1000 : Int) ^ (11-i.val) % 1000 := by
  rw [regionalBlock, prefix_is_regional_cell]

def generatedPrecarry (l : Ledger) (i : Fin 12) : Int :=
  regionalBlock .closure i + regionalBlock .propagation i -
    regionalBlock .autoscale i - ((register l).digits[i.val]! : Int)

theorem generated_precarry_evaluates (l : Ledger)
    (hl : (register l).digits = [234,543,140,729,659,824,621,58,914,794,146,601]) :
    generatedPrecarry l = preCarry := by
  funext i
  unfold generatedPrecarry regionalBlock
  rw [hl, generated_prefix_evaluates.1, generated_prefix_evaluates.2.1,
    generated_prefix_evaluates.2.2]
  fin_cases i <;> norm_num [preCarry]

theorem generated_negative_support (l : Ledger)
    (hl : (register l).digits = [234,543,140,729,659,824,621,58,914,794,146,601]) :
    (Finset.univ.filter fun i : Fin 12 => generatedPrecarry l i < 0) = alphaHexad := by
  rw [generated_precarry_evaluates l hl]
  exact signed_support_exact

/-- Unlike the earlier declared-vector cut, this incidence is evaluated on
the pre-carry vector actually composed from the generated regional blocks. -/
def originFromPrecarry (l : Ledger) : Finset (Fin 12) :=
  (hexadSupport ∩ autoscaleSupport) \
    ((Finset.univ.filter fun i : Fin 12 => generatedPrecarry l i < 0) ∪ appSupport)

theorem origin_from_precarry_eq (l : Ledger)
    (hl : (register l).digits = [234,543,140,729,659,824,621,58,914,794,146,601]) :
    originFromPrecarry l = originSupport := by
  unfold originFromPrecarry
  rw [generated_negative_support l hl]
  rfl

theorem origin_from_precarry_nonempty (l : Ledger)
    (hl : (register l).digits = [234,543,140,729,659,824,621,58,914,794,146,601]) :
    (originFromPrecarry l).Nonempty := by
  rw [origin_from_precarry_eq l hl, origin_support_exact]
  simp

def generatedOrigin (l : Ledger)
    (hl : (register l).digits = [234,543,140,729,659,824,621,58,914,794,146,601]) : Fin 12 :=
  (originFromPrecarry l).min' (origin_from_precarry_nonempty l hl)

theorem generated_origin_eq (l : Ledger)
    (hl : (register l).digits = [234,543,140,729,659,824,621,58,914,794,146,601]) :
    generatedOrigin l hl = origin := by
  have h : generatedOrigin l hl ∈ originFromPrecarry l :=
    Finset.min'_mem _ (origin_from_precarry_nonempty l hl)
  rw [origin_from_precarry_eq l hl, origin_support_exact] at h
  rw [Finset.mem_singleton.mp h, origin_eq_zero]

def generatedRadial (l : Ledger)
    (hl : (register l).digits = [234,543,140,729,659,824,621,58,914,794,146,601]) : Space 12 :=
  radial (marked (generatedOrigin l hl))

theorem generated_radial_eq (l : Ledger)
    (hl : (register l).digits = [234,543,140,729,659,824,621,58,914,794,146,601]) :
    generatedRadial l hl = selectedRadial := by
  unfold generatedRadial
  rw [generated_origin_eq l hl]
  rfl

theorem generated_precarry_lattice_properties (l : Ledger)
    (hl : (register l).digits = [234,543,140,729,659,824,621,58,914,794,146,601]) :
    pairing (generatedRadial l hl) (generatedRadial l hl) = 54 ∧
    Module.Finite ℤ (neighborSubgroup wittCode (generatedRadial l hl)) ∧
    Module.Free ℤ (neighborSubgroup wittCode (generatedRadial l hl)) ∧
    Module.finrank ℤ (neighborSubgroup wittCode (generatedRadial l hl)) = 24 ∧
    EvenNeighbor wittCode (generatedRadial l hl) ∧
    IntegralNeighbor wittCode (generatedRadial l hl) ∧
    integralDual (neighborSubgroup wittCode (generatedRadial l hl)) =
      neighbor wittCode (generatedRadial l hl) ∧
    (∀ x ∈ neighbor wittCode (generatedRadial l hl), x ≠ 0 → 4 ≤ pairing x x) ∧
    (∃ x ∈ neighbor wittCode (generatedRadial l hl), pairing x x = 4) := by
  rw [generated_radial_eq l hl]
  exact ⟨selected_radial_norm, selected_lattice_properties.1,
    selected_lattice_properties.2.1, selected_lattice_properties.2.2.1,
    selected_lattice_properties.2.2.2.2.2⟩

#print axioms closure_cell_computation
#print axioms propagation_cell_computation
#print axioms autoscale_pairs_computation
#print axioms autoscale_cell_computation
#print axioms selected_depth_stops
#print axioms prefix_is_regional_cell
#print axioms regional_block_is_cell_readout
#print axioms generated_precarry_evaluates
#print axioms generated_negative_support
#print axioms origin_from_precarry_eq
#print axioms generated_origin_eq
#print axioms generated_radial_eq
#print axioms generated_precarry_lattice_properties

end HMT.I.RegionalPrecarry
end
