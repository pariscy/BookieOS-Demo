import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI

from weekly_match_scout import run_weekly_match_scout
from bet_researcher import run_bet_researcher


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="BookieOS HQ",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# GLOBAL STREAMLIT STYLE
# =========================================================

st.markdown(
    """
<style>

html, body, [class*="css"] {
    font-family: Inter, Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 50% -10%, rgba(241,196,0,0.09), transparent 35%),
        radial-gradient(circle at 5% 30%, rgba(68,136,62,0.08), transparent 25%),
        #080b09;
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
    padding-top: 0.6rem;
    padding-bottom: 3rem;
    max-width: 1700px;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(13,17,14,0.92);
    border: 1px solid rgba(241,196,0,0.18) !important;
    border-radius: 18px;
    box-shadow: 0 0 30px rgba(0,0,0,0.4);
}

[data-testid="stChatMessage"] {
    background: rgba(14,18,15,0.92);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
}

[data-testid="stChatInput"] {
    border-radius: 14px;
}

.stButton > button {
    background: linear-gradient(135deg, #F1C400, #CBA600);
    color: #10120f;
    font-weight: 900;
    border: none;
    border-radius: 12px;
}

.stButton > button:hover {
    background: #FFD928;
    color: #10120f;
    border: none;
}

h1, h2, h3 {
    color: #F4F7F3;
}

p {
    color: #AAB2AC;
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
# HQ VISUAL
# =========================================================

hq_html = """
<!DOCTYPE html>
<html>
<head>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: transparent;
    font-family: Arial, Helvetica, sans-serif;
    overflow: hidden;
    color: white;
}

.hq {
    position: relative;
    width: 100%;
    height: 620px;
    overflow: hidden;

    background:
        linear-gradient(rgba(8,12,9,.78), rgba(6,9,7,.93)),
        repeating-linear-gradient(
            90deg,
            rgba(241,196,0,.025) 0px,
            rgba(241,196,0,.025) 1px,
            transparent 1px,
            transparent 70px
        ),
        repeating-linear-gradient(
            0deg,
            rgba(68,136,62,.025) 0px,
            rgba(68,136,62,.025) 1px,
            transparent 1px,
            transparent 70px
        );

    border: 1px solid rgba(241,196,0,.20);
    border-radius: 24px;

    box-shadow:
        inset 0 0 80px rgba(0,0,0,.8),
        0 0 50px rgba(0,0,0,.5);
}


/* =======================================================
   TOP HUD
======================================================= */

.topbar {
    position: absolute;
    top: 18px;
    left: 26px;
    right: 26px;

    display: flex;
    align-items: center;
    justify-content: space-between;
}

.brand {
    font-size: 28px;
    font-weight: 900;
    letter-spacing: 3px;
}

.brand-yellow {
    color: #F1C400;
}

.brand-green {
    color: #62C65B;
}

.subtitle {
    margin-top: 5px;
    color: #758078;
    font-size: 10px;
    letter-spacing: 2px;
}

.clock {
    text-align: right;
    color: #BBC3BD;
    font-size: 11px;
    letter-spacing: 1px;
}

.clock strong {
    display: block;
    color: #F1C400;
    font-size: 20px;
}


/* =======================================================
   CORE
======================================================= */

.core-zone {
    position: absolute;

    left: 50%;
    top: 52%;

    transform: translate(-50%, -50%);

    width: 330px;
    height: 330px;
}

.core-ring-1,
.core-ring-2,
.core-ring-3 {
    position: absolute;
    border-radius: 50%;
}

.core-ring-1 {
    inset: 0;
    border: 1px solid rgba(241,196,0,.25);
    animation: rotate 18s linear infinite;
}

.core-ring-2 {
    inset: 27px;
    border: 2px dashed rgba(68,136,62,.45);
    animation: rotateReverse 13s linear infinite;
}

.core-ring-3 {
    inset: 58px;
    border: 1px solid rgba(241,196,0,.65);
    box-shadow:
        0 0 25px rgba(241,196,0,.25),
        inset 0 0 25px rgba(241,196,0,.15);
    animation: pulse 2.5s ease-in-out infinite;
}

.core {
    position: absolute;

    width: 150px;
    height: 150px;

    left: 90px;
    top: 90px;

    border-radius: 50%;

    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;

    background:
        radial-gradient(circle at 50% 45%,
            rgba(255,231,104,.95),
            rgba(241,196,0,.55) 18%,
            rgba(46,92,40,.25) 48%,
            rgba(5,10,6,.9) 75%
        );

    border: 2px solid #F1C400;

    box-shadow:
        0 0 20px #F1C400,
        0 0 50px rgba(241,196,0,.45),
        0 0 100px rgba(68,136,62,.25);

    animation: corePulse 2.4s ease-in-out infinite;
}

.core-title {
    font-weight: 900;
    font-size: 18px;
    letter-spacing: 2px;
}

.core-small {
    color: #D3D8D4;
    font-size: 8px;
    margin-top: 5px;
    letter-spacing: 1px;
}

.core-online {
    color: #79E16C;
    font-size: 9px;
    margin-top: 8px;
}


/* =======================================================
   CONNECTION LINES
======================================================= */

.line {
    position: absolute;
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        #F1C400,
        rgba(68,136,62,.9),
        transparent
    );

    opacity: .65;
    transform-origin: center;
    box-shadow: 0 0 8px rgba(241,196,0,.5);
}

.l1 {
    width: 205px;
    left: calc(50% - 355px);
    top: 210px;
    transform: rotate(15deg);
}

.l2 {
    width: 190px;
    left: calc(50% - 350px);
    top: 315px;
}

.l3 {
    width: 210px;
    left: calc(50% - 360px);
    top: 420px;
    transform: rotate(-15deg);
}

.r1 {
    width: 205px;
    right: calc(50% - 355px);
    top: 210px;
    transform: rotate(-15deg);
}

.r2 {
    width: 190px;
    right: calc(50% - 350px);
    top: 315px;
}

.r3 {
    width: 210px;
    right: calc(50% - 360px);
    top: 420px;
    transform: rotate(15deg);
}


/* =======================================================
   AGENT NODES
======================================================= */

.agent {
    position: absolute;

    width: 260px;
    min-height: 100px;

    padding: 14px 16px;

    background:
        linear-gradient(
            135deg,
            rgba(18,25,20,.96),
            rgba(8,13,10,.92)
        );

    border: 1px solid rgba(241,196,0,.20);
    border-radius: 14px;

    box-shadow:
        inset 0 0 20px rgba(68,136,62,.04),
        0 0 18px rgba(0,0,0,.45);
}

.agent.online {
    border-color: rgba(79,195,72,.40);
}

.agent.planned {
    opacity: .72;
}

.agent-icon {
    float: left;

    width: 46px;
    height: 46px;

    border-radius: 50%;

    margin-right: 12px;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 21px;

    background: rgba(241,196,0,.07);

    border: 1px solid rgba(241,196,0,.35);

    box-shadow:
        0 0 15px rgba(241,196,0,.10);
}

.online .agent-icon {
    border-color: rgba(86,216,77,.55);
    box-shadow: 0 0 15px rgba(86,216,77,.13);
}

.agent-name {
    font-size: 13px;
    font-weight: 900;
    letter-spacing: .5px;
}

.agent-desc {
    margin-top: 5px;
    color: #78837B;
    font-size: 9px;
    line-height: 1.4;
}

.status-online {
    margin-top: 8px;
    color: #73E16B;
    font-size: 9px;
    font-weight: 900;
    letter-spacing: 1px;
}

.status-next {
    margin-top: 8px;
    color: #F1C400;
    font-size: 9px;
    font-weight: 900;
    letter-spacing: 1px;
}

.a1 {
    left: 4%;
    top: 145px;
}

.a2 {
    left: 4%;
    top: 270px;
}

.a3 {
    left: 4%;
    top: 395px;
}

.a4 {
    right: 4%;
    top: 145px;
}

.a5 {
    right: 4%;
    top: 270px;
}

.a6 {
    right: 4%;
    top: 395px;
}


/* =======================================================
   BOTTOM HUD
======================================================= */

.bottom-status {
    position: absolute;

    bottom: 15px;
    left: 50%;

    transform: translateX(-50%);

    color: #657067;

    font-size: 9px;
    letter-spacing: 2px;
}

.bottom-status span {
    color: #F1C400;
}


/* =======================================================
   ANIMATIONS
======================================================= */

@keyframes rotate {

    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

@keyframes rotateReverse {

    from {
        transform: rotate(360deg);
    }

    to {
        transform: rotate(0deg);
    }
}

@keyframes pulse {

    0%,100% {
        opacity: .4;
        transform: scale(.98);
    }

    50% {
        opacity: 1;
        transform: scale(1.03);
    }
}

@keyframes corePulse {

    0%,100% {
        box-shadow:
            0 0 18px #F1C400,
            0 0 45px rgba(241,196,0,.35);
    }

    50% {
        box-shadow:
            0 0 28px #F1C400,
            0 0 80px rgba(241,196,0,.60);
    }
}


/* =======================================================
   RESPONSIVE
======================================================= */

@media (max-width: 1000px) {

    .agent {
        width: 205px;
    }

    .core-zone {
        transform: translate(-50%, -50%) scale(.82);
    }

}

</style>
</head>


<body>

<div class="hq">


    <!-- TOP -->

    <div class="topbar">

        <div>

            <div class="brand">

                <span class="brand-yellow">
                    ◉ BOOKIE
                </span>

                <span class="brand-green">
                    OS
                </span>

            </div>

            <div class="subtitle">
                ARTIFICIAL INTELLIGENCE OPERATIONS SYSTEM · BOOKIECO HQ
            </div>

        </div>


        <div class="clock">

            LARNACA · CYPRUS

            <strong id="clock">
                00:00:00
            </strong>

            HQ NETWORK ACTIVE

        </div>

    </div>



    <!-- CONNECTIONS -->

    <div class="line l1"></div>
    <div class="line l2"></div>
    <div class="line l3"></div>

    <div class="line r1"></div>
    <div class="line r2"></div>
    <div class="line r3"></div>



    <!-- LEFT AGENTS -->

    <div class="agent online a1">

        <div class="agent-icon">
            🔎
        </div>

        <div class="agent-name">
            WEEKLY MATCH SCOUT
        </div>

        <div class="agent-desc">
            Scans upcoming sport events and identifies the strongest marketing opportunities.
        </div>

        <div class="status-online">
            ● ONLINE
        </div>

    </div>



    <div class="agent online a2">

        <div class="agent-icon">
            🧠
        </div>

        <div class="agent-name">
            BET RESEARCHER
        </div>

        <div class="agent-desc">
            Analyses teams, players, form, statistics and betting concepts.
        </div>

        <div class="status-online">
            ● ONLINE · AUTO
        </div>

    </div>



    <div class="agent planned a3">

        <div class="agent-icon">
            📣
        </div>

        <div class="agent-name">
            MARKETING MANAGER
        </div>

        <div class="agent-desc">
            Converts agent intelligence into BookieCo's weekly marketing plan.
        </div>

        <div class="status-next">
            COMING NEXT
        </div>

    </div>



    <!-- RIGHT AGENTS -->

    <div class="agent planned a4">

        <div class="agent-icon">
            🎁
        </div>

        <div class="agent-name">
            PROMOTION SELECTOR
        </div>

        <div class="agent-desc">
            Selects the most suitable BookieCo promotion for each event or campaign.
        </div>

        <div class="status-next">
            PLANNED
        </div>

    </div>



    <div class="agent planned a5">

        <div class="agent-icon">
            🎨
        </div>

        <div class="agent-name">
            CREATIVE DIRECTOR
        </div>

        <div class="agent-desc">
            Chooses templates, visual direction, players, teams and campaign assets.
        </div>

        <div class="status-next">
            PLANNED
        </div>

    </div>



    <div class="agent planned a6">

        <div class="agent-icon">
            ✍️
        </div>

        <div class="agent-name">
            SOCIAL MEDIA WRITER
        </div>

        <div class="agent-desc">
            Creates headlines, captions, story copy and calls-to-action.
        </div>

        <div class="status-next">
            PLANNED
        </div>

    </div>



    <!-- CENTRAL CORE -->

    <div class="core-zone">

        <div class="core-ring-1"></div>
        <div class="core-ring-2"></div>
        <div class="core-ring-3"></div>

        <div class="core">

            <div>

                <div class="core-title">
                    BOOKIEOS
                </div>

                <div class="core-small">
                    CENTRAL INTELLIGENCE
                </div>

                <div class="core-online">
                    ● CORE ONLINE
                </div>

            </div>

        </div>

    </div>



    <div class="bottom-status">

        BOOKIECO SCIENTIFIC OPERATIONS HQ
        ·
        <span>2 AGENTS ACTIVE</span>
        ·
        MARKETING NETWORK

    </div>

</div>


<script>

function updateClock() {

    const now = new Date();

    document.getElementById("clock").innerText =
        now.toLocaleTimeString(
            "en-GB",
            {
                hour12: false
            }
        );
}

updateClock();

setInterval(
    updateClock,
    1000
);

</script>


</body>
</html>
"""


components.html(
    hq_html,
    height=640,
    scrolling=False
)


# =========================================================
# COMMAND TERMINAL
# =========================================================

left_space, command, right_space = st.columns(
    [0.12, 1, 0.12]
)


with command:

    with st.container(border=True):

        st.subheader(
            "◉ BOOKIEOS COMMAND TERMINAL"
        )

        st.caption(
            "Issue a command to the BookieCo AI network."
        )


        # =================================================
        # VOICE
        # =================================================

        voice_prompt = None

        audio = st.audio_input(
            "🎤 Voice Command"
        )


        if audio is not None:

            try:

                transcription = (
                    client.audio.transcriptions.create(
                        model="gpt-4o-mini-transcribe",
                        file=audio,
                        language="el"
                    )
                )

                voice_prompt = transcription.text

                st.info(
                    f"🎙️ {voice_prompt}"
                )


            except Exception as e:

                st.error(
                    f"Voice error: {e}"
                )


        # =================================================
        # CHAT
        # =================================================

        text_prompt = st.chat_input(
            "Enter command..."
        )

        user_prompt = (
            text_prompt
            or voice_prompt
        )


        # =================================================
        # PROCESS
        # =================================================

        if user_prompt:

            with st.chat_message("user"):

                st.write(
                    user_prompt
                )


            with st.chat_message("assistant"):


                lower_prompt = (
                    user_prompt.lower()
                )


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


                # =========================================
                # AGENT WORKFLOW
                # =========================================

                if use_scout:

                    try:

                        st.markdown(
                            "### 🔎 WEEKLY MATCH SCOUT"
                        )

                        st.caption(
                            "Agent activated · researching live sporting schedule"
                        )


                        with st.spinner(
                            "SCOUT ACTIVE..."
                        ):

                            scout_report = (
                                run_weekly_match_scout(
                                    user_prompt
                                )
                            )


                        st.write(
                            scout_report
                        )


                        st.divider()


                        st.markdown(
                            "### 🧠 BET RESEARCHER"
                        )

                        st.caption(
                            "Agent activated · analysing Scout intelligence"
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
                            "RESEARCHER ACTIVE..."
                        ):

                            research_report = (
                                run_bet_researcher(
                                    researcher_task
                                )
                            )


                        st.write(
                            research_report
                        )


                    except Exception as e:

                        st.error(
                            f"Agent system error: {e}"
                        )


                # =========================================
                # NORMAL BOOKIEOS
                # =========================================

                else:

                    try:

                        response = (
                            client.responses.create(

                                model="gpt-5.6-luna",

                                instructions="""
You are BookieOS.

You are the central artificial intelligence
operating system for BookieCo.

BookieCo is a retail betting company in Cyprus.

ACTIVE AGENTS:

1. Weekly Match Scout
2. Bet Researcher

Weekly Match Scout researches upcoming sporting
events for BookieCo marketing.

Bet Researcher researches teams, players,
statistics and proposed betting concepts.

PLANNED AGENTS:

Marketing Manager
Promotion Selector
Creative Director
Social Media Writer

BookieOS currently does NOT have access to
BookieCo live markets or odds.

Never invent odds.

Never claim that a betting market exists at
BookieCo unless it has been verified.

If the user speaks Greek, answer in Greek.

If the user speaks English, answer in English.

Keep responses concise and practical.
""",

                                input=user_prompt
                            )
                        )


                        st.write(
                            response.output_text
                        )


                    except Exception as e:

                        st.error(
                            f"BookieOS error: {e}"
                        )


# =========================================================
# LOWER HQ PANELS
# =========================================================

st.write("")


p1, p2, p3 = st.columns(3)


with p1:

    with st.container(border=True):

        st.markdown(
            "### 🟢 ACTIVE SYSTEMS"
        )

        st.write(
            "**Weekly Match Scout**"
        )

        st.caption(
            "ONLINE"
        )

        st.write(
            "**Bet Researcher**"
        )

        st.caption(
            "ONLINE · AUTOMATIC"
        )


with p2:

    with st.container(border=True):

        st.markdown(
            "### 📡 CURRENT NETWORK"
        )

        st.write(
            "**Department:** Marketing"
        )

        st.write(
            "**Agents Active:** 2"
        )

        st.write(
            "**BookieOS Core:** ONLINE"
        )


with p3:

    with st.container(border=True):

        st.markdown(
            "### 🧪 DEVELOPMENT"
        )

        st.write(
            "**Next:** Marketing Manager"
        )

        st.write(
            "**Later:** Promotions + Creative"
        )

        st.write(
            "**Future:** Risk · AML · Operations"
        )
