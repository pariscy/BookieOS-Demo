import streamlit as st
from openai import OpenAI

from weekly_match_scout import run_weekly_match_scout
from sports_news_monitor import run_sports_news_monitor
from competitor_watch import run_competitor_watch
from sports_calendar import run_sports_calendar
from bet_researcher import run_bet_researcher
from marketing_manager import run_marketing_manager
from sports_article_writer import run_sports_article_writer
from marketing_brainstorm import run_marketing_brainstorm
from research_agent import run_research_agent


st.set_page_config(page_title="BION", page_icon="◉", layout="wide")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


st.markdown(
    """
    <style>
    /* Two independently scrolling work areas */
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stColumn"]) {
        align-items: stretch;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        height: calc(100vh - 175px);
        overflow-y: auto;
        overscroll-behavior: contain;
        padding-right: 14px;
        scrollbar-gutter: stable;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child {
        border-left: 1px solid rgba(255,255,255,.10);
        padding-left: 24px;
        padding-right: 12px;
    }

    /* Make all right-panel text inputs clearly visible */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child textarea {
        min-height: 92px !important;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child [data-baseweb="textarea"],
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child [data-baseweb="select"] {
        width: 100% !important;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]::-webkit-scrollbar {
        width: 8px;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]::-webkit-scrollbar-thumb {
        background: rgba(241,196,0,.25);
        border-radius: 20px;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]::-webkit-scrollbar-track {
        background: transparent;
    }

    @media (max-width: 900px) {
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            height: auto;
            overflow: visible;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child {
            border-left: none;
            padding-left: 0;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


for key, default in {
    "main_title": "BION READY",
    "main_report": None,
    "research_task_input": (
        "Research the most interesting football matches in the next 7 days for a Cyprus betting audience. "
        "Identify 5 matches, explain why each is interesting, and suggest betting-market angles worth investigating. "
        "Do not invent odds."
    ),
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


GREEK_LANGUAGE_RULE = """
ΓΛΩΣΣΙΚΟΣ ΚΑΝΟΝΑΣ BION:
- Απάντησε στα Ελληνικά.
- Κράτησε τα ονόματα ομάδων στην αρχική/καθιερωμένη μορφή τους.
- Κράτησε τα ονόματα διοργανώσεων στην αρχική/καθιερωμένη μορφή τους, π.χ. Champions League, Premier League, Europa League, Formula 1, EuroLeague.
- Κράτησε τα bet types και τη standard betting ορολογία στα Αγγλικά, π.χ. BTTS, Over 2.5, HT/FT, Correct Score, Player to Score, Bet Builder.
- Όλα τα υπόλοιπα πρέπει να είναι στα Ελληνικά.
"""


def contains_any(text, words):
    return any(word in text for word in words)


def detect_agent(user_prompt):
    text = user_prompt.lower()
    if contains_any(text, ["deep research", "research agent", "κάνε έρευνα", "κανε ερευνα", "βαθιά έρευνα", "βαθια ερευνα", "ερεύνησε", "ερευνησε"]): return "research"
    if contains_any(text, ["brainstorm", "marketing brainstorm", "ιδέες marketing", "ιδεες marketing", "ιδέες μάρκετινγκ", "ιδεες μαρκετινγκ", "καμπάνια", "καμπανια"]): return "brainstorm"
    if contains_any(text, ["ανταγωνισ", "competitor", "τι κάνουν οι άλλοι", "τι κανουν οι αλλοι"]): return "competitor"
    if contains_any(text, ["sports news", "αθλητικά νέα", "αθλητικα νεα", "τραυματισ", "τιμωρί", "τιμωρι", "suspension", "injury", "ποιος λείπει", "ποιος λειπει"]): return "news"
    if contains_any(text, ["sports calendar", "ημερολόγιο", "ημερολογιο", "90 μέρες", "90 μερες", "επόμενους 3 μήνες", "επομενους 3 μηνες", "μεγάλα events", "μεγαλα events"]): return "calendar"
    if contains_any(text, ["γράψε άρθρο", "γραψε αρθρο", "άρθρο", "αρθρο", "sports article", "news article", "article writer"]): return "article"
    if contains_any(text, ["weekly match", "match scout", "matches this week", "matches next week", "find matches", "best matches", "αγώνες εβδομάδας", "αγωνες εβδομαδας", "βρες αγώνες", "βρες αγωνες", "καλύτεροι αγώνες", "καλυτεροι αγωνες"]): return "scout"
    return "bion"


def set_main_result(title, content):
    st.session_state.main_title = title
    st.session_state.main_report = content


def run_weekly_workflow(user_prompt):
    with st.spinner("🔎 Το Weekly Match Scout κάνει έρευνα..."):
        scout_report = run_weekly_match_scout(client, user_prompt)
    researcher_task = f"""{GREEK_LANGUAGE_RULE}\nΑνάλυσε ΚΑΘΕ προτεινόμενο football betting idea. Έλεγξε current form, παίκτες, τραυματισμούς/τιμωρίες και πρόσφατα στατιστικά. Βαθμολόγησε STRONG, REASONABLE ή WEAK. Μην δώσεις odds ή επινοήσεις BookieCo market availability.\n\nSCOUT REPORT:\n{scout_report}"""
    with st.spinner("🧠 Το Bet Researcher αναλύει τα bet types..."):
        research_report = run_bet_researcher(client, researcher_task)
    with st.spinner("📣 Το Marketing Manager ετοιμάζει το πλάνο..."):
        marketing_report = run_marketing_manager(scout_report, research_report)
    combined = f"""## 🔎 Weekly Match Scout\n\n{scout_report}\n\n---\n\n## 🧠 Bet Researcher\n\n{research_report}\n\n---\n\n## 📣 Marketing Manager\n\n{marketing_report}"""
    set_main_result("Weekly Marketing Workflow", combined)


st.title("◉ BION")
st.caption("BookieCo Intelligence Operations Network")
st.divider()

# Wider controls panel while keeping the report area dominant.
main_column, agent_column = st.columns([3, 1.35], gap="large")

with main_column:
    st.subheader("BION")
    st.caption("Μίλησε ή γράψε φυσικά στα Ελληνικά. Το BION θα επιλέξει τον σωστό agent.")
    voice_prompt = None
    audio = st.audio_input("🎤 Μίλησε στο BION")
    if audio is not None:
        try:
            transcription = client.audio.transcriptions.create(model="gpt-4o-mini-transcribe", file=audio, language="el")
            voice_prompt = transcription.text
            st.write("🎙️", voice_prompt)
        except Exception as e: st.error(f"Σφάλμα φωνής: {e}")
    text_prompt = st.chat_input("Ρώτησε το BION...")
    user_prompt = text_prompt or voice_prompt
    if user_prompt:
        selected_agent = detect_agent(user_prompt)
        try:
            if selected_agent == "scout": run_weekly_workflow(user_prompt)
            elif selected_agent == "research":
                with st.spinner("🔬 Το Research Agent κάνει live web research..."): result = run_research_agent(client, user_prompt)
                set_main_result("🔬 Research Agent 09", result)
            elif selected_agent == "brainstorm":
                with st.spinner("💡 Το Marketing Brainstorm σκέφτεται..."): result = run_marketing_brainstorm(client, user_prompt)
                set_main_result("💡 Marketing Brainstorm", result)
            elif selected_agent == "competitor":
                with st.spinner("🏆 Έλεγχος ανταγωνιστών..."): result = run_competitor_watch(client)
                set_main_result("🏆 Competitor Watch", result)
            elif selected_agent == "news":
                with st.spinner("🚨 Έλεγχος sports news..."): result = run_sports_news_monitor(client, user_prompt)
                set_main_result("🚨 Sports News Monitor", result)
            elif selected_agent == "calendar":
                with st.spinner("📅 Έλεγχος επόμενων 90 ημερών..."): result = run_sports_calendar(client)
                set_main_result("📅 Sports Calendar", result)
            elif selected_agent == "article":
                with st.spinner("📰 Δημιουργία άρθρου..."): result = run_sports_article_writer(client, user_prompt, language="Greek", length="Medium")
                set_main_result("📰 Sports Article Writer", result)
            else:
                response = client.responses.create(model="gpt-5.6-luna", instructions=f"""You are BION, the central AI assistant for BookieCo, a retail betting company in Cyprus.\n{GREEK_LANGUAGE_RULE}\nAVAILABLE AGENTS: Weekly Match Scout, Bet Researcher, Marketing Manager, Sports News Monitor, Competitor Watch, Sports Calendar, Sports Article Writer, Marketing Brainstorm, Research Agent 09.\nPLANNED: Promotion Selector, Creative Director, Social Media Writer.\nNever invent BookieCo odds or market availability. Keep answers practical and concise.""", input=user_prompt)
                set_main_result("◉ BION", response.output_text)
        except Exception as e: st.error(f"Σφάλμα agent: {e}")

    st.divider()
    st.markdown(f"## {st.session_state.main_title}")
    if st.session_state.main_report:
        with st.container(border=True): st.markdown(st.session_state.main_report)
    else:
        with st.container(border=True): st.caption("Τα αποτελέσματα από οποιονδήποτε agent θα εμφανίζονται εδώ, σε όλο το διαθέσιμο πλάτος.")

with agent_column:
    st.subheader("Ενεργοί Agents")
    agents = [
        ("🔎 Weekly Match Scout", "ΣΥΝΔΕΔΕΜΕΝΟ"), ("🧠 Bet Researcher", "ΣΥΝΔΕΔΕΜΕΝΟ · AUTO"),
        ("📣 Marketing Manager", "ΣΥΝΔΕΔΕΜΕΝΟ · AUTO"), ("🚨 Sports News Monitor", "ΣΥΝΔΕΔΕΜΕΝΟ · MANUAL / VOICE"),
        ("🏆 Competitor Watch", "ΣΥΝΔΕΔΕΜΕΝΟ · MANUAL / VOICE"), ("📅 Sports Calendar", "ΣΥΝΔΕΔΕΜΕΝΟ · MANUAL / VOICE"),
        ("📰 Sports Article Writer", "ΣΥΝΔΕΔΕΜΕΝΟ · MANUAL / VOICE"), ("💡 Marketing Brainstorm", "ΣΥΝΔΕΔΕΜΕΝΟ · MANUAL / VOICE"),
        ("🔬 Research Agent 09", "TEST · MANUAL / VOICE"),
    ]
    for name, status in agents:
        st.write(f"🟢 {name}"); st.caption(status)
    st.divider()

    st.subheader("🔎 Weekly Workflow")
    weekly_request = st.text_area("Περίοδος / αίτημα", value="Βρες τους καλύτερους αγώνες της επόμενης εβδομάδας για marketing.", height=100, key="weekly_request_input")
    if st.button("🔎 RUN WEEKLY WORKFLOW", use_container_width=True):
        try: run_weekly_workflow(weekly_request)
        except Exception as e: st.error(f"Σφάλμα Weekly Workflow: {e}")
    st.divider()

    st.subheader("🔬 Research Agent 09")
    st.text_area("Τι θέλεις να ερευνήσει;", height=120, key="research_task_input")
    if st.button("🔬 RUN RESEARCH", type="primary", use_container_width=True):
        task = st.session_state.research_task_input.strip()
        if task:
            try:
                with st.spinner("Live web research..."): result = run_research_agent(client, task)
                set_main_result("🔬 Research Agent 09", result)
            except Exception as e: st.error(f"Σφάλμα Research Agent: {e}")
        else: st.warning("Γράψε πρώτα τι θέλεις να ερευνήσει.")
    st.divider()

    st.subheader("🚨 Sports News")
    if st.button("🚨 Έλεγχος Sports News", use_container_width=True):
        try:
            with st.spinner("Έλεγχος σημαντικών αθλητικών νέων..."): result = run_sports_news_monitor(client, f"{GREEK_LANGUAGE_RULE}\nΚάνε ανεξάρτητο έλεγχο current sports news που μπορούν πραγματικά να επηρεάσουν το BookieCo.")
            set_main_result("🚨 Sports News Monitor", result)
        except Exception as e: st.error(f"Σφάλμα Sports News Monitor: {e}")
    st.divider()

    st.subheader("🏆 Competitor Watch")
    if st.button("🏆 Έλεγχος Ανταγωνιστών", use_container_width=True):
        try:
            with st.spinner("Έλεγχος δραστηριότητας ανταγωνιστών..."): result = run_competitor_watch(client)
            set_main_result("🏆 Competitor Watch", result)
        except Exception as e: st.error(f"Σφάλμα Competitor Watch: {e}")
    st.divider()

    st.subheader("📅 Sports Calendar")
    if st.button("📅 Επόμενες 90 Ημέρες", use_container_width=True):
        try:
            with st.spinner("Δημιουργία 90-day Sports Calendar..."): result = run_sports_calendar(client)
            set_main_result("📅 Sports Calendar", result)
        except Exception as e: st.error(f"Σφάλμα Sports Calendar: {e}")
    st.divider()

    st.subheader("📰 Sports Article Writer")
    article_brief = st.text_area("Τι θέλεις να γράψει;", placeholder="π.χ. Γράψε άρθρο για το αποψινό Champions League...", height=110, key="article_brief_input")
    article_length_label = st.selectbox("Μήκος άρθρου", ["Σύντομο", "Μεσαίο", "Μεγάλο"], key="article_length")
    article_length_map = {"Σύντομο":"Short", "Μεσαίο":"Medium", "Μεγάλο":"Long"}
    if st.button("📰 Δημιουργία Άρθρου", use_container_width=True):
        if article_brief.strip():
            try:
                with st.spinner("Δημιουργία άρθρου..."): result = run_sports_article_writer(client, article_brief, language="Greek", length=article_length_map[article_length_label])
                set_main_result("📰 Sports Article Writer", result)
            except Exception as e: st.error(f"Σφάλμα Sports Article Writer: {e}")
        else: st.warning("Γράψε πρώτα τι θέλεις να περιλαμβάνει το άρθρο.")
    st.divider()

    st.subheader("💡 Marketing Brainstorm")
    brainstorm_challenge = st.text_area("Για ποιο θέμα θέλεις ιδέες;", placeholder="π.χ. Ιδέες για καμπάνια Champions League...", height=110, key="brainstorm_challenge_input")
    brainstorm_goal = st.selectbox("Στόχος", ["Γενικές ιδέες marketing", "Αύξηση επισκεψιμότητας στα καταστήματα", "Brand awareness", "Καμπάνια για special event", "Customer engagement", "Κάτι ασυνήθιστο / πειραματικό"], key="brainstorm_goal")
    if st.button("💡 Δημιουργία Ιδεών", use_container_width=True):
        if brainstorm_challenge.strip():
            try:
                with st.spinner("Το Marketing Brainstorm σκέφτεται..."): result = run_marketing_brainstorm(client, brainstorm_challenge, goal=brainstorm_goal)
                set_main_result("💡 Marketing Brainstorm", result)
            except Exception as e: st.error(f"Σφάλμα Marketing Brainstorm: {e}")
        else: st.warning("Γράψε πρώτα για ποιο θέμα θέλεις ιδέες.")
    st.divider()

    st.write("⚪ 🎁 Promotion Selector"); st.caption("ΑΝΑΜΟΝΗ ΓΙΑ COMPANY FILES")
    st.write("⚪ 🎨 Creative Director"); st.caption("ΠΡΟΓΡΑΜΜΑΤΙΣΜΕΝΟ")
    st.write("⚪ ✍️ Social Media Writer"); st.caption("ΠΡΟΓΡΑΜΜΑΤΙΣΜΕΝΟ")
    st.divider(); st.success("BION ONLINE")