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
    "sports_news_report", "competitor_report", "sports_calendar_report",
    "calendar_promo_ideas", "sports_article_report", "brainstorm_report"
]:
    if key not in st.session_state:
        st.session_state[key] = None

st.title("◉ BOOKIEOS")
st.caption("BookieCo Artificial Intelligence Operating System")
st.divider()
main_column, agent_column = st.columns([3, 1])

with main_column:
    st.subheader("BookieOS")
    st.caption("Ask BookieOS in English or Greek.")
    voice_prompt = None
    audio = st.audio_input("🎤 Talk to BookieOS")
    if audio is not None:
        try:
            transcription = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe", file=audio, language="el"
            )
            voice_prompt = transcription.text
            st.write("🎙️", voice_prompt)
        except Exception as e:
            st.error(f"Voice error: {e}")

    text_prompt = st.chat_input("Ask BookieOS...")
    user_prompt = text_prompt or voice_prompt

    if user_prompt:
        with st.chat_message("user"):
            st.write(user_prompt)
        with st.chat_message("assistant"):
            lower_prompt = user_prompt.lower()
            scout_words = [
                "weekly match", "match scout", "matches this week", "matches next week",
                "football this week", "football next week", "weekly football", "find matches",
                "marketing matches", "find games", "best games", "best matches",
                "αγώνες εβδομάδας", "αγωνες εβδομαδας", "αγώνες αυτής της εβδομάδας",
                "αγωνες αυτης της εβδομαδας", "αγώνες επόμενης εβδομάδας",
                "αγωνες επομενης εβδομαδας", "βρες αγώνες", "βρες αγωνες"
            ]
            use_scout = any(word in lower_prompt for word in scout_words)

            if use_scout:
                try:
                    with st.spinner("🔎 Weekly Match Scout is researching..."):
                        scout_report = run_weekly_match_scout(client, user_prompt)
                    st.markdown("### 🔎 Weekly Match Scout")
                    st.write(scout_report)
                    st.divider()

                    with st.spinner("🧠 Bet Researcher is analysing..."):
                        researcher_task = f"""
The Weekly Match Scout produced the report below.
Analyse EVERY proposed football betting idea. Research current team form, important player information, injuries and suspensions when relevant, and recent statistics. Rate each idea STRONG, REASONABLE or WEAK. We want interesting betting ideas for BookieCo marketing, including logical player, goals, BTTS, HT/FT, corners, cards and bet-builder concepts. Avoid boring extremely safe selections and unnecessary complexity. Do NOT provide betting odds, invent BookieCo odds, or claim a market is available at BookieCo. If an idea is weak, suggest a better betting angle.

SCOUT REPORT:
{scout_report}
"""
                        research_report = run_bet_researcher(client, researcher_task)
                    st.markdown("### 🧠 Bet Researcher")
                    st.write(research_report)
                    st.divider()

                    with st.spinner("📣 Marketing Manager is building the weekly plan..."):
                        marketing_report = run_marketing_manager(scout_report, research_report)
                    st.markdown("### 📣 Marketing Manager")
                    st.write(marketing_report)
                    st.success("Marketing analysis complete.")
                except Exception as e:
                    st.error(f"Agent error: {e}")
            else:
                try:
                    response = client.responses.create(
                        model="gpt-5.6-luna",
                        instructions="""
You are BookieOS, the central AI assistant for BookieCo, a retail betting company in Cyprus.

AUTOMATIC MARKETING WORKFLOW:
1. Weekly Match Scout
2. Bet Researcher
3. Marketing Manager

INDEPENDENT MANUAL AGENTS:
4. Sports News Monitor — checks important current sports developments.
5. Competitor Watch — checks public competitor marketing activity relevant to Cyprus.
6. Sports Calendar — looks about 90 days ahead for major sporting marketing opportunities and has an optional Promo Ideas tool. Promo ideas are concepts only, never approved/active promotions.
7. Sports Article Writer — creates editorial-style Greek or English sports/news articles and verifies current sports facts when needed.
8. Marketing Brainstorm — develops creative, practical BookieCo campaign and marketing ideas from a problem, opportunity, season or objective. It can research current information when useful.

PLANNED AGENTS: Promotion Selector, Creative Director, Social Media Writer.
BookieOS does not have access to live BookieCo betting markets or odds. Never invent odds or claim a market is available unless verified. Answer in the user's language and keep responses practical and concise.
""",
                        input=user_prompt
                    )
                    st.write(response.output_text)
                except Exception as e:
                    st.error(f"BookieOS error: {e}")

with agent_column:
    st.subheader("Live Agents")
    agents = [
        ("🔎 Weekly Match Scout", "CONNECTED"),
        ("🧠 Bet Researcher", "CONNECTED · AUTO"),
        ("📣 Marketing Manager", "CONNECTED · AUTO"),
        ("🚨 Sports News Monitor", "CONNECTED · MANUAL"),
        ("🏆 Competitor Watch", "CONNECTED · MANUAL"),
        ("📅 Sports Calendar", "CONNECTED · MANUAL"),
        ("📰 Sports Article Writer", "CONNECTED · MANUAL"),
        ("💡 Marketing Brainstorm", "CONNECTED · MANUAL"),
    ]
    for name, status in agents:
        st.write(f"🟢 {name}")
        st.caption(status)

    st.divider()
    st.subheader("🚨 Sports Intelligence")
    st.caption("Check major injuries, suspensions and important sports news.")
    if st.button("🚨 Check Sports News", use_container_width=True):
        try:
            with st.spinner("Checking current sports news..."):
                request = """
Perform a standalone current sports intelligence check. Search current sports news and identify only important developments that could realistically matter to BookieCo. Focus on major football injuries, suspensions, star players ruled out or returning, goalkeeper injuries, manager changes, major transfers, postponements, cancellations, squad problems and important lineup developments. Give extra attention to Cyprus football, Cyprus teams in Europe, Greek teams, Champions League, Europa League, Conference League, Premier League, La Liga, Serie A, Bundesliga and major internationals. Mention major Formula 1 or basketball news if important enough. Only show genuinely useful developments. Mark each item MAJOR, WATCH or UPDATE and include TEAM/EVENT, NEWS, WHY IT MATTERS and STATUS. If there are no important developments, say so clearly.
"""
                st.session_state.sports_news_report = run_sports_news_monitor(client, request)
        except Exception as e:
            st.error(f"Sports News Monitor error: {e}")
    if st.session_state.sports_news_report:
        with st.container(border=True):
            st.markdown("### Latest Alerts")
            st.write(st.session_state.sports_news_report)
    else:
        with st.container(border=True):
            st.caption("No sports intelligence check has been run yet.")

    st.divider()
    st.subheader("🏆 Competitor Intelligence")
    st.caption("Check recent promotions and marketing activity from competitors.")
    if st.button("🏆 Check Competitors", use_container_width=True):
        try:
            with st.spinner("Checking competitor activity..."):
                st.session_state.competitor_report = run_competitor_watch(client)
        except Exception as e:
            st.error(f"Competitor Watch error: {e}")
    if st.session_state.competitor_report:
        with st.container(border=True):
            st.markdown("### Latest Competitor Report")
            st.write(st.session_state.competitor_report)
    else:
        with st.container(border=True):
            st.caption("No competitor check has been run yet.")

    st.divider()
    st.subheader("📅 Sports Calendar")
    st.caption("Look ahead 90 days for major marketing opportunities.")
    if st.button("📅 Check Next 90 Days", use_container_width=True):
        try:
            with st.spinner("Building the 90-day sports calendar..."):
                st.session_state.sports_calendar_report = run_sports_calendar(client)
                st.session_state.calendar_promo_ideas = None
        except Exception as e:
            st.error(f"Sports Calendar error: {e}")
    if st.session_state.sports_calendar_report:
        with st.container(border=True):
            st.markdown("### 90-Day Marketing Radar")
            st.write(st.session_state.sports_calendar_report)
        if st.button("💡 Create Promo Ideas", use_container_width=True):
            try:
                with st.spinner("Creating special-event promo ideas..."):
                    promo_task = f"""
You are helping BookieCo brainstorm SPECIAL EVENT promotion concepts from the 90-day sports calendar below. Select only events that genuinely deserve a special campaign. Be creative, but every idea is a CONCEPT ONLY — NEEDS REVIEW. Never invent BookieCo odds, claim a market exists, copy competitors, or present a concept as active/approved. For each selected opportunity give EVENT, DATE, WHY IT DESERVES A PROMO, PROMO NAME, PROMO CONCEPT, HOW IT WORKS, WHY CUSTOMERS MAY FIND IT INTERESTING, MARKETING POTENTIAL, RECOMMENDED CONTENT, PREPARATION TIME and STATUS. End with the best 3 concepts ranked.

90-DAY SPORTS CALENDAR:
{st.session_state.sports_calendar_report}
"""
                    promo_response = client.responses.create(model="gpt-5.6-luna", input=promo_task)
                    st.session_state.calendar_promo_ideas = promo_response.output_text
            except Exception as e:
                st.error(f"Promo Ideas error: {e}")
        if st.session_state.calendar_promo_ideas:
            with st.container(border=True):
                st.markdown("### 💡 Special Event Promo Ideas")
                st.warning("Concepts only — these are not approved BookieCo promotions.")
                st.write(st.session_state.calendar_promo_ideas)
    else:
        with st.container(border=True):
            st.caption("No 90-day calendar check has been run yet.")

    st.divider()
    st.subheader("📰 Sports Article Writer")
    st.caption("Create a short sports/news article for external websites.")
    article_brief = st.text_area("Article brief", placeholder="Example: Write an article about the upcoming Champions League match and naturally mention BookieCo...", key="article_brief_input")
    article_language = st.selectbox("Language", ["Greek", "English"], key="article_language")
    article_length = st.selectbox("Length", ["Short", "Medium", "Long"], key="article_length")
    if st.button("📰 Create Article", use_container_width=True):
        if not article_brief.strip():
            st.warning("Write a short brief first.")
        else:
            try:
                with st.spinner("Sports Article Writer is working..."):
                    st.session_state.sports_article_report = run_sports_article_writer(
                        client, article_brief, language=article_language, length=article_length
                    )
            except Exception as e:
                st.error(f"Sports Article Writer error: {e}")
    if st.session_state.sports_article_report:
        with st.container(border=True):
            st.markdown("### Article Draft")
            st.write(st.session_state.sports_article_report)
    else:
        with st.container(border=True):
            st.caption("No article has been created yet.")

    st.divider()
    st.subheader("💡 Marketing Brainstorm")
    st.caption("Give BookieOS a marketing problem or opportunity and let it develop campaign ideas.")
    brainstorm_challenge = st.text_area(
        "What do you want ideas for?",
        placeholder="Example: September is quiet and I want ideas to bring more people into our shops...",
        key="brainstorm_challenge_input"
    )
    brainstorm_goal = st.selectbox(
        "Goal",
        ["General marketing ideas", "Increase shop traffic", "Brand awareness", "Special event campaign", "Customer engagement", "Something unusual / experimental"],
        key="brainstorm_goal"
    )
    if st.button("💡 Brainstorm Ideas", use_container_width=True):
        if not brainstorm_challenge.strip():
            st.warning("Tell the agent what you want ideas for first.")
        else:
            try:
                with st.spinner("Marketing Brainstorm is thinking and researching..."):
                    st.session_state.brainstorm_report = run_marketing_brainstorm(
                        client, brainstorm_challenge, goal=brainstorm_goal
                    )
            except Exception as e:
                st.error(f"Marketing Brainstorm error: {e}")
    if st.session_state.brainstorm_report:
        with st.container(border=True):
            st.markdown("### Brainstorm Results")
            st.write(st.session_state.brainstorm_report)
    else:
        with st.container(border=True):
            st.caption("No brainstorm has been run yet.")

    st.divider()
    st.write("⚪ 🎁 Promotion Selector")
    st.caption("WAITING FOR COMPANY FILES")
    st.write("⚪ 🎨 Creative Director")
    st.caption("PLANNED")
    st.write("⚪ ✍️ Social Media Writer")
    st.caption("PLANNED")
    st.divider()
    st.success("BOOKIEOS ONLINE")
