from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.common import PyObjectId


class FeeInfo(BaseModel):
    amount: float = Field(..., description="Application fee in local currency (e.g. 30.0)")
    currency: str = Field(default="INR", description="Currency code")
    notes: Optional[str] = Field(default=None, description="Fee breakdown or exemption details")


class ServiceBase(BaseModel):
    slug: str = Field(..., description="Unique slug for the service, e.g. income-certificate")
    title: str = Field(..., description="Full official title of the certificate service")
    short_description: str = Field(..., description="Brief one-line overview of the service")
    overview: str = Field(..., description="Detailed description of what the certificate is used for")
    category: str = Field(..., description="Category: Revenue, Welfare, Civil, Domicile, etc.")
    department: str = Field(..., description="Issuing authority or department name")
    validity_period: str = Field(..., description="Certificate validity duration, e.g. 1 Year, Lifetime")
    estimated_processing_days: int = Field(..., description="Expected processing duration in days")
    fee: FeeInfo = Field(..., description="Fee structure details")
    official_portal_url: Optional[str] = Field(default=None, description="Direct URL to official portal for application")
    eligibility_criteria: List[str] = Field(default_factory=list, description="Key requirements to be eligible")
    tags: List[str] = Field(default_factory=list, description="Search and filter tags")
    is_active: bool = Field(default=True, description="Whether this service is currently active")


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    short_description: Optional[str] = None
    overview: Optional[str] = None
    category: Optional[str] = None
    department: Optional[str] = None
    validity_period: Optional[str] = None
    estimated_processing_days: Optional[int] = None
    fee: Optional[FeeInfo] = None
    official_portal_url: Optional[str] = None
    eligibility_criteria: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class ServiceInDB(ServiceBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
        arbitrary_types_allowed=True
    )


class ServiceResponse(ServiceBase):
    id: str = Field(..., description="MongoDB string Object ID")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )
