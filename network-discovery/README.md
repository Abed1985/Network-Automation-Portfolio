# Network Discovery and Structured Parsing

This section is a sanitized version of Ansible playbooks originally used for LLDP/CDP/ARP collection, discovery-protocol enablement, and SNMP baseline pushes.

The public version keeps the reusable techniques and removes customer names, logs, raw configs, public IPs, SNMP secrets, and hardcoded device credentials.

## What It Demonstrates

- Structured CDP, LLDP, and ARP collection with `ansible.utils.cli_parse` and NTC TextFSM templates.
- Mixed-vendor discovery targets: Cisco IOS, Cisco NX-OS, and Huawei VRP examples.
- Discovery protocol enablement for Cisco IOS lab devices.
- SNMPv3 baseline configuration for IOS and NX-OS with ACL scoping.
- `no_log: true` on tasks that render SNMP secrets.
- Post-processing parsed neighbor JSON into a topology edge list.
- Enriching ARP tables with normalized MAC addresses, OUI values, and vendor names.
- Reachability reporting, SNMP sysDescr probing, archived syslog searching, and MAC table density checks.

## Playbooks

| Playbook | Purpose |
| --- | --- |
| `collect_cdp_structured.yml` | Parse Cisco CDP neighbors into JSON. |
| `collect_lldp_structured.yml` | Parse LLDP neighbors across Cisco/Huawei style targets. |
| `collect_arp_structured.yml` | Parse ARP tables into JSON. |
| `enable_cisco_discovery_protocols.yml` | Enable CDP and LLDP globally on Cisco IOS. |
| `configure_snmpv3_ios.yml` | Configure IOS SNMPv3 view/group/user plus ACL. |
| `configure_snmpv3_nxos.yml` | Configure NX-OS SNMPv3 user/group plus ACL. |

## Example Usage

```bash
cd network-discovery
export LAB_ANSIBLE_USER=netops
export LAB_ANSIBLE_PASSWORD='example-password'
export SNMPV3_AUTH_PASSWORD='replace-in-lab'
export SNMPV3_PRIV_PASSWORD='replace-in-lab'

ansible-playbook playbooks/collect_cdp_structured.yml
ansible-playbook playbooks/collect_lldp_structured.yml
ansible-playbook playbooks/collect_arp_structured.yml
ansible-playbook playbooks/enable_cisco_discovery_protocols.yml --check
ansible-playbook playbooks/configure_snmpv3_ios.yml --check
ansible-playbook playbooks/configure_snmpv3_nxos.yml --check
```

Build a simple topology edge list from collected neighbor JSON:

```bash
python parsers/build_topology_edges.py artifacts/lldp --output artifacts/topology_edges.csv
```

Enrich an ARP CSV with MAC vendor/OUI details:

```bash
python parsers/enrich_arp_vendors.py sample_arp.csv --output artifacts/arp_enriched.csv --offline
```

Remove `--offline` in a lab with Internet access to query `api.macvendors.com`; results are cached in `artifacts/oui_cache.csv`.

Run additional local discovery utilities:

```bash
python tools/reachability_report.py sample_devices.csv --output artifacts/reachability.csv
python tools/snmp_sysdescr_probe.py sample_devices.csv --dry-run --output artifacts/snmp_sysdescr.csv
python tools/switch_port_density.py sample_mac_table.csv --output artifacts/potential_downstream_ports.csv
python tools/syslog_archive_search.py artifacts/logs edge-router-1 DHCP --output artifacts/syslog_matches.log
```

## Sanitization Notes

- Inventory IPs use documentation ranges only.
- SNMP hosts use `192.0.2.200` and `192.0.2.201` examples.
- SNMPv3 auth/privacy values come from environment variables.
- Raw customer config exports, logs, and `.retry` files are intentionally excluded.
- ARP vendor enrichment uses sanitized sample IP/MAC data and keeps API lookups optional.
- Utilities migrated from the old `Network-Programing` repo use local sample files and documentation IP ranges only.
