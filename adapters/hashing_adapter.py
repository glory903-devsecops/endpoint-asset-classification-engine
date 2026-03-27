import hashlib
from pathlib import Path
from domain.interfaces import IHashStrategy

class SHA256HashingAdapter(IHashStrategy):
    def calculate(self, file_path: Path) -> str:
        """파일의 SHA-256 해시값을 계산합니다. 대용량 파일을 고려하여 청크 단위로 읽습니다."""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except FileNotFoundError:
            return ""
