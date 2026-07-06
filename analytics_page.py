"""
Analytics Dashboard
--------------------
Shows aggregate (anonymous) statistics about how citizens are using the
app: which schemes are matched most often, which documents citizens most
commonly lack, and basic demographic breakdowns. Useful for government
staff to see where citizens need the most help.
"""

import streamlit as st
import pandas as pd
import db


def render_analytics():
    st.title("📊 Analytics Dashboard")
    st.caption("Aggregate, anonymous statistics from all citizen searches.")

    data = db.get_analytics()

    if data["total_searches"] == 0:
        st.info("No searches yet. Once citizens start using 'Find My Schemes', data will appear here.")
        return

    st.metric("Total Searches", data["total_searches"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏆 Most Matched Schemes")
        if data["top_schemes"]:
            df = pd.DataFrame(data["top_schemes"], columns=["Scheme", "Times Matched"])
            st.bar_chart(df.set_index("Scheme"))
        else:
            st.write("No data yet.")

    with col2:
        st.subheader("📄 Most Commonly Missing Documents")
        if data["top_missing_docs"]:
            df2 = pd.DataFrame(data["top_missing_docs"], columns=["Document", "Times Missing"])
            st.bar_chart(df2.set_index("Document"))
        else:
            st.write("No data yet - citizens have all their documents!")

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("👥 Occupation Breakdown")
        if data["occupation_breakdown"]:
            df3 = pd.DataFrame(data["occupation_breakdown"], columns=["Occupation", "Count"])
            st.bar_chart(df3.set_index("Occupation"))

    with col4:
        st.subheader("🎂 Age Distribution")
        if data["ages"]:
            df4 = pd.DataFrame({"Age": data["ages"]})
            st.bar_chart(df4["Age"].value_counts().sort_index())

    st.caption("This data is anonymous - no names or personal identifiers are stored, only demographic "
               "fields (age, gender, occupation, income bracket, category) and which schemes matched.")
