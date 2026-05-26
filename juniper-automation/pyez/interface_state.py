import argparse

from jnpr.junos.utils.config import Config

from common import add_connection_args, open_device


def parse_args():
    parser = argparse.ArgumentParser(description="Enable or disable a Junos interface with a commit check.")
    add_connection_args(parser)
    parser.add_argument("interface", help="Interface name, for example ge-0/0/1")
    parser.add_argument("state", choices=["enable", "disable"], help="Desired interface state")
    parser.add_argument("--commit", action="store_true", help="Commit the change; otherwise dry-run and rollback")
    return parser.parse_args()


def main():
    args = parse_args()
    command = f"delete interfaces {args.interface} disable" if args.state == "enable" else f"set interfaces {args.interface} disable"

    with open_device(args) as device:
        with Config(device, mode="exclusive") as config:
            config.load(command, format="set")
            config.pdiff()
            config.commit_check()
            if args.commit:
                config.commit(comment=f"{args.state} {args.interface} via PyEZ automation")
                print("Configuration committed")
            else:
                config.rollback()
                print("Dry run only: candidate configuration rolled back")


if __name__ == "__main__":
    main()
