import argparse
import csv
import os
import time
from getpass import getpass
from pathlib import Path

import paramiko


def parse_args():
    parser = argparse.ArgumentParser(description="Push command files to legacy ScreenOS/SSG devices over SSH.")
    parser.add_argument("--devices", required=True, help="CSV with columns name,host,username")
    parser.add_argument("--commands", required=True, help="Command file to send line by line")
    parser.add_argument("--password-env", default="SCREENOS_PASSWORD", help="Environment variable containing device password")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between commands")
    parser.add_argument("--confirm", action="store_true", help="Actually connect and send commands")
    return parser.parse_args()


def load_devices(path):
    with open(path, newline="", encoding="utf-8") as csv_file:
        yield from csv.DictReader(csv_file)


def send_commands(device, commands, password, delay):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    client.connect(device["host"], username=device["username"], password=password, look_for_keys=False)
    shell = client.invoke_shell()
    shell.send("\n")
    time.sleep(delay)
    for command in commands:
        shell.send(command.rstrip() + "\n")
        time.sleep(delay)
    output = shell.recv(65535).decode("utf-8", errors="replace")
    client.close()
    return output


def main():
    args = parse_args()
    commands = Path(args.commands).read_text(encoding="utf-8").splitlines()
    password = os.getenv(args.password_env) or getpass("Device password: ")

    for device in load_devices(args.devices):
        if not args.confirm:
            print(f"DRY RUN: would send {len(commands)} commands to {device['name']} ({device['host']})")
            continue
        output = send_commands(device, commands, password, args.delay)
        output_path = Path("artifacts/screenos") / f"{device['name']}.log"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
        print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
