import sys
import os
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가 (한국어 경로 등 인코딩 이슈 해결)
project_root = str(Path(__file__).parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from adapters.filesystem_adapter import FileSystemAdapter
from adapters.hashing_adapter import SHA256HashingAdapter
from adapters.encryption_adapter import FernetEncryptionAdapter
from adapters.mcp_logger_adapter import MCPLoggerAdapter
from use_cases.classification import AssetClassificationUseCase
from use_cases.isolation import ThreatIsolationUseCase

def main():
    print("=== Endpoint Asset Governance Engine ===")
    
    # 1. 의존성 주입 (Dependency Injection)
    file_op = FileSystemAdapter()
    hasher = SHA256HashingAdapter()
    
    # 보안 권고에 따른 고정 키 (실제 운영환경에서는 환경변수나 KMS 연동 필요)
    # 여기서는 고정된 bytes를 사용하거나 새로 생성합니다.
    enc_key = b'v-p6v_Z-v9_v_v-v_v_v_v-v_v_v_v-v_v_v_v_v=' # 임시 키 (Fernet 형식)
    encryption = FernetEncryptionAdapter(enc_key)
    logger = MCPLoggerAdapter("governance_audit.log")

    # 유스케이스 초기화
    classification_service = AssetClassificationUseCase(file_op, hasher, logger)
    isolation_service = ThreatIsolationUseCase(file_op, encryption, logger)

    # 2. 경로 설정 (샘플 테스트용)
    base_dir = Path("g:/내 드라이브/99.Develop/Endpoint_Asset_Classification_Engine/test_data")
    source_dir = base_dir / "inbox"
    work_dir = base_dir / "Work_Assets"
    personal_dir = base_dir / "Personal_Assets"
    isolation_dir = base_dir / "Security_Alert_Samples"

    # 디렉토리 보장
    for d in [source_dir, work_dir, personal_dir, isolation_dir]:
        file_op.ensure_directory(d)

    # 3. 프로세스 실행
    print(f"Scanning {source_dir}...")
    
    files = list(source_dir.glob("*"))
    if not files:
        print("분류할 파일이 없습니다. 테스트 데이터를 생성하거나 inbox에 파일을 넣어주세요.")
        return

    for file_path in files:
        if file_path.is_dir():
            continue
            
        print(f"Processing: {file_path.name}")
        
        # 특정 파일(예: malware 키워드)은 격리 대상으로 처리
        if "malware" in file_path.name.lower() or "threat" in file_path.name.lower():
            print(f"  [Security Alert] {file_path.name} is being isolated...")
            isolation_service.isolate_threat(file_path, isolation_dir)
        else:
            print(f"  [Scan] Classifying {file_path.name}...")
            classification_service.classify_and_move(file_path, work_dir, personal_dir)

    print("=== Governance Process Completed ===")

if __name__ == "__main__":
    main()
