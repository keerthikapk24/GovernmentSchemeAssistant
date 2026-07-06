"""
Document Verification Agent
----------------------------
For a given scheme, checks which required documents the citizen
already has (based on what they selected in the form) and which
ones are still missing.
"""


def check_documents(scheme, documents_owned):
    required = scheme["documents"]
    have = [doc for doc in required if doc in documents_owned]
    missing = [doc for doc in required if doc not in documents_owned]
    return {
        "required": required,
        "have": have,
        "missing": missing,
        "ready_to_apply": len(missing) == 0,
    }
