import argparse
import re
from pathlib import Path


USERNAME_LINE = re.compile(r"^\s*username\s+(?P<user>\S+)\s+.*\s+(?P<kind>password|secret)(?:\s+\d+)?\s+\S+", re.IGNORECASE)


def parse_user_credentials(config_text):
    users = {}
    for line in config_text.splitlines():
        match = USERNAME_LINE.match(line)
        if match:
            users[match.group("user")] = match.group("kind").lower()
    return users


def build_cleanup_commands(candidate_config, running_config):
    candidate_users = parse_user_credentials(candidate_config)
    running_users = parse_user_credentials(running_config)
    commands = []
    for username, candidate_kind in candidate_users.items():
        if candidate_kind == "secret" and running_users.get(username) == "password":
            commands.append(f"no username {username}")
    return commands


def parse_args():
    parser = argparse.ArgumentParser(description="Build IOS cleanup commands for legacy local users using password instead of secret.")
    parser.add_argument("--candidate", required=True, help="Candidate config containing desired username secret lines")
    parser.add_argument("--running", required=True, help="Current running config or show-run username output")
    parser.add_argument("--output", default="artifacts/ios_user_cleanup.txt")
    return parser.parse_args()


def main():
    args = parse_args()
    candidate = Path(args.candidate).read_text(encoding="utf-8")
    running = Path(args.running).read_text(encoding="utf-8")
    commands = build_cleanup_commands(candidate, running)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(commands) + ("\n" if commands else ""), encoding="utf-8")
    print(f"Wrote {len(commands)} commands to {output_path}")


if __name__ == "__main__":
    main()
