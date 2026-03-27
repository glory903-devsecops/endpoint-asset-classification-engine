from pathlib import Path
from domain.interfaces import IFileOperation, IHashStrategy, IMCPLogger
from domain.models import AssetMetadata, AssetCategory
from datetime import datetime

class AssetClassificationUseCase:
    """메타데이터를 기반으로 자산을 분류하고 제자리에 배치하는 비즈니스 로직입니다."""

    def __init__(self, file_op: IFileOperation, hasher: IHashStrategy, logger: IMCPLogger):
        self.file_op = file_op
        self.hasher = hasher
        self.logger = logger

    def classify_and_move(self, source_path: Path, work_root: Path, personal_root: Path) -> AssetMetadata:
        """단일 파일을 분류하여 이동시킵니다."""
        file_name = source_path.name.lower()
        
        # 기본 분류 로직: 키워드 기반
        if "work" in file_name or "project" in file_name:
            category = AssetCategory.WORK
            target_dir = work_root
        else:
            category = AssetCategory.PERSONAL
            target_dir = personal_root

        # 해시 계산
        file_hash = self.hasher.calculate(source_path)
        
        # 메타데이터 생성
        metadata = AssetMetadata(
            original_name=source_path.name,
            current_path=source_path,
            category=category,
            file_hash=file_hash,
            is_malware=False, # 위협 엔진에서 나중에 판단
            detected_at=datetime.now()
        )

        # 파일 이동
        dest_path = target_dir / source_path.name
        self.file_op.move_file(source_path, dest_path)
        
        # 업데이트된 메타데이터 경로
        metadata.current_path = dest_path

        # MCP 로깅
        self.logger.log_asset(metadata)

        return metadata
