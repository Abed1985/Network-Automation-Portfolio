import argparse
import csv
from collections import Counter
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Identify likely downstream switch/AP ports from MAC table density.")
    parser.add_argument("mac_table_csv", help="CSV containing device,port,mac_address columns")
    parser.add_argument("--threshold", type=int, default=3, help="Minimum MAC count per port")
    parser.add_argument("--output", default="artifacts/potential_downstream_ports.csv")
    return parser.parse_args()


def main():
    args = parse_args()
    counters = Counter()
    with open(args.mac_table_csv, newline="", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            device = row.get("device") or row.get("hostname") or "unknown-device"
            port = row.get("port") or row.get("interface") or row.get("destination_port")
            if port:
                counters[(device, port)] += 1

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=["device", "port", "mac_count", "classification"])
        writer.writeheader()
        for (device, port), count in sorted(counters.items()):
            if count >= args.threshold:
                writer.writerow({"device": device, "port": port, "mac_count": count, "classification": "possible-switch-or-ap"})
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
