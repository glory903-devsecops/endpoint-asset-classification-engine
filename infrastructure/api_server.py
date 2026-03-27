from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import json
import os
import sys

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from adapters.filesystem_adapter import FileSystemAdapter
from adapters.hashing_adapter import SHA256HashingAdapter
from adapters.logging_adapter import MCPLoggerAdapter
from adapters.signature_adapter import SignatureAdapter
from use_cases.classification import AssetClassificationUseCase

app = FastAPI(title="Asset Governance Engine v2.5 API")

# CORS 설정 (React Dashboard 대역 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    root_path: str

@app.get("/api/stats")
async def get_stats():
    """로그 파일을 분석하여 현재 통계 데이터를 반환합니다."""
    log_file = project_root / "governance_audit.log"
    if not log_file.exists():
        return {"total": 0, "work": 0, "personal": 0, "security": 0, "recent": []}
    
    stats = {"total": 0, "work": 0, "personal": 0, "security": 0, "recent": []}
    
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.split(" - ", 1)
                if len(parts) < 2: continue
                data = json.loads(parts[1])
                
                cat = data.get("category")
                if cat == "Work": stats["work"] += 1
                elif cat == "Personal": stats["personal"] += 1
                elif "Sample" in cat or "Threat" in str(cat): stats["security"] += 1
                
                stats["total"] += 1
                stats["recent"].append(data)
                
        stats["recent"] = stats["recent"][-10:] # 최신 10개만 유지
    except Exception as e:
        print(f"Stats analysis error: {e}")
        
    return stats

@app.post("/api/scan")
async def start_scan(request: ScanRequest):
    """지정된 경로를 동적으로 스캔하고 인플레이스 분류를 수행합니다."""
    root = Path(request.root_path)
    if not root.is_dir():
        raise HTTPException(status_code=400, detail=f"'{request.root_path}' is not a valid directory.")

    # 1. 아키텍처 의존성 주입
    file_op = FileSystemAdapter()
    hasher = SHA256HashingAdapter()
    logger = MCPLoggerAdapter(str(project_root / "governance_audit.log"))
    sig_provider = SignatureAdapter()
    
    classification_service = AssetClassificationUseCase(file_op, hasher, logger, sig_provider)
    
    # 2. 인플레이스 타겟 폴더 설정 (지정된 루트 내부)
    work_dir = root / "Work_Assets"
    personal_dir = root / "Personal_Assets"
    
    scan_results = {"total": 0, "work": 0, "personal": 0, "threat": 0}
    
    # 3. 재귀적 파일 스캔 및 분류
    # 주의: 이미 분류된 폴더는 건너뜀
    exclude_dirs = {"Work_Assets", "Personal_Assets", "Threat_Samples", "venv", ".git", "node_modules"}
    
    try:
        files_to_process = []
        for file_path in root.rglob("*"):
            if file_path.is_file():
                # 이미 분류 폴더에 들어있는 파일은 제외
                if any(ex in file_path.parts for ex in exclude_dirs):
                    continue
                files_to_process.append(file_path)
        
        for file_path in files_to_process:
            try:
                # 상대 경로 계산 (하위 폴더 구조 유지용)
                relative_path = file_path.parent.relative_to(root)
                classification_service.classify_and_move(
                    file_path, work_dir, personal_dir, relative_path
                )
                scan_results["total"] += 1
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                
        return {"status": "success", "summary": scan_results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
