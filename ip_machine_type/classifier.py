"""IP address to machine type classifier."""

import ipaddress
import subprocess
import re
from typing import Optional


def _is_private_ip(ip: str) -> bool:
    """Check if IP is in private/local range."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        return False


def _get_location_type(ip: str) -> str:
    """Determine if IP is local or VPS (public)."""
    return "local" if _is_private_ip(ip) else "vps"


def _parse_os_from_nmap_output(output: str) -> Optional[str]:
    """Parse OS from nmap stdout - handles OS details, Running, Aggressive OS guesses."""
    output_lower = output.lower()

    def _check_line(line: str) -> Optional[str]:
        line_lower = line.lower()
        if "linux" in line_lower and "windows" not in line_lower:
            return "linux"
        if "windows" in line_lower or "microsoft" in line_lower:
            return "windows"
        if "mac os" in line_lower or "macos" in line_lower or "darwin" in line_lower or "apple" in line_lower:
            return "macos"
        return None

    for line in output.splitlines():
        line_lower = line.lower()
        # Match: "OS details:", "Running:", "Aggressive OS guesses:"
        if any(x in line_lower for x in ("running:", "os details:", "aggressive os guesses:")):
            result = _check_line(line)
            if result:
                return result

    # Fallback: any mention in full output
    if "linux" in output_lower and "windows" not in output_lower:
        return "linux"
    if "windows" in output_lower or "microsoft" in output_lower:
        return "windows"
    if "darwin" in output_lower or "mac os" in output_lower or "macos" in output_lower:
        return "macos"
    return None


def _detect_os_nmap(ip: str) -> Optional[str]:
    """Detect OS using nmap -O (requires nmap and root/sudo)."""
    # -Pn: skip host discovery (many hosts block ICMP)
    # -p: scan common ports - OS detection needs open+closed ports
    # --osscan-guess: include aggressive guesses
    try:
        result = subprocess.run(
            [
                "nmap",
                "-Pn",
                "-O",
                "--osscan-guess",
                "-n",
                "-p", "22,80,443,445,21,8080",
                "--host-timeout", "15s",
                ip,
            ],
            capture_output=True,
            text=True,
            timeout=35,
        )
        if result.returncode != 0:
            return None

        return _parse_os_from_nmap_output(result.stdout)
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return None


def _detect_os_ttl(ip: str) -> Optional[str]:
    """Fallback: infer OS from ping TTL (heuristic)."""
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "3", ip],
            capture_output=True,
            text=True,
            timeout=6,
        )
        if result.returncode != 0:
            return None

        # TTL patterns: Windows ~128, Linux ~64, MacOS ~64/255
        match = re.search(r"ttl[= ](\d+)", result.stdout, re.I)
        if not match:
            return None

        ttl = int(match.group(1))
        # Initial TTL: Windows=128, Linux=64, MacOS=64/255
        if ttl >= 120:
            return "windows"
        if 60 <= ttl < 120:
            return "linux"
        if ttl >= 200:
            return "macos"
        return "linux"  # Default for 64-ish
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return None


def _detect_os(ip: str) -> str:
    """Detect OS using nmap first, then TTL fallback, then default."""
    os_type = _detect_os_nmap(ip)
    if os_type:
        return os_type
    os_type = _detect_os_ttl(ip)
    if os_type:
        return os_type
    # VPS/public IPs are overwhelmingly Linux; local is often Linux too
    return "linux"


def classify_ip(ip: str) -> str:
    """
    Classify an IP address into machine type.

    Returns one of:
    - local windows, local linux, local macos
    - windows vps, linux vps, macos vps
    """
    ip = ip.strip()
    if not ip:
        raise ValueError("IP address cannot be empty")

    location = _get_location_type(ip)
    os_type = _detect_os(ip)

    return f"{location} {os_type}"
