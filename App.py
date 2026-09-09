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
# STREAMLIT DESIGN
# =========================================================

st.markdown(
    """
<style>

html, body, .stApp {
    background: #030605 !important;
}

.stApp {
    background:
        radial-gradient(circle at 50% 10%,
        rgba(241,196,0,.07), transparent 32%),

        radial-gradient(circle at 10% 40%,
        rgba(68,136,62,.08), transparent 25%),

        radial-gradient(circle at 90% 40%,
        rgba(0,180,110,.05), transparent 25%),

        linear-gradient(180deg,#07100b,#020403) !important;
}

header {
    background: transparent !important;
}

#MainMenu, footer {
    visibility: hidden;
}

.block-container {
    max-width: 1650px;
    padding-top: .5rem;
    padding-bottom: 4rem;
}


/* SCI FI FLOOR GRID */

.stApp::after {

    content: "";
    position: fixed;

    left: -10%;
    right: -10%;
    bottom: -25%;

    height: 55%;

    pointer-events: none;

    background-image:

        linear-gradient(
        rgba(241,196,0,.06) 1px,
        transparent 1px),

        linear-gradient(
        90deg,
        rgba(68,136,62,.06) 1px,
        transparent 1px);

    background-size: 60px 60px;

    transform:
        perspective(500px)
        rotateX(65deg);

    transform-origin: center top;

    z-index: 0;
}


/* REAL STREAMLIT UI */

[data-testid="stVerticalBlockBorderWrapper"] {

    background:
        linear-gradient(
        145deg,
        rgba(10,16,12,.94),
        rgba(5,9,6,.94));

    border:
        1px solid rgba(241,196,0,.22) !important;

    border-radius: 18px;

    box-shadow:
        0 0 35px rgba(0,0,0,.5);

    backdrop-filter: blur(12px);
}


[data-testid="stChatMessage"] {

    background:
        rgba(8,14,10,.94);

    border:
        1px solid rgba(241,196,0,.13);

    border-radius: 15px;
}


[data-testid="stChatInput"] {
    border-radius: 14px;
}


.stButton > button {

    background:
        linear-gradient(
        135deg,
        #F1C400,
        #C9A500);

    color: #10120f;

    border: none;

    font-weight: 900;

    border-radius: 10px;
}


h1,h2,h3 {
    color: #F5F7F5;
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
# BOOKIEOS HQ
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

    color: white;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    overflow: hidden;
}


/* ======================================================
   HQ ROOM
====================================================== */

.hq {

    position: relative;

    width: 100%;
    height: 650px;

    overflow: hidden;

    border-radius: 25px;

    border:
        1px solid rgba(241,196,0,.28);

    background:

        radial-gradient(
            circle at 50% 48%,
            rgba(241,196,0,.10),
            transparent 25%
        ),

        radial-gradient(
            circle at 50% 48%,
            rgba(68,136,62,.08),
            transparent 42%
        ),

        repeating-linear-gradient(
            90deg,
            rgba(241,196,0,.025) 0px,
            rgba(241,196,0,.025) 1px,
            transparent 1px,
            transparent 80px
        ),

        repeating-linear-gradient(
            0deg,
            rgba(68,136,62,.02) 0px,
            rgba(68,136,62,.02) 1px,
            transparent 1px,
            transparent 80px
        ),

        linear-gradient(
            180deg,
            #07100b,
            #020503
        );

    box-shadow:
        inset 0 0 120px #000,
        0 0 50px rgba(0,0,0,.7);
}


/* STARS */

.stars {

    position: absolute;

    inset: 0;

    opacity: .35;

    background-image:

        radial-gradient(
            white 1px,
            transparent 1px
        );

    background-size:
        95px 95px;

    animation:
        starsMove 30s linear infinite;
}


/* ======================================================
   TOP BAR
====================================================== */

.logo {

    position: absolute;

    top: 24px;
    left: 32px;

    font-size: 30px;

    font-weight: 900;

    letter-spacing: 3px;
}

.yellow {
    color: #F1C400;
}

.green {
    color: #55C650;
}

.subtitle {

    position: absolute;

    top: 65px;
    left: 34px;

    font-size: 9px;

    letter-spacing: 2px;

    color: #718078;
}


.location {

    position: absolute;

    right: 32px;
    top: 27px;

    text-align: right;

    color: #718078;

    font-size: 9px;

    letter-spacing: 1px;
}


.location strong {

    display: block;

    color: #F1C400;

    font-size: 19px;

    margin-top: 4px;
}


/* ======================================================
   CENTRAL BOOKIEOS CORE
====================================================== */

.core-system {

    position: absolute;

    left: 50%;
    top: 52%;

    transform:
        translate(-50%,-50%);

    width: 360px;
    height: 360px;
}


.ring {

    position: absolute;

    border-radius: 50%;
}


.ring-one {

    inset: 0;

    border:
        1px solid rgba(241,196,0,.30);

    border-left-color:
        #F1C400;

    border-right-color:
        #44883E;

    animation:
        rotate 18s linear infinite;
}


.ring-two {

    inset: 30px;

    border:
        2px dashed rgba(68,136,62,.40);

    animation:
        reverseRotate 13s linear infinite;
}


.ring-three {

    inset: 65px;

    border:
        1px solid rgba(241,196,0,.60);

    box-shadow:
        0 0 30px rgba(241,196,0,.15);

    animation:
        ringPulse 2.5s ease-in-out infinite;
}


.core {

    position: absolute;

    left: 95px;
    top: 95px;

    width: 170px;
    height: 170px;

    border-radius: 50%;

    display: flex;

    align-items: center;
    justify-content: center;

    text-align: center;

    border:
        2px solid #F1C400;

    background:

        radial-gradient(
            circle at 50% 42%,
            rgba(255,225,72,.92),
            rgba(241,196,0,.48) 18%,
            rgba(68,136,62,.20) 43%,
            rgba(3,8,5,.98) 72%
        );

    box-shadow:
        0 0 25px #F1C400,
        0 0 70px rgba(241,196,0,.38),
        0 0 120px rgba(68,136,62,.16);

    animation:
        corePulse 2.2s ease-in-out infinite;
}


.core-name {

    font-size: 20px;

    font-weight: 900;

    letter-spacing: 2px;
}


.core-sub {

    margin-top: 5px;

    font-size: 7px;

    color: #B9C1BA;

    letter-spacing: 1.5px;
}


.core-online {

    margin-top: 10px;

    font-size: 8px;

    color: #73E66C;

    font-weight: 900;

    letter-spacing: 1px;
}


/* ======================================================
   AGENTS
====================================================== */

.agent {

    position: absolute;

    width: 260px;

    min-height: 104px;

    padding: 14px;

    border-radius: 14px;

    background:

        linear-gradient(
            135deg,
            rgba(14,23,17,.96),
            rgba(5,10,7,.94)
        );

    border:
        1px solid rgba(241,196,0,.25);

    box-shadow:
        0 0 25px rgba(0,0,0,.5);
}


.agent.online {

    border-color:
        rgba(83,213,77,.45);

    box-shadow:
        0 0 18px rgba(68,136,62,.10);
}


.agent-title {

    font-size: 12px;

    font-weight: 900;

    letter-spacing: .4px;
}


.agent-job {

    margin-top: 7px;

    color: #78847B;

    font-size: 9px;

    line-height: 1.45;
}


.status-online {

    margin-top: 8px;

    color: #70E568;

    font-size: 8px;

    font-weight: 900;

    letter-spacing: 1px;
}


.status-planned {

    margin-top: 8px;

    color: #F1C400;

    font-size: 8px;

    font-weight: 900;

    letter-spacing: 1px;
}


.a1 {
    left: 4%;
    top: 140px;
}

.a2 {
    left: 4%;
    top: 275px;
}

.a3 {
    left: 4%;
    top: 410px;
}


.a4 {
    right: 4%;
    top: 140px;
}

.a5 {
    right: 4%;
    top: 275px;
}

.a6 {
    right: 4%;
    top: 410px;
}


/* ======================================================
   CONNECTION BEAMS
====================================================== */

.beam {

    position: absolute;

    width: 190px;
    height: 1px;

    background:

        linear-gradient(
            90deg,
            transparent,
            rgba(241,196,0,.9),
            rgba(68,136,62,.8),
            transparent
        );

    box-shadow:
        0 0 9px rgba(241,196,0,.4);

    opacity: .6;

    animation:
        beamPulse 2s ease-in-out infinite;
}


.b1 {
    left: calc(50% - 355px);
    top: 200px;
}

.b2 {
    left: calc(50% - 355px);
    top: 335px;
}

.b3 {
    left: calc(50% - 355px);
    top: 470px;
}


.b4 {
    right: calc(50% - 355px);
    top: 200px;
}

.b5 {
    right: calc(50% - 355px);
    top: 335px;
}

.b6 {
    right: calc(50% - 355px);
    top: 470px;
}


/* ======================================================
   FLOATING SPORTS OBJECTS
====================================================== */

.sport {

    position: absolute;

    display: flex;

    align-items: center;
    justify-content: center;

    width: 64px;
    height: 64px;

    border-radius: 50%;

    font-size: 28px;

    background:

        radial-gradient(
            circle,
            rgba(241,196,0,.13),
            rgba(5,12,8,.60)
        );

    border:
        1px solid rgba(241,196,0,.25);

    box-shadow:
        0 0 25px rgba(241,196,0,.10);

    animation:
        float 6s ease-in-out infinite;
}


.football {

    left: 30%;
    top: 100px;
}


.basketball {

    right: 29%;
    top: 105px;

    animation-delay: -1.5s;
}


.f1 {

    left: 30%;
    bottom: 50px;

    animation-delay: -3s;
}


.tennis {

    right: 29%;
    bottom: 55px;

    animation-delay: -4.5s;
}


.trophy {

    left: 50%;
    top: 87px;

    transform: translateX(-50%);

    width: 48px;
    height: 48px;

    font-size: 21px;

    animation:
        trophyFloat 6s ease-in-out infinite;
}


/* ======================================================
   BOTTOM STATUS
====================================================== */

.footer {

    position: absolute;

    bottom: 17px;
    left: 50%;

    transform:
        translateX(-50%);

    color: #667268;

    font-size: 8px;

    letter-spacing: 2px;

    white-space: nowrap;
}


.footer span {
    color: #F1C400;
}


/* ======================================================
   ANIMATION
====================================================== */

@keyframes rotate {

    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}


@keyframes reverseRotate {

    from {
        transform: rotate(360deg);
    }

    to {
        transform: rotate(0deg);
    }
}


@keyframes corePulse {

    0%,100% {

        box-shadow:
            0 0 22px #F1C400,
            0 0 60px rgba(241,196,0,.30);
    }

    50% {

        box-shadow:
            0 0 38px #F1C400,
            0 0 100px rgba(241,196,0,.52);
    }
}


@keyframes ringPulse {

    0%,100% {
        opacity: .4;
    }

    50% {
        opacity: 1;
    }
}


@keyframes beamPulse {

    0%,100% {
        opacity: .25;
    }

    50% {
        opacity: .9;
    }
}


@keyframes float {

    0%,100% {
        transform:
            translateY(0px)
            rotate(-4deg);
    }

    50% {
        transform:
            translateY(-20px)
            rotate(7deg);
    }
}


@keyframes trophyFloat {

    0%,100% {
        transform:
            translateX(-50%)
            translateY(0px);
    }

    50% {
        transform:
            translateX(-50%)
            translateY(-15px);
    }
}


@keyframes starsMove {

    from {
        background-position: 0 0;
    }

    to {
        background-position: 95px 95px;
    }
}


/* ======================================================
   SMALL SCREENS
====================================================== */

@media(max-width:1100px) {

    .agent {
        width: 215px;
    }

    .core-system {

        transform:
            translate(-50%,-50%)
            scale(.78);
    }

    .sport {
        opacity: .5;
    }
}

</style>

</head>


<body>

<div class="hq">


    <div class="stars"></div>


    <!-- LOGO -->

    <div class="logo">

        <span class="yellow">
            ◉ BOOKIE
        </span>

        <span class="green">
            OS
        </span>

    </div>


    <div class="subtitle">
        BOOKIECO ARTIFICIAL INTELLIGENCE · SCIENTIFIC OPERATIONS HQ
    </div>


    <div class="location">

        LARNACA · CYPRUS

        <strong id="clock">
            00:00:00
        </strong>

        HQ NETWORK ONLINE

    </div>



    <!-- FLOATING SPORTS -->

    <div class="sport football">
        ⚽
    </div>

    <div class="sport basketball">
        🏀
    </div>

    <div class="sport f1">
        🏎️
    </div>

    <div class="sport tennis">
        🎾
    </div>

    <div class="sport trophy">
        🏆
    </div>



    <!-- BEAMS -->

    <div class="beam b1"></div>
    <div class="beam b2"></div>
    <div class="beam b3"></div>

    <div class="beam b4"></div>
    <div class="beam b5"></div>
    <div class="beam b6"></div>



    <!-- LEFT AGENTS -->

    <div class="agent online a1">

        <div class="agent-title">
            🔎 WEEKLY MATCH SCOUT
        </div>

        <div class="agent-job">
            Finds the strongest upcoming sporting events for BookieCo marketing.
        </div>

        <div class="status-online">
            ● ONLINE
        </div>

    </div>


    <div class="agent online a2">

        <div class="agent-title">
            🧠 BET RESEARCHER
        </div>

        <div class="agent-job">
            Researches teams, players, statistics and betting concepts.
        </div>

        <div class="status-online">
            ● ONLINE · AUTO
        </div>

    </div>


    <div class="agent a3">

        <div class="agent-title">
            📣 MARKETING MANAGER
        </div>

        <div class="agent-job">
            Creates BookieCo's final weekly marketing plan.
        </div>

        <div class="status-planned">
            COMING NEXT
        </div>

    </div>



    <!-- RIGHT AGENTS -->

    <div class="agent a4">

        <div class="agent-title">
            🎁 PROMOTION SELECTOR
        </div>

        <div class="agent-job">
            Selects the best BookieCo promotion for each event.
        </div>

        <div class="status-planned">
            PLANNED
        </div>

    </div>


    <div class="agent a5">

        <div class="agent-title">
            🎨 CREATIVE DIRECTOR
        </div>

        <div class="agent-job">
            Controls templates, graphics and campaign creative direction.
        </div>

        <div class="status-planned">
            PLANNED
        </div>

    </div>


    <div class="agent a6">

        <div class="agent-title">
            ✍️ SOCIAL MEDIA WRITER
        </div>

        <div class="agent-job">
            Creates headlines, captions, stories and calls-to-action.
        </div>

        <div class="status-planned">
            PLANNED
        </div>

    </div>



    <!-- CENTRAL CORE -->

    <div class="core-system">

        <div class="ring ring-one"></div>

        <div class="ring ring-two"></div>

        <div class="ring ring-three"></div>


        <div class="core">

            <div>

                <div class="core-name">
                    BOOKIEOS
                </div>

                <div class="core-sub">
                    CENTRAL INTELLIGENCE
                </div>

                <div class="core-online">
                    ● CORE ONLINE
                </div>

            </div>

        </div>

    </div>



    <div class="footer">

        BOOKIECO AI HEADQUARTERS
        &nbsp;·&nbsp;
        <span>2 AGENTS ACTIVE</span>
        &nbsp;·&nbsp;
        MARKETING NETWORK

    </div>


</div>


<script>

function clock() {

    const now = new Date();

    document.getElementById("clock").innerText =
        now.toLocaleTimeString(
            "en-GB",
            {
                hour12:false
            }
        );
}

clock();

setInterval(
    clock,
    1000
);

</script>


</body>

</html>
"""


components.html(
    hq_html,
    height=665,
    scrolling=False
)


# =========================================================
# COMMAND CONSOLE
# =========================================================

space1, console, space2 = st.columns(
    [0.10, 1, 0.10]
)


with console:

    with st.container(border=True):

        st.subheader(
            "◉ BOOKIEOS COMMAND CONSOLE"
        )

        st.caption(
            "Command the BookieCo AI network."
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

                voice_prompt = (
                    transcription.text
                )

                st.info(
                    f"🎙️ {voice_prompt}"
                )


            except Exception as e:

                st.error(
                    f"Voice error: {e}"
                )


        # =================================================
        # TEXT
        # =================================================

        text_prompt = st.chat_input(
            "Ask BookieOS..."
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
                # SCOUT + RESEARCHER
                # =========================================

                if use_scout:

                    try:

                        st.markdown(
                            "### 🔎 WEEKLY MATCH SCOUT"
                        )

                        st.caption(
                            "Agent activated · researching upcoming sporting events"
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
