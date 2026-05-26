import argparse
import csv
from pathlib import Path

import yaml


def parse_args():
    parser = argparse.ArgumentParser(description="Render an Ansible inventory from a device CSV.")
    parser.add_argument("csv_file", help="CSV with columns name,host,platform,group")
    parser.add_argument("--output", default="artifacts/generated_inventory.yml")
    return parser.parse_args()


def main():
    args = parse_args()
    inventory = {"all": {"children": {}}}
    with open(args.csv_file, newline="", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            group = row.get("group") or "network_devices"
            children = inventory["all"]["children"]
            children.setdefault(group, {"hosts": {}})
            children[group]["hosts"][row["name"]] = {
                "ansible_host": row["host"],
                "platform": row.get("platform", "unknown"),
            }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(yaml.safe_dump(inventory, sort_keys=False), encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
