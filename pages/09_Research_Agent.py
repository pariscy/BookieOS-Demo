import streamlit as st
from openai import OpenAI

from research_agent import run_research_agent


st.set_page_config(page_title="BION Research Agent 09", page_icon="🔬", layout="wide")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🔬 RESEARCH AGENT 09")
st.caption("BION — BookieCo Intelligence Operations Network")
st.info("Αυτός ο agent είναι απομονωμένος για δοκιμές και δεν αλλάζει το υπάρχον workflow του BION.")

example = (
    "Research the most interesting football matches in the next 7 days for a Cyprus betting audience. "
    "Identify 5 matches, explain why each is interesting, and suggest betting-market angles worth investigating. "
    "Do not invent odds."
)

if "research_task" not in st.session_state:
    st.session_state.research_task = example

st.text_area(
    "Τι θέλεις να ερευνήσει;",
    key="research_task",
    height=150,
)

if st.button("🔎 RUN RESEARCH", type="primary", use_container_width=True):
    task = st.session_state.research_task.strip()

    if not task:
        st.warning("Γράψε πρώτα ένα research request.")
    else:
        try:
            with st.spinner("Το Research Agent κάνει live web research..."):
                result = run_research_agent(client, task)

            st.divider()
            st.markdown("## Research Report")
            st.write(result)
        except Exception as e:
            st.error(f"Σφάλμα Research Agent: {e}")
