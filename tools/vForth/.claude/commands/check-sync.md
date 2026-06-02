---
description: Check which inc/ and lib/ files are out of sync with SD/tools/vForth/ (read-only audit).
---

Audit synchronization between the root inc/ and lib/ directories and their copies
under SD/tools/vForth/. This command is read-only -- it never copies files.

Steps:
1. For every file in inc/:
   - Check if SD/tools/vForth/inc/<filename> exists.
   - If missing: mark MISSING.
   - If present but root file is newer (by timestamp or size difference): mark OUTDATED.
   - If identical (same size, root not newer): mark OK.

2. For every file in lib/ (skip binary files: *.bin):
   - Same check against SD/tools/vForth/lib/<filename>.

3. Also check the reverse: files present in SD/tools/vForth/inc/ or SD/tools/vForth/lib/
   but absent from the root directories. Mark these as ORPHAN (may be safe to delete
   from SD/).

4. Print a summary:
   - List all MISSING files.
   - List all OUTDATED files.
   - List all ORPHAN files (if any).
   - Report the count of OK files (do not list them individually).
   - If everything is in sync, print: "All files synchronized."

5. Do NOT copy any files. To apply corrections, use /sd-sync.