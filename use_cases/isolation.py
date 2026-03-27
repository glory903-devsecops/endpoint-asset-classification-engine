from pathlib import Path
from domain.interfaces import IFileOperation, IEncryptionStrategy, IMCPLogger
from domain.models import AssetMetadata, AssetCategory
from datetime import datetime

class ThreatIsolationUseCase:
    """위협 샘플 혹은 민감 데이터를 격리 디렉토리로 이동시키고 암호화하여 보호합니다."""

    def __init__(self, file_op: IFileOperation, encryption: IEncryptionStrategy, logger: IMCPLogger):
        self.file_op = file_op
        self.encryption = encryption
        self.logger = logger

    def isolate_threat(self, threat_file: Path, isolation_root: Path) -> AssetMetadata:
        """위협 파일을 격리하고 암호화합니다."""
        
        # 파일 읽기 및 암호화
        try:
            with open(threat_file, "rb") as f:
                data = f.read()
            
            encrypted_data = self.encryption.encrypt(data)
            
            # 격리 경로 설정
            # 보안을 위해 확장자를 .locked로 변경
            isolated_name = threat_file.name + ".locked"
            isolated_path = isolation_root / isolated_name
            
            # 격리 디렉토리 보장
            self.file_op.ensure_directory(isolation_root)
            
            # 암호화된 파일 쓰기
            with open(isolated_path, "wb") as f:
                f.write(encrypted_data)
            
            # 원본 파일 삭제 (보안 조치)
            if threat_file.exists():
                threat_file.unlink()
            
            # 메타데이터 생성
            metadata = AssetMetadata(
                original_name=threat_file.name,
                current_path=isolated_path,
                category=AssetCategory.VULNERABILITY_SAMPLE,
                file_hash="unknown-encrypted", # 암호화전 해시를 넘기는 것이 더 좋음
                is_malware=True,
                detected_at=datetime.now()
            )
            
            # MCP 로깅
            self.logger.log_asset(metadata)
            
            return metadata
        except Exception as e:
            # 로깅 후 예외 전달
            print(f"격리 중 오류 발생: {e}")
            raise e
