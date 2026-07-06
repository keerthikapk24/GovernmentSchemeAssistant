"""
Citizen Profile Agent
----------------------
Takes raw input from the Streamlit form and turns it into a clean,
structured "profile" dictionary that every other agent will use.

This is intentionally simple - its job is just to organize the data,
not to make decisions.
"""


def build_profile(age, gender, occupation, annual_income, category,
                   disability, land_owner, documents_owned):
    profile = {
        "age": age,
        "gender": gender,
        "occupation": occupation,
        "annual_income": annual_income,
        "category": category,
        "disability": disability,
        "land_owner": land_owner,
        "documents_owned": documents_owned,
    }
    return profile
