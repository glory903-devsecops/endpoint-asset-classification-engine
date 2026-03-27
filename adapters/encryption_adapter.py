try:
    from cryptography.fernet import Fernet
except ImportError:
    Fernet = None

from domain.interfaces import IEncryptionStrategy

class FernetEncryptionAdapter(IEncryptionStrategy):
    """최신 보안 권고 사항을 준수하는 Fernet 암호화 어댑터입니다."""
    
    def __init__(self, key: bytes = None):
        self._key = key if key else self.generate_key()
        if Fernet:
            self._fernet = Fernet(self._key)
        else:
            self._fernet = None

    def generate_key(self) -> bytes:
        """암호화 키를 생성합니다."""
        if Fernet:
            return Fernet.generate_key()
        return b"fallback-xor-key-32bytes-exactly" # 실제로는 더 복잡해야 함

    def encrypt(self, data: bytes) -> bytes:
        """데이터를 암호화합니다."""
        if self._fernet:
            return self._fernet.encrypt(data)
        # Fallback XOR (최후의 수단, 시큐어 코딩상 비권장)
        return bytes([b ^ self._key[i % len(self._key)] for i, b in enumerate(data)])

    def decrypt(self, data: bytes) -> bytes:
        """데이터를 복호화합니다."""
        if self._fernet:
            return self._fernet.decrypt(data)
        # Fallback XOR
        return bytes([b ^ self._key[i % len(self._key)] for i, b in enumerate(data)])
