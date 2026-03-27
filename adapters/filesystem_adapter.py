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

    def get_safe_path(self, target_path: Path) -> Path:
        """충돌 방지를 위해 중복되지 않는 안전한 경로를 생성합니다 (예: file_(1).txt)."""
        if not self.exists(target_path):
            return target_path
            
        base = target_path.parent / target_path.stem
        suffix = target_path.suffix
        counter = 1
        
        while True:
            new_path = Path(f"{base}_({counter}){suffix}")
            if not self.exists(new_path):
                return new_path
            counter += 1

    def ensure_directory(self, path: Path) -> None:
        """디렉토리를 생성합니다. (이미 존재하면 무시)"""
        path.mkdir(parents=True, exist_ok=True)
