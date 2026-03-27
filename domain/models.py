from enum import Enum
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

class AssetCategory(Enum):
    WORK = "Work"
    PERSONAL = "Personal"
    VULNERABILITY_SAMPLE = "Security_Alert_Samples"

@dataclass
class AssetMetadata:
    original_name: str
    current_path: Path
    category: AssetCategory
    file_hash: str
    is_malware: bool
    detected_at: datetime
