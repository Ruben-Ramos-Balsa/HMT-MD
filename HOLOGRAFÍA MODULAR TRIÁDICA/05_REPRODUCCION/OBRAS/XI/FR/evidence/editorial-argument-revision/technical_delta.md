# Documentary builder delta

The mathematical code and Lean statements are retained. Packaging and verification
now ignore macOS Finder `.DS_Store` metadata at every level, both in the inventory
and in the isolated staging copy. Previously the inventory included
`output/.DS_Store` while the closed reconstruction deliberately omitted the output
directory, producing a spurious missing-file failure. No scientific input is
excluded by this correction. The current sealed verification remains authoritative
only when its manifest hash matches the package.

The English structural-fidelity reader uses the paired Spanish argument revision;
the original reference is preserved separately. The manifest edition identifiers
refer to 15 September 2026; the established builder status identifiers and PDF
basenames remain stable for compatibility and do not identify the edition alone.
