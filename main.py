#!/usr/bin/env python3
"""Tell a Whole Story in 32 Characters — make.fun entry.

Writes one Wi-Fi network name (max 32 characters) to /output/entry.txt.
Stdlib only, no network, no dependencies.

Run: python3 main.py
"""

import os

LINE = "IChangedTheLocksNotTheWiFi"

MAX_CHARS = 32


def validate_entry(line: str) -> str:
    """Check the entry against the competition gate and return it unchanged.

    The gate accepts exactly one line of 1-32 UTF-8 characters, not
    whitespace-only. Fail loudly instead of shipping an entry the
    scorer would refuse.
    """
    if not line.strip():
        raise SystemExit("entry line is empty or whitespace-only")
    if "\n" in line or "\r" in line:
        raise SystemExit("entry line must be a single line")
    if not 1 <= len(line) <= MAX_CHARS:
        raise SystemExit(
            f"entry line is {len(line)} characters, must be 1-{MAX_CHARS}"
        )
    return line


def write_entry(line: str, out_dir: str) -> str:
    """Write the validated entry to entry.txt and return the path.

    Reads the file back after writing and refuses to report success
    unless the on-disk content matches the entry exactly, so a
    truncated or mangled write is caught here, not by the scorer.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != line:
        raise SystemExit(f"entry.txt mismatch: wrote {line!r}, read back {written!r}")
    return path


def main() -> None:
    line = validate_entry(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(line, out_dir)
    print(f"Wrote {len(line)} characters to {path}")


if __name__ == "__main__":
    main()
