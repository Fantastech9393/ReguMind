import streamlit as st
from analyzer import analyze_query

st.set_page_config(page_title="ReguMind — Compliance Assistant", layout="centered")

st.title("ReguMind — AI-Powered Compliance Assistant")
st.caption(
    "Information provided for educational purposes only. Verify with official sources or compliance counsel before implementation."
)

with st.expander("What is ReguMind?"):
    st.write(
        """
        ReguMind helps you explore compliance frameworks and retrieve:
        1. Exact quotes from official or public sources.
        2. Plain-language action summaries for practical application.
        3. Citations including framework, section, and source links.
        4. A confidence score based on content similarity.
        
        Try queries like “GDPR Article 30” or “HIPAA Security Rule 164.312”.
        """
    )

query = st.text_input(
    "Ask about a framework, section, or control:",
    placeholder="e.g., GDPR Article 30"
)
run = st.button("Analyze")

if run:
    with st.spinner("Analyzing your query..."):
        result = analyze_query(query)

    if not result.get("ok"):
        st.error(result.get("message", "Something went wrong."))
    else:
        st.subheader(f"{result.get('framework', 'Unknown Framework')} — {result.get('section', '')}")
        st.write(f"**{result.get('title', '')}**")

        # --- Exact Quote ---
        st.markdown("### Exact Quote")
        with st.expander("View full quote"):
            st.markdown(result.get("quote", "(No quote available)").replace("\n", "  \n"))

        # --- Action Guidance ---
        st.markdown("### Action Guidance")
        actions = result.get("actions", [])
        if actions:
            for a in actions:
                st.write(f"- {a}")
        else:
            st.write(result.get("action_guidance", "No operational guidance available for this section."))

        # --- Citation Info ---
        st.markdown("### Citation")
        citation = result.get("citation", {})
        st.write(f"**Source:** {citation.get('source_url', '(add link)')}")
        st.write(f"**Last Reviewed:** {citation.get('last_reviewed', '(add date)')}")

        # --- Confidence Score ---
        confidence = result.get("confidence", 0.0)
        st.progress(confidence)
        st.write(f"**Confidence:** {confidence * 100:.1f}%")
