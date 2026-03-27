from abc import ABC, abstractmethod
from pathlib import Path
from .models import AssetMetadata

class IFileOperation(ABC):
    @abstractmethod
    def move_file(self, src: Path, dest: Path) -> None:
        """이동을 수행합니다."""
        pass

    @abstractmethod
    def exists(self, path: Path) -> bool:
        """파일 존재 여부를 확인합니다."""
        pass

    @abstractmethod
    def ensure_directory(self, path: Path) -> None:
        """디렉토리가 존재하는지 확인하고 없으면 생성합니다."""
        pass

class IHashStrategy(ABC):
    @abstractmethod
    def calculate(self, file_path: Path) -> str:
        """파일의 해시값을 계산합니다."""
        pass

class IMCPLogger(ABC):
    @abstractmethod
    def log_asset(self, metadata: AssetMetadata) -> None:
        """자산 정보를 MCP 로그 형식으로 기록합니다."""
        pass

class IEncryptionStrategy(ABC):
    @abstractmethod
    def encrypt(self, data: bytes) -> bytes:
        """데이터를 암호화합니다."""
        pass

    @abstractmethod
    def decrypt(self, data: bytes) -> bytes:
        """데이터를 복호화합니다."""
        pass

    @abstractmethod
    def generate_key(self) -> bytes:
        """암호화 키를 생성합니다."""
        pass
