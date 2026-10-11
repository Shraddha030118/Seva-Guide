from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import get_current_user
from app.firestore_service import get_service_by_slug, get_service_checklist, get_user_checklist, save_user_checklist

router = APIRouter(prefix="/checklists", tags=["Checklists & Step Guides"])


def normalize_user_checklist(service_slug: str, payload: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not payload:
        return None

    result = dict(payload)
    result.setdefault("service_slug", service_slug)
    result.setdefault("created_at", datetime.utcnow())
    result.setdefault("updated_at", datetime.utcnow())
    return result


@router.get("/{service_slug}", summary="Get a public checklist by service slug")
async def get_public_checklist(service_slug: str):
    service = get_service_by_slug(service_slug)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Checklist for service '{service_slug}' not found")

    checklist = get_service_checklist(service_slug)
    if not checklist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Checklist data for service '{service_slug}' not found")
    return {
        "id": checklist.get("id") or f"checklist-{service_slug}",
        "service_slug": service.get("slug"),
        "service_title": service.get("title", "Service"),
        "documents_required": checklist.get("documents_required", []),
        "application_steps": checklist.get("application_steps", []),
        "eligibility_checklist": checklist.get("eligibility_checklist", []),
        "common_mistakes": checklist.get("common_mistakes", []),
        "helpful_tips": checklist.get("helpful_tips", []),
        "faqs": checklist.get("faqs", []),
        "created_at": checklist.get("created_at", datetime.utcnow()),
        "updated_at": checklist.get("updated_at", datetime.utcnow()),
    }


@router.get("/me", summary="List all saved user checklists")
async def list_user_checklists(user=Depends(get_current_user)):
    uid = user["uid"]
    docs = []
    from app.firebase import get_firestore_db

    snapshot = get_firestore_db().collection("users").document(uid).collection("checklists").stream()
    for document in snapshot:
        payload = document.to_dict() or {}
        payload["id"] = document.id
        docs.append(payload)
    return docs


@router.get("/me/{service_slug}", summary="Get a saved user checklist by service slug")
async def get_user_checklist_by_slug(service_slug: str, user=Depends(get_current_user)):
    uid = user["uid"]
    checklist = get_user_checklist(uid, service_slug)
    if not checklist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Checklist for service '{service_slug}' not found for this user",
        )
    return normalize_user_checklist(service_slug, checklist)


@router.post("/me/{service_slug}", status_code=status.HTTP_200_OK, summary="Save the user's checklist progress")
async def save_checklist_for_service(service_slug: str, payload: Dict[str, Any], user=Depends(get_current_user)):
    uid = user["uid"]
    body = dict(payload)
    body["service_slug"] = service_slug
    body["updated_at"] = datetime.utcnow()
    body["created_at"] = body.get("created_at", datetime.utcnow())

    saved = save_user_checklist(uid, service_slug, body)
    return normalize_user_checklist(service_slug, saved)
