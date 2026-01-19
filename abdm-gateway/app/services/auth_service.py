from app.core.config import get_settings
from app.core.security import create_access_token
from app.database.connection import SessionLocal
from app.database.models import Client
from sqlalchemy.orm import Session

settings = get_settings()

def get_db_session() -> Session:
    """Get a database session."""
    return SessionLocal()

def validate_client_credentials(client_id: str, client_secret: str) -> bool:
    """
    Validate client credentials against the database.
    
    Args:
        client_id: Client identifier
        client_secret: Client secret
        
    Returns:
        True if credentials are valid, False otherwise
    """
    if not client_id or not client_secret:
        return False
    
    db = get_db_session()
    try:
        client = db.query(Client).filter(Client.client_id == client_id).first()
        if client and client.client_secret == client_secret:
            return True
        return False
    finally:
        db.close()

def issue_access_token(client_id: str, cm_id: str) -> str:
    token = create_access_token({"clientId": client_id, "cmId": cm_id})
    return {
        "accessToken": token,
        "expiresIn": settings.jwt_expiry_seconds,
        "tokenType": "Bearer"
    }