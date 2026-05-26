import argparse

from jnpr.junos.utils.start_shell import StartShell

from common import add_connection_args, open_device


SAFE_EXAMPLES = [
    "ls -al /var/tmp",
    "df -h",
    "cli -c 'show system storage'",
]


def parse_args():
    parser = argparse.ArgumentParser(description="Run a Junos shell command through PyEZ StartShell.")
    add_connection_args(parser)
    parser.add_argument("command", help="Shell command to run")
    parser.add_argument("--confirm", action="store_true", help="Run the shell command")
    return parser.parse_args()


def main():
    args = parse_args()
    if not args.confirm:
        print("Dry run only: add --confirm to run the shell command")
        print("Safe example commands:")
        for example in SAFE_EXAMPLES:
            print(f"  {example}")
        return

    with open_device(args) as device:
        with StartShell(device) as shell:
            ok, output = shell.run(args.command)
    print(f"Success: {ok}")
    print(output)


if __name__ == "__main__":
    main()
