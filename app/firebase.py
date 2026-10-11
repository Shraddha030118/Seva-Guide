import json
import logging
import os
from typing import Any, Dict, Optional

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ModuleNotFoundError:  # pragma: no cover - optional dependency in local/offline mode
    firebase_admin = None
    credentials = None
    firestore = None

logger = logging.getLogger("sevaguide.firebase")
_db: Optional[Any] = None


def get_firebase_service_account() -> Optional[Dict[str, str]]:
    raw_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON", "").strip()
    if raw_json:
        try:
            payload = json.loads(raw_json)
            if isinstance(payload, dict):
                return payload
        except json.JSONDecodeError as exc:
            raise ValueError("FIREBASE_SERVICE_ACCOUNT_JSON must be valid JSON") from exc

    private_key = os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n").strip()
    if not private_key or private_key.startswith("-----BEGIN PRIVATE KEY-----\\nYOUR_KEY_HERE"):
        return None

    return {
        "type": "service_account",
        "project_id": os.getenv("FIREBASE_PROJECT_ID", ""),
        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID", ""),
        "private_key": private_key,
        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL", ""),
        "client_id": os.getenv("FIREBASE_CLIENT_ID", ""),
        "auth_uri": os.getenv("FIREBASE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
        "token_uri": os.getenv("FIREBASE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
        "auth_provider_x509_cert_url": os.getenv(
            "FIREBASE_AUTH_PROVIDER_CERT_URL",
            "https://www.googleapis.com/oauth2/v1/certs",
        ),
        "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL", ""),
    }


def initialize_firebase_admin() -> Optional[Any]:
    global _db

    if firebase_admin is None or firestore is None or credentials is None:
        logger.warning(
            "Firebase Admin SDK is not installed. Running with offline/mock Firestore mode."
        )
        _db = None
        return None

    service_account = get_firebase_service_account()
    if not service_account:
        logger.warning(
            "Firebase Admin is not configured. Set FIREBASE_SERVICE_ACCOUNT_JSON or valid FIREBASE_PRIVATE_KEY values to enable Firestore/Auth integrations."
        )
        _db = None
        return None

    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate(service_account)
        firebase_admin.initialize_app(cred)

    if _db is None:
        _db = firestore.client()
    return firebase_admin.get_app()


def get_firestore_db() -> Any:
    if _db is None:
        initialize_firebase_admin()
    return _db
