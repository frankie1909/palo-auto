import os
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from panos.firewall import Firewall

load_dotenv()

host    = os.getenv("PANOS_HOST")
api_key = os.getenv("PANOS_API_KEY")
verify  = os.getenv("PANOS_VERIFY_TLS", "true").lower() == "true"

fw = Firewall(hostname=host, api_key=api_key)

# Set TLS verification on the XML API handle (correct way)
fw.xapi.ssl_verify = verify

# Run the operational command
raw_xml = fw.op("show system info", xml=True)

# Parse XML from bytes
root = ET.fromstring(raw_xml)

model  = root.findtext(".//model")
serial = root.findtext(".//serial")
swver  = root.findtext(".//sw-version")

print(f"Connected to {host}")
print(f"  Model: {model}")
print(f"  Serial: {serial}")
print(f"  PAN-OS: {swver}")
