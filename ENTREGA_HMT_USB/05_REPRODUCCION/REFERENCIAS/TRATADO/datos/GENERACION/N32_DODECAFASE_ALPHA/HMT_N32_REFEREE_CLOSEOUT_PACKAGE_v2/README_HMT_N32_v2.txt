HMT N32 (Referee Closeout) - Package v2
======================================

This package bundles:
  (A) N32 referee closure (ILP uniqueness for K_R12 + frozen seeds/routes + definition vs verification)
  (B) N32 addendum: upstream U12/U6 generator from APP/TPK + gauge-module scan + internal filtering report

Files
-----
A) Referee closure
  - ventana_HMT_N32_referee_closeout.tex / .pdf
  - hmt_n32_referee_closure.py
  - HMT_N32_ILP_model.lp
  - HMT_N32_certificate.json

B) Upstream U12 + gauge canonicity
  - ventana_HMT_N32_upstream_U12_gauge_canonicity.tex / .pdf
  - hmt_n32_upstream_u12_gauge_scan.py
  - n32_u6_seed_table.csv
  - n32_uid_representative_seed.csv
  - n32_variant_scan.json
  - HMT_N32_UPSTREAM_U12_CERTIFICATE.json

How to reproduce (suggested)
----------------------------
1) Upstream scan:
   python hmt_n32_upstream_u12_gauge_scan.py
   This rewrites the CSV/JSON outputs and the upstream certificate.

2) Referee closure:
   python hmt_n32_referee_closure.py
   This prints (and/or writes) the ILP/uniqueness certificate information.

3) Verify integrity (sha256):
   sha256sum -c HMT_N32_PACKAGE_MANIFEST_v2.sha256

Notes
-----
- All computations are alpha-free: alpha is only used (if at all) in *verification* scripts outside this package.
- The upstream scan enumerates all seeds in (Z_9^2 x D_4)^2 (104,976 seeds).
