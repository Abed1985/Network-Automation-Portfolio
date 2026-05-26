import argparse
import json
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Build a simple topology edge list from parsed CDP/LLDP JSON files.")
    parser.add_argument("input_dir", help="Directory containing per-device JSON discovery files")
    parser.add_argument("--output", default="artifacts/topology_edges.csv", help="CSV output path")
    return parser.parse_args()


def neighbor_name(record):
    for key in ["neighbor", "neighbor_name", "neighbor_id", "destination_host", "remote_system_name"]:
        if key in record and record[key]:
            return record[key]
    return "unknown-neighbor"


def local_interface(record):
    for key in ["local_interface", "local_port", "interface", "local_intf"]:
        if key in record and record[key]:
            return record[key]
    return "unknown-interface"


def remote_interface(record):
    for key in ["neighbor_interface", "remote_port", "remote_interface", "port_id"]:
        if key in record and record[key]:
            return record[key]
    return "unknown-interface"


def main():
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows = ["source,source_interface,neighbor,neighbor_interface"]
    for json_file in sorted(input_dir.glob("*.json")):
        source = json_file.stem
        records = json.loads(json_file.read_text(encoding="utf-8"))
        for record in records:
            rows.append(
                f"{source},{local_interface(record)},{neighbor_name(record)},{remote_interface(record)}"
            )

    output_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
