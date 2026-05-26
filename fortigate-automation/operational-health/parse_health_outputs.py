import argparse
import csv
import re
from pathlib import Path


IPSEC_PATTERN = re.compile(r"'(?P<tunnel>[^']+)'\s+\S+\s+selectors\(total,up\):\s+(?P<selectors>\d+/\d+)")


def parse_bgp(text, vdom="root"):
    rows = []
    for line in text.splitlines():
        parts = line.split()
        if not parts:
            continue
        if re.match(r"^\d+\.\d+\.\d+\.\d+$", parts[0]):
            state = parts[-1]
            rows.append({"vdom": vdom, "neighbor": parts[0], "status": "up" if state.isdigit() else "down", "state": state})
    return rows


def parse_ipsec(text, vdom="root"):
    rows = []
    for line in text.splitlines():
        match = IPSEC_PATTERN.search(line)
        if match:
            selectors = match.group("selectors")
            rows.append({"vdom": vdom, "tunnel": match.group("tunnel"), "status": "up" if selectors == "1/1" else "down", "selectors": selectors})
    return rows


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args():
    parser = argparse.ArgumentParser(description="Parse saved FortiGate BGP or IPsec command output into CSV.")
    parser.add_argument("input_file")
    parser.add_argument("--type", choices=["bgp", "ipsec"], required=True)
    parser.add_argument("--vdom", default="root")
    parser.add_argument("--output", default="artifacts/fortigate_health.csv")
    return parser.parse_args()


def main():
    args = parse_args()
    text = Path(args.input_file).read_text(encoding="utf-8")
    if args.type == "bgp":
        rows = parse_bgp(text, args.vdom)
        write_csv(Path(args.output), rows, ["vdom", "neighbor", "status", "state"])
    else:
        rows = parse_ipsec(text, args.vdom)
        write_csv(Path(args.output), rows, ["vdom", "tunnel", "status", "selectors"])
    print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
