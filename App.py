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


st.set_page_config(page_title="BookieOS", page_icon="◉", layout="wide")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


for key in [
    "sports_news_report",
    "competitor_report",
    "sports_calendar_report",
    "calendar_promo_ideas",
    "sports_article_report",
    "brainstorm_report",
]:
    if key not in st.session_state:
        st.session_state[key] = None


GREEK_LANGUAGE_RULE = """
ΓΛΩΣΣΙΚΟΣ ΚΑΝΟΝΑΣ BOOKIEOS:
- Απάντησε στα Ελληνικά.
- Κράτησε τα ονόματα ομάδων στην αρχική/καθιερωμένη μορφή τους, π.χ. Manchester City, Real Madrid, APOEL.
- Κράτησε τα ονόματα διοργανώσεων στην αρχική/καθιερωμένη μορφή τους, π.χ. Champions League, Premier League, Europa League, Formula 1, EuroLeague.
- Κράτησε τα bet types και τη standard betting ορολογία στα Αγγλικά, π.χ. BTTS, Over 2.5, HT/FT, Correct Score, Player to Score, Bet Builder.
- Μην μεταφράζεις ονόματα ομάδων, ονόματα διοργανώσεων ή bet types.
- Όλα τα υπόλοιπα πρέπει να είναι στα Ελληνικά.
"""


def contains_any(text, words):
    return any(word in text for word in words)


def detect_agent(user_prompt):
    text = user_prompt.lower()

    if contains_any(text, [
        "brainstorm", "marketing brainstorm", "ιδέες marketing", "ιδεες marketing",
        "ιδέες μάρκετινγκ", "ιδεες μαρκετινγκ", "καμπάνια", "καμπανια",
        "ιδέες για καμπάνια", "ιδεες για καμπανια"
    ]):
        return "brainstorm"

    if contains_any(text, [
        "ανταγωνισ", "competitor", "τι κάνουν οι άλλοι", "τι κανουν οι αλλοι",
        "προσφορές ανταγωνιστών", "προσφορες ανταγωνιστων"
    ]):
        return "competitor"

    if contains_any(text, [
        "sports news", "αθλητικά νέα", "αθλητικα νεα", "τραυματισ", "τιμωρί",
        "τιμωρι", "suspension", "injury", "ποιος λείπει", "ποιος λειπει"
    ]):
        return "news"

    if contains_any(text, [
        "sports calendar", "ημερολόγιο", "ημερολογιο", "90 μέρες", "90 μερες",
        "επόμενους 3 μήνες", "επομενους 3 μηνες", "μεγάλα events", "μεγαλα events"
    ]):
        return "calendar"

    if contains_any(text, [
        "γράψε άρθρο", "γραψε αρθρο", "άρθρο", "αρθρο", "sports article",
        "news article", "article writer"
    ]):
        return "article"

    if contains_any(text, [
        "weekly match", "match scout", "matches this week", "matches next week",
        "football this week", "football next week", "find matches", "best matches",
        "αγώνες εβδομάδας", "αγωνες εβδομαδας", "αγώνες αυτής της εβδομάδας",
        "αγωνες αυτης της εβδομαδας", "αγώνες επόμενης εβδομάδας",
        "αγωνες επομενης εβδομαδας", "βρες αγώνες", "βρες αγωνες",
        "καλύτεροι αγώνες", "καλυτεροι αγωνες"
    ]):
        return "scout"

    return "bookieos"


def run_weekly_workflow(user_prompt):
    with st.spinner("🔎 Το Weekly Match Scout κάνει έρευνα..."):
        scout_report = run_weekly_match_scout(client, user_prompt)

    st.markdown("### 🔎 Weekly Match Scout")
    st.write(scout_report)
    st.divider()

    researcher_task = f"""
{GREEK_LANGUAGE_RULE}

Το Weekly Match Scout δημιούργησε την παρακάτω αναφορά.
Ανάλυσε ΚΑΘΕ προτεινόμενο football betting idea.
Έλεγξε current form, σημαντικές πληροφορίες παικτών, τραυματισμούς/τιμωρίες όταν χρειάζεται και πρόσφατα στατιστικά.
Βαθμολόγησε κάθε idea ως STRONG, REASONABLE ή WEAK.
Θέλουμε ενδιαφέροντα bet types για BookieCo marketing, όχι βαρετές ή υπερβολικά safe επιλογές.
Μην δώσεις odds, μην επινοήσεις BookieCo odds και μην ισχυριστείς ότι κάποιο market υπάρχει στο BookieCo.
Αν ένα idea είναι WEAK, πρότεινε καλύτερο betting angle.

SCOUT REPORT:
{scout_report}
"""

    with st.spinner("🧠 Το Bet Researcher αναλύει τα bet types..."):
        research_report = run_bet_researcher(client, researcher_task)

    st.markdown("### 🧠 Bet Researcher")
    st.write(research_report)
    st.divider()

    with st.spinner("📣 Το Marketing Manager ετοιμάζει το εβδομαδιαίο πλάνο..."):
        marketing_report = run_marketing_manager(scout_report, research_report)

    st.markdown("### 📣 Marketing Manager")
    st.write(marketing_report)
    st.success("Η ανάλυση marketing ολοκληρώθηκε.")


st.title("◉ BOOKIEOS")
st.caption("Το σύστημα τεχνητής νοημοσύνης της BookieCo")
st.divider()

main_column, agent_column = st.columns([3, 1])


with main_column:
    st.subheader("BookieOS")
    st.caption("Μίλησε ή γράψε φυσικά στα Ελληνικά. Το BookieOS θα επιλέξει τον σωστό agent.")

    voice_prompt = None
    audio = st.audio_input("🎤 Μίλησε στο BookieOS")

    if audio is not None:
        try:
            transcription = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio,
                language="el",
            )
            voice_prompt = transcription.text
            st.write("🎙️", voice_prompt)
        except Exception as e:
            st.error(f"Σφάλμα φωνής: {e}")

    text_prompt = st.chat_input("Ρώτησε το BookieOS...")
    user_prompt = text_prompt or voice_prompt

    if user_prompt:
        with st.chat_message("user"):
            st.write(user_prompt)

        with st.chat_message("assistant"):
            selected_agent = detect_agent(user_prompt)

            try:
                if selected_agent == "scout":
                    run_weekly_workflow(user_prompt)

                elif selected_agent == "brainstorm":
                    st.caption("💡 Δρομολόγηση → Marketing Brainstorm")
                    with st.spinner("💡 Το Marketing Brainstorm σκέφτεται και κάνει έρευνα..."):
                        result = run_marketing_brainstorm(client, user_prompt)
                    st.write(result)

                elif selected_agent == "competitor":
                    st.caption("🏆 Δρομολόγηση → Competitor Watch")
                    with st.spinner("🏆 Έλεγχος δραστηριότητας ανταγωνιστών..."):
                        result = run_competitor_watch(client)
                    st.write(result)

                elif selected_agent == "news":
                    st.caption("🚨 Δρομολόγηση → Sports News Monitor")
                    with st.spinner("🚨 Έλεγχος σημαντικών αθλητικών νέων..."):
                        result = run_sports_news_monitor(client, user_prompt)
                    st.write(result)

                elif selected_agent == "calendar":
                    st.caption("📅 Δρομολόγηση → Sports Calendar")
                    with st.spinner("📅 Έλεγχος επόμενων 90 ημερών..."):
                        result = run_sports_calendar(client)
                    st.write(result)

                elif selected_agent == "article":
                    st.caption("📰 Δρομολόγηση → Sports Article Writer")
                    with st.spinner("📰 Το Sports Article Writer γράφει το άρθρο..."):
                        result = run_sports_article_writer(
                            client,
                            user_prompt,
                            language="Greek",
                            length="Medium",
                        )
                    st.write(result)

                else:
                    response = client.responses.create(
                        model="gpt-5.6-luna",
                        instructions=f"""
You are BookieOS, the central AI assistant for BookieCo, a retail betting company in Cyprus.

{GREEK_LANGUAGE_RULE}

AVAILABLE AGENTS:
- Weekly Match Scout
- Bet Researcher
- Marketing Manager
- Sports News Monitor
- Competitor Watch
- Sports Calendar
- Sports Article Writer
- Marketing Brainstorm

PLANNED AGENTS:
- Promotion Selector
- Creative Director
- Social Media Writer

BookieOS does not currently have verified access to live BookieCo betting markets or odds.
Never invent odds or claim a market is available unless verified.
Keep answers practical and concise.
""",
                        input=user_prompt,
                    )
                    st.write(response.output_text)

            except Exception as e:
                st.error(f"Σφάλμα agent: {e}")


with agent_column:
    st.subheader("Ενεργοί Agents")

    agents = [
        ("🔎 Weekly Match Scout", "ΣΥΝΔΕΔΕΜΕΝΟ"),
        ("🧠 Bet Researcher", "ΣΥΝΔΕΔΕΜΕΝΟ · AUTO"),
        ("📣 Marketing Manager", "ΣΥΝΔΕΔΕΜΕΝΟ · AUTO"),
        ("🚨 Sports News Monitor", "ΣΥΝΔΕΔΕΜΕΝΟ · MANUAL / VOICE"),
        ("🏆 Competitor Watch", "ΣΥΝΔΕΔΕΜΕΝΟ · MANUAL / VOICE"),
        ("📅 Sports Calendar", "ΣΥΝΔΕΔΕΜΕΝΟ · MANUAL / VOICE"),
        ("📰 Sports Article Writer", "ΣΥΝΔΕΔΕΜΕΝΟ · MANUAL / VOICE"),
        ("💡 Marketing Brainstorm", "ΣΥΝΔΕΔΕΜΕΝΟ · MANUAL / VOICE"),
    ]

    for name, status in agents:
        st.write(f"🟢 {name}")
        st.caption(status)

    st.divider()

    st.subheader("🚨 Αθλητική Ενημέρωση")
    st.caption("Έλεγξε σημαντικούς τραυματισμούς, τιμωρίες και νέα που μπορούν να επηρεάσουν το marketing.")

    if st.button("🚨 Έλεγχος Sports News", use_container_width=True):
        try:
            with st.spinner("Έλεγχος σημαντικών αθλητικών νέων..."):
                request = f"""
{GREEK_LANGUAGE_RULE}
Κάνε ανεξάρτητο έλεγχο current sports news και βρες μόνο εξελίξεις που μπορούν πραγματικά να επηρεάσουν το BookieCo.
Εστίασε σε σημαντικούς τραυματισμούς, τιμωρίες, star players εκτός, επιστροφές, goalkeeper injuries, manager changes, σημαντικά transfers, postponements, cancellations, squad problems και lineup developments.
Δώσε επιπλέον προσοχή σε Cyprus football, Cyprus teams in Europe, Greek teams, Champions League, Europa League, Conference League, Premier League, La Liga, Serie A, Bundesliga και major internationals.
"""
                st.session_state.sports_news_report = run_sports_news_monitor(client, request)
        except Exception as e:
            st.error(f"Σφάλμα Sports News Monitor: {e}")

    if st.session_state.sports_news_report:
        with st.container(border=True):
            st.markdown("### Τελευταίες Ενημερώσεις")
            st.write(st.session_state.sports_news_report)
    else:
        with st.container(border=True):
            st.caption("Δεν έχει γίνει ακόμη έλεγχος sports news.")

    st.divider()

    st.subheader("🏆 Ανταγωνισμός")
    st.caption("Έλεγξε πρόσφατες καμπάνιες και marketing δραστηριότητα ανταγωνιστών.")

    if st.button("🏆 Έλεγχος Ανταγωνιστών", use_container_width=True):
        try:
            with st.spinner("Έλεγχος δραστηριότητας ανταγωνιστών..."):
                st.session_state.competitor_report = run_competitor_watch(client)
        except Exception as e:
            st.error(f"Σφάλμα Competitor Watch: {e}")

    if st.session_state.competitor_report:
        with st.container(border=True):
            st.markdown("### Τελευταία Αναφορά Ανταγωνισμού")
            st.write(st.session_state.competitor_report)
    else:
        with st.container(border=True):
            st.caption("Δεν έχει γίνει ακόμη έλεγχος ανταγωνιστών.")

    st.divider()

    st.subheader("📅 Sports Calendar")
    st.caption("Δες περίπου 90 ημέρες μπροστά για σημαντικές marketing ευκαιρίες.")

    if st.button("📅 Έλεγχος Επόμενων 90 Ημερών", use_container_width=True):
        try:
            with st.spinner("Δημιουργία 90-day Sports Calendar..."):
                st.session_state.sports_calendar_report = run_sports_calendar(client)
                st.session_state.calendar_promo_ideas = None
        except Exception as e:
            st.error(f"Σφάλμα Sports Calendar: {e}")

    if st.session_state.sports_calendar_report:
        with st.container(border=True):
            st.markdown("### 90-Day Marketing Radar")
            st.write(st.session_state.sports_calendar_report)

        if st.button("💡 Δημιουργία Promo Ideas", use_container_width=True):
            try:
                with st.spinner("Δημιουργία promo concepts..."):
                    promo_task = f"""
{GREEK_LANGUAGE_RULE}
Βοήθησε τη BookieCo να δημιουργήσει SPECIAL EVENT promotion concepts από το 90-day Sports Calendar παρακάτω.
Διάλεξε μόνο events που αξίζουν πραγματικά ειδική καμπάνια.
Κάθε ιδέα είναι μόνο CONCEPT — NEEDS REVIEW και όχι ενεργή ή εγκεκριμένη προσφορά.
Μην επινοείς BookieCo odds ή market availability και μην αντιγράφεις competitors.
Για κάθε concept δώσε event, date, γιατί αξίζει special promo, promo name, concept, πώς θα λειτουργούσε, marketing potential, recommended content, preparation time και status.
Στο τέλος κατάταξε τα καλύτερα 3.

90-DAY SPORTS CALENDAR:
{st.session_state.sports_calendar_report}
"""
                    promo_response = client.responses.create(
                        model="gpt-5.6-luna",
                        input=promo_task,
                    )
                    st.session_state.calendar_promo_ideas = promo_response.output_text
            except Exception as e:
                st.error(f"Σφάλμα Promo Ideas: {e}")

        if st.session_state.calendar_promo_ideas:
            with st.container(border=True):
                st.markdown("### 💡 Special Event Promo Ideas")
                st.warning("Μόνο concepts — δεν είναι εγκεκριμένες προσφορές της BookieCo.")
                st.write(st.session_state.calendar_promo_ideas)
    else:
        with st.container(border=True):
            st.caption("Δεν έχει δημιουργηθεί ακόμη 90-day calendar.")

    st.divider()

    st.subheader("📰 Sports Article Writer")
    st.caption("Δημιούργησε σύντομο αθλητικό/news άρθρο στα Ελληνικά για εξωτερικό website.")

    article_brief = st.text_area(
        "Τι θέλεις να γράψει;",
        placeholder="Παράδειγμα: Γράψε άρθρο για τον επερχόμενο αγώνα του Champions League και κάνε φυσική αναφορά στη BookieCo...",
        key="article_brief_input",
    )

    article_length_label = st.selectbox(
        "Μήκος άρθρου",
        ["Σύντομο", "Μεσαίο", "Μεγάλο"],
        key="article_length",
    )
    article_length_map = {
        "Σύντομο": "Short",
        "Μεσαίο": "Medium",
        "Μεγάλο": "Long",
    }

    if st.button("📰 Δημιουργία Άρθρου", use_container_width=True):
        if not article_brief.strip():
            st.warning("Γράψε πρώτα τι θέλεις να περιλαμβάνει το άρθρο.")
        else:
            try:
                with st.spinner("Το Sports Article Writer γράφει το άρθρο..."):
                    st.session_state.sports_article_report = run_sports_article_writer(
                        client,
                        article_brief,
                        language="Greek",
                        length=article_length_map[article_length_label],
                    )
            except Exception as e:
                st.error(f"Σφάλμα Sports Article Writer: {e}")

    if st.session_state.sports_article_report:
        with st.container(border=True):
            st.markdown("### Πρόχειρο Άρθρο")
            st.write(st.session_state.sports_article_report)
    else:
        with st.container(border=True):
            st.caption("Δεν έχει δημιουργηθεί ακόμη άρθρο.")

    st.divider()

    st.subheader("💡 Marketing Brainstorm")
    st.caption("Δώσε ένα marketing πρόβλημα ή στόχο και πάρε δημιουργικές, πρακτικές ιδέες.")

    brainstorm_challenge = st.text_area(
        "Για ποιο θέμα θέλεις ιδέες;",
        placeholder="Παράδειγμα: Ο Σεπτέμβριος είναι ήσυχος και θέλω ιδέες για να φέρουμε περισσότερο κόσμο στα καταστήματα...",
        key="brainstorm_challenge_input",
    )

    brainstorm_goal = st.selectbox(
        "Στόχος",
        [
            "Γενικές ιδέες marketing",
            "Αύξηση επισκεψιμότητας στα καταστήματα",
            "Brand awareness",
            "Καμπάνια για special event",
            "Customer engagement",
            "Κάτι ασυνήθιστο / πειραματικό",
        ],
        key="brainstorm_goal",
    )

    if st.button("💡 Δημιουργία Ιδεών", use_container_width=True):
        if not brainstorm_challenge.strip():
            st.warning("Πες πρώτα στον agent για ποιο θέμα θέλεις ιδέες.")
        else:
            try:
                with st.spinner("Το Marketing Brainstorm σκέφτεται και κάνει έρευνα..."):
                    st.session_state.brainstorm_report = run_marketing_brainstorm(
                        client,
                        brainstorm_challenge,
                        goal=brainstorm_goal,
                    )
            except Exception as e:
                st.error(f"Σφάλμα Marketing Brainstorm: {e}")

    if st.session_state.brainstorm_report:
        with st.container(border=True):
            st.markdown("### Αποτελέσματα Brainstorm")
            st.write(st.session_state.brainstorm_report)
    else:
        with st.container(border=True):
            st.caption("Δεν έχει γίνει ακόμη brainstorm.")

    st.divider()

    st.write("⚪ 🎁 Promotion Selector")
    st.caption("ΑΝΑΜΟΝΗ ΓΙΑ COMPANY FILES")

    st.write("⚪ 🎨 Creative Director")
    st.caption("ΠΡΟΓΡΑΜΜΑΤΙΣΜΕΝΟ")

    st.write("⚪ ✍️ Social Media Writer")
    st.caption("ΠΡΟΓΡΑΜΜΑΤΙΣΜΕΝΟ")

    st.divider()
    st.success("BOOKIEOS ONLINE")
