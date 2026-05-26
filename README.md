# Network Automation Portfolio

A curated portfolio repo showing practical NetDevOps work across Cisco Ansible automation, Juniper PyEZ scripts, and Juniper Ansible/Jinja workflows.

The source material came from retired lab and automation folders. This public version is intentionally cleaned up: credentials are pulled from environment variables, lab IPs use documentation ranges, generated output is excluded, and scripts include guardrails around disruptive operations.

## Sections

| Section | Focus | Highlights |
| --- | --- | --- |
| `cisco-ansible-campus` | Cisco IOS campus lab automation | Show-command collection, config backup, access-switch baseline, security hardening |
| `juniper-automation/pyez` | Junos Python automation | Facts, RPCs, XPath, BGP validation, SCP, rescue config, shell access, config diff/rollback, commit confirmed, reboot/software guardrails |
| `juniper-automation/ansible` | Junos Ansible and Jinja | Facts, command execution, ISIS config rendering, optional commit-confirm deployment |

## Portfolio Story

This repo is designed to show range rather than one narrow workflow:

- Multi-vendor automation: Cisco IOS and Junos.
- Multiple automation styles: Ansible playbooks, Jinja templates, PyEZ Python scripts.
- Operational safety: dry-run defaults, check mode, commit confirmed, explicit confirmation flags.
- Public-safe hygiene: no real credentials, no raw device outputs, no private URLs, no public-routable lab IPs.

## Diagrams

Cisco campus Ansible workflow:

![Cisco campus Ansible topology](docs/cisco-campus-ansible-topology.png)

Juniper automation workflow:

![Juniper automation topology](docs/juniper-automation-topology.png)

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Cisco examples:

```bash
cd cisco-ansible-campus
ansible-playbook playbooks/collect_show_version.yml --check
ansible-playbook playbooks/campus_baseline.yml --check
```

Juniper Ansible examples:

```bash
cd juniper-automation/ansible
ansible-playbook playbooks/get_facts.yml --check
ansible-playbook playbooks/configure_isis_interfaces.yml
```

Juniper PyEZ examples:

```bash
cd juniper-automation/pyez
python show_version.py --host 198.51.100.11
python rpc_queries.py --host 198.51.100.11 interfaces --xpath './/physical-interface/name'
python config_workflow.py --host 198.51.100.11 --config ../ansible/artifacts/isis/core-a_isis_interfaces.conf
```

## Sanitization Notes

- All credentials are expected from environment variables or interactive prompts.
- Example device management IPs use `192.0.2.0/24` and `198.51.100.0/24`.
- Example routed links use `203.0.113.0/24`.
- Runtime artifacts are written under `artifacts/`, which is ignored by Git.
- Legacy `.retry`, raw command output, local logs, generated configs, and backup files were intentionally left out.
