import json
import logging
import re
from typing import Optional, Dict, Any, List
from app.config import settings
from app.schemas.ai import TermExplanationResponse, EligibilityInquiryResponse

logger = logging.getLogger("sevaguide.ai")

# Curated knowledge base of common Indian bureaucratic terms for instant fallback
CURATED_TERMS: Dict[str, Dict[str, str]] = {
    "domicile": {
        "term": "Domicile (अधिवास)",
        "simplified_explanation": "A legal concept that refers to the permanent home state where you intend to live permanently. Unlike a temporary rental residence, you can legally have only one domicile state at any time in India.",
        "real_world_example": "If you move from Bihar to Karnataka for a 2-year job, your continuous stay may be in Karnataka, but your domicile remains Bihar unless you establish permanent roots.",
        "actionable_tip": "Do not apply for domicile certificates in two states simultaneously, as holding dual domicile is illegal."
    },
    "creamy layer": {
        "term": "Creamy Layer (क्रीमी लेयर)",
        "simplified_explanation": "A category within OBC (Other Backward Classes) whose household annual gross income exceeds ₹8 Lakhs or whose parents hold senior government positions. They are not eligible for reservation benefits.",
        "real_world_example": "If an OBC student's parents earn ₹9.5 Lakhs annually, they fall in the Creamy Layer and must apply in the General (Unreserved) category.",
        "actionable_tip": "If your parental income is below ₹8 Lakhs, you must obtain an 'OBC Non-Creamy Layer (NCL)' certificate with updated income proof."
    },
    "non-creamy layer": {
        "term": "Non-Creamy Layer (NCL)",
        "simplified_explanation": "OBC applicants whose family income is below ₹8 Lakhs per year. This status qualifies candidates for affirmative action quotas in central and state educational institutions and government jobs.",
        "real_world_example": "An OBC candidate whose parents run a small grocery shop earning ₹4 Lakhs/yr qualifies for Non-Creamy Layer fee concessions and quota seats.",
        "actionable_tip": "NCL status is tied to income, so this certificate must usually be renewed every 1 to 3 financial years."
    },
    "self-attestation": {
        "term": "Self-Attestation (स्व-प्रमाणित)",
        "simplified_explanation": "The process where you certify that a photocopy of your original document is true and genuine by signing it yourself, eliminating the need to visit a Gazetted Officer or Notary.",
        "real_world_example": "Before scanning your Aadhaar photocopy, write 'Self Attested', sign your name, and write today's date across the blank area.",
        "actionable_tip": "Always sign across the photocopy in a clear blank space without obscuring your photo, ID number, or address."
    },
    "tehsildar": {
        "term": "Tehsildar / Tahsildar (तहसीलदार)",
        "simplified_explanation": "A Class-II gazetted administrative revenue officer in charge of a Tehsil/Taluk who holds statutory powers to issue income, caste, and residence certificates.",
        "real_world_example": "When your application passes through the village patwari, the Tehsildar reviews the field report and applies their digital signature.",
        "actionable_tip": "Always ensure your application is submitted under the correct Tehsil corresponding to your permanent family residence."
    },
    "patwari": {
        "term": "Patwari / Lekhpal (पटवारी / लेखपाल)",
        "simplified_explanation": "A village-level revenue officer responsible for maintaining local land records, crop surveys, and conducting ground-level verification of family income and caste claims.",
        "real_world_example": "The Patwari may visit your locality or call you to inspect original electricity bills, family ration cards, or talk to neighbors.",
        "actionable_tip": "Keep original hard copies ready for verification when the Patwari conducts the locality inquiry."
    },
    "paternal lineage": {
        "term": "Paternal Lineage (पितृ पक्ष)",
        "simplified_explanation": "Tracing legal lineage and social category strictly through your father, paternal grandfather, or father's blood relatives.",
        "real_world_example": "To get a caste certificate, you must provide your father's or paternal uncle's school leaving certificate or caste certificate, not your mother's.",
        "actionable_tip": "If your father does not hold a digital caste certificate, obtain his school admission register extract (Dakhil-Kharij) where caste is stated."
    },
    "khasra": {
        "term": "Khasra / Khatauni (खसरा / खतौनी)",
        "simplified_explanation": "Legal land revenue documents in India that specify parcel numbers, land area, ownership titles, and agricultural crop cultivation history.",
        "real_world_example": "If your family earns income from farming, the Revenue Department requires the Khatauni extract to verify annual agricultural income.",
        "actionable_tip": "You can download certified computerized copies of Khatauni from your state's Bhulekh land records portal."
    },
    "vamshavruksha": {
        "term": "Vamshavruksha / Pedigree Tree (वंशावली)",
        "simplified_explanation": "A certified genealogical tree diagram detailing blood relations across 2 to 3 generations to establish connection with an ancestor who held a caste or land record.",
        "real_world_example": "Used when your father has passed away or has no certificate, proving you are the grandson of someone who held an authentic historical caste record.",
        "actionable_tip": "Get the genealogy chart signed by the local Gram Panchayat Secretary or revenue inspector before submitting."
    }
}


class GeminiService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL
        self._client = None
        self._init_client()

    def _init_client(self):
        if self.api_key and self.api_key.strip():
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key.strip())
                logger.info(f"Gemini AI Client initialized successfully with model {self.model_name}")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini Client: {e}. Falling back to rule-based engine.")
                self._client = None
        else:
            logger.info("GEMINI_API_KEY is not configured. SevaGuide AI running in offline/knowledge-base mode.")

    async def explain_term(self, term: str, context: Optional[str] = None, language: str = "English") -> TermExplanationResponse:
        """
        Explains complex administrative or government jargon in simple language for citizens.
        Supports English and Kannada (ಕನ್ನಡ).
        Uses Gemini API when configured, otherwise uses the curated civil services knowledge base.
        """
        clean_term = term.strip().lower()
        is_kannada = "kannada" in (language or "").lower()

        # Curated Kannada dictionary mappings
        CURATED_KANNADA = {
            "domicile": {
                "term": "Domicile (ವಾಸಸ್ಥಳ / ಅಧಿವಾಸ ಪ್ರಮಾಣ)",
                "simplified_explanation": "ನೀವು ಒಂದು ರಾಜ್ಯದಲ್ಲಿ ಶಾಶ್ವತವಾಗಿ ನೆಲೆಸಿರುವಿರಿ ಎಂಬುದನ್ನು ದೃಢೀಕರಿಸುವ ಕಾನೂನುಬದ್ಧ ದಾಖಲೆ. ಭಾರತದಲ್ಲಿ ಒಬ್ಬ ನಾಗರಿಕರು ಏಕಕಾಲದಲ್ಲಿ ಕೇವಲ ಒಂದು ರಾಜ್ಯದ ವಾಸಸ್ಥಳ ಪ್ರಮಾಣವನ್ನು ಮಾತ್ರ ಹೊಂದಲು ಸಾಧ್ಯ.",
                "real_world_example": "ಕರ್ನಾಟಕದಲ್ಲಿ ರಾಜ್ಯ ಕೋಟಾದ ಇಂಜಿನಿಯರಿಂಗ್ ಅಥವಾ ವೈದ್ಯಕೀಯ ಸೀಟು ಪಡೆಯಲು ಕನಿಷ್ಠ 7-10 ವರ್ಷಗಳ ನಿರಂತರ ವ್ಯಾಸಂಗ ಅಥವಾ ವಾಸದ ಪುರಾವೆ ಅಗತ್ಯ.",
                "actionable_tip": "ಎರಡು ಬೇರೆ ಬೇರೆ ರಾಜ್ಯಗಳಲ್ಲಿ ಏಕಕಾಲದಲ್ಲಿ ವಾಸಸ್ಥಳ ಪ್ರಮಾಣ ಪತ್ರಕ್ಕೆ ಅರ್ಜಿ ಸಲ್ಲಿಸುವುದು ಕಾನೂನುಬಾಹಿರ."
            },
            "creamy layer": {
                "term": "Creamy Layer (ಕೆನೆ ಪದರ)",
                "simplified_explanation": "ಹಿಂದುಳಿದ ವರ್ಗಗಳ (OBC) ಕುಟುಂಬಗಳಲ್ಲಿ ವಾರ್ಷಿಕ ಒಟ್ಟು ಆದಾಯ ₹8 ಲಕ್ಷಕ್ಕಿಂತ ಹೆಚ್ಚಿರುವ ಅಥವಾ ಪೋಷಕರು ಉನ್ನತ ಸರ್ಕಾರಿ ಹುದ್ದೆಯಲ್ಲಿರುವ ವರ್ಗ. ಇವರಿಗೆ ಮೀಸಲಾತಿ ಸೌಲಭ್ಯಗಳು ಸಿಗುವುದಿಲ್ಲ.",
                "real_world_example": "ಪೋಷಕರ ವಾರ್ಷಿಕ ಆದಾಯ ₹9 ಲಕ್ಷವಾಗಿದ್ದರೆ, ಅವರು ಸಾಮಾನ್ಯ (General) ವರ್ಗದಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಬೇಕಾಗುತ್ತದೆ.",
                "actionable_tip": "ನಿಮ್ಮ ಕುಟುಂಬದ ಆದಾಯ ₹8 ಲಕ್ಷಕ್ಕಿಂತ ಕಡಿಮೆಯಿದ್ದರೆ 'ನಾನ್-ಕ್ರೀಮಿ ಲೇಯರ್ (NCL)' ಪ್ರಮಾಣ ಪತ್ರ ಪಡೆಯಿರಿ."
            },
            "non-creamy layer": {
                "term": "Non-Creamy Layer (ಕೆನೆರಹಿತ ಪದರ - NCL)",
                "simplified_explanation": "ಹಿಂದುಳಿದ ವರ್ಗಗಳ (OBC) ಕುಟುಂಬಗಳ ವಾರ್ಷಿಕ ಆದಾಯ ₹8 ಲಕ್ಷಕ್ಕಿಂತ ಕಡಿಮೆಯಿರುವ ಅರ್ಹ ವರ್ಗ. ಇವರಿಗೆ ಶೈಕ್ಷಣಿಕ ಸೀಟು ಮತ್ತು ಉದ್ಯೋಗಗಳಲ್ಲಿ ಮೀಸಲಾತಿ ಸೌಲಭ್ಯ ಲಭ್ಯವಿರುತ್ತದೆ.",
                "real_world_example": "ಸಣ್ಣ ವ್ಯಾಪಾರ ಅಥವಾ ಕೃಷಿ ಮಾಡುವ ಪೋಷಕರ ಆದಾಯ ₹4 ಲಕ್ಷವಾಗಿದ್ದರೆ, ಅವರಿಗೆ ಶುಲ್ಕ ವಿನಾಯಿತಿ ಮತ್ತು ಮೀಸಲಾತಿ ಅನ್ವಯಿಸುತ್ತದೆ.",
                "actionable_tip": "ಇದು ಆದಾಯ ಆಧಾರಿತವಾಗಿರುವುದರಿಂದ ಸಾಮಾನ್ಯವಾಗಿ ಪ್ರತಿ 1 ರಿಂದ 3 ವರ್ಷಗಳಿಗೊಮ್ಮೆ ನವೀಕರಿಸಬೇಕು."
            },
            "self-attestation": {
                "term": "Self-Attestation (ಸ್ವಯಂ ದೃಢೀಕರಣ)",
                "simplified_explanation": "ದಾಖಲೆಯ ಜೆರಾಕ್ಸ್ ಪ್ರತಿ ಮೇಲೆ ನೀವೇ 'Self Attested' ಎಂದು ಬರೆದು ಸಹಿ ಮಾಡುವ ಸರಳ ಪ್ರಕ್ರಿಯೆ. ಗೆಜೆಟೆಡ್ ಅಧಿಕಾರಿ ಅಥವಾ ನೋಟರಿ ಬಳಿ ಹೋಗುವ ಅಗತ್ಯವಿಲ್ಲ.",
                "real_world_example": "ಆಧಾರ್ ಕಾರ್ಡ್ ಜೆರಾಕ್ಸ್ ಪ್ರತಿಯ ಖಾಲಿ ಜಾಗದಲ್ಲಿ ನಿಮ್ಮ ಸಹಿ ಮತ್ತು ದಿನಾಂಕವನ್ನು ನಮೂದಿಸಿ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
                "actionable_tip": "ನಿಮ್ಮ ಫೋಟೋ, ಹೆಸರು ಅಥವಾ ಆಧಾರ್ ಸಂಖ್ಯೆಯನ್ನು ಮರೆಮಾಡದಂತೆ ಖಾಲಿ ಜಾಗದಲ್ಲಿ ಸಹಿ ಮಾಡಿ."
            },
            "tehsildar": {
                "term": "Tehsildar (ತಹಶೀಲ್ದಾರ್)",
                "simplified_explanation": "ತಾಲ್ಲೂಕು ಮಟ್ಟದ ಕಂದಾಯ ಮುಖ್ಯಸ್ಥರು. ಆದಾಯ, ಜಾತಿ ಮತ್ತು ವಾಸಸ್ಥಳ ಪ್ರಮಾಣ ಪತ್ರಗಳನ್ನು ಪರಿಶೀಲಿಸಿ ಅನುಮೋದಿಸುವ ಅಧಿಕಾರ ಇವರಿಗೆ ಇರುತ್ತದೆ.",
                "real_world_example": "ಗ್ರಾಮ ಆಡಳಿತಾಧಿಕಾರಿ ನೀಡಿದ ವರದಿಯನ್ನು ಪರಿಶೀಲಿಸಿ ತಹಶೀಲ್ದಾರರು ಡಿಜಿಟಲ್ ಸಹಿ ಮೂಲಕ ಪ್ರಮಾಣ ಪತ್ರ ನೀಡುತ್ತಾರೆ.",
                "actionable_tip": "ನಿಮ್ಮ ಕಾಯಂ ವಾಸಸ್ಥಳವಿರುವ ಸರಿಯಾದ ತಾಲ್ಲೂಕಿನಲ್ಲೇ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ."
            },
            "patwari": {
                "term": "Patwari / Village Admin Officer (ಗ್ರಾಮ ಆಡಳಿತಾಧಿಕಾರಿ / VAO)",
                "simplified_explanation": "ಗ್ರಾಮ ಅಥವಾ ಬಡಾವಣೆ ಮಟ್ಟದಲ್ಲಿ ಜಮೀನು ದಾಖಲೆಗಳು ಮತ್ತು ಸ್ಥಳೀಯ ಆದಾಯ ತನಿಖೆ ನಡೆಸುವ ಕಂದಾಯ ಅಧಿಕಾರಿ.",
                "real_world_example": "ಸ್ಥಳ ಪರಿಶೀಲನೆಗೆ ಗ್ರಾಮ ಆಡಳಿತಾಧಿಕಾರಿಗಳು ಬಂದಾಗ ರೇಷನ್ ಕಾರ್ಡ್, ಕರೆಂಟ್ ಬಿಲ್ ಮೂಲ ಪ್ರತಿಗಳನ್ನು ತೋರಿಸಬೇಕು.",
                "actionable_tip": "ಪರಿಶೀಲನೆಗೆ ಅಧಿಕಾರಿಗಳು ಕೋರಿದಾಗ ತೋರಿಸಲು ಮೂಲ ದಾಖಲೆಗಳನ್ನು ಸಿದ್ಧವಾಗಿಟ್ಟುಕೊಳ್ಳಿ."
            }
        }

        # Check curated fallback dictionary
        target_dict = CURATED_KANNADA if is_kannada else CURATED_TERMS
        for key, entry in target_dict.items():
            if key in clean_term or clean_term in key:
                return TermExplanationResponse(
                    term=entry["term"],
                    simplified_explanation=entry["simplified_explanation"],
                    real_world_example=entry["real_world_example"],
                    actionable_tip=entry["actionable_tip"],
                    source="knowledge_base"
                )

        # If Gemini client is active, query the model in requested language
        if self._client:
            try:
                lang_instruction = "Respond completely in natural, easy-to-understand Kannada (ಕನ್ನಡ)." if is_kannada else "Respond in plain simple English."
                prompt = f"""You are SevaGuide AI, an assistant helping Indian citizens understand government paperwork, certificate applications, and bureaucratic terms.
Explain the following official or administrative term in very simple, plain language that an everyday citizen or first-time applicant can easily understand:
Term: "{term}"
Context: "{context or 'Indian Government Civil Services & Certificates'}"
Target Language: "{'Kannada (ಕನ್ನಡ)' if is_kannada else 'English'}"
{lang_instruction}

Respond ONLY with a valid JSON object strictly matching this schema:
{{
  "term": "{term}",
  "simplified_explanation": "A clear, plain-language 2-3 sentence definition without jargon in the target language.",
  "real_world_example": "A realistic practical example showing how this term affects a certificate application or citizen.",
  "actionable_tip": "A practical takeaway or advice for the applicant."
}}
"""
                response = self._client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )

                text = response.text.strip()
                text = re.sub(r"^```json\s*", "", text)
                text = re.sub(r"\s*```$", "", text)
                data = json.loads(text)

                return TermExplanationResponse(
                    term=data.get("term", term),
                    simplified_explanation=data.get("simplified_explanation", ""),
                    real_world_example=data.get("real_world_example", ""),
                    actionable_tip=data.get("actionable_tip", ""),
                    source="gemini"
                )
            except Exception as e:
                logger.error(f"Error invoking Gemini API for term explanation: {e}")

        # Graceful dynamic fallback when Gemini is offline
        if is_kannada:
            return TermExplanationResponse(
                term=term,
                simplified_explanation=f"'{term}' ಎಂಬುದು ಸರ್ಕಾರಿ ಪ್ರಮಾಣ ಪತ್ರ ಪ್ರಕ್ರಿಯೆಯಲ್ಲಿ ಬಳಸಲಾಗುವ ಅಧಿಕೃತ ಕಂದಾಯ ಪದವಾಗಿದೆ. ಅರ್ಜಿದಾರರ ಅರ್ಹತೆಯನ್ನು ಸಾಬೀತುಪಡಿಸಲು ಈ ನಿಯಮ ಅನ್ವಯಿಸುತ್ತದೆ.",
                real_world_example=f"ಸ್ಥಳ ಪರಿಶೀಲನೆಯ ಸಮಯದಲ್ಲಿ ಅಧಿಕಾರಿಗಳು {term} ಗೆ ಸಂಬಂಧಿಸಿದ ಪುರಾವೆಗಳನ್ನು ಪರಿಶೀಲಿಸಬಹುದು.",
                actionable_tip="ಅರ್ಜಿ ಸಲ್ಲಿಸುವ ಮೊದಲು ಅಗತ್ಯವಿರುವ ಪೂರಕ ದಾಖಲೆಗಳನ್ನು ಸಿದ್ಧಪಡಿಸಿಕೊಳ್ಳಿ.",
                source="knowledge_base"
            )

        return TermExplanationResponse(
            term=term.title(),
            simplified_explanation=(
                f"'{term.title()}' is an official administrative term used by the government in certificate processing. "
                "It generally specifies a legal requirement, designated authority, or documentation criterion "
                "that the applicant must fulfill to establish authentic eligibility."
            ),
            real_world_example=(
                f"During field verification, the revenue office or verification inspector may check evidence related to {term.lower()} "
                "before sanctioning the certificate."
            ),
            actionable_tip="Check the document checklist for your certificate to ensure you have attached the corresponding supporting proof.",
            source="knowledge_base"
        )

    async def evaluate_eligibility(
        self,
        service: Dict[str, Any],
        checklist: Optional[Dict[str, Any]],
        user_query: str,
        applicant_profile: Optional[Dict[str, Any]] = None,
        language: str = "English"
    ) -> EligibilityInquiryResponse:
        """
        Evaluates a citizen's eligibility question against official criteria using Gemini AI,
        grounded in the database schema of the certificate.
        """
        service_title = service.get("title", "Certificate Service")
        criteria = service.get("eligibility_criteria", [])
        docs = [d.get("document_name") for d in (checklist.get("documents_required", []) if checklist else [])]

        if self._client:
            try:
                grounding_context = f"""
Certificate: {service_title}
Issuing Authority: {service.get('department')}
Validity: {service.get('validity_period')}
Statutory Eligibility Criteria:
{json.dumps(criteria, indent=2)}

Required Documents:
{json.dumps(docs, indent=2)}

Common Rejection Pitfalls:
{json.dumps(checklist.get('common_mistakes', []) if checklist else [], indent=2)}
"""
                prompt = f"""You are SevaGuide AI, an official citizen assistance expert.
Evaluate whether the citizen is eligible for the certificate based on their inquiry and the official government requirements.

{grounding_context}

Citizen Question: "{user_query}"
Citizen Profile Details: {json.dumps(applicant_profile or {})}

Provide a structured assessment. Respond ONLY with a valid JSON object matching this schema:
{{
  "assessment": "Likely Eligible | Conditional / Specific Proof Required | Likely Ineligible | Needs Clarification",
  "reasoning": "Clear explanation in 2-4 sentences explaining why they are or are not eligible based on government criteria.",
  "required_documents_highlight": ["List of 2 to 4 crucial documents the citizen must arrange"],
  "suggested_action": "Specific concrete next step the applicant should take right now."
}}
"""
                response = self._client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )

                text = response.text.strip()
                text = re.sub(r"^```json\s*", "", text)
                text = re.sub(r"\s*```$", "", text)
                data = json.loads(text)

                return EligibilityInquiryResponse(
                    service_slug=service.get("slug"),
                    service_title=service_title,
                    assessment=data.get("assessment", "Conditional / Specific Proof Required"),
                    reasoning=data.get("reasoning", "Based on the provided information, your eligibility depends on submitting acceptable supporting documentation."),
                    required_documents_highlight=data.get("required_documents_highlight", docs[:3]),
                    suggested_action=data.get("suggested_action", "Gather your proof of identity, address, and supporting revenue records."),
                    source="gemini"
                )
            except Exception as e:
                logger.error(f"Error invoking Gemini API for eligibility inquiry: {e}")

        # Deterministic rules-based advisor when Gemini is offline
        slug = service.get("slug", "")
        q_lower = user_query.lower()

        assessment = "Conditional / Specific Proof Required"
        reasoning = f"To qualify for {service_title}, you must fulfill all statutory criteria: {'; '.join(criteria[:2])}."
        suggested_action = "Prepare your identity proof and primary supporting certificates before applying on the official portal."

        if "income" in slug:
            if "student" in q_lower:
                reasoning = "Students are generally dependents, so your eligibility and income limit will be assessed based on your parents' or legal guardian's total household income."
                suggested_action = "Obtain your parents' latest salary slips, ITR, or Gram Panchayat income declaration."
            elif any(w in q_lower for w in ["8 lakh", "ews", "scholarship"]):
                reasoning = "If your total family gross annual income from all sources is within the specified ceiling, you qualify for an Income Certificate and related welfare concessions."
                suggested_action = "Calculate income from salary, agriculture, and business, then draft the self-declaration affidavit."
        elif "caste" in slug:
            if "mother" in q_lower:
                assessment = "Likely Ineligible / Special Legal Exception Required"
                reasoning = "Under standard Indian civil regulations, caste is inherited strictly through the paternal lineage (father's family). Maternal caste is only permitted under exceptional court orders."
                suggested_action = "Trace your father's or grandfather's school records or ancestral land records indicating caste."
            else:
                reasoning = "You are eligible if your community is notified in the Central or State reservation gazette and you have documentary proof of paternal blood lineage."
                suggested_action = "Obtain certified copies of your father's or paternal relative's caste certificate or school leaving certificate."
        elif "residence" in slug:
            if any(w in q_lower for w in ["15 year", "10 year", "born", "school"]):
                assessment = "Likely Eligible"
                reasoning = "You meet the standard residential longevity requirement (continuous schooling or 5-15 years stay in the state)."
                suggested_action = "Compile school transfer certificates or consecutive utility bills demonstrating continuous stay."
            elif any(w in q_lower for w in ["college", "1 year", "2 year", "temporary"]):
                assessment = "Conditional / Specific Proof Required"
                reasoning = "Temporary stay for college or temporary employment usually does not grant permanent domicile unless continuous minimum tenure (typically 5 to 15 years) is established."
                suggested_action = "Check if your parents hold permanent property or ancestral domicile in this state."

        return EligibilityInquiryResponse(
            service_slug=slug,
            service_title=service_title,
            assessment=assessment,
            reasoning=reasoning,
            required_documents_highlight=docs[:3] if docs else ["Proof of Identity", "Proof of Address"],
            suggested_action=suggested_action,
            source="rules_engine"
        )


gemini_service = GeminiService()
