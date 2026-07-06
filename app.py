"""
Government Scheme Assistant - Main App
----------------------------------------
This Streamlit file is the UI layer and navigation controller.
It gates access behind login/guest, then routes to:
  - Home              : the citizen-facing scheme finder (all 6 agents)
  - My Saved Profiles  : logged-in citizens can revisit past searches
  - Admin Panel        : admins can add/edit/delete schemes
  - Analytics          : admins can see aggregate usage statistics
"""

import streamlit as st
from dotenv import load_dotenv
load_dotenv()  # loads GROQ_API_KEY from a .env file if you create one

import db
db.init_db()

from auth import require_login_or_guest
from agents.profile_agent import build_profile
from agents.faq_agent import answer_question
from agents.pdf_agent import generate_pdf, TAMIL_FONT_AVAILABLE, TAMIL_FONT_ERROR
from orchestrator import run_pipeline
from translations import t, translate_doc, scheme_field, DOCUMENT_TRANSLATIONS
from admin import render_admin_panel
from analytics_page import render_analytics

st.set_page_config(page_title="Government Scheme Assistant", page_icon="🏛️", layout="wide")

# ==================== AUTH GATE ====================
if not require_login_or_guest():
    st.stop()

user = st.session_state.user  # "guest" or {"id", "username", "is_admin"}
is_logged_in = isinstance(user, dict)
is_admin = is_logged_in and user.get("is_admin")

# ==================== SIDEBAR: account + navigation ====================
if is_logged_in:
    st.sidebar.success(f"👤 Logged in as **{user['username']}**")
else:
    st.sidebar.info("👤 Guest mode (profiles won't be saved)")

if st.sidebar.button("Log Out"):
    st.session_state.user = None
    st.session_state.pop("results", None)
    st.session_state.pop("profile", None)
    st.rerun()

nav_options = ["🏠 Home"]
if is_logged_in:
    nav_options.append("💾 My Saved Profiles")
if is_admin:
    nav_options.append("🛠️ Admin Panel")
    nav_options.append("📊 Analytics")

page = st.sidebar.radio("Navigate", nav_options)
st.sidebar.divider()

if page == "🛠️ Admin Panel":
    render_admin_panel()
    st.stop()

if page == "📊 Analytics":
    render_analytics()
    st.stop()

# ==================== LANGUAGE SELECTOR ====================
lang_choice = st.sidebar.selectbox("🌐 Language / மொழி", ["English", "தமிழ்"])
lang = "ta" if lang_choice == "தமிழ்" else "en"

st.title(t(lang, "app_title"))
st.caption(t(lang, "app_caption"))

MASTER_DOCUMENT_LIST = sorted(set(DOCUMENT_TRANSLATIONS.keys()))

if "results" not in st.session_state:
    st.session_state.results = None


# ==================== SHARED: results renderer ====================
def render_results_section():
    results = st.session_state.results

    if len(results) == 0:
        st.warning(t(lang, "no_match"))
        return

    st.success(t(lang, "eligible_count", count=len(results)))

    col_a, col_b = st.columns([1, 1])
    with col_a:
        pdf_results = run_pipeline(st.session_state.profile, lang="en", log=False)
        pdf_buffer = generate_pdf(st.session_state.profile, pdf_results, lang="en")
        st.download_button(
            label=t(lang, "download_pdf_button"),
            data=pdf_buffer,
            file_name="my_scheme_report.pdf",
            mime="application/pdf",
        )
    with col_b:
        if is_logged_in:
            if st.button("💾 Save this profile for later"):
                db.save_profile(user["id"], st.session_state.profile)
                st.success("Profile saved! Find it under 'My Saved Profiles'.")
        else:
            st.caption("Log in to save this profile and revisit it later.")

    if t(lang, "pdf_note"):
        st.caption(t(lang, "pdf_note"))

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        t(lang, "tab_eligible"), t(lang, "tab_documents"), t(lang, "tab_guide"),
        t(lang, "tab_deadlines"), t(lang, "tab_faq")
    ])

    with tab1:
        for r in results:
            scheme = r["scheme"]
            name = scheme_field(scheme, "name", lang)
            sector = scheme_field(scheme, "sector", lang)
            desc = scheme_field(scheme, "description", lang)
            with st.expander(f"✅ {name}  —  ({sector})", expanded=True):
                st.write(desc)
                st.markdown(f"**{t(lang, 'why_eligible')}**")
                for reason in r["reasons"]:
                    st.write(f"- {reason}")

    with tab2:
        for r in results:
            scheme = r["scheme"]
            name = scheme_field(scheme, "name", lang)
            docs = r["documents"]
            st.markdown(f"### {name}")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f" **{t(lang, 'have_docs')}**")
                if docs["have"]:
                    for d in docs["have"]:
                        st.write(f"- {translate_doc(d, lang)}")
                else:
                    st.write(t(lang, "none_yet"))
            with col2:
                st.markdown(f" **{t(lang, 'missing_docs')}**")
                if docs["missing"]:
                    for d in docs["missing"]:
                        st.write(f"- {translate_doc(d, lang)}")
                else:
                    st.write(t(lang, "all_ready"))
            st.divider()

    with tab3:
        for r in results:
            scheme = r["scheme"]
            name = scheme_field(scheme, "name", lang)
            office = scheme_field(scheme, "office", lang)
            steps = scheme_field(scheme, "how_to_apply", lang)
            st.markdown(f"### {name}")
            for i, step in enumerate(steps, start=1):
                st.write(f"{i}. {step}")
            st.write(f"**{t(lang, 'apply_online')}** {scheme['apply_link']}")
            st.write(f"**{t(lang, 'or_visit')}** {office}")
            st.divider()

    with tab4:
        for r in results:
            scheme = r["scheme"]
            name = scheme_field(scheme, "name", lang)
            deadline = r["deadline"]
            if deadline["urgent"]:
                st.error(f"**{name}** — ⏰ {deadline['status']}")
            else:
                st.write(f"**{name}** — {deadline['status']}")

    with tab5:
        st.write(t(lang, "faq_intro"))
        question = st.text_input(t(lang, "faq_placeholder"))
        if st.button(t(lang, "ask_button")):
            if question.strip():
                with st.spinner(t(lang, "thinking")):
                    answer = answer_question(question, lang=lang, context_schemes=results)
                st.write(answer)
            else:
                st.warning(t(lang, "faq_empty_warning"))


# ==================== PAGE: Home ====================
if page == "🏠 Home":
    st.sidebar.header(t(lang, "sidebar_header"))

    age = st.sidebar.slider(t(lang, "age_label"), 0, 100, 25)

    gender_opts = list(t(lang, "gender_options").keys())
    gender = st.sidebar.selectbox(
        t(lang, "gender_label"), gender_opts,
        format_func=lambda x: t(lang, "gender_options")[x]
    )

    occupation_opts = list(t(lang, "occupation_options").keys())
    occupation = st.sidebar.selectbox(
        t(lang, "occupation_label"), occupation_opts,
        format_func=lambda x: t(lang, "occupation_options")[x]
    )

    annual_income = st.sidebar.number_input(t(lang, "income_label"), min_value=0, value=200000, step=10000)

    category_opts = list(t(lang, "category_options").keys())
    category = st.sidebar.selectbox(
        t(lang, "category_label"), category_opts,
        format_func=lambda x: t(lang, "category_options")[x]
    )

    disability = st.sidebar.checkbox(t(lang, "disability_label"))
    land_owner = st.sidebar.checkbox(t(lang, "land_label"))

    documents_owned = st.sidebar.multiselect(
        t(lang, "documents_label"), MASTER_DOCUMENT_LIST,
        format_func=lambda d: translate_doc(d, lang)
    )

    find_btn = st.sidebar.button(t(lang, "find_button"), type="primary", use_container_width=True)

    if find_btn:
        profile = build_profile(age, gender, occupation, annual_income, category,
                                 disability, land_owner, documents_owned)
        st.session_state.results = run_pipeline(profile, lang=lang, log=True)
        st.session_state.profile = profile
        st.session_state.results_lang = lang

    # If the language was switched after results were already computed,
    # silently refresh them in the new language so nothing stays mismatched.
    if st.session_state.results is not None and st.session_state.get("results_lang") != lang:
        st.session_state.results = run_pipeline(st.session_state.profile, lang=lang, log=False)
        st.session_state.results_lang = lang

    if st.session_state.results is None:
        st.info(t(lang, "start_hint"))
    else:
        render_results_section()


# ==================== PAGE: My Saved Profiles ====================
elif page == "💾 My Saved Profiles":
    st.title("💾 My Saved Profiles")
    st.caption("Revisit a profile you saved earlier without re-entering your details.")

    saved = db.get_saved_profiles(user["id"])

    if not saved:
        st.info("You haven't saved any profiles yet. Go to Home, find your schemes, "
                 "then click 'Save this profile for later'.")
    else:
        for sp in saved:
            with st.expander(f"Age {sp['age']} | {sp['occupation'].title()} | "
                              f"Saved on {sp['saved_at'][:10]}"):
                st.write(f"Gender: {sp['gender'].title()}, Income: Rs {sp['annual_income']:,}, "
                         f"Category: {sp['category'].upper()}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔍 View Results", key=f"view_{sp['id']}"):
                        profile = {
                            "age": sp["age"], "gender": sp["gender"], "occupation": sp["occupation"],
                            "annual_income": sp["annual_income"], "category": sp["category"],
                            "disability": sp["disability"], "land_owner": sp["land_owner"],
                            "documents_owned": sp["documents_owned"],
                        }
                        st.session_state.profile = profile
                        st.session_state.results = run_pipeline(profile, lang=lang, log=False)
                        st.session_state.results_lang = lang
                with col2:
                    if st.button("🗑️ Delete", key=f"del_{sp['id']}"):
                        db.delete_saved_profile(sp["id"], user["id"])
                        st.rerun()

        if st.session_state.results is not None:
            st.divider()
            render_results_section()
