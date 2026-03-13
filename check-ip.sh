#!/usr/bin/env bash
# Check your public/online IP address
# Works on macOS, Linux, and Windows (Git Bash, WSL, Cygwin)

set -e

SERVICES=(
    "https://ifconfig.me/ip"
    "https://icanhazip.com"
    "https://api.ipify.org"
    "https://ipinfo.io/ip"
)

get_ip() {
    local url="$1"
    local raw
    if command -v curl &>/dev/null; then
        raw=$(curl -sSf --connect-timeout 5 --max-time 10 "$url" 2>/dev/null)
    elif command -v wget &>/dev/null; then
        raw=$(wget -qO- --timeout=10 "$url" 2>/dev/null)
    else
        return 1
    fi
    echo "$raw" | tr -d '[:space:]'
}

for url in "${SERVICES[@]}"; do
    ip=$(get_ip "$url")
    if [[ -n "$ip" && "$ip" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "$ip"
        exit 0
    fi
done

echo "Error: Could not fetch public IP. Install curl or wget." >&2
exit 1
