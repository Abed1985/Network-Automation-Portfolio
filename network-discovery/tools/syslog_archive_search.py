import argparse
import gzip
import re
from pathlib import Path


def iter_lines(path):
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as log_file:
            yield from log_file
    else:
        with path.open(encoding="utf-8", errors="replace") as log_file:
            yield from log_file


def parse_args():
    parser = argparse.ArgumentParser(description="Search local syslog archives for lines matching all supplied patterns.")
    parser.add_argument("log_dir", help="Directory containing .log, .txt, or .gz files")
    parser.add_argument("patterns", nargs="+", help="Regex patterns; all must match")
    parser.add_argument("--output", default="artifacts/syslog_matches.log")
    return parser.parse_args()


def main():
    args = parse_args()
    compiled = [re.compile(pattern, re.IGNORECASE) for pattern in args.patterns]
    matches = []
    for path in sorted(Path(args.log_dir).glob("*")):
        if path.is_dir() or path.suffix not in [".log", ".txt", ".gz"]:
            continue
        for line_number, line in enumerate(iter_lines(path), start=1):
            if all(pattern.search(line) for pattern in compiled):
                matches.append(f"{path.name}:{line_number}:{line}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(matches), encoding="utf-8")
    print(f"Wrote {len(matches)} matching lines to {output_path}")


if __name__ == "__main__":
    main()
