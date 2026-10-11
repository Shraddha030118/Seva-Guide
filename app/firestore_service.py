from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.firebase import get_firestore_db

DEFAULT_SERVICES: List[Dict[str, Any]] = [
    {
        "slug": "income-certificate",
        "title": "Income Certificate (आय प्रमाण पत्र)",
        "short_description": "Official proof of annual household income for scholarship, fee concession, and welfare benefits.",
        "overview": "Certifies total annual income from all sources. Essential for university scholarships, EWS quota, fee waivers, and state subsidies.",
        "category": "Revenue & Welfare",
        "department": "Revenue Department (Tehsildar / Sub-Divisional Magistrate)",
        "validity_period": "1 Financial Year (April 1 to March 31)",
        "estimated_processing_days": 10,
        "fee": {"amount": 30.0, "currency": "INR"},
        "official_portal_url": "https://serviceonline.gov.in",
        "eligibility_criteria": [
            "Applicant or family must be resident in the Tehsil jurisdiction.",
            "Income from all family members must be declared transparently.",
            "Must possess primary proof of identity and local address.",
        ],
        "tags": ["income", "scholarship", "ews", "revenue"],
        "checklist": {
            "documents_required": [
                {"document_name": "Aadhaar Card", "required": True},
                {"document_name": "Residence Proof", "required": True},
                {"document_name": "Income Declaration", "required": True},
            ],
            "common_mistakes": ["Unverified annual income figures", "Missing residence proof"],
        },
    },
    {
        "slug": "caste-certificate",
        "title": "Caste Certificate (जाति प्रमाण पत्र)",
        "short_description": "Statutory certificate establishing SC, ST, OBC, or SEBC category status for reservation and scheme benefits.",
        "overview": "Definitive proof of belonging to a reserved community under Presidential orders. Required for educational quotas and government recruitment.",
        "category": "Social Justice & Empowerment",
        "department": "District Administration / Revenue Department (SDM / Tehsildar)",
        "validity_period": "Lifetime (SC/ST); Annual / Subject to Creamy Layer (OBC)",
        "estimated_processing_days": 15,
        "fee": {"amount": 30.0, "currency": "INR"},
        "official_portal_url": "https://serviceonline.gov.in",
        "eligibility_criteria": [
            "Applicant must belong to a community notified in the Presidential gazette.",
            "Paternal lineage proof (father/grandfather document) is mandatory.",
            "For OBC Non-Creamy Layer, annual family income must be under ₹8 Lakh.",
        ],
        "tags": ["caste", "reservation", "obc", "sc", "st"],
        "checklist": {
            "documents_required": [
                {"document_name": "Caste Proof", "required": True},
                {"document_name": "Father's Caste Record", "required": True},
                {"document_name": "Address Proof", "required": True},
            ],
            "common_mistakes": ["Using maternal lineage without legal exception", "Missing paternal proof"],
        },
    },
    {
        "slug": "residence-certificate",
        "title": "Residence / Domicile Certificate (मूल निवास प्रमाण पत्र)",
        "short_description": "Official proof of permanent residence or domicile within a specific State or Union Territory.",
        "overview": "Establishes continuous long-term residence within the state. Mandatory for state-quota college seats and civil services recruitment.",
        "category": "Revenue & General Administration",
        "department": "Revenue Department (Tehsildar / District Magistrate)",
        "validity_period": "Lifetime (unless domicile is permanently shifted)",
        "estimated_processing_days": 14,
        "fee": {"amount": 35.0, "currency": "INR"},
        "official_portal_url": "https://serviceonline.gov.in",
        "eligibility_criteria": [
            "Continuous residence in the state for minimum period mandated by state law (typically 3 to 15 years).",
            "Or proof of owning ancestral land/property in the state.",
            "Or born in the state with continuous schooling in the state.",
        ],
        "tags": ["domicile", "residence", "state-quota", "admissions"],
        "checklist": {
            "documents_required": [
                {"document_name": "Address Proof", "required": True},
                {"document_name": "School / Residence Record", "required": True},
                {"document_name": "Parent's Proof", "required": False},
            ],
            "common_mistakes": ["Temporary rental proof mistaken for domicile", "Missing continuity records"],
        },
    },
]


def _normalize_document(document: Any) -> Optional[Dict[str, Any]]:
    if document is None or document.to_dict is None:
        return None

    data = document.to_dict() or {}
    data["id"] = document.id
    return data


def _fallback_services() -> List[Dict[str, Any]]:
    return [dict(service) for service in DEFAULT_SERVICES]


def get_certificates_collection():
    db = get_firestore_db()
    if db is None:
        return None
    return db.collection("certificates")


def get_user_checklist_collection(uid: str):
    db = get_firestore_db()
    if db is None:
        return None
    return db.collection("users").document(uid).collection("checklists")


def list_services(category: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
    db_collection = get_certificates_collection()
    if db_collection is None:
        services = _fallback_services()
    else:
        docs = db_collection.stream()
        services = []

        for document in docs:
            payload = _normalize_document(document)
            if not payload:
                continue
            if payload.get("is_active") is False:
                continue
            services.append(payload)

    if category:
        category_term = category.lower()
        services = [
            service
            for service in services
            if category_term in str(service.get("category", "")).lower()
        ]

    if search:
        search_term = search.lower()
        services = [
            service
            for service in services
            if search_term in str(service.get("title", "")).lower()
            or search_term in str(service.get("overview", "")).lower()
            or search_term in " ".join(str(tag).lower() for tag in service.get("tags", []))
            or search_term in str(service.get("short_description", "")).lower()
        ]

    return sorted(services, key=lambda item: str(item.get("title", "")).lower())


def get_service_by_slug(slug: str) -> Optional[Dict[str, Any]]:
    db_collection = get_certificates_collection()
    if db_collection is None:
        for service in _fallback_services():
            if service.get("slug") == slug:
                return dict(service)
        return None

    document = db_collection.document(slug).get()
    if not document.exists:
        return None
    return _normalize_document(document)


def _build_default_checklist(service: Dict[str, Any]) -> Dict[str, Any]:
    checklist = dict(service.get("checklist") or {})
    slug = str(service.get("slug", "")).lower()

    checklist.setdefault("documents_required", [
        {"document_name": "Identity Proof", "required": True},
        {"document_name": "Address Proof", "required": True},
        {"document_name": "Supporting Declaration", "required": True},
    ])

    checklist.setdefault("application_steps", [
        {"step_no": 1, "title": "Collect documents", "description": "Gather all primary identity, address, and supporting proof required for the application."},
        {"step_no": 2, "title": "Fill the form", "description": "Complete the official certificate form and ensure the details match your government records."},
        {"step_no": 3, "title": "Submit and verify", "description": "Submit the application with self-attested copies and verify status with the local authority."},
    ])

    checklist.setdefault("eligibility_checklist", [
        "I have the required identity and address proof ready.",
        "I understand the local jurisdiction and document requirements.",
        "I am prepared to provide supporting declarations or lineage proof if required.",
    ])

    if "caste" in slug:
        checklist["common_mistakes"] = checklist.get("common_mistakes") or [
            "Using maternal lineage instead of paternal lineage when required.",
            "Submitting old or expired caste documents without renewal.",
        ]
        checklist["helpful_tips"] = checklist.get("helpful_tips") or [
            "Keep both fathers' and grandparents' records ready for verification.",
            "Carry a self-attested copy of all supporting papers to the revenue office.",
        ]
    elif "income" in slug:
        checklist["common_mistakes"] = checklist.get("common_mistakes") or [
            "Using estimated income instead of verified declarations.",
            "Submitting income documents without the latest proof.",
        ]
        checklist["helpful_tips"] = checklist.get("helpful_tips") or [
            "Match income figures across salary slips, tax documents, and declarations.",
            "Prepare a current address proof and family income summary before applying.",
        ]
    else:
        checklist["common_mistakes"] = checklist.get("common_mistakes") or [
            "Using a temporary address instead of permanent residence proof.",
            "Missing continuity proof for the required residence period.",
        ]
        checklist["helpful_tips"] = checklist.get("helpful_tips") or [
            "Check the local residence duration requirement before filing.",
            "Keep a chronological set of address records ready for verification.",
        ]

    checklist.setdefault("faqs", [
        {"question": "What if my submitted document is unclear or missing a page?", "answer": "Submit a clear, self-attested scan and include the missing page before verification."},
        {"question": "How long does the application generally take?", "answer": "Most applications are reviewed within a few business days, though local verification may extend the timeline."},
    ])
    return checklist


def get_service_checklist(slug: str) -> Optional[Dict[str, Any]]:
    service = get_service_by_slug(slug)
    if not service:
        return None
    if service.get("checklist"):
        return _build_default_checklist(service)
    return _build_default_checklist(service)


def save_user_checklist(uid: str, service_slug: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    collection = get_user_checklist_collection(uid)
    if collection is None:
        return dict(payload)
    ref = collection.document(service_slug)
    ref.set(payload, merge=True)
    saved = ref.get()
    return _normalize_document(saved) or payload


def get_user_checklist(uid: str, service_slug: str) -> Optional[Dict[str, Any]]:
    collection = get_user_checklist_collection(uid)
    if collection is None:
        return None
    document = collection.document(service_slug).get()
    if not document.exists:
        return None
    return _normalize_document(document)
