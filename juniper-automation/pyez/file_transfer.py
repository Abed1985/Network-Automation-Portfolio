import argparse

from jnpr.junos.utils.scp import SCP

from common import add_connection_args, open_device


def parse_args():
    parser = argparse.ArgumentParser(description="Copy files to or from a Junos device with PyEZ SCP.")
    add_connection_args(parser)
    parser.add_argument("direction", choices=["put", "get"], help="Transfer direction")
    parser.add_argument("source", help="Local source for put, remote source for get")
    parser.add_argument("destination", help="Remote destination for put, local destination for get")
    parser.add_argument("--confirm", action="store_true", help="Perform the transfer")
    return parser.parse_args()


def main():
    args = parse_args()
    if not args.confirm:
        print(f"Dry run only: would {args.direction} {args.source} to {args.destination}")
        return

    with open_device(args) as device:
        with SCP(device, progress=True) as scp:
            if args.direction == "put":
                scp.put(args.source, remote_path=args.destination)
            else:
                scp.get(args.source, local_path=args.destination)
    print("Transfer completed")


if __name__ == "__main__":
    main()
