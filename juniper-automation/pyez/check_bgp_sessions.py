import argparse
import sys

from common import add_connection_args, open_device


def parse_args():
    parser = argparse.ArgumentParser(description="Validate Junos BGP peer state with PyEZ RPCs.")
    add_connection_args(parser)
    return parser.parse_args()


def main():
    args = parse_args()
    established = 0
    not_established = 0

    with open_device(args) as device:
        bgp_data = device.rpc.get_bgp_summary_information()
        for state in bgp_data.xpath("bgp-peers/peer-state"):
            if state.text == "Established":
                established += 1
            else:
                not_established += 1

    total = established + not_established
    print(f"BGP sessions established: {established}/{total}")
    if not_established:
        print("Warning: one or more BGP sessions are not established")
        sys.exit(1)


if __name__ == "__main__":
    main()
