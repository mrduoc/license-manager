from dataclasses import dataclass

@dataclass
class LicenseKey:
    pc_id: str
    key: str
    name: str
    expires: str
    active: bool = True
    service: str = ""
