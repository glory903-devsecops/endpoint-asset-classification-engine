from pathlib import Path
from domain.interfaces import IFileOperation, IHashStrategy, IMCPLogger, ISignatureProvider
from domain.models import AssetMetadata, AssetCategory
from datetime import datetime

class AssetClassificationUseCase:
    """
    지능형 시그니처 분석 및 가중치 기반 스코어링을 통해 자산을 분류합니다.
    하드코딩을 배제하고 ISignatureProvider를 통해 동적으로 규칙을 수신합니다.
    """

    def __init__(self, file_op: IFileOperation, hasher: IHashStrategy, logger: IMCPLogger, signature_provider: ISignatureProvider):
        self.file_op = file_op
        self.hasher = hasher
        self.logger = logger
        self.signature_provider = signature_provider
        self._refresh_signatures()

    def _refresh_signatures(self):
        self._sig_data = self.signature_provider.get_signatures()

    def classify_and_move(self, source_path: Path, work_root: Path, personal_root: Path, relative_path: Path = Path(".")) -> AssetMetadata:
        """자산을 지능적으로 분류하고 이동시킵니다."""
        
        # 1. 스코어링 기반 분류
        scores = self._calculate_scores(source_path)
        
        # 가장 높은 점수를 가진 카테고리 선정
        # 우선순위: Threat > Work > Personal
        category = AssetCategory.PERSONAL
        
        if scores["threat"] > 0:
            # 위협은 즉시 처리 (ThreatIsolationUseCase에서 별도 처리 가능하지만 메타데이터는 생성)
            is_malware = True
            category = AssetCategory.VULNERABILITY_SAMPLE
        elif scores["work"] > scores["personal"]:
            is_malware = False
            category = AssetCategory.WORK
        else:
            is_malware = False
            category = AssetCategory.PERSONAL

        target_root = work_root if category == AssetCategory.WORK else personal_root
        if category == AssetCategory.VULNERABILITY_SAMPLE:
            # Threat는 위협 격리 폴더로 (main.py에서 isolation_dir로 전달됨)
            pass 

        # 2. 계층 구조 보존 및 이동 실행
        dest_dir = target_root / relative_path
        self.file_op.ensure_directory(dest_dir)
        
        file_hash = self.hasher.calculate(source_path) if source_path.is_file() else ""
        dest_path = dest_dir / source_path.name
        
        # 중복 방지
        if self.file_op.exists(dest_path) and source_path.is_file():
            if file_hash == self.hasher.calculate(dest_path):
                return AssetMetadata(source_path.name, dest_path, category, file_hash, is_malware, datetime.now())
            dest_path = self.file_op.get_safe_path(dest_path)

        metadata = AssetMetadata(
            original_name=source_path.name,
            current_path=source_path,
            category=category,
            file_hash=file_hash,
            is_malware=is_malware,
            detected_at=datetime.now()
        )

        self.file_op.move_file(source_path, dest_path)
        metadata.current_path = dest_path
        self.logger.log_asset(metadata)

        return metadata

    def _calculate_scores(self, path: Path) -> dict:
        """확장자, 마커, 키워드 가중치를 계산합니다."""
        scores = {"work": 0, "personal": 0, "threat": 0}
        name_lower = path.name.lower()
        ext_lower = path.suffix.lower()
        
        # A. 확장자 매칭 (가중치 20)
        for cat in scores.keys():
            if ext_lower in self._sig_data[cat]["extensions"]:
                scores[cat] += 20
                
        # B. 키워드 매칭 (가중치 10)
        for cat in scores.keys():
            for kw in self._sig_data[cat]["keywords"]:
                if kw in name_lower:
                    scores[cat] += 10
                    
        # C. 프로젝트 마커 (가중치 50 - 강력한 지표)
        if path.is_dir():
            for marker in self._sig_data["work"]["markers"]:
                if (path / marker).exists():
                    scores["work"] += 50
                    
        return scores

    def is_project_directory(self, path: Path) -> bool:
        """Legacy API 지원 (main.py 등에서 사용 가능)"""
        return self._calculate_scores(path)["work"] >= 50
