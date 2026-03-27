import json
from pathlib import Path
from domain.interfaces import ISignatureProvider

class SignatureAdapter(ISignatureProvider):
    """
    로컬 및 원격 저장소에서 지능형 분류를 위한 시그니처와 키워드를 제공하는 어댑터입니다.
    """

    def __init__(self, config: dict = None):
        self.config = config or {}
        # 기본 시그니처 세트 (연구 기반)
        self._signatures = {
                    "work": {
                "extensions": [
                    ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".java", ".cpp", ".h", ".cs", 
                    ".php", ".rb", ".rs", ".swift", ".kt", ".sh", ".sql", ".md", ".json", 
                    ".yaml", ".yml", ".html", ".css", ".hwp", ".pdf", ".docx", ".xlsx"
                ],
                "markers": [
                    ".git", "node_modules", "venv", "package.json", "requirements.txt", 
                    "pom.xml", "build.gradle", "Dockerfile", "Makefile", ".vscode", ".idea"
                ],
                "keywords": [
                    "project", "enterprise", "confidential", "architecture", "sow", 
                    "contract", "prd", "spec", "design", "development", "implementation",
                    "woodmetal", "wms", "j-", "검사성적서", "공정", "관리"
                ]
            },
            "personal": {
                "extensions": [
                    ".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mov", ".avi", ".mp3", ".wav", 
                    ".zip", ".rar", ".iso", ".dmg", ".pkg", ".torrent"
                ],
                "keywords": [
                    "photo", "video", "chat", "whatsapp", "telegram", "game", "netflix", 
                    "personal", "trip", "family", "hobby"
                ]
            },
            "threat": {
                "extensions": [
                    ".exe", ".scr", ".com", ".msi", ".dll", ".vbs", ".ps1", ".bat", 
                    ".docm", ".xlsm", ".pptm"
                ],
                "keywords": [
                    "malware", "virus", "threat", "payload", "infect", "hack", "crack"
                ]
            }
        }
        
    def get_signatures(self) -> dict:
        """
        설정된 원격 URL이 있다면 최신 시그니처를 동기화하고, 그렇지 않으면 기본 세트를 반환합니다.
        """
        remote_url = self.config.get("security", {}).get("remote_signature_url")
        if remote_url:
            # 실제 구현 시 requests 등을 사용하여 fetching 로직 추가 가능
            # 현재는 확장성을 위해 인터페이스만 유지
            pass
            
        return self._signatures
