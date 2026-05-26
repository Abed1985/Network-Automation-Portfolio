import argparse
import os
from getpass import getpass

from netmiko import ConnectHandler


SUPPORTED_TYPES = ["cisco_ios", "cisco_nxos", "hp_procurve", "juniper_junos"]


def parse_args():
    parser = argparse.ArgumentParser(description="Push command sets to one or more devices with Netmiko.")
    parser.add_argument("--hosts", required=True, help="Comma-separated host list")
    parser.add_argument("--device-type", default="cisco_ios", choices=SUPPORTED_TYPES)
    parser.add_argument("--username", default=os.getenv("LAB_ANSIBLE_USER"))
    parser.add_argument("--commands", help="Comma-separated commands")
    parser.add_argument("--commands-file", help="File containing commands")
    parser.add_argument("--confirm", action="store_true", help="Actually send commands")
    return parser.parse_args()


def command_list(args):
    if args.commands_file:
        with open(args.commands_file, encoding="utf-8") as command_file:
            return [line.strip() for line in command_file if line.strip()]
    if args.commands:
        return [command.strip() for command in args.commands.split(",") if command.strip()]
    raise SystemExit("Provide --commands or --commands-file")


def main():
    args = parse_args()
    username = args.username or input("Username: ")
    password = os.getenv("LAB_ANSIBLE_PASSWORD") or getpass("Password: ")
    commands = command_list(args)

    for host in [item.strip() for item in args.hosts.split(",") if item.strip()]:
        if not args.confirm:
            print(f"DRY RUN: would send {len(commands)} commands to {host} as {args.device_type}")
            continue
        session = ConnectHandler(device_type=args.device_type, host=host, username=username, password=password)
        output = session.send_config_set(commands)
        session.disconnect()
        print(f"{host}:\n{output}")


if __name__ == "__main__":
    main()
