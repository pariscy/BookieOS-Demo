import streamlit as st
from openai import OpenAI

from weekly_match_scout import run_weekly_match_scout
from sports_news_monitor import run_sports_news_monitor
from bet_researcher import run_bet_researcher
from marketing_manager import run_marketing_manager


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="BookieOS",
    page_icon="◉",
    layout="wide"
)


# =========================================================
# OPENAI
# =========================================================

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


# =========================================================
# HEADER
# =========================================================

st.title("◉ BOOKIEOS")

st.caption(
    "BookieCo Artificial Intelligence Operating System"
)

st.divider()


# =========================================================
# LAYOUT
# =========================================================

main_column, agent_column = st.columns([3, 1])


# =========================================================
# MAIN BOOKIEOS
# =========================================================

with main_column:

    st.subheader("BookieOS")

    st.caption(
        "Ask BookieOS in English or Greek."
    )

    # -----------------------------------------------------
    # VOICE INPUT
    # -----------------------------------------------------

    voice_prompt = None

    audio = st.audio_input(
        "🎤 Talk to BookieOS"
    )

    if audio is not None:

        try:

            transcription = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio,
                language="el"
            )

            voice_prompt = transcription.text

            st.write(
                "🎙️",
                voice_prompt
            )

        except Exception as e:

            st.error(
                f"Voice error: {e}"
            )

    # -----------------------------------------------------
    # TEXT INPUT
    # -----------------------------------------------------

    text_prompt = st.chat_input(
        "Ask BookieOS..."
    )

    user_prompt = text_prompt or voice_prompt

    # -----------------------------------------------------
    # REQUEST
    # -----------------------------------------------------

    if user_prompt:

        with st.chat_message("user"):
            st.write(user_prompt)

        with st.chat_message("assistant"):

            lower_prompt = user_prompt.lower()

            scout_words = [
                "weekly match",
                "match scout",
                "matches this week",
                "matches next week",
                "football this week",
                "football next week",
                "weekly football",
                "find matches",
                "marketing matches",
                "find games",
                "best games",
                "best matches",

                "αγώνες εβδομάδας",
                "αγωνες εβδομαδας",
                "αγώνες αυτής της εβδομάδας",
                "αγωνες αυτης της εβδομαδας",
                "αγώνες επόμενης εβδομάδας",
                "αγωνες επομενης εβδομαδας",
                "βρες αγώνες",
                "βρες αγωνες"
            ]

            use_scout = any(
                word in lower_prompt
                for word in scout_words
            )

            # =================================================
            # FULL SPORTS MARKETING WORKFLOW
            # =================================================

            if use_scout:

                try:

                    # =========================================
                    # AGENT 1 — WEEKLY MATCH SCOUT
                    # =========================================

                    with st.spinner(
                        "🔎 Weekly Match Scout is researching..."
                    ):

                        scout_report = run_weekly_match_scout(
                            client,
                            user_prompt
                        )

                    st.markdown(
                        "### 🔎 Weekly Match Scout"
                    )

                    st.write(
                        scout_report
                    )

                    st.divider()

                    # =========================================
                    # AGENT 2 — SPORTS NEWS MONITOR
                    # =========================================

                    with st.spinner(
                        "🚨 Sports News Monitor is checking injuries, suspensions and major news..."
                    ):

                        news_report = run_sports_news_monitor(
                            client,
                            scout_report
                        )

                    st.markdown(
                        "### 🚨 Sports News Monitor"
                    )

                    st.write(
                        news_report
                    )

                    st.divider()

                    # =========================================
                    # AGENT 3 — BET RESEARCHER
                    # =========================================

                    with st.spinner(
                        "🧠 Bet Researcher is analysing..."
                    ):

                        researcher_task = f"""
The Weekly Match Scout has selected sporting events
for possible BookieCo marketing.

The Sports News Monitor has also researched current
injuries, suspensions, player availability and other
important developments.

Analyse EVERY proposed football betting idea.

Use BOTH reports.

If the Sports News Monitor found an injury,
suspension or other important development, take
that information into account.

If a proposed player bet involves a player who is:

- injured
- suspended
- doubtful
- unlikely to start
- unavailable

DO NOT recommend that player betting idea.

Find a better alternative when possible.

For each football match:

1. Research current team form.
2. Research important player information.
3. Research injuries and suspensions.
4. Research recent statistics.
5. Evaluate the proposed betting idea.

Rate each idea:

STRONG
REASONABLE
WEAK

We want interesting betting ideas for BookieCo
marketing.

Avoid boring extremely safe selections.

Interesting ideas can include:

- Player to score
- Player to score + team win
- Player to score + Over 2.5
- Team win + BTTS
- Result + Over goals
- HT/FT
- Team to win both halves
- Player shots on target
- Corners
- Cards
- Logical bet-builder combinations

Do NOT make combinations complicated just for
the sake of it.

IMPORTANT:

Do NOT provide betting odds.

Do NOT invent BookieCo odds.

Do NOT claim that a betting market is available
at BookieCo.

Market availability will be verified by another
system in the future.

If an idea is weak, suggest a better betting angle.


WEEKLY MATCH SCOUT REPORT:

{scout_report}


SPORTS NEWS MONITOR REPORT:

{news_report}
"""

                        research_report = run_bet_researcher(
                            client,
                            researcher_task
                        )

                    st.markdown(
                        "### 🧠 Bet Researcher"
                    )

                    st.write(
                        research_report
                    )

                    st.divider()

                    # =========================================
                    # AGENT 4 — MARKETING MANAGER
                    # =========================================

                    with st.spinner(
                        "📣 Marketing Manager is building the weekly plan..."
                    ):

                        marketing_report = run_marketing_manager(
                            scout_report,
                            research_report
                        )

                    st.markdown(
                        "### 📣 Marketing Manager"
                    )

                    st.write(
                        marketing_report
                    )

                    st.success(
                        "Sports marketing analysis complete."
                    )

                except Exception as e:

                    st.error(
                        f"Agent error: {e}"
                    )

            # =================================================
            # NORMAL BOOKIEOS
            # =================================================

            else:

                try:

                    response = client.responses.create(

                        model="gpt-5.6-luna",

                        instructions="""
You are BookieOS.

You are the central AI assistant for BookieCo,
a retail betting company in Cyprus.

CONNECTED SPECIALIST AGENTS:

1. Weekly Match Scout

Researches upcoming sporting events that may
be useful for BookieCo marketing.

2. Sports News Monitor

Checks important current sports news including
major injuries, suspensions, player availability,
manager changes, postponements and other
developments that could affect BookieCo's
sports analysis.

3. Bet Researcher

Researches teams, players, statistics and
proposed football betting ideas.

It receives information from both the Weekly
Match Scout and Sports News Monitor.

4. Marketing Manager

Receives the research and decides which
sporting opportunities BookieCo should
actually market.

The Marketing Manager evaluates every day
independently.

There are no automatic skip days.

If several genuinely strong opportunities
exist on the same day, several may be selected.

PLANNED MARKETING AGENTS:

- Promotion Selector
- Creative Director
- Social Media Writer

BookieOS currently does NOT have access to
BookieCo live betting markets or odds.

Never invent odds.

Never claim that a betting market is available
at BookieCo unless it has actually been verified.

If the user speaks Greek, answer in Greek.

If the user speaks English, answer in English.

Keep responses practical and concise.
""",

                        input=user_prompt
                    )

                    st.write(
                        response.output_text
                    )

                except Exception as e:

                    st.error(
                        f"BookieOS error: {e}"
                    )


# =========================================================
# AGENT PANEL
# =========================================================

with agent_column:

    st.subheader(
        "Live Agents"
    )

    st.write(
        "🟢 🔎 Weekly Match Scout"
    )

    st.caption(
        "CONNECTED"
    )

    st.write(
        "🟢 🚨 Sports News Monitor"
    )

    st.caption(
        "CONNECTED · AUTO"
    )

    st.write(
        "🟢 🧠 Bet Researcher"
    )

    st.caption(
        "CONNECTED · AUTO"
    )

    st.write(
        "🟢 📣 Marketing Manager"
    )

    st.caption(
        "CONNECTED · AUTO"
    )

    st.write(
        "⚪ 🎁 Promotion Selector"
    )

    st.caption(
        "WAITING FOR COMPANY FILES"
    )

    st.write(
        "⚪ 🎨 Creative Director"
    )

    st.caption(
        "PLANNED"
    )

    st.write(
        "⚪ ✍️ Social Media Writer"
    )

    st.caption(
        "PLANNED"
    )

    st.divider()

    st.success(
        "BOOKIEOS ONLINE"
    )
