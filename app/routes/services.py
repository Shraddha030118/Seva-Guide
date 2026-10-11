from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.auth import get_current_user
from app.firestore_service import (
    get_service_by_slug,
    get_service_checklist as get_service_checklist_data,
    list_services as list_firebase_services,
)

router = APIRouter(prefix="/services", tags=["Certificate Services"])


def normalize_service(service: dict) -> dict:
    if not service:
        return service
    return {
        **service,
        "id": service.get("id") or service.get("slug"),
        "created_at": service.get("created_at", datetime.utcnow()),
        "updated_at": service.get("updated_at", datetime.utcnow()),
    }


def normalize_checklist(service: dict, checklist: dict) -> dict:
    if not checklist:
        return checklist

    return {
        "id": checklist.get("id") or f"checklist-{service.get('slug', 'service')}",
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


@router.get("", summary="List all certificate services")
async def list_services(
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search keyword in title or overview"),
    user=Depends(get_current_user),
):
    services = list_firebase_services(category=category, search=search)
    return [normalize_service(service) for service in services]


@router.get("/{slug}", summary="Get service by slug")
async def get_service(slug: str, user=Depends(get_current_user)):
    service = get_service_by_slug(slug)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Service '{slug}' not found")
    return normalize_service(service)


@router.get("/{slug}/checklist", summary="Get checklist and guide for a service")
async def get_service_checklist_route(slug: str, user=Depends(get_current_user)):
    service = get_service_by_slug(slug)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Certificate service '{slug}' not found")

    checklist = get_service_checklist_data(slug)
    if not checklist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Checklist data for service '{slug}' not found")
    return normalize_checklist(service, checklist)


@router.get("/{slug}/documents", summary="Get document requirements for a service")
async def get_service_documents(slug: str, user=Depends(get_current_user)):
    service = get_service_by_slug(slug)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Certificate service '{slug}' not found")

    checklist = get_service_checklist_data(slug)
    if not checklist:
        return []
    return checklist.get("documents_required", [])
