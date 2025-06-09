import json
from pathlib import Path
LICENSE_FILE = Path(__file__).parent / "license.json"

def load_all():
    if not LICENSE_FILE.exists():
        return {}
    with open(LICENSE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_all(data):
    with open(LICENSE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def add_license(pc_id, key, expires, name="", service="LICENSE"):
    data = load_all()
    data[pc_id] = {
        "name": name,
        "key": key,
        "active": True,
        "expires": expires,
        "service": service
    }
    save_all(data)


def update_license(pc_id, name, expires):
    data = load_all()
    if pc_id in data:
        data[pc_id]["name"] = name
        data[pc_id]["expires"] = expires
        save_all(data)

def toggle_license(pc_id):
    data = load_all()
    if pc_id in data:
        data[pc_id]["active"] = not data[pc_id].get("active", True)
        save_all(data)

def delete_license(pc_id):
    data = load_all()
    if pc_id in data:
        del data[pc_id]
        save_all(data)

def check_license(pc_id, key=None):
    data = load_all()
    if pc_id in data:
        license = data[pc_id]
        if key is None:
            return license["key"]
        return license["key"] == key and license.get("active", False)
    return False

def load_by_service(service):
    data = load_all()
    return {k: v for k, v in data.items() if v.get("service", "").upper() == service.upper()}