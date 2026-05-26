# PyEZ Recipe Gallery

These scripts turn the original Juniper lab snippets into reusable portfolio examples. The point is to show PyEZ breadth while keeping the public repo clean, parameterized, and safe.

## Recipes

| Script | Capability Shown | Legacy Script Ideas Represented |
| --- | --- | --- |
| `show_version.py` | Device facts and software inventory | `show_version.py`, `juniper_facts.py` |
| `check_bgp_sessions.py` | RPC parsing and health-check exit codes | `check_bgp.py` |
| `rpc_queries.py` | Direct Junos RPC calls, XML output, optional XPath extraction | `junos_pyez_rpc.py`, `active_config.py`, `xpath_config.py` |
| `config_workflow.py` | Load config, print diff, rollback, commit confirmed, sync commit | `load_config.py`, `load_config_set.py`, `load_config_text.py`, `compare_config.py`, `commit_check.py`, `commit_confirm.py`, `commit_comment.py`, `commit_sync.py`, `rollback_config.py` |
| `interface_state.py` | Small targeted config changes with commit check | `disable_int.py`, `enable_int.py` |
| `rescue_config.py` | Save, inspect, reload, or delete rescue configuration | `rescue_save.py`, `rollback_rescue.py` |
| `file_transfer.py` | SCP upload/download with PyEZ | `copy_junos.py`, `copy_junos_messages.py` |
| `shell_command.py` | StartShell operational checks | `junos_unix_shell.py`, `junos_cli.py`, `verify_image_junos.py` |
| `reboot_device.py` | Guarded immediate or scheduled reboot | `junos_rebootnow.py`, `junos_rebootlater.py` |
| `software_install.py` | Validated software install and optional reboot | `junos_sw_install.py` |

## Safety Model

- Credentials come from `JUNOS_USER` / `JUNOS_PASSWORD` or interactive prompts.
- Destructive or disruptive actions require explicit flags such as `--commit`, `--confirm`, or `--reboot`.
- Config workflows print diffs and roll back by default.
- Reboot, shell, SCP, rescue, and software workflows default to dry-run messaging.

## Example Usage

```bash
export JUNOS_USER=netops
export JUNOS_PASSWORD='example-password'

python show_version.py --host 198.51.100.11
python rpc_queries.py --host 198.51.100.11 route --table inet.0 --xpath './/rt-entry/nh/to'
python check_bgp_sessions.py --host 198.51.100.11
python interface_state.py --host 198.51.100.11 ge-0/0/1 disable
python config_workflow.py --host 198.51.100.11 --config ../ansible/artifacts/isis/core-a_isis_interfaces.conf
python rescue_config.py --host 198.51.100.11 get
python file_transfer.py --host 198.51.100.11 get /var/log/messages ./artifacts/logs --confirm
python shell_command.py --host 198.51.100.11 "cli -c 'show system storage'" --confirm
```

Use documentation-range IPs in examples. Replace them only in a local lab inventory or local command line.
