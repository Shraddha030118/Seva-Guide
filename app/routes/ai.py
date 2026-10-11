from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException

from app.auth import get_current_user
from app.firestore_service import get_service_by_slug, get_service_checklist
from app.schemas.ai import (
    EligibilityInquiryRequest,
    EligibilityInquiryResponse,
    TermExplanationRequest,
    TermExplanationResponse,
)
from app.services.gemini_service import CURATED_TERMS, gemini_service

router = APIRouter(prefix="/ai", tags=["Gemini AI Assistant"])


@router.post(
    "/explain-term",
    response_model=TermExplanationResponse,
    summary="Explain bureaucratic or government terminology in simple language",
)
async def explain_official_term(request: TermExplanationRequest, user=Depends(get_current_user)):
    result = await gemini_service.explain_term(
        term=request.term,
        context=request.context,
        language=request.language,
    )
    return result


@router.post(
    "/check-eligibility",
    response_model=EligibilityInquiryResponse,
    summary="Answer citizen eligibility questions based on official certificate rules",
)
async def check_service_eligibility(request: EligibilityInquiryRequest, user=Depends(get_current_user)):
    service = get_service_by_slug(request.service_slug)
    if not service:
        raise HTTPException(
            status_code=404,
            detail=f"Certificate service '{request.service_slug}' not found",
        )

    checklist = get_service_checklist(request.service_slug)
    response = await gemini_service.evaluate_eligibility(
        service=service,
        checklist=checklist,
        user_query=request.user_query,
        applicant_profile=request.applicant_profile,
    )
    return response


@router.get(
    "/popular-terms",
    response_model=List[Dict[str, str]],
    summary="List common official terms available for instant explanation",
)
async def get_popular_terms(user=Depends(get_current_user)):
    terms = []
    for key, item in CURATED_TERMS.items():
        terms.append({
            "key": key,
            "term": item["term"],
            "short_summary": item["simplified_explanation"][:120] + "...",
        })
    return terms
