import streamlit as st
from openai import OpenAI

from weekly_match_scout import run_weekly_match_scout
from bet_researcher import run_bet_researcher


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="BookieOS",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# BOOKIECO COLORS
# =========================================================

BOOKIE_YELLOW = "#F1C400"
BOOKIE_GREEN = "#44883E"
BOOKIE_DARK = "#212322"
BOOKIE_PANEL = "#17191A"
BOOKIE_PANEL_2 = "#111314"
BOOKIE_TEXT = "#F4F4F4"
BOOKIE_MUTED = "#9FA3A6"


# =========================================================
# CUSTOM DESIGN
# =========================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background:
            radial-gradient(circle at 20% 0%, rgba(68,136,62,0.10), transparent 30%),
            radial-gradient(circle at 80% 0%, rgba(241,196,0,0.08), transparent 30%),
            {BOOKIE_PANEL_2};
        color: {BOOKIE_TEXT};
    }}

    header {{
        background: transparent !important;
    }}

    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }}

    /* -------------------------------------------------- */
    /* LOGO / HEADER                                      */
    /* -------------------------------------------------- */

    .bookie-header {{
        background: linear-gradient(
            135deg,
            rgba(33,35,34,0.98),
            rgba(20,22,21,0.98)
        );
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 24px 28px;
        margin-bottom: 22px;
        box-shadow: 0px 18px 60px rgba(0,0,0,0.25);
    }}

    .bookie-logo {{
        font-size: 34px;
        font-weight: 900;
        letter-spacing: 2px;
        margin: 0;
    }}

    .bookie-logo-yellow {{
        color: {BOOKIE_YELLOW};
    }}

    .bookie-logo-green {{
        color: {BOOKIE_GREEN};
    }}

    .bookie-subtitle {{
        color: {BOOKIE_MUTED};
        font-size: 13px;
        margin-top: 4px;
        letter-spacing: 1.2px;
        text-transform: uppercase;
    }}

    .system-live {{
        display: inline-block;
        margin-top: 14px;
        background: rgba(68,136,62,0.12);
        color: #7ED374;
        border: 1px solid rgba(68,136,62,0.4);
        border-radius: 999px;
        padding: 7px 12px;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
    }}

    /* -------------------------------------------------- */
    /* PANELS                                             */
    /* -------------------------------------------------- */

    .panel {{
        background: rgba(23,25,26,0.96);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0px 12px 35px rgba(0,0,0,0.20);
    }}

    .panel-title {{
        font-size: 14px;
        font-weight: 900;
        color: white;
        margin-bottom: 5px;
        letter-spacing: 0.5px;
    }}

    .panel-subtitle {{
        color: {BOOKIE_MUTED};
        font-size: 12px;
        margin-bottom: 12px;
    }}

    /* -------------------------------------------------- */
    /* AGENT CARDS                                        */
    /* -------------------------------------------------- */

    .agent-card {{
        background: linear-gradient(
            145deg,
            rgba(30,32,31,1),
            rgba(22,24,23,1)
        );
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 15px;
        padding: 14px;
        margin-bottom: 11px;
    }}

    .agent-name {{
        font-size: 14px;
        font-weight: 800;
        color: white;
        margin-bottom: 5px;
    }}

    .agent-job {{
        color: {BOOKIE_MUTED};
        font-size: 11px;
        line-height: 1.4;
        margin-bottom: 9px;
    }}

    .agent-online {{
        display: inline-block;
        background: rgba(68,136,62,0.13);
        border: 1px solid rgba(68,136,62,0.35);
        color: #7ED374;
        padding: 4px 8px;
        border-radius: 999px;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.7px;
    }}

    .agent-coming {{
        display: inline-block;
        background: rgba(241,196,0,0.10);
        border: 1px solid rgba(241,196,0,0.30);
        color: {BOOKIE_YELLOW};
        padding: 4px 8px;
        border-radius: 999px;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.7px;
    }}

    /* -------------------------------------------------- */
    /* METRIC CARDS                                       */
    /* -------------------------------------------------- */

    .metric-card {{
        background: rgba(23,25,26,0.96);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 16px;
        min-height: 100px;
    }}

    .metric-label {{
        color: {BOOKIE_MUTED};
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    .metric-value {{
        color: white;
        font-size: 24px;
        font-weight: 900;
        margin-top: 5px;
    }}

    .metric-yellow {{
        color: {BOOKIE_YELLOW};
    }}

    .metric-green {{
        color: #7ED374;
    }}

    /* -------------------------------------------------- */
    /* CHAT                                               */
    /* -------------------------------------------------- */

    [data-testid="stChatMessage"] {{
        background: rgba(23,25,26,0.92);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 8px;
    }}

    [data-testid="stChatInput"] {{
        border-radius: 14px;
    }}

    textarea {{
        border-radius: 12px !important;
    }}

    /* -------------------------------------------------- */
    /* BUTTONS                                            */
    /* -------------------------------------------------- */

    .stButton > button {{
        background: linear-gradient(
            135deg,
            {BOOKIE_YELLOW},
            #D7AD00
        );
        color: #111;
        border: none;
        border-radius: 12px;
        font-weight: 900;
        padding: 0.65rem 1rem;
    }}

    .stButton > button:hover {{
        border: none;
        color: #111;
        filter: brightness(1.05);
    }}

    hr {{
        border-color: rgba(255,255,255,0.06);
    }}

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

st.markdown(
    f"""
    <div class="bookie-header">

        <div class="bookie-logo">
            <span class="bookie-logo-yellow">◉ BOOKIE</span><span class="bookie-logo-green">OS</span>
        </div>

        <div class="bookie-subtitle">
            BookieCo Artificial Intelligence Operating System
        </div>

        <div class="system-live">
            ● SYSTEM ONLINE
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TOP METRICS
# =========================================================

metric_1, metric_2, metric_3, metric_4 = st.columns(4)


with metric_1:

    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Active Agents</div>
            <div class="metric-value metric-green">2</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with metric_2:

    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">System</div>
            <div class="metric-value metric-green">ONLINE</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with metric_3:

    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Department</div>
            <div class="metric-value metric-yellow">MARKETING</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with metric_4:

    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Next Agent</div>
            <div class="metric-value">MANAGER</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# =========================================================
# MAIN LAYOUT
# =========================================================

main_column, agent_column = st.columns(
    [3.2, 1],
    gap="large"
)


# =========================================================
# MAIN CHAT PANEL
# =========================================================

with main_column:

    st.markdown(
        """
        <div class="panel">
            <div class="panel-title">
                BOOKIEOS COMMAND CENTER
            </div>
            <div class="panel-subtitle">
                Talk to BookieOS. It will route tasks to the correct specialist agent.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


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
    # TEXT INPUT
    # =====================================================

    text_prompt = st.chat_input(
        "Ask BookieOS..."
    )

    user_prompt = text_prompt or voice_prompt


    # =====================================================
    # REQUEST HANDLING
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
            # AGENT WORKFLOW
            # =================================================

            if use_scout:

                try:

                    # =========================================
                    # AGENT 1
                    # =========================================

                    st.markdown(
                        "### 🔎 Weekly Match Scout"
                    )

                    with st.spinner(
                        "Scout is researching upcoming events..."
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


                    with st.spinner(
                        "Researcher is analysing the betting ideas..."
                    ):

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

Currently connected specialist agents:

1. Weekly Match Scout
2. Bet Researcher

Weekly Match Scout researches upcoming sporting
events that may be useful for BookieCo marketing.

Bet Researcher researches proposed football
betting ideas and evaluates whether they make sense.

BookieOS currently does NOT have access to
BookieCo live betting markets or odds.

Never invent odds.

Never claim that a betting market is available
at BookieCo unless it has actually been verified.

Future marketing agents will include:

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
# AGENT CONTROL PANEL
# =========================================================

with agent_column:

    st.markdown(
        """
        <div class="panel">
            <div class="panel-title">
                AGENT NETWORK
            </div>
            <div class="panel-subtitle">
                BookieOS specialist workforce
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # SCOUT
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="agent-card">

            <div class="agent-name">
                🔎 Weekly Match Scout
            </div>

            <div class="agent-job">
                Finds the strongest upcoming sports events for marketing.
            </div>

            <div class="agent-online">
                ● ONLINE
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # RESEARCHER
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="agent-card">

            <div class="agent-name">
                🧠 Bet Researcher
            </div>

            <div class="agent-job">
                Researches teams, players, statistics and betting angles.
            </div>

            <div class="agent-online">
                ● ONLINE · AUTO
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # MARKETING MANAGER
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="agent-card">

            <div class="agent-name">
                📣 Marketing Manager
            </div>

            <div class="agent-job">
                Decides what BookieCo should post and builds the weekly plan.
            </div>

            <div class="agent-coming">
                COMING NEXT
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # PROMOTION SELECTOR
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="agent-card">

            <div class="agent-name">
                🎁 Promotion Selector
            </div>

            <div class="agent-job">
                Selects the best BookieCo promotion for each day or event.
            </div>

            <div class="agent-coming">
                PLANNED
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # CREATIVE DIRECTOR
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="agent-card">

            <div class="agent-name">
                🎨 Creative Director
            </div>

            <div class="agent-job">
                Chooses templates, graphics, players and creative direction.
            </div>

            <div class="agent-coming">
                PLANNED
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # SOCIAL WRITER
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="agent-card">

            <div class="agent-name">
                ✍️ Social Media Writer
            </div>

            <div class="agent-job">
                Writes headlines, captions, stories and calls-to-action.
            </div>

            <div class="agent-coming">
                PLANNED
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <div style="
            margin-top:16px;
            text-align:center;
            color:{BOOKIE_MUTED};
            font-size:11px;
        ">
            BOOKIECO AI NETWORK
            <br>
            VERSION 0.1
        </div>
        """,
        unsafe_allow_html=True
    )
