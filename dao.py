import json
from pathlib import Path

LICENSE_FILE = Path("license.json")

def load_all():
    if not LICENSE_FILE.exists():
        return {}
    with open(LICENSE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_all(data):
    with open(LICENSE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def add_license(pc_id, key, expires):
    data = load_all()
    data[pc_id] = {
        "key": key,
        "active": True,
        "expires": expires
    }
    save_all(data)

def toggle_license(pc_id):
    data = load_all()
    if pc_id in data:
        data[pc_id]["active"] = not data[pc_id]["active"]
        save_all(data)

def delete_license(pc_id):
    data = load_all()
    if pc_id in data:
        del data[pc_id]
        save_all(data)
