# Standalone bundle reproduction check

Archive checked: `artifacts/user_provider_game/20260906/reproducible_bundle.zip`.
SHA-256: `177bef4f67e732543b661e8c6967b0531f9f2fb796e9e27bcccd2caa98115762`.
The archive contains 101 manifest-listed files plus its manifest; every listed file matched its original source SHA-256.

The archive was extracted into a fresh directory outside the repository. No source files were copied into that directory after extraction.

1. Ran the three new-model test files with Python 3.12.13 and `requirements-user-game-20260906.txt`: **14 passed in 1.27 seconds**.
2. Built the manuscript with `latexmk -pdf`, using only the extracted TeX, tables, figures, and bibliography: **13 pages**, exit code 0.
3. Checked the final extracted-build log: no overfull/underfull boxes, undefined references, missing characters, or warnings.
4. Rendered both the delivered PDF and freshly compiled PDF at the same resolution: **all 13 pages had identical pixel hashes**. PDF container hashes can differ because compilation metadata changes; this check compares the actual page rendering.

The full 50,625-pair numerical replay was already performed on the pinned experiment and source files; it was not repeated a third time during this archive-extraction check. The extracted tests verify that the included source hashes and numerical replay certificate match those results. The package reproduces the new finite normalized-task model, not the full historical project or a real market.
