import base64

from cryptography.fernet import Fernet

from app.config.settings import get_settings


class EncryptionService:
    def __init__(self):
        settings = get_settings()
        key = settings.encryption_key.encode()
        self.cipher = Fernet(key)

    def encrypt(self, text: str) -> str:
        encrypted_bytes = self.cipher.encrypt(text.encode())
        return base64.b64encode(encrypted_bytes).decode()

    def decrypt(self, encrypted_text: str) -> str:
        encrypted_bytes = base64.b64decode(encrypted_text.encode())
        decrypted_bytes = self.cipher.decrypt(encrypted_bytes)
        return decrypted_bytes.decode()
