import hashlib
import hmac
import uuid

from app.config import settings


def _sign(contact_hex: str) -> str:
    return hmac.new(
        settings.JWT_SECRET.encode(), contact_hex.encode(), hashlib.sha256
    ).hexdigest()


def make_unsubscribe_token(contact_id: uuid.UUID) -> str:
    contact_hex = contact_id.hex
    return f"{contact_hex}.{_sign(contact_hex)}"


def verify_unsubscribe_token(token: str) -> uuid.UUID | None:
    parts = token.split(".")
    if len(parts) != 2:
        return None
    contact_hex, signature = parts
    if not hmac.compare_digest(signature, _sign(contact_hex)):
        return None
    try:
        return uuid.UUID(hex=contact_hex)
    except ValueError:
        return None
