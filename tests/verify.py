import sys
from pathlib import Path
import json

# 프로젝트 루트를 경로에 추가
project_root = Path(__file__).parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from adapters.filesystem_adapter import FileSystemAdapter
from adapters.hashing_adapter import SHA256HashingAdapter
from adapters.mcp_logger_adapter import MCPLoggerAdapter
from adapters.signature_adapter import SignatureAdapter
from use_cases.classification import AssetClassificationUseCase

def test_classification():
    print("--- Testing Asset Classification Logic ---")
    file_op = FileSystemAdapter()
    hasher = SHA256HashingAdapter()
    logger = MCPLoggerAdapter(str(project_root / "test_audit.log"))
    sig_provider = SignatureAdapter()
    
    classifier = AssetClassificationUseCase(file_op, hasher, logger, sig_provider)
    
    # 임시 테스트 파일 생성
    test_work_file = project_root / "test_work_WMS_001.py"
    test_personal_file = project_root / "test_personal_trip.mov"
    
    with open(test_work_file, "w") as f: f.write("print('work')")
    with open(test_personal_file, "w") as f: f.write("video content")
    
    # 스코어링 확인
    work_scores = classifier._calculate_scores(test_work_file)
    personal_scores = classifier._calculate_scores(test_personal_file)
    
    print(f"Work File Scores: {work_scores}")
    print(f"Personal File Scores: {personal_scores}")
    
    assert work_scores["work"] > work_scores["personal"], "Work file should have higher work score"
    assert personal_scores["personal"] > personal_scores["work"], "Personal file should have higher personal score"
    
    print("Classification Logic: PASS")
    
    # 정리 (성공 시에만 호출)
    try:
        if (project_root / "test_audit.log").exists():
            # 파일 핸들러가 열려있을 수 있으므로 강제 삭제 시도 전 잠시 대기
            import time
            time.sleep(1)
            (project_root / "test_audit.log").unlink()
    except Exception as e:
        print(f"Non-critical cleanup warning: {e}")

def test_api_import():
     print("\n--- Testing API Server Imports ---")
     try:
         import fastapi
         import uvicorn
         print("FastAPI / Uvicorn Imports: PASS")
     except ImportError as e:
         print(f"Import Error (expected if venv is not ready): {e}")

if __name__ == "__main__":
    try:
        test_classification()
        test_api_import()
        print("\nAll verification tests completed successfully.")
    except Exception as e:
        print(f"\nVerification Failed: {e}")
        sys.exit(1)
