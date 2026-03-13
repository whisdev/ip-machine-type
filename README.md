# ip-machine-type

Check machine type from an IP address.

**Input:** IP address  
**Output:** `IP: machine type`

## Machine types

| Type | Description |
|------|-------------|
| local windows | Private IP + Windows |
| local linux | Private IP + Linux |
| local macos | Private IP + macOS |
| windows vps | Public IP + Windows |
| linux vps | Public IP + Linux |
| macos vps | Public IP + macOS |

## Install

```bash
cd ip-machine-type
pip install -e .
```

For best OS detection, install `nmap`:

- **Linux:** `apt install nmap` or `yum install nmap`
- **macOS:** `brew install nmap`
- **Windows:** [nmap.org/download](https://nmap.org/download.html)

OS detection may require root/sudo for nmap `-O` scans.

## Usage

```bash
ip-machine-type 192.168.1.1
# 192.168.1.1: local linux

ip-machine-type 8.8.8.8
# 8.8.8.8: linux vps
```

## Python API

```python
from ip_machine_type import classify_ip

machine_type = classify_ip("192.168.1.1")
print(machine_type)  # "local linux"
```
