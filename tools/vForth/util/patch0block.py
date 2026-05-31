#!/usr/bin/env python3
"""
patch0block.py  --  overwrite the first 512 bytes of !Blocks-64.bin
                    with the content of version/0BLOCK.txt

Usage:
    python util/patch0block.py
Run from the vForth project root (tools/vForth).
"""

import sys
import os

SRC  = os.path.join("version", "0BLOCK.txt")
DST  = "!Blocks-64.bin"
SIZE = 512

src_size = os.path.getsize(SRC)
if src_size != SIZE:
    sys.exit(f"ERROR: {SRC} is {src_size} bytes, expected {SIZE}")

dst_size = os.path.getsize(DST)
if dst_size < SIZE:
    sys.exit(f"ERROR: {DST} is only {dst_size} bytes, too small")

with open(SRC, "rb") as f:
    data = f.read(SIZE)

with open(DST, "r+b") as f:
    f.seek(0)
    f.write(data)

print(f"OK: wrote {SIZE} bytes from {SRC} into {DST} at offset 0")
