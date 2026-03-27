import sys
import os
from pathlib import Path

# 표준 출력을 UTF-8로 재구성 (Windows의 CP949 인코딩 이슈 해결)
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        # Python < 3.7 대응 (필요시)
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 프로젝트 루트를 sys.path에 추가 (한국어 경로 등 인코딩 이슈 해결)
project_root = str(Path(__file__).parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from adapters.filesystem_adapter import FileSystemAdapter
from adapters.hashing_adapter import SHA256HashingAdapter
from adapters.encryption_adapter import FernetEncryptionAdapter
from adapters.mcp_logger_adapter import MCPLoggerAdapter
from adapters.signature_adapter import SignatureAdapter
from use_cases.classification import AssetClassificationUseCase
from use_cases.isolation import ThreatIsolationUseCase

import argparse
import json

def load_config(config_path: Path) -> dict:
    """설정 파일을 로드합니다."""
    if not config_path.exists():
        # 기본 설정 반환
        return {
            "enterprise": {"keywords": [], "signatures": []},
            "paths": {"inbox": "test_data/inbox", "work_assets": "Work_Assets", "personal_assets": "Personal_Assets", "security_alerts": "Security_Alert_Samples", "audit_log": "governance_audit.log"},
            "security": {"encryption_key": "p_W8vB8X8X8X8X8X8X8X8X8X8X8X8X8X8X8X8X8X8X8=", "isolate_keywords": ["malware", "threat", "virus"]}
        }
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Endpoint Asset Governance Engine v2.4")
    parser.add_argument("--config", type=str, default="config/settings.json", help="설정 파일 경로")
    parser.add_argument("--dry-run", action="store_true", help="실제 이동 없이 분류 결과만 시뮬레이션합니다.")
    args = parser.parse_args()

    # 1. 환경 설정 로드
    base_dir = Path(__file__).parent.absolute()
    config = load_config(base_dir / args.config)
    
    print("=== Endpoint Asset Governance Engine v2.4 (Intelligent) ===")
    if args.dry_run:
        print("[!] DRY-RUN MODE: 실제 파일 이동이 발생하지 않습니다.")
    
    # 2. 의존성 주입 (Dependency Injection)
    file_op = FileSystemAdapter()
    hasher = SHA256HashingAdapter()
    
    # 설정에서 암호화 키 로드
    enc_key = config["security"]["encryption_key"].encode()
    encryption = FernetEncryptionAdapter(enc_key)
    logger = MCPLoggerAdapter(config["paths"]["audit_log"])
    
    # 지능형 시그니처 배포기 (Remote-Ready)
    signature_provider = SignatureAdapter(config)

    # 유스케이스 초기화 (설정 주입)
    classification_service = AssetClassificationUseCase(file_op, hasher, logger, signature_provider)
    isolation_service = ThreatIsolationUseCase(file_op, encryption, logger)

    # 경로 설정
    source_dir = base_dir / config["paths"]["inbox"]
    work_dir = base_dir / config["paths"]["work_assets"]
    personal_dir = base_dir / config["paths"]["personal_assets"]
    isolation_dir = base_dir / config["paths"]["security_alerts"]

    # 디렉토리 보장
    for d in [source_dir, work_dir, personal_dir, isolation_dir]:
        file_op.ensure_directory(d)

    # 3. 프로세스 실행 (Recursive & Intelligent)
    print(f"Scanning {source_dir}...")
    
    processed_paths = set()
    isolate_keywords = config["security"]["isolate_keywords"]

    # rglob("*")으로 모든 파일과 폴더 탐색
    for file_path in source_dir.rglob("*"):
        if any(file_path.is_relative_to(p) for p in processed_paths):
            continue

        relative_path = file_path.relative_to(source_dir).parent
        
        # 3.1 프로젝트 단위 탐지 (Signature Move)
        if file_path.is_dir() and classification_service.is_project_directory(file_path):
            print(f"  [Project/Work Folder] {file_path.name}")
            if not args.dry_run:
                classification_service.classify_and_move(file_path, work_dir, personal_dir, relative_path)
            processed_paths.add(file_path)
            continue

        # 3.2 단일 파일 처리
        if file_path.is_file():
            # 보안 위협 탐지
            if any(kw in file_path.name.lower() for kw in isolate_keywords):
                print(f"  [Security Alert] {file_path.name} (Isolating...)")
                if not args.dry_run:
                    isolation_service.isolate_threat(file_path, isolation_dir)
            else:
                # 분류 결과 예측 (Dry-run 시각화)
                category = classification_service.classify_and_move(file_path, work_dir, personal_dir, relative_path) if not args.dry_run else "Simulated"
                print(f"  [Scan] Process: {file_path.name}")
                if args.dry_run:
                    # Dry-run 시에도 로직 테스트를 위해 결과 예측 출력
                    scores = classification_service._calculate_scores(file_path)
                    mock_category = "Work" if scores["work"] > scores["personal"] else "Personal"
                    if scores["threat"] > 0: mock_category = "THREAT"
                    print(f"    -> Predicted Category: {mock_category} (Scores: {scores})")

    print("=== Governance Process Completed ===")

if __name__ == "__main__":
    main()
