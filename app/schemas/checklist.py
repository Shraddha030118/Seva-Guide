from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.common import PyObjectId


class DocumentRequirement(BaseModel):
    document_name: str = Field(..., description="Name of required document, e.g., Aadhaar Card")
    category: str = Field(..., description="Document category: Identity, Address, Income, Age, Category, Photo")
    accepted_options: List[str] = Field(default_factory=list, description="Alternative acceptable documents")
    is_mandatory: bool = Field(default=True, description="Whether document is strictly mandatory")
    description: Optional[str] = Field(default=None, description="Detailed explanation of requirements")
    format_guidelines: Optional[str] = Field(default=None, description="Format, size, and self-attestation instructions")


class ApplicationStep(BaseModel):
    step_number: int = Field(..., description="Step order sequence number starting from 1")
    phase: str = Field(..., description="Phase name: Preparation, Portal Registration, Form Filing, Verification, Download")
    title: str = Field(..., description="Title of the step")
    description: str = Field(..., description="Detailed instructions for completing this step")
    action_items: List[str] = Field(default_factory=list, description="Actionable checklist items for the user")
    estimated_time: str = Field(..., description="Estimated time to complete this step (e.g., 15 mins)")
    online_or_offline: str = Field(default="Online", description="Online, Offline, or Hybrid")


class FAQItem(BaseModel):
    question: str = Field(..., description="Commonly asked question by applicants")
    answer: str = Field(..., description="Clear answer or solution")


class ChecklistBase(BaseModel):
    service_slug: str = Field(..., description="Slug of the service this checklist belongs to")
    service_title: str = Field(..., description="Title of the service")
    documents_required: List[DocumentRequirement] = Field(default_factory=list, description="Mandatory and optional documents")
    application_steps: List[ApplicationStep] = Field(default_factory=list, description="Step-by-step guidance flow")
    eligibility_checklist: List[str] = Field(default_factory=list, description="Checklist items to self-verify eligibility")
    common_mistakes: List[str] = Field(default_factory=list, description="Frequent rejection reasons to avoid")
    helpful_tips: List[str] = Field(default_factory=list, description="Pro tips for faster processing")
    faqs: List[FAQItem] = Field(default_factory=list, description="Frequently asked questions")


class ChecklistCreate(ChecklistBase):
    pass


class ChecklistUpdate(BaseModel):
    documents_required: Optional[List[DocumentRequirement]] = None
    application_steps: Optional[List[ApplicationStep]] = None
    eligibility_checklist: Optional[List[str]] = None
    common_mistakes: Optional[List[str]] = None
    helpful_tips: Optional[List[str]] = None
    faqs: Optional[List[FAQItem]] = None


class ChecklistInDB(ChecklistBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
        arbitrary_types_allowed=True
    )


class ChecklistResponse(ChecklistBase):
    id: str = Field(..., description="MongoDB string Object ID")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )
