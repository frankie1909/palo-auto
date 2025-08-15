# 🚀 palo-auto — Automating Palo Alto Firewalls from a Spreadsheet

**palo-auto** turns customer-friendly spreadsheets into full firewall configurations — all via the Palo Alto Networks API.  
No endless clicking in the GUI, no hand-crafted XML, just structured data → automated push.  

**Goal:** Provide a ready-to-use template & environment where:
1. Customers fill out networks, services, and policy details in a predefined Excel file.
2. You run automation scripts to validate, convert, and push the config to PAN-OS.
3. Secrets and API access are handled securely (no accidental leaks to Git).

---

## 🛠 Why this exists

Manually entering firewall objects, services, and rules is:
- **Slow** —  hundreds of repetitive clicks.
- **Error-prone** — inconsistent names, typos, wrong zones.
- **Hard to standardize** — each engineer does it differently.

With **palo-auto**:
- You give your customer a **clean, validated Excel template**.
- They give it back with all required info (zones, objects, addresses, services, NAT, policies).
- You run one automation process to **push it all over the API** in a consistent order.

---

## 📦 What’s inside

- **Excel/CSV Template** — Multi-sheet structure for Tags, Zones, Interfaces, Routes, Objects, Groups, Services, Policies, NAT.
- **Environment Setup** — Scripts to install dependencies in a Python virtual environment.
- **Secure API Key Handling** — `.env` file creation, `.gitignore` preconfigured to avoid secret leaks.
- **Connectivity Test** — `test_connect.py` to ensure the API works before pushing.
- **Example API Scripts** — Show how to create objects, set passwords, or adjust mgmt IP over the API.

---

## 🚀 Quickstart

```bash
# 1) Clone the repo
git clone https://github.com/<your-org>/palo-auto.git
cd palo-auto

# 2) Create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate    # Windows: .\.venv\Scripts\Activate.ps1
pip install --upgrade pip

# 3) Install dependencies
pip install pan-os-python pan-python requests python-dotenv

# If on Python 3.12+ and you see "No module named 'distutils'":
pip install setuptools

# 4) Generate an API key into .env
python get_panos_key.py --host <FW-MGMT-IP-or-FQDN> --user <username> --no-verify
# use --verify if your mgmt cert is valid

# 5) Test connectivity
python test_connect.py
