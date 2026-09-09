import streamlit as st
from openai import OpenAI

from weekly_match_scout import run_weekly_match_scout
from bet_researcher import run_bet_researcher


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="BookieOS",
    page_icon="◉",
    layout="wide"
)

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

                "αγώνες εβδομάδας",
                "αγωνες εβδομαδας",
                "αγώνες αυτής της εβδομάδας",
                "αγωνες αυτης της εβδομαδας",
                "αγώνες επόμενης εβδομάδας",
                "αγωνες επομενης εβδομαδας"
            ]


            use_scout = any(
                word in lower_prompt
                for word in scout_words
            )


            # =================================================
            # WEEKLY MATCH WORKFLOW
            # =================================================

            if use_scout:

                try:

                    # -----------------------------------------
                    # AGENT 1
                    # -----------------------------------------

                    with st.spinner(
                        "Weekly Match Scout is researching..."
                    ):

                        scout_report = run_weekly_match_scout(
                            user_prompt
                        )


                    st.markdown(
                        "### 🔎 Weekly Match Scout"
                    )

                    st.write(
                        scout_report
                    )

                    st.divider()


                    # -----------------------------------------
                    # AGENT 2
                    # -----------------------------------------

                    with st.spinner(
                        "Bet Researcher is analysing..."
                    ):

                        researcher_task = f"""
The Weekly Match Scout produced the report below.

Analyse EVERY proposed football betting idea.

For each match:

1. Research current team form.
2. Research important player information.
3. Research injuries/suspensions when relevant.
4. Research recent statistics.
5. Evaluate the proposed betting idea.

Rate each idea:

STRONG
REASONABLE
WEAK

We want interesting betting ideas for BookieCo marketing.

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

Do NOT make combinations complicated just for the sake of it.

IMPORTANT:

Do NOT provide betting odds.

Do NOT invent BookieCo odds.

Do NOT claim that a betting market is available at BookieCo.

Market availability will be verified by another system in the future.

If an idea is weak, suggest a better betting angle.

SCOUT REPORT:

{scout_report}
"""


                        research_report = run_bet_researcher(
                            researcher_task
                        )


                    st.markdown(
                        "### 🧠 Bet Researcher"
                    )

                    st.write(
                        research_report
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

Currently connected specialist agents:

1. Weekly Match Scout
2. Bet Researcher

Weekly Match Scout researches upcoming sporting
events that may be useful for BookieCo marketing.

Bet Researcher researches the proposed football
betting ideas and evaluates whether they make sense.

IMPORTANT:

BookieOS currently does NOT have access to
BookieCo's live betting markets or odds.

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
        "🟢 Weekly Match Scout"
    )

    st.caption(
        "CONNECTED"
    )


    st.write(
        "🟢 Bet Researcher"
    )

    st.caption(
        "CONNECTED · AUTO"
    )


    st.write(
        "⚪ Marketing Manager"
    )

    st.caption(
        "COMING NEXT"
    )


    st.write(
        "⚪ Promotion Selector"
    )

    st.caption(
        "COMING NEXT"
    )


    st.divider()


    st.success(
        "BOOKIEOS ONLINE"
    )
