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
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# COLORS / CSS
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(circle at 15% 0%, rgba(68,136,62,0.10), transparent 28%),
        radial-gradient(circle at 85% 0%, rgba(241,196,0,0.08), transparent 28%),
        #101211;
}

header {
    background: transparent !important;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1550px;
}

/* TITLES */

h1, h2, h3 {
    color: #F4F4F4;
}

p {
    color: #B4B8B5;
}

/* CONTAINERS */

[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(23,25,24,0.94);
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 16px;
}

/* METRICS */

[data-testid="stMetric"] {
    background: rgba(23,25,24,0.96);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 15px 18px;
    border-radius: 15px;
}

[data-testid="stMetricLabel"] {
    color: #9FA3A0;
}

[data-testid="stMetricValue"] {
    color: #F1C400;
}

/* CHAT */

[data-testid="stChatMessage"] {
    background: rgba(23,25,24,0.95);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    margin-bottom: 10px;
}

[data-testid="stChatInput"] {
    border-radius: 14px;
}

/* BUTTONS */

.stButton > button {
    background: #F1C400;
    color: #151515;
    border: none;
    border-radius: 10px;
    font-weight: 800;
}

.stButton > button:hover {
    background: #FFD51A;
    color: #151515;
    border: none;
}

/* STATUS */

.online {
    color: #70D36B;
    font-weight: 800;
}

.planned {
    color: #F1C400;
    font-weight: 800;
}

.small-text {
    color: #8F9591;
    font-size: 0.82rem;
}

.agent-title {
    font-size: 1rem;
    font-weight: 800;
    color: white;
}

.logo {
    font-size: 2.2rem;
    font-weight: 900;
    letter-spacing: 2px;
}

.logo-yellow {
    color: #F1C400;
}

.logo-green {
    color: #44883E;
}

.system-text {
    color: #70D36B;
    font-weight: 800;
    letter-spacing: 1px;
}

</style>
""",
    unsafe_allow_html=True
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

with st.container(border=True):

    st.markdown(
        """
<span class="logo">
<span class="logo-yellow">◉ BOOKIE</span><span class="logo-green">OS</span>
</span>
""",
        unsafe_allow_html=True
    )

    st.caption(
        "BOOKIECO ARTIFICIAL INTELLIGENCE OPERATING SYSTEM"
    )

    st.markdown(
        '<span class="system-text">● SYSTEM ONLINE</span>',
        unsafe_allow_html=True
    )


# =========================================================
# METRICS
# =========================================================

st.write("")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "ACTIVE AGENTS",
        "2"
    )

with m2:
    st.metric(
        "SYSTEM",
        "ONLINE"
    )

with m3:
    st.metric(
        "DEPARTMENT",
        "MARKETING"
    )

with m4:
    st.metric(
        "NEXT AGENT",
        "MARKETING MANAGER"
    )


st.write("")


# =========================================================
# MAIN LAYOUT
# =========================================================

main, agents = st.columns(
    [3.2, 1],
    gap="large"
)


# =========================================================
# COMMAND CENTER
# =========================================================

with main:

    with st.container(border=True):

        st.subheader(
            "◉ BOOKIEOS COMMAND CENTER"
        )

        st.caption(
            "Give BookieOS a command. It will send the work to the correct specialist agents."
        )


    st.write("")


    # =====================================================
    # VOICE
    # =====================================================

    voice_prompt = None

    audio = st.audio_input(
        "🎤 Voice Command"
    )

    if audio is not None:

        try:

            transcription = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio,
                language="el"
            )

            voice_prompt = transcription.text

            st.info(
                f"🎙️ {voice_prompt}"
            )

        except Exception as e:

            st.error(
                f"Voice error: {e}"
            )


    # =====================================================
    # CHAT INPUT
    # =====================================================

    text_prompt = st.chat_input(
        "Ask BookieOS..."
    )

    user_prompt = text_prompt or voice_prompt


    # =====================================================
    # PROCESS COMMAND
    # =====================================================

    if user_prompt:

        with st.chat_message("user"):

            st.write(
                user_prompt
            )


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
            # WEEKLY MARKETING WORKFLOW
            # =================================================

            if use_scout:

                try:

                    # =========================================
                    # AGENT 1
                    # =========================================

                    st.markdown(
                        "### 🔎 Weekly Match Scout"
                    )

                    st.caption(
                        "Searching upcoming sporting events..."
                    )


                    with st.spinner(
                        "Scout working..."
                    ):

                        scout_report = run_weekly_match_scout(
                            user_prompt
                        )


                    st.write(
                        scout_report
                    )


                    st.divider()


                    # =========================================
                    # AGENT 2
                    # =========================================

                    st.markdown(
                        "### 🧠 Bet Researcher"
                    )

                    st.caption(
                        "Researching the Scout's recommendations..."
                    )


                    researcher_task = f"""
The Weekly Match Scout produced the report below.

Analyse EVERY proposed football betting idea.

For each match:

1. Research current team form.
2. Research important player information.
3. Research injuries and suspensions when relevant.
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


                    with st.spinner(
                        "Researcher working..."
                    ):

                        research_report = run_bet_researcher(
                            researcher_task
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

CONNECTED AGENTS:

1. Weekly Match Scout
2. Bet Researcher

Weekly Match Scout researches upcoming sporting
events for BookieCo marketing.

Bet Researcher researches proposed betting ideas,
teams, players and statistics.

BookieOS currently does NOT have access to
BookieCo live markets or odds.

Never invent odds.

Never claim a betting market is available at
BookieCo unless it has been verified.

PLANNED MARKETING AGENTS:

Marketing Manager
Promotion Selector
Creative Director
Social Media Writer

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
# AGENT NETWORK
# =========================================================

with agents:

    with st.container(border=True):

        st.subheader(
            "AGENT NETWORK"
        )

        st.caption(
            "Marketing Department"
        )


    # =====================================================
    # AGENT 1
    # =====================================================

    with st.container(border=True):

        st.markdown(
            "### 🔎 Weekly Match Scout"
        )

        st.caption(
            "Finds the strongest upcoming sporting events for marketing."
        )

        st.markdown(
            '<span class="online">● ONLINE</span>',
            unsafe_allow_html=True
        )


    # =====================================================
    # AGENT 2
    # =====================================================

    with st.container(border=True):

        st.markdown(
            "### 🧠 Bet Researcher"
        )

        st.caption(
            "Researches teams, players, statistics and betting angles."
        )

        st.markdown(
            '<span class="online">● ONLINE · AUTO</span>',
            unsafe_allow_html=True
        )


    # =====================================================
    # AGENT 3
    # =====================================================

    with st.container(border=True):

        st.markdown(
            "### 📣 Marketing Manager"
        )

        st.caption(
            "Decides what BookieCo should post and builds the weekly content plan."
        )

        st.markdown(
            '<span class="planned">COMING NEXT</span>',
            unsafe_allow_html=True
        )


    # =====================================================
    # AGENT 4
    # =====================================================

    with st.container(border=True):

        st.markdown(
            "### 🎁 Promotion Selector"
        )

        st.caption(
            "Chooses the best BookieCo promotion for each day or event."
        )

        st.markdown(
            '<span class="planned">PLANNED</span>',
            unsafe_allow_html=True
        )


    # =====================================================
    # AGENT 5
    # =====================================================

    with st.container(border=True):

        st.markdown(
            "### 🎨 Creative Director"
        )

        st.caption(
            "Chooses templates, graphics, players and creative direction."
        )

        st.markdown(
            '<span class="planned">PLANNED</span>',
            unsafe_allow_html=True
        )


    # =====================================================
    # AGENT 6
    # =====================================================

    with st.container(border=True):

        st.markdown(
            "### ✍️ Social Media Writer"
        )

        st.caption(
            "Writes headlines, captions, stories and calls-to-action."
        )

        st.markdown(
            '<span class="planned">PLANNED</span>',
            unsafe_allow_html=True
        )


    st.caption(
        "BOOKIECO AI NETWORK · v0.1"
    )
