# Cisco Ansible Campus Automation

This section contains sanitized Ansible examples for a Cisco IOS campus lab. It is based on GNS3-style network automation workflows: collect operational state, back up configuration, and apply a repeatable access-switch baseline.

## What It Demonstrates

- Inventory design for core and access device groups.
- Environment-sourced credentials instead of committed passwords.
- Operational collection with `cisco.ios.ios_command`.
- Configuration management with `cisco.ios.ios_config` and `cisco.ios.ios_vlans`.
- Campus hardening patterns: Rapid PVST, UDLD, DHCP snooping, ARP inspection, port security, BPDU guard, and IPv6 RA guard.

## Demo Topology

![Cisco campus Ansible topology](../docs/cisco-campus-ansible-topology.png)

## Run Examples

```bash
cd cisco-ansible-campus
export LAB_ANSIBLE_USER=netops
export LAB_ANSIBLE_PASSWORD='example-password'
export LAB_ENABLE_PASSWORD='example-enable-password'
ansible-playbook playbooks/collect_show_version.yml
ansible-playbook playbooks/collect_running_config.yml
ansible-playbook playbooks/campus_baseline.yml --check
```

The inventory uses documentation-range IPs from `192.0.2.0/24`; replace them only in your local lab inventory.
