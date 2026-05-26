import argparse
from lxml import etree

from common import add_connection_args, open_device


RPC_CHOICES = {
    "route": "get_route_information",
    "software": "get_software_information",
    "interfaces": "get_interface_information",
    "bgp-summary": "get_bgp_summary_information",
}


def parse_args():
    parser = argparse.ArgumentParser(description="Run common Junos RPC calls and print XML output.")
    add_connection_args(parser)
    parser.add_argument("rpc", choices=RPC_CHOICES, help="Friendly RPC name to execute")
    parser.add_argument("--table", default="inet.0", help="Route table used by the route RPC")
    parser.add_argument("--xpath", help="Optional XPath expression to extract selected nodes")
    return parser.parse_args()


def main():
    args = parse_args()
    with open_device(args) as device:
        rpc_name = RPC_CHOICES[args.rpc]
        rpc = getattr(device.rpc, rpc_name)
        response = rpc(table=args.table) if args.rpc == "route" else rpc()

    nodes = response.xpath(args.xpath) if args.xpath else [response]
    for node in nodes:
        print(etree.tostring(node, pretty_print=True, encoding="unicode"))


if __name__ == "__main__":
    main()
