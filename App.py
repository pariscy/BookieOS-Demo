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

for key in ["sports_news_report", "competitor_report", "sports_calendar_report", "calendar_promo_ideas", "sports_article_report", "brainstorm_report", "research_report"]:
    if key not in st.session_state:
        st.session_state[key] = None

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

def run_weekly_workflow(user_prompt):
    with st.spinner("🔎 Το Weekly Match Scout κάνει έρευνα..."):
        scout_report = run_weekly_match_scout(client, user_prompt)
    st.markdown("### 🔎 Weekly Match Scout"); st.write(scout_report); st.divider()
    researcher_task = f"""{GREEK_LANGUAGE_RULE}\nΑνάλυσε ΚΑΘΕ προτεινόμενο football betting idea. Έλεγξε current form, παίκτες, τραυματισμούς/τιμωρίες και πρόσφατα στατιστικά. Βαθμολόγησε STRONG, REASONABLE ή WEAK. Μην δώσεις odds ή επινοήσεις BookieCo market availability.\n\nSCOUT REPORT:\n{scout_report}"""
    with st.spinner("🧠 Το Bet Researcher αναλύει τα bet types..."):
        research_report = run_bet_researcher(client, researcher_task)
    st.markdown("### 🧠 Bet Researcher"); st.write(research_report); st.divider()
    with st.spinner("📣 Το Marketing Manager ετοιμάζει το πλάνο..."):
        marketing_report = run_marketing_manager(scout_report, research_report)
    st.markdown("### 📣 Marketing Manager"); st.write(marketing_report); st.success("Η ανάλυση marketing ολοκληρώθηκε.")

st.title("◉ BION")
st.caption("BookieCo Intelligence Operations Network")
st.divider()
main_column, agent_column = st.columns([3, 1])

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
        with st.chat_message("user"): st.write(user_prompt)
        with st.chat_message("assistant"):
            selected_agent = detect_agent(user_prompt)
            try:
                if selected_agent == "scout": run_weekly_workflow(user_prompt)
                elif selected_agent == "research":
                    st.caption("🔬 Δρομολόγηση → Research Agent 09")
                    with st.spinner("🔬 Το Research Agent κάνει live web research..."): result = run_research_agent(client, user_prompt)
                    st.write(result)
                elif selected_agent == "brainstorm":
                    st.caption("💡 Δρομολόγηση → Marketing Brainstorm")
                    with st.spinner("💡 Το Marketing Brainstorm σκέφτεται..."): result = run_marketing_brainstorm(client, user_prompt)
                    st.write(result)
                elif selected_agent == "competitor":
                    st.caption("🏆 Δρομολόγηση → Competitor Watch")
                    with st.spinner("🏆 Έλεγχος ανταγωνιστών..."): result = run_competitor_watch(client)
                    st.write(result)
                elif selected_agent == "news":
                    st.caption("🚨 Δρομολόγηση → Sports News Monitor")
                    with st.spinner("🚨 Έλεγχος sports news..."): result = run_sports_news_monitor(client, user_prompt)
                    st.write(result)
                elif selected_agent == "calendar":
                    st.caption("📅 Δρομολόγηση → Sports Calendar")
                    with st.spinner("📅 Έλεγχος επόμενων 90 ημερών..."): result = run_sports_calendar(client)
                    st.write(result)
                elif selected_agent == "article":
                    st.caption("📰 Δρομολόγηση → Sports Article Writer")
                    with st.spinner("📰 Δημιουργία άρθρου..."): result = run_sports_article_writer(client, user_prompt, language="Greek", length="Medium")
                    st.write(result)
                else:
                    response = client.responses.create(model="gpt-5.6-luna", instructions=f"""You are BION, the central AI assistant for BookieCo, a retail betting company in Cyprus.\n{GREEK_LANGUAGE_RULE}\nAVAILABLE AGENTS: Weekly Match Scout, Bet Researcher, Marketing Manager, Sports News Monitor, Competitor Watch, Sports Calendar, Sports Article Writer, Marketing Brainstorm, Research Agent 09.\nPLANNED: Promotion Selector, Creative Director, Social Media Writer.\nNever invent BookieCo odds or market availability. Keep answers practical and concise.""", input=user_prompt)
                    st.write(response.output_text)
            except Exception as e: st.error(f"Σφάλμα agent: {e}")

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

    st.subheader("🔬 Research Agent 09")
    st.caption("Απομονωμένο test agent για live, source-backed web research.")
    default_research = "Research the most interesting football matches in the next 7 days for a Cyprus betting audience. Identify 5 matches, explain why each is interesting, and suggest betting-market angles worth investigating. Do not invent odds."
    research_task = st.text_area("Τι θέλεις να ερευνήσει;", value=default_research, height=130, key="research_task_input")
    if st.button("🔬 RUN RESEARCH", use_container_width=True):
        if research_task.strip():
            try:
                with st.spinner("Το Research Agent κάνει live web research..."): st.session_state.research_report = run_research_agent(client, research_task)
            except Exception as e: st.error(f"Σφάλμα Research Agent: {e}")
    if st.session_state.research_report:
        with st.container(border=True): st.markdown("### Research Report"); st.write(st.session_state.research_report)
    st.divider()

    st.subheader("🚨 Αθλητική Ενημέρωση")
    if st.button("🚨 Έλεγχος Sports News", use_container_width=True):
        try:
            with st.spinner("Έλεγχος σημαντικών αθλητικών νέων..."):
                st.session_state.sports_news_report = run_sports_news_monitor(client, f"{GREEK_LANGUAGE_RULE}\nΚάνε ανεξάρτητο έλεγχο current sports news που μπορούν πραγματικά να επηρεάσουν το BookieCo.")
        except Exception as e: st.error(f"Σφάλμα Sports News Monitor: {e}")
    if st.session_state.sports_news_report:
        with st.container(border=True): st.write(st.session_state.sports_news_report)
    st.divider()

    st.subheader("🏆 Ανταγωνισμός")
    if st.button("🏆 Έλεγχος Ανταγωνιστών", use_container_width=True):
        try:
            with st.spinner("Έλεγχος δραστηριότητας ανταγωνιστών..."): st.session_state.competitor_report = run_competitor_watch(client)
        except Exception as e: st.error(f"Σφάλμα Competitor Watch: {e}")
    if st.session_state.competitor_report:
        with st.container(border=True): st.write(st.session_state.competitor_report)
    st.divider()

    st.subheader("📅 Sports Calendar")
    if st.button("📅 Έλεγχος Επόμενων 90 Ημερών", use_container_width=True):
        try:
            with st.spinner("Δημιουργία 90-day Sports Calendar..."): st.session_state.sports_calendar_report = run_sports_calendar(client); st.session_state.calendar_promo_ideas = None
        except Exception as e: st.error(f"Σφάλμα Sports Calendar: {e}")
    if st.session_state.sports_calendar_report:
        with st.container(border=True): st.write(st.session_state.sports_calendar_report)
        if st.button("💡 Δημιουργία Promo Ideas", use_container_width=True):
            try:
                promo_response = client.responses.create(model="gpt-5.6-luna", input=f"{GREEK_LANGUAGE_RULE}\nΔημιούργησε μόνο concepts για special-event promotions. Μην επινοείς odds ή BookieCo market availability.\n\nCALENDAR:\n{st.session_state.sports_calendar_report}")
                st.session_state.calendar_promo_ideas = promo_response.output_text
            except Exception as e: st.error(f"Σφάλμα Promo Ideas: {e}")
        if st.session_state.calendar_promo_ideas:
            with st.container(border=True): st.write(st.session_state.calendar_promo_ideas)
    st.divider()

    st.subheader("📰 Sports Article Writer")
    article_brief = st.text_area("Τι θέλεις να γράψει;", key="article_brief_input")
    article_length_label = st.selectbox("Μήκος άρθρου", ["Σύντομο", "Μεσαίο", "Μεγάλο"], key="article_length")
    article_length_map = {"Σύντομο":"Short", "Μεσαίο":"Medium", "Μεγάλο":"Long"}
    if st.button("📰 Δημιουργία Άρθρου", use_container_width=True):
        if not article_brief.strip(): st.warning("Γράψε πρώτα τι θέλεις να περιλαμβάνει το άρθρο.")
        else:
            try:
                with st.spinner("Δημιουργία άρθρου..."): st.session_state.sports_article_report = run_sports_article_writer(client, article_brief, language="Greek", length=article_length_map[article_length_label])
            except Exception as e: st.error(f"Σφάλμα Sports Article Writer: {e}")
    if st.session_state.sports_article_report:
        with st.container(border=True): st.write(st.session_state.sports_article_report)
    st.divider()

    st.subheader("💡 Marketing Brainstorm")
    brainstorm_challenge = st.text_area("Για ποιο θέμα θέλεις ιδέες;", key="brainstorm_challenge_input")
    brainstorm_goal = st.selectbox("Στόχος", ["Γενικές ιδέες marketing", "Αύξηση επισκεψιμότητας στα καταστήματα", "Brand awareness", "Καμπάνια για special event", "Customer engagement", "Κάτι ασυνήθιστο / πειραματικό"], key="brainstorm_goal")
    if st.button("💡 Δημιουργία Ιδεών", use_container_width=True):
        if not brainstorm_challenge.strip(): st.warning("Πες πρώτα στον agent για ποιο θέμα θέλεις ιδέες.")
        else:
            try:
                with st.spinner("Το Marketing Brainstorm σκέφτεται..."): st.session_state.brainstorm_report = run_marketing_brainstorm(client, brainstorm_challenge, goal=brainstorm_goal)
            except Exception as e: st.error(f"Σφάλμα Marketing Brainstorm: {e}")
    if st.session_state.brainstorm_report:
        with st.container(border=True): st.write(st.session_state.brainstorm_report)
    st.divider()

    st.write("⚪ 🎁 Promotion Selector"); st.caption("ΑΝΑΜΟΝΗ ΓΙΑ COMPANY FILES")
    st.write("⚪ 🎨 Creative Director"); st.caption("ΠΡΟΓΡΑΜΜΑΤΙΣΜΕΝΟ")
    st.write("⚪ ✍️ Social Media Writer"); st.caption("ΠΡΟΓΡΑΜΜΑΤΙΣΜΕΝΟ")
    st.divider(); st.success("BION ONLINE")