# Project execution notes

### WSL temporary directory

- Trigger: `TEMP` or `TMP` resolves to a Windows-mounted path under `/mnt/c`.
- Risk: long multiprocessing runs and pytest capture can emit WSL `p9handler` errors or lose temporary files.
- Rule: run experiments, tests, and figure builds with `TMPDIR=/tmp TEMP=/tmp TMP=/tmp`.
- Verification: confirm generated caches and pytest temporary paths are under `/tmp`.

