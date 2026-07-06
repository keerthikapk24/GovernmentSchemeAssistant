"""
Application Guide Agent
------------------------
Provides step-by-step instructions on how and where to apply
for a given scheme.
"""


def get_guide(scheme):
    return {
        "steps": scheme["how_to_apply"],
        "apply_link": scheme["apply_link"],
        "office": scheme["office"],
    }
