from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TermExplanationRequest(BaseModel):
    term: str = Field(..., min_length=2, max_length=100, description="The official/bureaucratic term to simplify")
    context: Optional[str] = Field(default=None, description="Optional certificate or department context, e.g., 'Caste Certificate'")
    language: Optional[str] = Field(default="English", description="Target language: English or Hinglish")


class TermExplanationResponse(BaseModel):
    term: str
    simplified_explanation: str
    real_world_example: str
    actionable_tip: str
    source: str = Field(description="Engine used: 'gemini' or 'knowledge_base'")


class EligibilityInquiryRequest(BaseModel):
    service_slug: str = Field(..., description="Certificate service slug, e.g., 'income-certificate', 'caste-certificate', 'residence-certificate'")
    user_query: str = Field(..., min_length=3, description="Citizen's question describing their background or situation")
    applicant_profile: Optional[Dict[str, Any]] = Field(default=None, description="Optional structured profile attributes")
    language: Optional[str] = Field(default="English", description="Target language: English or Kannada")


class EligibilityInquiryResponse(BaseModel):
    service_slug: str
    service_title: str
    assessment: str = Field(description="Likely Eligible, Conditional / Specific Proof Required, Likely Ineligible, or Needs Information")
    reasoning: str = Field(description="Clear explanation tailored to the citizen's situation")
    required_documents_highlight: List[str] = Field(default_factory=list, description="Documents the citizen specifically needs")
    suggested_action: str = Field(description="Next practical step for the citizen")
    disclaimer: str = Field(default="This is an automated advisory guide based on statutory government guidelines. The final decision rests with the competent issuing authority.")
    source: str = Field(description="Engine used: 'gemini' or 'rules_engine'")
