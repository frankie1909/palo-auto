import argparse
import getpass
import os
import sys
import textwrap
import xml.etree.ElementTree as ET

import requests

def get_api_key(host: str, username: str, password: str, verify_tls: bool):
    # PAN-OS XML API keygen
    url = f"https://{host}/api/"
    params = {"type": "keygen", "user": username, "password": password}
    resp = requests.get(url, params=params, timeout=20, verify=verify_tls)
    resp.raise_for_status()
    # Parse <key>...</key>
    try:
        root = ET.fromstring(resp.text)
        key = root.findtext(".//key")
        if not key:
            raise ValueError("No <key> found in response")
        return key
    except ET.ParseError as e:
        raise RuntimeError(f"Failed to parse XML: {e}\nRaw response:\n{resp.text[:500]}")

def write_env_file(path: str, host: str, username: str, api_key: str, verify_tls: bool):
    # Create .env content
    contents = textwrap.dedent(f"""\
        # PAN-OS connection settings
        PANOS_HOST={host}
        PANOS_USERNAME={username}
        PANOS_API_KEY={api_key}
        PANOS_VERIFY_TLS={"true" if verify_tls else "false"}
        """)
    # Avoid overly permissive perms on POSIX
    if os.name == "posix":
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        fd = os.open(path, flags, 0o600)
        with os.fdopen(fd, "w") as f:
            f.write(contents)
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(contents)

def main():
    parser = argparse.ArgumentParser(description="Fetch PAN-OS API key and write .env")
    parser.add_argument("--host", required=True, help="Firewall mgmt IP or hostname")
    parser.add_argument("--user", required=True, help="Username (e.g., admin)")
    parser.add_argument("--env", default=".env", help="Output .env path (default: .env)")
    parser.add_argument("--verify", dest="verify", action="store_true", help="Verify TLS (default)")
    parser.add_argument("--no-verify", dest="verify", action="store_false", help="Disable TLS verification (lab)")
    parser.set_defaults(verify=True)
    args = parser.parse_args()

    password = getpass.getpass("Password: ")
    try:
        api_key = get_api_key(args.host, args.user, password, args.verify)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    write_env_file(args.env, args.host, args.user, api_key, args.verify)
    print(f"✓ API key fetched and saved to {args.env}")
    print("Reminder: .env is in .gitignore; do not commit it.")

if __name__ == "__main__":
    main()
