"""
Initial seed data for SevaGuide's three core certificate services:
1. Income Certificate
2. Caste Certificate
3. Residence / Domicile Certificate
"""

SERVICES_SEED = [
    {
        "slug": "income-certificate",
        "title": "Income Certificate (आय प्रमाण पत्र)",
        "short_description": "Official proof of annual household income for scholarship, fee concession, and welfare benefits.",
        "overview": (
            "An Income Certificate is an official government document certifying the total annual "
            "income of an individual or their household from all sources (salary, agriculture, business, etc.). "
            "It is required to access government fee waivers, welfare pensions, tertiary scholarships, "
            "subsidized food grain cards, and reservation benefits under the Economically Weaker Section (EWS)."
        ),
        "category": "Revenue & Welfare",
        "department": "Revenue Department (Tehsildar / Sub-Divisional Magistrate)",
        "validity_period": "1 Financial Year (April 1 to March 31)",
        "estimated_processing_days": 10,
        "fee": {
            "amount": 30.0,
            "currency": "INR",
            "notes": "Nominal government statutory fee ₹30. CSC/Kiosk convenience fee may range from ₹15 to ₹20."
        },
        "official_portal_url": "https://serviceonline.gov.in",
        "eligibility_criteria": [
            "Applicant or their family must be resident within the territorial jurisdiction of the issuing authority.",
            "Income from all earning family members and all sources must be declared transparently.",
            "Must possess primary proof of identity and local address."
        ],
        "tags": ["revenue", "scholarship", "ews", "welfare", "financial-aid"],
        "is_active": True
    },
    {
        "slug": "caste-certificate",
        "title": "Caste Certificate (जाति प्रमाण पत्र)",
        "short_description": "Statutory certificate establishing SC, ST, OBC, or SEBC category status for reservation and scheme benefits.",
        "overview": (
            "A Caste Certificate serves as definitive legal proof that an individual belongs to a particular "
            "Scheduled Caste (SC), Scheduled Tribe (ST), or Other Backward Class (OBC) recognized by the "
            "Constitution of India. It enables affirmative action benefits including educational institution "
            "reservations, competitive exam age relaxations, government employment quotas, and specialized subsidies."
        ),
        "category": "Social Justice & Empowerment",
        "department": "District Administration / Revenue Department (SDM / Tehsildar)",
        "validity_period": "Lifetime (SC/ST); Annual / Subject to Creamy Layer review (OBC Non-Creamy Layer)",
        "estimated_processing_days": 15,
        "fee": {
            "amount": 30.0,
            "currency": "INR",
            "notes": "Statutory fee ₹30. No charge for BPL card holders in many states."
        },
        "official_portal_url": "https://serviceonline.gov.in",
        "eligibility_criteria": [
            "Applicant must belong to a caste or community notified in the Presidential Order or State Government gazette.",
            "Lineage proof (paternal caste document of father, grandfather, or blood relative) must be available.",
            "For OBC Non-Creamy Layer (NCL), family income must not exceed the specified threshold (currently ₹8 Lakh/annum)."
        ],
        "tags": ["reservation", "education", "employment", "obc", "sc-st", "welfare"],
        "is_active": True
    },
    {
        "slug": "residence-certificate",
        "title": "Residence / Domicile Certificate (मूल निवास प्रमाण पत्र)",
        "short_description": "Official proof of permanent residence or domicile within a specific State or Union Territory.",
        "overview": (
            "A Residence or Domicile Certificate proves that a citizen has lived continuously in a particular "
            "state or locality for the statutory period (typically 3 to 15 years depending on the state). "
            "It is mandatory for state-quota university admissions, state civil services recruitment, "
            "allotment of housing under state welfare boards, and localized government tender bidding."
        ),
        "category": "Revenue & General Administration",
        "department": "Revenue Department (Tehsildar / District Magistrate)",
        "validity_period": "Lifetime (unless the holder permanently relocates their domicile to another state)",
        "estimated_processing_days": 14,
        "fee": {
            "amount": 35.0,
            "currency": "INR",
            "notes": "State administrative charge ₹35. Citizen facilitation centers may add ₹10 scanning fee."
        },
        "official_portal_url": "https://serviceonline.gov.in",
        "eligibility_criteria": [
            "Continuous residence in the respective state/UT for the minimum period mandated by state law (usually 3 to 15 years).",
            "Or proof of owning immovable ancestral property/land in the jurisdiction.",
            "Or applicant was born in the state and completed basic school education within it."
        ],
        "tags": ["domicile", "residence", "state-quota", "local-preference", "admissions"],
        "is_active": True
    }
]

CHECKLISTS_SEED = [
    {
        "service_slug": "income-certificate",
        "service_title": "Income Certificate",
        "documents_required": [
            {
                "document_name": "Proof of Identity",
                "category": "Identity",
                "accepted_options": ["Aadhaar Card", "Voter ID (EPIC)", "Passport", "Driving License"],
                "is_mandatory": True,
                "description": "Clear government-issued photo identity with matching name and DOB.",
                "format_guidelines": "Scanned PDF or JPEG, under 2 MB, self-attested."
            },
            {
                "document_name": "Proof of Address",
                "category": "Address",
                "accepted_options": ["Ration Card", "Electricity Bill (last 3 months)", "Registered Rent Agreement", "Water Bill"],
                "is_mandatory": True,
                "description": "Demonstrates current place of stay within the Tehsildar's jurisdiction.",
                "format_guidelines": "Scanned PDF, readable consumer number and applicant/guardian name."
            },
            {
                "document_name": "Income Proof / Salary Slip",
                "category": "Income",
                "accepted_options": ["Latest 3-Month Salary Slips + Form 16", "Income Tax Returns (ITR-V)", "Gram Panchayat / Ward Councillor Certificate", "Land Revenue Khasra/Khatauni for agricultural income"],
                "is_mandatory": True,
                "description": "Official proof supporting the declared annual income figure.",
                "format_guidelines": "Original signed employer letter or officially stamped revenue slip."
            },
            {
                "document_name": "Self-Declaration / Income Affidavit",
                "category": "Affidavit",
                "accepted_options": ["Notarized Stamp Paper Affidavit (₹10 - ₹50)", "State E-District Format Self-Declaration"],
                "is_mandatory": True,
                "description": "Sworn statement affirming all declared earnings from all sources are truthful.",
                "format_guidelines": "Signed by applicant (or guardian if applicant is minor)."
            },
            {
                "document_name": "Recent Passport Size Photograph",
                "category": "Photo",
                "accepted_options": ["Color photo with white or light background"],
                "is_mandatory": True,
                "description": "Taken within the last 6 months, facing camera straight.",
                "format_guidelines": "JPEG format, dimensions 3.5cm x 4.5cm, file size between 20 KB and 100 KB."
            }
        ],
        "application_steps": [
            {
                "step_number": 1,
                "phase": "Preparation",
                "title": "Compile & Self-Attest Verification Documents",
                "description": "Gather all income slips, identity proofs, and address documents. Cross-check that the spelling of names matches exactly across all records.",
                "action_items": [
                    "Download the state self-declaration format",
                    "Print copies and sign 'Self-Attested' across each document",
                    "Scan all records into clear PDF format under 500 KB each"
                ],
                "estimated_time": "30 mins",
                "online_or_offline": "Offline"
            },
            {
                "step_number": 2,
                "phase": "Portal Registration",
                "title": "Register on the State ServiceOnline / E-District Portal",
                "description": "Create a citizen profile on your state's official service portal (e.g., e-District or ServicePlus) using your Aadhaar or mobile number.",
                "action_items": [
                    "Visit official portal (e.g., serviceonline.gov.in)",
                    "Complete OTP verification via mobile",
                    "Set up secure citizen login credentials"
                ],
                "estimated_time": "10 mins",
                "online_or_offline": "Online"
            },
            {
                "step_number": 3,
                "phase": "Form Filing",
                "title": "Fill the Income Certificate Application Form",
                "description": "Select 'Revenue Services' -> 'Issuance of Income Certificate'. Enter personal details, family members' occupations, and detailed income breakdown.",
                "action_items": [
                    "Select correct district, sub-division (SDM), and Tehsil",
                    "Provide breakdown: Salary, Business, Agriculture, and Other sources",
                    "Upload prepared PDF documents and photograph"
                ],
                "estimated_time": "20 mins",
                "online_or_offline": "Online"
            },
            {
                "step_number": 4,
                "phase": "Payment & Submission",
                "title": "Pay Government Fee and Save Acknowledgement",
                "description": "Pay the statutory nominal fee using UPI, Net Banking, or Debit Card. Download the Application Acknowledgement containing your unique Application Reference Number (ARN).",
                "action_items": [
                    "Complete payment (approx. ₹30)",
                    "Download and print Application Receipt / ARN slip",
                    "Note down the ARN for tracking"
                ],
                "estimated_time": "5 mins",
                "online_or_offline": "Online"
            },
            {
                "step_number": 5,
                "phase": "Verification & Download",
                "title": "Field Verification & Digital Certificate Download",
                "description": "The Patwari / Lekhpal verifies the local income details. Upon approval by the Tehsildar, a digitally signed certificate is issued with a verifiable QR code.",
                "action_items": [
                    "Track status using ARN on the portal",
                    "Be available if the local revenue officer requests quick physical verification",
                    "Download digitally signed PDF directly from citizen portal or DigiLocker"
                ],
                "estimated_time": "7-10 days",
                "online_or_offline": "Online"
            }
        ],
        "eligibility_checklist": [
            "Are you a resident of the district where applying?",
            "Do you have valid proof of earnings (salary slip, ITR, or panchayat declaration)?",
            "Does the applicant's name on Aadhaar match educational and bank records?",
            "Have you prepared the self-declaration affidavit?"
        ],
        "common_mistakes": [
            "Excluding agricultural or rental earnings from the declared total income.",
            "Submitting blurry scans where seals or text are illegible.",
            "Mismatch in father's name or spelling across identity cards and income documents.",
            "Failing to renew before the new financial year begins."
        ],
        "helpful_tips": [
            "Always link your issued certificate to DigiLocker for instant authentic presentation anywhere.",
            "Apply in the month of April/May to maximize the certificate's utility across the entire academic year.",
            "If working in the unorganized sector, obtain a signed income recommendation from your local Ward Councillor or Gram Pradhan before filing."
        ],
        "faqs": [
            {
                "question": "What is the validity period of an Income Certificate?",
                "answer": "Most states issue Income Certificates valid for one financial year (April 1st to March 31st). Some schemes accept it for 6 months to 1 year from date of issue."
            },
            {
                "question": "Can a student apply in their own name?",
                "answer": "Yes, but since students are usually dependents, the declared income is the total household/parental income, and the parent's income proof must be attached."
            },
            {
                "question": "How can I verify the authenticity of my downloaded certificate?",
                "answer": "Modern government certificates have a QR code and digital signature. Scan the QR code or use the 'Verify Certificate' feature on the state portal."
            }
        ]
    },
    {
        "service_slug": "caste-certificate",
        "service_title": "Caste Certificate",
        "documents_required": [
            {
                "document_name": "Applicant Identity Proof",
                "category": "Identity",
                "accepted_options": ["Aadhaar Card", "Voter ID Card", "Passport", "School ID with photo"],
                "is_mandatory": True,
                "description": "Government photo identity document.",
                "format_guidelines": "Self-attested scan, PDF under 1 MB."
            },
            {
                "document_name": "Paternal Lineage Proof (Most Critical)",
                "category": "Lineage",
                "accepted_options": ["Father's Caste Certificate", "Grandfather's Land Revenue Record indicating caste", "Paternal Uncle/Sibling's Caste Certificate", "School Leaving Certificate of Father mentioning caste"],
                "is_mandatory": True,
                "description": "Caste in India is derived from the paternal lineage. Paternal blood relation proof is mandatory.",
                "format_guidelines": "Certified copy with legible state seal and certificate reference number."
            },
            {
                "document_name": "Proof of Residence / Domicile",
                "category": "Address",
                "accepted_options": ["Domicile Certificate", "Ration Card", "Electricity Bill", "Ancestral Land Record"],
                "is_mandatory": True,
                "description": "Proof showing the family's residence in the state on or before the cutoff date (e.g. 1950 for SC/ST, 1993 for OBC in many states).",
                "format_guidelines": "Scanned PDF format."
            },
            {
                "document_name": "Non-Creamy Layer (NCL) Income Proof (For OBC Applicants)",
                "category": "Income",
                "accepted_options": ["3 Years ITR", "Salary Slip of Parents", "Tehsildar Income Certificate"],
                "is_mandatory": False,
                "description": "Only mandatory for OBC applicants seeking Non-Creamy Layer benefit (family income under ₹8 Lakh/yr).",
                "format_guidelines": "Current financial year valid proof."
            },
            {
                "document_name": "Affidavit / Caste Genealogy Tree (Vamshavruksha)",
                "category": "Affidavit",
                "accepted_options": ["Family Genealogy chart certified by local revenue officer or notary"],
                "is_mandatory": True,
                "description": "Depicts relationship of the applicant to the relative holding an existing caste certificate.",
                "format_guidelines": "Notarized on appropriate stamp paper."
            }
        ],
        "application_steps": [
            {
                "step_number": 1,
                "phase": "Preparation",
                "title": "Establish Paternal Lineage & Historical Residence Records",
                "description": "Secure the caste certificate or school records of your father or paternal grandfather. Verify your caste name matches the Central/State official list.",
                "action_items": [
                    "Obtain father's or grandfather's primary caste certificate",
                    "Prepare family pedigree / genealogy chart",
                    "Scan all records in high resolution"
                ],
                "estimated_time": "1-2 days",
                "online_or_offline": "Offline"
            },
            {
                "step_number": 2,
                "phase": "Portal Registration",
                "title": "Access the State Revenue / Social Welfare Portal",
                "description": "Log into your state's citizen service portal (such as e-District or Seva Sindhu).",
                "action_items": [
                    "Sign in with credentials or Aadhaar SSO",
                    "Navigate to 'Backward Class & Social Welfare' or 'Revenue Services'"
                ],
                "estimated_time": "10 mins",
                "online_or_offline": "Online"
            },
            {
                "step_number": 3,
                "phase": "Form Filing",
                "title": "Fill Details and Caste Category Form",
                "description": "Input specific sub-caste, caste serial number as per state gazette, paternal relation details, and residential history.",
                "action_items": [
                    "Select correct category: SC, ST, or OBC / SEBC",
                    "Specify sub-caste accurately (exact spelling)",
                    "Upload paternal documents and affidavit"
                ],
                "estimated_time": "25 mins",
                "online_or_offline": "Online"
            },
            {
                "step_number": 4,
                "phase": "Verification",
                "title": "Local Revenue & Vigilance Enquiry",
                "description": "The Revenue Inspector (RI) and Village Administrative Officer (VAO/Patwari) conduct a locality inquiry to verify social background and paternal origin.",
                "action_items": [
                    "Cooperate with village officer verification",
                    "Provide original documents if requested during spot inspection",
                    "Monitor portal updates"
                ],
                "estimated_time": "7-10 days",
                "online_or_offline": "Hybrid"
            },
            {
                "step_number": 5,
                "phase": "Issuance",
                "title": "Receive Digitally Signed Caste Certificate",
                "description": "Once sanctioned by the SDM or Revenue Divisional Officer (RDO), download the barcode/QR-enabled certificate.",
                "action_items": [
                    "Download digital copy",
                    "Verify spelling of applicant name and caste in the official PDF",
                    "Store in DigiLocker account"
                ],
                "estimated_time": "3-5 days",
                "online_or_offline": "Online"
            }
        ],
        "eligibility_checklist": [
            "Is your caste listed in the Central or State reservation list?",
            "Do you have documentary evidence of father's caste status?",
            "Has your family resided in the state since the statutory cutoff date?",
            "If applying for OBC-NCL, is parental gross annual income below ₹8 Lakh?"
        ],
        "common_mistakes": [
            "Submitting maternal caste certificate (caste is legally inherited from father under standard personal laws).",
            "Mispelling the sub-caste name compared to the official gazette entry.",
            "Submitting expired Non-Creamy Layer income declarations.",
            "Applying in the wrong district (must apply in father's native origin district)."
        ],
        "helpful_tips": [
            "If your father does not have a caste certificate, obtain his Primary School Leaving Certificate where caste is recorded.",
            "Central Government jobs require the certificate in the 'Government of India' prescribed format, distinct from state formats.",
            "SC and ST certificates are valid for a lifetime and do not require periodic renewal."
        ],
        "faqs": [
            {
                "question": "Can I obtain a caste certificate from my mother's caste?",
                "answer": "Generally, caste is recognized through the paternal lineage. Maternal caste certificate is only accepted under exceptional judicial rulings (e.g., single mother upbringing with proof of social disabilities)."
            },
            {
                "question": "Does an OBC certificate expire?",
                "answer": "The caste category itself never expires, but the 'Non-Creamy Layer' (NCL) status is tied to income and typically requires an updated income certificate every 1-3 financial years."
            },
            {
                "question": "What is the difference between State format and Central format?",
                "answer": "State certificates qualify you for state quotas and state govt jobs. Central certificates follow a specific Ministry of Personnel format required for UPSC, SSC, NEET, JEE, and Central Universities."
            }
        ]
    },
    {
        "service_slug": "residence-certificate",
        "service_title": "Residence / Domicile Certificate",
        "documents_required": [
            {
                "document_name": "Proof of Identity",
                "category": "Identity",
                "accepted_options": ["Aadhaar Card", "Voter ID Card", "Passport", "Driving License"],
                "is_mandatory": True,
                "description": "Applicant's valid photo ID card.",
                "format_guidelines": "Scanned PDF under 1 MB, self-attested."
            },
            {
                "document_name": "Proof of Continuous Residence",
                "category": "Residence Proof",
                "accepted_options": ["Continuous School/College Certificates (10+ years)", "Electricity bills for consecutive years", "Ancestral Land Registry (Registry / Khatiyan / 7/12)", "Continuous Voter List Extracts"],
                "is_mandatory": True,
                "description": "Evidence demonstrating uninterrupted residence for the statutory duration (usually 3 to 15 years).",
                "format_guidelines": "Scanned copies demonstrating timeline of continuous stay."
            },
            {
                "document_name": "Proof of Birth",
                "category": "Birth Proof",
                "accepted_options": ["Birth Certificate (issued by Municipal Corp / Gram Panchayat)", "Class 10 Matriculation Certificate"],
                "is_mandatory": True,
                "description": "Verifies date and place of birth of applicant.",
                "format_guidelines": "Clear scan of original birth record."
            },
            {
                "document_name": "Self-Declaration of Non-Dual Domicile",
                "category": "Affidavit",
                "accepted_options": ["Notarized Affidavit stating no domicile claimed in any other State"],
                "is_mandatory": True,
                "description": "An individual cannot legally hold domicile in more than one Indian State simultaneously.",
                "format_guidelines": "Printed on non-judicial stamp paper or uploaded as e-declaration."
            },
            {
                "document_name": "Passport Size Photograph",
                "category": "Photo",
                "accepted_options": ["Recent studio photograph"],
                "is_mandatory": True,
                "description": "Passport size color photograph.",
                "format_guidelines": "JPEG format, under 50 KB."
            }
        ],
        "application_steps": [
            {
                "step_number": 1,
                "phase": "Preparation",
                "title": "Collect Historical Residence & Education Proofs",
                "description": "Gather education marksheets showing schooling in the state from primary to high school, or past utility bills/land records.",
                "action_items": [
                    "Compile school transfer certificates or admission registers",
                    "Verify continuous residency timeline matches state requirement (e.g. 5, 10, or 15 years)",
                    "Sign the non-dual domicile undertaking"
                ],
                "estimated_time": "1 day",
                "online_or_offline": "Offline"
            },
            {
                "step_number": 2,
                "phase": "Portal Registration",
                "title": "Login to State E-Services Portal",
                "description": "Log into the official state citizen portal (e-District / CSC Digital Seva / Antyodaya Saral).",
                "action_items": [
                    "Sign up with Mobile and Aadhaar",
                    "Select 'Issuance of Domicile / Residence Certificate'"
                ],
                "estimated_time": "10 mins",
                "online_or_offline": "Online"
            },
            {
                "step_number": 3,
                "phase": "Form Filing",
                "title": "Complete Online Application & Document Upload",
                "description": "Enter residential address, years of stay, parentage details, and upload scanned evidentiary proofs.",
                "action_items": [
                    "Fill current address and permanent address",
                    "Enter number of continuous years residing at location",
                    "Upload identity, residence proof, and affidavit"
                ],
                "estimated_time": "20 mins",
                "online_or_offline": "Online"
            },
            {
                "step_number": 4,
                "phase": "Verification",
                "title": "Patwari / Revenue Inspector Field Verification",
                "description": "The local revenue inspector conducts neighborhood verification and cross-checks voter records or land title registers.",
                "action_items": [
                    "Track progress using application reference ID",
                    "Promptly respond if the officer requests original document inspection"
                ],
                "estimated_time": "7-10 days",
                "online_or_offline": "Hybrid"
            },
            {
                "step_number": 5,
                "phase": "Issuance",
                "title": "Download Signed Domicile Certificate",
                "description": "Upon final approval from the Sub-Divisional Magistrate or Tehsildar, download the digitally signed residence certificate.",
                "action_items": [
                    "Download the final certificate PDF",
                    "Verify the electronic signature stamp and QR validation code",
                    "Store in DigiLocker"
                ],
                "estimated_time": "3 days",
                "online_or_offline": "Online"
            }
        ],
        "eligibility_checklist": [
            "Have you resided in the state for the minimum required years?",
            "Do you have schooling certificates or land records in this state?",
            "Are you prepared to declare that you do not hold domicile in another state?",
            "Is your permanent residential address clearly documented?"
        ],
        "common_mistakes": [
            "Claiming domicile in two states simultaneously (can lead to criminal prosecution and certificate cancellation).",
            "Presenting only a temporary rent agreement without long-term supporting residence proof.",
            "Address differences between Aadhaar card and state voter list.",
            "Applying in a new district without completing the required residency tenure in that location."
        ],
        "helpful_tips": [
            "Continuous schooling certificates (Class 1 to 10) are considered the strongest residence evidence for students.",
            "A Domicile Certificate generally has permanent lifetime validity unless you relocate permanently.",
            "Both parents' domicile certificates make the child's application virtually instant in most states."
        ],
        "faqs": [
            {
                "question": "Can I hold a Domicile Certificate of two states at the same time?",
                "answer": "No. Under the Constitution of India and state domicile laws, a citizen can have only one domicile of choice at any given time. Holding two is illegal."
            },
            {
                "question": "What is the difference between Residence Certificate and Domicile Certificate?",
                "answer": "In many states, the terms are used interchangeably. Strictly, 'Residence' proves current physical stay, whereas 'Domicile' implies permanent legal home with intention of permanent residence."
            },
            {
                "question": "Does a Domicile Certificate expire?",
                "answer": "No. Domicile certificates typically carry lifetime validity as long as you continue to maintain domicile in that state."
            }
        ]
    }
]
