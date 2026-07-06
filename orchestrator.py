"""
Orchestrator
------------
This is the "agentic" control layer. It doesn't do any domain logic
itself - it just calls the right agent at the right time and passes
data between them, the way a manager coordinates a team.

Flow:
  profile -> Eligibility Agent -> for each matched scheme:
                Document Agent, Guide Agent, Deadline Agent
             -> log the search for the Analytics Dashboard
"""

from agents.eligibility_agent import find_eligible_schemes
from agents.document_agent import check_documents
from agents.guide_agent import get_guide
from agents.deadline_agent import get_deadline_status
import db


def run_pipeline(profile, lang="en", log=True):
    schemes = db.get_all_schemes()
    matches = find_eligible_schemes(profile, schemes, lang)

    results = []
    for match in matches:
        scheme = match["scheme"]
        results.append({
            "scheme": scheme,
            "reasons": match["reasons"],
            "documents": check_documents(scheme, profile["documents_owned"]),
            "guide": get_guide(scheme),
            "deadline": get_deadline_status(scheme),
        })

    if log:
        db.log_search(profile, results)

    return results
