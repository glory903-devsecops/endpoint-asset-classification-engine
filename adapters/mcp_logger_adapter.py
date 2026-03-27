import json
import logging
from domain.interfaces import IMCPLogger
from domain.models import AssetMetadata

class MCPLoggerAdapter(IMCPLogger):
    """Model Context Protocol (MCP) 형식을 준환하는 로거 어댑터입니다.
    AI 모델이 파일을 자산으로 인식할 수 있도록 정형화된 JSON을 출력합니다."""
    
    def __init__(self, log_file: str = "asset_governance.log"):
        self.logger = logging.getLogger("AssetGovernance")
        self.logger.setLevel(logging.INFO)
        
        # 파일 핸들러 설정
        fh = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def log_asset(self, metadata: AssetMetadata) -> None:
        """자산 메타데이터를 MCP가 해석하기 쉬운 JSON 형식으로 로그에 남깁니다."""
        log_entry = {
            "type": "asset_metadata",
            "name": metadata.original_name,
            "path": str(metadata.current_path),
            "category": metadata.category.value,
            "hash": metadata.file_hash,
            "security_warning": metadata.is_malware,
            "timestamp": metadata.detected_at.isoformat()
        }
        self.logger.info(json.dumps(log_entry, ensure_ascii=False))
