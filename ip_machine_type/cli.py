#!/usr/bin/env python3
"""CLI for ip-machine-type: IP to machine type."""

import sys
from .classifier import classify_ip


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: ip-machine-type <ip_address>", file=sys.stderr)
        return 1

    ip = sys.argv[1]
    try:
        machine_type = classify_ip(ip)
        print(f"{ip}: {machine_type}")
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
