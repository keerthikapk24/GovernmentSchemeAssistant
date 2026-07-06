"""
FAQ Agent
---------
Answers open-ended questions about government schemes, in English or Tamil.

If a GROQ_API_KEY is set (free tier: https://console.groq.com), this
calls a real LLM for smart, natural-language answers in the chosen language.

If no API key is set yet, it falls back to simple keyword matching
against a small local FAQ list, so the app still works out of the box
while you're setting up your API key.
"""

import os
import requests

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

FALLBACK_FAQS = {
    "en": {
        "aadhaar": "Aadhaar is a 12-digit unique identity number issued by UIDAI to Indian residents, based on biometric and demographic data.",
        "income certificate": "An income certificate is an official document issued by the state government certifying your annual family income. It is issued by your local Tehsildar / Revenue Office.",
        "caste certificate": "A caste certificate confirms a person's caste (SC/ST/OBC) for availing reservation benefits. It is issued by the Revenue Department / Tehsildar office.",
        "how long": "Processing times vary by scheme, typically between 2 to 8 weeks after document verification.",
        "domicile": "A domicile certificate proves that a person is a resident of a particular state, issued by the Revenue Department.",
        "csc": "A Common Service Centre (CSC) is a government-authorized digital service point in villages/towns that helps citizens apply for schemes, get certificates, and access online government services.",
        "bank passbook": "A bank passbook is a small booklet showing your account details and transaction history - most schemes need it to verify your account for direct benefit transfer.",
        "reject": "If your application is rejected, check the reason mentioned (usually a document issue), correct it, and reapply. You can also visit the concerned office in person for help.",
    },
    "ta": {
        "aadhaar": "ஆதார் என்பது UIDAI வழங்கும் 12 இலக்க தனித்துவ அடையாள எண், இது உயிரியல் மற்றும் மக்கள்தொகை தரவை அடிப்படையாகக் கொண்டது.",
        "income certificate": "வருமான சான்றிதழ் என்பது உங்கள் குடும்பத்தின் ஆண்டு வருமானத்தை உறுதிப்படுத்தும் அரசு ஆவணம். இது உங்கள் தாலுகா அலுவலகம் / வருவாய்த் துறையால் வழங்கப்படுகிறது.",
        "caste certificate": "சாதி சான்றிதழ் ஒரு நபரின் சாதியை (SC/ST/OBC) உறுதிப்படுத்துகிறது, இதை வருவாய்த் துறை வழங்குகிறது.",
        "how long": "செயலாக்க நேரம் திட்டத்தைப் பொறுத்து மாறுபடும், பொதுவாக ஆவண சரிபார்ப்புக்குப் பிறகு 2 முதல் 8 வாரங்கள் ஆகலாம்.",
        "domicile": "குடியுரிமை சான்றிதழ் ஒரு நபர் குறிப்பிட்ட மாநிலத்தில் வசிப்பவர் என்பதை உறுதிப்படுத்துகிறது, இது வருவாய்த் துறையால் வழங்கப்படுகிறது.",
        "csc": "பொது சேவை மையம் (CSC) என்பது கிராமங்கள்/நகரங்களில் உள்ள அரசு அங்கீகரிக்கப்பட்ட டிஜிட்டல் சேவை மையம், இது திட்டங்களுக்கு விண்ணப்பிக்கவும், சான்றிதழ்கள் பெறவும் உதவுகிறது.",
        "bank passbook": "வங்கி பாஸ்புக் என்பது உங்கள் கணக்கு விவரங்களைக் காட்டும் சிறு புத்தகம் - நேரடி பலன் பரிமாற்றத்திற்காக பெரும்பாலான திட்டங்களுக்கு இது தேவை.",
        "reject": "உங்கள் விண்ணப்பம் நிராகரிக்கப்பட்டால், குறிப்பிட்ட காரணத்தை (பொதுவாக ஆவணப் பிரச்சனை) சரிபார்த்து, சரிசெய்து மீண்டும் விண்ணப்பிக்கவும்.",
    },
}

FALLBACK_NOT_FOUND = {
    "en": ("I don't have a smart answer for that yet without an API key set up. "
           "Add your free GROQ_API_KEY in a .env file for full AI-powered answers, "
           "or check the official scheme portal linked in the Application Guide tab."),
    "ta": ("API கீ இல்லாமல் இதற்கு எனக்கு துல்லியமான பதில் இல்லை. "
           "முழு AI பதில்களுக்கு .env கோப்பில் GROQ_API_KEY சேர்க்கவும், "
           "அல்லது விண்ணப்ப வழிகாட்டி டேபில் உள்ள அதிகாரப்பூர்வ இணையதளத்தை பார்க்கவும்."),
}


def _fallback_answer(question, lang):
    question_lower = question.lower()
    faqs = FALLBACK_FAQS.get(lang, FALLBACK_FAQS["en"])
    for keyword, answer in faqs.items():
        if keyword in question_lower:
            return answer
    return FALLBACK_NOT_FOUND.get(lang, FALLBACK_NOT_FOUND["en"])


def answer_question(question, lang="en", context_schemes=None):
    if not GROQ_API_KEY:
        return _fallback_answer(question, lang)

    scheme_context = ""
    if context_schemes:
        names = ", ".join([s["scheme"]["name"] for s in context_schemes])
        scheme_context = f"The user is currently eligible for these schemes: {names}. "

    language_instruction = (
        "Answer ONLY in Tamil language, in simple words a farmer with basic literacy can understand."
        if lang == "ta" else
        "Answer in simple, clear English."
    )

    system_prompt = (
        "You are a helpful assistant that explains Indian government welfare "
        "schemes in simple, friendly language for citizens who may not be familiar "
        "with government processes. Keep answers short and clear (3-5 sentences). "
        + scheme_context + language_instruction
    )

    try:
        response = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question},
                ],
                "max_tokens": 300,
            },
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception:
        return f"(AI service error, showing basic answer instead) {_fallback_answer(question, lang)}"
