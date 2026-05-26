import argparse
import os
from getpass import getpass
from pathlib import Path

from netmiko import ConnectHandler


COMMANDS = [
    "diagnose sys vd list | grep name=",
    "get router info bgp summary",
    "get vpn ipsec tunnel summary",
]


def parse_args():
    parser = argparse.ArgumentParser(description="Collect FortiGate VDOM, BGP, and IPsec health commands with Netmiko.")
    parser.add_argument("--host", required=True, help="FortiGate hostname or management IP")
    parser.add_argument("--username", default=os.getenv("FORTIGATE_USER"))
    parser.add_argument("--device-type", default="fortinet")
    parser.add_argument("--output-dir", default="artifacts/fortigate-health")
    parser.add_argument("--confirm", action="store_true", help="Actually connect to the device")
    return parser.parse_args()


def main():
    args = parse_args()
    username = args.username or input("Username: ")
    password = os.getenv("FORTIGATE_PASSWORD") or getpass("Password: ")
    output_dir = Path(args.output_dir)

    if not args.confirm:
        print(f"DRY RUN: would collect {len(COMMANDS)} commands from {args.host}")
        return

    connection = ConnectHandler(device_type=args.device_type, host=args.host, username=username, password=password)
    output_dir.mkdir(parents=True, exist_ok=True)
    for command in COMMANDS:
        output = connection.send_command_timing(command)
        safe_name = command.replace(" ", "_").replace("/", "_").replace("|", "pipe")
        path = output_dir / f"{args.host}-{safe_name}.txt"
        path.write_text(output, encoding="utf-8")
        print(f"Wrote {path}")
    connection.disconnect()


if __name__ == "__main__":
    main()
