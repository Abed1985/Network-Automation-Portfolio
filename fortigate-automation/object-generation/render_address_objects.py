import argparse
import csv
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def parse_args():
    parser = argparse.ArgumentParser(description="Render FortiGate address objects from CSV input.")
    parser.add_argument("--csv", default="sample_addresses.csv", help="CSV with name,subnet,comment columns")
    parser.add_argument("--template", default="address_objects.j2", help="Jinja2 template path")
    parser.add_argument("--output", default="artifacts/fortigate_address_objects.conf", help="Rendered FortiGate config output")
    return parser.parse_args()


def main():
    args = parse_args()
    csv_path = Path(args.csv)
    template_path = Path(args.template)
    output_path = Path(args.output)

    with csv_path.open(newline="", encoding="utf-8") as csv_file:
        addresses = list(csv.DictReader(csv_file))

    environment = Environment(loader=FileSystemLoader(str(template_path.parent or ".")), autoescape=False, trim_blocks=True, lstrip_blocks=True)
    template = environment.get_template(template_path.name)
    rendered = template.render(addresses=addresses)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
