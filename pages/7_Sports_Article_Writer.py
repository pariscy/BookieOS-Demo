import streamlit as st
from openai import OpenAI

from sports_article_writer import run_sports_article_writer


st.set_page_config(
    page_title="Sports Article Writer | BookieOS",
    page_icon="📰",
    layout="wide",
)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "sports_article_result" not in st.session_state:
    st.session_state.sports_article_result = None

st.title("📰 Sports Article Writer")
st.caption("Create short sports/news articles for external websites.")

with st.container(border=True):
    brief = st.text_area(
        "What should the article be about?",
        placeholder=(
            "Example: Write an article about the upcoming Champions League match, "
            "focusing on the teams, the importance of the game and a natural BookieCo mention."
        ),
        height=180,
    )

    col1, col2 = st.columns(2)

    with col1:
        language = st.selectbox(
            "Language",
            ["Greek", "English"],
            index=0,
        )

    with col2:
        length = st.selectbox(
            "Article length",
            ["Short", "Medium", "Long"],
            index=0,
        )

    if st.button("📰 Write Article", use_container_width=True, type="primary"):
        if not brief.strip():
            st.warning("Tell the agent what the article should be about first.")
        else:
            try:
                with st.spinner("Sports Article Writer is working..."):
                    st.session_state.sports_article_result = run_sports_article_writer(
                        client=client,
                        brief=brief,
                        language=language,
                        length=length,
                    )
            except Exception as e:
                st.error(f"Sports Article Writer error: {e}")

if st.session_state.sports_article_result:
    st.divider()
    st.subheader("Finished Article")

    with st.container(border=True):
        st.write(st.session_state.sports_article_result)

    st.caption(
        "Review factual, promotional and regulatory details before sending the article for publication."
    )
