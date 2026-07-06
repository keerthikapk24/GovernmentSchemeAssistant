"""
Eligibility Agent
-----------------
Compares a citizen profile against every scheme's eligibility rules
and returns the list of schemes the person qualifies for, along with
a plain-language reason for each match - in English or Tamil.

Rule-based on purpose: this is the backbone of the app and must be
predictable and explainable, not left to an LLM to guess.
"""

from translations import t

REASON_TEMPLATES = {
    "en": {
        "min_age": "Age is above the minimum of {val}",
        "max_age": "Age is within the limit of {val}",
        "gender": "Gender matches scheme requirement",
        "occupation": "Occupation '{val}' is covered",
        "max_income": "Income is within the limit of Rs {val}",
        "disability": "Disability status matches requirement",
        "land_owner_true": "Owns agricultural land as required",
        "land_owner_false": "Does not own land, matching this scheme's requirement",
    },
    "ta": {
        "min_age": "வயது குறைந்தபட்சம் {val} க்கு மேல் உள்ளது",
        "max_age": "வயது {val} வரம்புக்குள் உள்ளது",
        "gender": "பாலினம் திட்டத்தின் தேவைக்குப் பொருந்துகிறது",
        "occupation": "தொழில் '{val}' இத்திட்டத்தில் அடங்கும்",
        "max_income": "வருமானம் ரூ.{val} வரம்புக்குள் உள்ளது",
        "disability": "மாற்றுத்திறன் நிலை தேவைக்குப் பொருந்துகிறது",
        "land_owner_true": "தேவைப்படும் விவசாய நிலம் உள்ளது",
        "land_owner_false": "நிலம் இல்லை, இத்திட்டத்தின் தேவைக்குப் பொருந்துகிறது",
    },
}


def _check_rule(profile, rules, lang="en"):
    """Returns (is_eligible: bool, reasons: list[str]) for one scheme."""
    reasons = []
    templates = REASON_TEMPLATES.get(lang, REASON_TEMPLATES["en"])

    if "min_age" in rules and profile["age"] < rules["min_age"]:
        return False, []
    if "min_age" in rules:
        reasons.append(templates["min_age"].format(val=rules["min_age"]))

    if "max_age" in rules and profile["age"] > rules["max_age"]:
        return False, []
    if "max_age" in rules:
        reasons.append(templates["max_age"].format(val=rules["max_age"]))

    if "gender" in rules and profile["gender"] not in rules["gender"]:
        return False, []
    if "gender" in rules:
        reasons.append(templates["gender"])

    if "occupation" in rules and profile["occupation"] not in rules["occupation"]:
        return False, []
    if "occupation" in rules:
        occ_label = t(lang, "occupation_options").get(profile["occupation"], profile["occupation"])
        reasons.append(templates["occupation"].format(val=occ_label))

    if "max_income" in rules and profile["annual_income"] > rules["max_income"]:
        return False, []
    if "max_income" in rules:
        reasons.append(templates["max_income"].format(val=f"{rules['max_income']:,}"))

    if "disability" in rules and rules["disability"] != profile["disability"]:
        return False, []
    if "disability" in rules and rules["disability"]:
        reasons.append(templates["disability"])

    if "land_owner" in rules and rules["land_owner"] != profile["land_owner"]:
        return False, []
    if "land_owner" in rules:
        if rules["land_owner"]:
            reasons.append(templates["land_owner_true"])
        else:
            reasons.append(templates["land_owner_false"])

    return True, reasons


def find_eligible_schemes(profile, schemes, lang="en"):
    """Returns a list of dicts: {scheme, reasons}"""
    matches = []
    for scheme in schemes:
        eligible, reasons = _check_rule(profile, scheme["eligibility"], lang)
        if eligible:
            matches.append({"scheme": scheme, "reasons": reasons})
    return matches
