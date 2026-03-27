import shutil
from pathlib import Path
from domain.interfaces import IFileOperation

class FileSystemAdapter(IFileOperation):
    def move_file(self, src: Path, dest: Path) -> None:
        """파일을 소스에서 목적지로 이동합니다. 목적지 부모 디렉토리가 없으면 생성합니다."""
        self.ensure_directory(dest.parent)
        shutil.move(str(src), str(dest))

    def exists(self, path: Path) -> bool:
        """파일 또는 디렉토리가 존재하는지 확인합니다."""
        return path.exists()

    def ensure_directory(self, path: Path) -> None:
        """디렉토리를 생성합니다. (이미 존재하면 무시)"""
        path.mkdir(parents=True, exist_ok=True)
