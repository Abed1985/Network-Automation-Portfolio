import argparse
import csv
import re
from pathlib import Path


BLOCK_PATTERNS = {
    "address": re.compile(r"^config firewall address$", re.IGNORECASE),
    "policy": re.compile(r"^config firewall policy$", re.IGNORECASE),
}
EDIT_PATTERN = re.compile(r'^edit\s+"?(?P<name>.+?)"?$')
SET_PATTERN = re.compile(r"^set\s+(?P<key>\S+)\s+(?P<value>.*)$")


def parse_block(config_text, block_type):
    in_block = False
    current = None
    records = []
    keys = ["id" if block_type == "policy" else "name"]

    for raw_line in config_text.splitlines():
        line = raw_line.strip()
        if BLOCK_PATTERNS[block_type].match(line):
            in_block = True
            continue
        if in_block and line == "end":
            in_block = False
            continue
        if not in_block:
            continue
        edit_match = EDIT_PATTERN.match(line)
        if edit_match:
            current = {keys[0]: edit_match.group("name")}
            continue
        if line == "next" and current:
            records.append(current)
            current = None
            continue
        set_match = SET_PATTERN.match(line)
        if current is not None and set_match:
            key = set_match.group("key")
            value = set_match.group("value").strip().strip('"')
            current[key] = value
            if key not in keys:
                keys.append(key)

    return records, keys


def write_csv(path, records, keys):
    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(records)


def parse_args():
    parser = argparse.ArgumentParser(description="Export FortiGate address or policy config blocks to CSV.")
    parser.add_argument("input_file", help="FortiGate config file")
    parser.add_argument("--type", choices=BLOCK_PATTERNS, default="policy")
    parser.add_argument("--output", default="artifacts/fortigate_export.csv")
    return parser.parse_args()


def main():
    args = parse_args()
    config_text = Path(args.input_file).read_text(encoding="utf-8")
    records, keys = parse_block(config_text, args.type)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_csv(output_path, records, keys)
    print(f"Wrote {len(records)} {args.type} records to {output_path}")


if __name__ == "__main__":
    main()
