"""
Translations
-------------
Central place for all English/Tamil text used in the UI.
To add a new language later, just add another dict (e.g. "hi" for Hindi)
following the same keys.
"""

UI_TEXT = {
    "en": {
        "app_title": "🏛️ Government Scheme Assistant",
        "app_caption": "Find schemes you qualify for, the documents you need, and how to apply — all in one place.",
        "sidebar_header": "👤 Your Profile",
        "language_label": "Language",
        "age_label": "Age",
        "gender_label": "Gender",
        "occupation_label": "Occupation",
        "income_label": "Annual Family Income (Rs)",
        "category_label": "Category",
        "disability_label": "I have a disability",
        "land_label": "I own agricultural land",
        "documents_label": "Documents you already have",
        "find_button": "🔍 Find My Schemes",
        "start_hint": "👈 Fill in your profile on the left and click **Find My Schemes** to get started.",
        "no_match": "No matching schemes found for this profile. Try adjusting the details.",
        "eligible_count": "✅ You are eligible for {count} scheme(s)!",
        "tab_eligible": "📋 Eligible Schemes",
        "tab_documents": "📄 Documents",
        "tab_guide": "🗺️ How to Apply",
        "tab_deadlines": "📅 Deadlines",
        "tab_faq": "💬 Ask a Question",
        "why_eligible": "Why you qualify:",
        "have_docs": "You already have:",
        "missing_docs": "Still needed:",
        "none_yet": "_None yet_",
        "all_ready": "_Nothing! You're ready to apply 🎉_",
        "apply_online": "Apply online:",
        "or_visit": "Or visit:",
        "faq_intro": "Ask anything about documents, schemes, or the application process.",
        "faq_placeholder": "Your question:",
        "ask_button": "Ask",
        "faq_empty_warning": "Please type a question first.",
        "thinking": "Thinking...",
        "download_pdf_button": "📥 Download PDF Report",
        "pdf_note": "",
        "pdf_title": "Government Scheme Eligibility Report",
        "pdf_generated_on": "Generated on: {date}",
        "pdf_eligible_intro": "You are eligible for {count} scheme(s):",
        "pdf_why_qualify": "Why you qualify:",
        "pdf_docs_have": "Documents - you already have:",
        "pdf_docs_missing": "Documents - still needed:",
        "pdf_how_to_apply": "How to apply:",
        "pdf_deadline": "Deadline:",
        "pdf_none_yet": "None yet",
        "pdf_all_ready": "Nothing - ready to apply!",
        "occupation_options": {
            "farmer": "Farmer", "student": "Student", "unemployed": "Unemployed",
            "self-employed": "Self-employed", "salaried": "Salaried",
            "senior_citizen": "Senior Citizen", "other": "Other"
        },
        "gender_options": {"male": "Male", "female": "Female", "other": "Other"},
        "category_options": {"general": "General", "obc": "OBC", "sc": "SC", "st": "ST"},
    },
    "ta": {
        "app_title": "🏛️ அரசு திட்ட உதவியாளர்",
        "app_caption": "நீங்கள் தகுதி பெறும் திட்டங்கள், தேவையான ஆவணங்கள், விண்ணப்பிக்கும் முறை — அனைத்தும் ஒரே இடத்தில்.",
        "sidebar_header": "👤 உங்கள் விவரங்கள்",
        "language_label": "மொழி",
        "age_label": "வயது",
        "gender_label": "பாலினம்",
        "occupation_label": "தொழில்",
        "income_label": "ஆண்டு குடும்ப வருமானம் (ரூ)",
        "category_label": "பிரிவு",
        "disability_label": "எனக்கு மாற்றுத்திறன் உள்ளது",
        "land_label": "எனக்கு விவசாய நிலம் உள்ளது",
        "documents_label": "உங்களிடம் ஏற்கனவே உள்ள ஆவணங்கள்",
        "find_button": "🔍 எனக்கான திட்டங்களைக் கண்டறி",
        "start_hint": "👈 இடதுபுறத்தில் உங்கள் விவரங்களை நிரப்பி **எனக்கான திட்டங்களைக் கண்டறி** என்பதைக் கிளிக் செய்யவும்.",
        "no_match": "இந்த விவரங்களுக்கு பொருந்தும் திட்டங்கள் இல்லை. விவரங்களை மாற்றி முயற்சிக்கவும்.",
        "eligible_count": "✅ நீங்கள் {count} திட்டத்திற்கு தகுதியுடையவர்!",
        "tab_eligible": "📋 தகுதியான திட்டங்கள்",
        "tab_documents": "📄 ஆவணங்கள்",
        "tab_guide": "🗺️ விண்ணப்பிக்கும் முறை",
        "tab_deadlines": "📅 கடைசி தேதிகள்",
        "tab_faq": "💬 கேள்வி கேளுங்கள்",
        "why_eligible": "நீங்கள் தகுதி பெறுவதற்கான காரணம்:",
        "have_docs": "உங்களிடம் ஏற்கனவே உள்ளது:",
        "missing_docs": "இன்னும் தேவை:",
        "none_yet": "_இதுவரை எதுவும் இல்லை_",
        "all_ready": "_எதுவும் இல்லை! நீங்கள் விண்ணப்பிக்க தயார் 🎉_",
        "apply_online": "ஆன்லைனில் விண்ணப்பிக்க:",
        "or_visit": "அல்லது இங்கு செல்லவும்:",
        "faq_intro": "ஆவணங்கள், திட்டங்கள் அல்லது விண்ணப்ப முறை பற்றி எதுவும் கேளுங்கள்.",
        "faq_placeholder": "உங்கள் கேள்வி:",
        "ask_button": "கேள்",
        "faq_empty_warning": "முதலில் ஒரு கேள்வியை தட்டச்சு செய்யவும்.",
        "thinking": "யோசிக்கிறேன்...",
        "download_pdf_button": "📥 PDF அறிக்கையைப் பதிவிறக்கவும்",
        "pdf_note": "",
        "pdf_title": "அரசு திட்ட தகுதி அறிக்கை",
        "pdf_generated_on": "உருவாக்கப்பட்ட தேதி: {date}",
        "pdf_eligible_intro": "நீங்கள் {count} திட்டத்திற்கு தகுதியுடையவர்:",
        "pdf_why_qualify": "நீங்கள் தகுதி பெறுவதற்கான காரணம்:",
        "pdf_docs_have": "ஆவணங்கள் - ஏற்கனவே உள்ளவை:",
        "pdf_docs_missing": "ஆவணங்கள் - இன்னும் தேவை:",
        "pdf_how_to_apply": "விண்ணப்பிக்கும் முறை:",
        "pdf_deadline": "கடைசி தேதி:",
        "pdf_none_yet": "எதுவும் இல்லை",
        "pdf_all_ready": "எதுவும் தேவையில்லை - விண்ணப்பிக்க தயார்!",
        "occupation_options": {
            "farmer": "விவசாயி", "student": "மாணவர்", "unemployed": "வேலையில்லாதவர்",
            "self-employed": "சுயதொழில்", "salaried": "சம்பளதாரர்",
            "senior_citizen": "மூத்த குடிமகன்", "other": "மற்றவை"
        },
        "gender_options": {"male": "ஆண்", "female": "பெண்", "other": "மற்றவை"},
        "category_options": {"general": "பொது", "obc": "OBC", "sc": "SC", "st": "ST"},
    },
}

# Document names shown in the multiselect and results - shared across all schemes
DOCUMENT_TRANSLATIONS = {
    "Aadhaar Card": "ஆதார் அட்டை",
    "PAN Card": "பான் அட்டை",
    "Income Certificate": "வருமான சான்றிதழ்",
    "Caste Certificate": "சாதி சான்றிதழ்",
    "Caste Certificate (if applicable)": "சாதி சான்றிதழ் (பொருந்தினால்)",
    "Bank Passbook": "வங்கி பாஸ்புக்",
    "Land Records": "நில பதிவு ஆவணங்கள்",
    "Ration Card": "குடும்ப அட்டை",
    "Domicile Certificate": "குடியுரிமை சான்றிதழ்",
    "Disability Certificate": "மாற்றுத்திறன் சான்றிதழ்",
    "Birth Certificate": "பிறப்பு சான்றிதழ்",
    "Passport Size Photo": "பாஸ்போர்ட் அளவு புகைப்படம்",
    "BPL Card / Income Certificate": "வறுமைக்கோட்டு அட்டை / வருமான சான்றிதழ்",
    "BPL Card": "வறுமைக்கோட்டு அட்டை",
    "School ID / Bonafide Certificate": "பள்ளி அடையாள அட்டை / நம்பகத்தன்மை சான்றிதழ்",
    "Age Proof": "வயது சான்று",
    "Mobile Number": "மொபைல் எண்",
    "Business/Project Plan": "வணிக/திட்ட திட்டம்",
    "Aadhaar Card of Guardian": "பாதுகாவலரின் ஆதார் அட்டை",
    "School Certificate (if applicable)": "பள்ளி சான்றிதழ் (பொருந்தினால்)",
}


def t(lang, key, **kwargs):
    """Get a translated UI string. Falls back to English if missing."""
    text = UI_TEXT.get(lang, UI_TEXT["en"]).get(key, UI_TEXT["en"].get(key, key))
    if kwargs:
        return text.format(**kwargs)
    return text


def translate_doc(doc_name, lang):
    """Translate a single document name."""
    if lang == "ta":
        return DOCUMENT_TRANSLATIONS.get(doc_name, doc_name)
    return doc_name


def scheme_field(scheme, field, lang):
    """Get a scheme's field in the selected language, falling back to English."""
    if lang == "ta":
        return scheme.get(f"{field}_ta", scheme.get(field))
    return scheme.get(field)
