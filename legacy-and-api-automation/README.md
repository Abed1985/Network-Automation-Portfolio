# Legacy and API Automation

This section curates useful patterns from older one-off scripts in `my-bit-codes`: Meraki Dashboard reporting, ScreenOS/SSG SSH automation, CSV-driven onboarding, Netmiko command pushes, and NAPALM operational reporting.

The original folders contain useful ideas, but also raw customer exports, generated files, embedded credentials, public IPs, and vendored third-party projects. This public version keeps the reusable techniques and removes those artifacts.

## What It Demonstrates

- Meraki Dashboard API reporting with environment-based credentials.
- Legacy ScreenOS/SSG command automation over SSH with Paramiko.
- CSV-to-Ansible-inventory rendering for onboarding batches.
- Multi-vendor config pushes with Netmiko, guarded by dry-run defaults.
- Interface status reporting with NAPALM.
- Offline remediation logic for IOS local-user cleanup and SONiC TACACS config synchronization.

## Examples

### Meraki Uplink Report

```bash
cd legacy-and-api-automation/meraki
export MERAKI_API_KEY='replace-in-lab'
export MERAKI_ORG_ID='replace-in-lab'
python meraki_uplink_report.py --output-prefix demo-org
```

### ScreenOS/SSG Command Push

```bash
cd legacy-and-api-automation/screenos
export SCREENOS_PASSWORD='replace-in-lab'
python screenos_config_push.py --devices sample_screenos_devices.csv --commands sample_screenos_commands.txt
python screenos_config_push.py --devices sample_screenos_devices.csv --commands sample_screenos_commands.txt --confirm
```

The script uses `RejectPolicy` for SSH host keys and defaults to dry-run mode. Add `--confirm` only in a lab or approved migration window.

### CSV Inventory Rendering

```bash
cd legacy-and-api-automation/onboarding
python csv_to_inventory.py sample_devices.csv --output artifacts/generated_inventory.yml
```

### Netmiko Config Push

```bash
cd legacy-and-api-automation/netmiko_napalm
export LAB_ANSIBLE_USER=netops
export LAB_ANSIBLE_PASSWORD='replace-in-lab'
python netmiko_config_push.py --hosts 192.0.2.31 --device-type cisco_ios --commands 'logging buffered 64000,service timestamps log datetime msec'
python netmiko_config_push.py --hosts 192.0.2.31 --device-type cisco_ios --commands 'logging buffered 64000' --confirm
```

### NAPALM Interface Report

```bash
cd legacy-and-api-automation/netmiko_napalm
export LAB_ANSIBLE_USER=netops
export LAB_ANSIBLE_PASSWORD='replace-in-lab'
python napalm_interface_report.py --hosts 192.0.2.31,192.0.2.32 --driver ios
```

### Remediation Logic

Generate IOS cleanup commands when a candidate config moves a user from `password` to `secret`:

```bash
cd legacy-and-api-automation/remediation
python ios_local_user_cleanup.py \
	--candidate sample_candidate_users.cfg \
	--running sample_running_users.cfg \
	--output artifacts/ios_user_cleanup.txt
```

Synchronize a SONiC `tacacs.json` passkey from sanitized `show tacacs` output:

```bash
python sonic_tacacs_sync.py \
	--show-tacacs sample_show_tacacs.txt \
	--json sample_tacacs.json \
	--output artifacts/tacacs_updated.json
```

## Sanitization Notes

- No original Meraki CSV exports are included.
- No ScreenOS/SSG device lists, outputs, or credentials are included.
- No legacy Telnet credential stores are included.
- No raw customer config files, videos, logs, or vendored third-party source trees are included.
- All example IPs use documentation ranges.
- Remediation examples operate on local sample files by default and do not connect to devices.
