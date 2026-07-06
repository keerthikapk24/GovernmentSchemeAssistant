"""
Admin Panel
-----------
Lets an admin user add, edit, or delete government schemes through a form,
instead of hand-editing JSON or Python code. All changes are saved to the
database immediately and take effect for every citizen using the app.
"""

import streamlit as st
import db

OCCUPATION_CHOICES = ["farmer", "student", "unemployed", "self-employed", "salaried", "senior_citizen", "other"]
GENDER_CHOICES = ["male", "female", "other"]


def _slugify(name):
    return name.strip().lower().replace(" ", "_").replace("-", "_")


def _scheme_form(existing=None):
    """Renders the add/edit form. Returns the scheme dict if submitted, else None."""
    e = existing or {}
    elig = e.get("eligibility", {})

    with st.form("scheme_form", clear_on_submit=False):
        st.subheader("Basic Info")
        name = st.text_input("Scheme Name (English)", value=e.get("name", ""))
        name_ta = st.text_input("Scheme Name (Tamil)", value=e.get("name_ta", ""))
        sector = st.text_input("Sector (English)", value=e.get("sector", ""))
        sector_ta = st.text_input("Sector (Tamil)", value=e.get("sector_ta", ""))
        description = st.text_area("Description (English)", value=e.get("description", ""))
        description_ta = st.text_area("Description (Tamil)", value=e.get("description_ta", ""))

        st.subheader("Eligibility Rules")
        st.caption("Leave a rule at its 'no requirement' setting if it shouldn't apply to this scheme.")

        col1, col2 = st.columns(2)
        with col1:
            has_min_age = st.checkbox("Has minimum age", value="min_age" in elig)
            min_age = st.number_input("Minimum age", 0, 100, elig.get("min_age", 18)) if has_min_age else None
        with col2:
            has_max_age = st.checkbox("Has maximum age", value="max_age" in elig)
            max_age = st.number_input("Maximum age", 0, 100, elig.get("max_age", 60)) if has_max_age else None

        gender_req = st.multiselect("Restrict to gender(s) (leave empty = no restriction)",
                                     GENDER_CHOICES, default=elig.get("gender", []))
        occupation_req = st.multiselect("Restrict to occupation(s) (leave empty = no restriction)",
                                         OCCUPATION_CHOICES, default=elig.get("occupation", []))

        has_max_income = st.checkbox("Has maximum income limit", value="max_income" in elig)
        max_income = st.number_input("Maximum annual income (Rs)", 0, 10000000,
                                      elig.get("max_income", 250000), step=10000) if has_max_income else None

        requires_disability = st.checkbox("Requires disability status", value=elig.get("disability", False))

        land_options = ["No requirement", "Must own land", "Must NOT own land"]
        land_default = 0
        if elig.get("land_owner") is True:
            land_default = 1
        elif elig.get("land_owner") is False:
            land_default = 2
        land_choice = st.selectbox("Land ownership requirement", land_options, index=land_default)

        st.subheader("Documents Required")
        documents_text = st.text_area("One document per line", value="\n".join(e.get("documents", [])))

        st.subheader("How to Apply")
        steps_text = st.text_area("Steps in English (one per line)",
                                   value="\n".join(e.get("how_to_apply", [])))
        steps_ta_text = st.text_area("Steps in Tamil (one per line, optional)",
                                      value="\n".join(e.get("how_to_apply_ta", [])))

        apply_link = st.text_input("Apply Online Link", value=e.get("apply_link", "https://"))
        office = st.text_input("Office to Visit (English)", value=e.get("office", ""))
        office_ta = st.text_input("Office to Visit (Tamil)", value=e.get("office_ta", ""))
        deadline = st.text_input("Deadline ('Rolling' or YYYY-MM-DD)", value=e.get("deadline", "Rolling"))

        submitted = st.form_submit_button("💾 Save Scheme", type="primary")

        if submitted:
            if not name or not description:
                st.error("Scheme name and description are required.")
                return None

            eligibility = {}
            if has_min_age:
                eligibility["min_age"] = int(min_age)
            if has_max_age:
                eligibility["max_age"] = int(max_age)
            if gender_req:
                eligibility["gender"] = gender_req
            if occupation_req:
                eligibility["occupation"] = occupation_req
            if has_max_income:
                eligibility["max_income"] = int(max_income)
            if requires_disability:
                eligibility["disability"] = True
            if land_choice == "Must own land":
                eligibility["land_owner"] = True
            elif land_choice == "Must NOT own land":
                eligibility["land_owner"] = False

            scheme_dict = {
                "id": e.get("id") or _slugify(name),
                "name": name, "name_ta": name_ta or name,
                "sector": sector, "sector_ta": sector_ta or sector,
                "description": description, "description_ta": description_ta or description,
                "eligibility": eligibility,
                "documents": [d.strip() for d in documents_text.split("\n") if d.strip()],
                "how_to_apply": [s.strip() for s in steps_text.split("\n") if s.strip()],
                "how_to_apply_ta": [s.strip() for s in steps_ta_text.split("\n") if s.strip()] or
                                   [s.strip() for s in steps_text.split("\n") if s.strip()],
                "apply_link": apply_link,
                "office": office, "office_ta": office_ta or office,
                "deadline": deadline,
            }
            return scheme_dict

    return None


def render_admin_panel():
    st.title("🛠️ Admin Panel")
    st.caption("Add, edit, or remove government schemes. Changes apply instantly for all citizens.")

    action = st.radio("Choose an action:", ["View All Schemes", "Add New Scheme", "Edit / Delete a Scheme"],
                       horizontal=True)

    if action == "View All Schemes":
        schemes = db.get_all_schemes()
        st.write(f"**{len(schemes)} schemes** currently in the system.")
        for s in schemes:
            with st.expander(f"{s['name']} ({s['sector']})"):
                st.json(s)

    elif action == "Add New Scheme":
        st.info("Fill in the form below to add a brand new scheme.")
        result = _scheme_form()
        if result:
            db.add_or_update_scheme(result)
            st.success(f"✅ '{result['name']}' has been added!")
            st.rerun()

    elif action == "Edit / Delete a Scheme":
        schemes = db.get_all_schemes()
        scheme_names = {s["name"]: s["id"] for s in schemes}
        chosen_name = st.selectbox("Select a scheme to edit or delete", list(scheme_names.keys()))

        if chosen_name:
            scheme_id = scheme_names[chosen_name]
            existing = db.get_scheme(scheme_id)

            result = _scheme_form(existing=existing)
            if result:
                db.add_or_update_scheme(result)
                st.success(f"✅ '{result['name']}' has been updated!")
                st.rerun()

            st.divider()
            st.warning("Danger zone")
            if st.button(f"🗑️ Delete '{chosen_name}' permanently"):
                db.delete_scheme(scheme_id)
                st.success(f"Deleted '{chosen_name}'.")
                st.rerun()
