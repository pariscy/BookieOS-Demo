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
# GLOBAL SCI-FI BACKGROUND
# =========================================================

st.markdown(
    """
<style>

html,
body,
.stApp {
    background: #050807 !important;
}

header {
    background: transparent !important;
}

#MainMenu,
footer {
    visibility: hidden;
}

.block-container {
    max-width: 1700px;
    padding-top: 0.5rem;
    padding-bottom: 4rem;
}


/* ==========================================
   SCI-FI SPACE BACKGROUND
========================================== */

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;

    background:

        radial-gradient(
            circle at 50% 20%,
            rgba(241,196,0,.12),
            transparent 28%
        ),

        radial-gradient(
            circle at 15% 45%,
            rgba(68,136,62,.10),
            transparent 25%
        ),

        radial-gradient(
            circle at 85% 60%,
            rgba(0,255,170,.05),
            transparent 25%
        ),

        radial-gradient(
            circle at 20% 10%,
            rgba(255,255,255,.8) 0px,
            transparent 1px
        ),

        radial-gradient(
            circle at 75% 15%,
            rgba(255,255,255,.6) 0px,
            transparent 1px
        ),

        radial-gradient(
            circle at 40% 70%,
            rgba(255,255,255,.5) 0px,
            transparent 1px
        ),

        linear-gradient(
            180deg,
            #07100b,
            #030504
        );

    background-size:
        auto,
        auto,
        auto,
        170px 170px,
        220px 220px,
        260px 260px,
        auto;
}


/* ==========================================
   FUTURISTIC GRID
========================================== */

.stApp::after {
    content: "";
    position: fixed;

    left: -10%;
    right: -10%;
    bottom: -25%;
    height: 60%;

    pointer-events: none;

    background-image:
        linear-gradient(
            rgba(241,196,0,.07) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(68,136,62,.07) 1px,
            transparent 1px
        );

    background-size: 55px 55px;

    transform:
        perspective(450px)
        rotateX(62deg);

    transform-origin: center top;

    mask-image:
        linear-gradient(
            to bottom,
            transparent,
            black 35%,
            black
        );

    z-index: 0;
}


/* ==========================================
   KEEP CONTENT ABOVE BACKGROUND
========================================== */

[data-testid="stAppViewContainer"] > .main {
    position: relative;
    z-index: 2;
}


/* ==========================================
   FLOATING SPORTS
========================================== */

.sports-space {
    position: fixed;
    inset: 0;
    pointer-events: none;
    overflow: hidden;
    z-index: 1;
}

.sport {
    position: absolute;

    display: flex;
    align-items: center;
    justify-content: center;

    width: 65px;
    height: 65px;

    border-radius: 50%;

    font-size: 28px;

    background:
        radial-gradient(
            circle,
            rgba(241,196,0,.15),
            rgba(9,16,11,.55)
        );

    border:
        1px solid rgba(241,196,0,.25);

    box-shadow:
        0 0 20px rgba(241,196,0,.10),
        inset 0 0 20px rgba(68,136,62,.08);

    backdrop-filter: blur(5px);

    animation:
        floatSport 8s ease-in-out infinite;
}

.s1 {
    left: 3%;
    top: 21%;
}

.s2 {
    right: 4%;
    top: 25%;
    animation-delay: -2s;
}

.s3 {
    left: 8%;
    top: 68%;
    animation-delay: -4s;
}

.s4 {
    right: 7%;
    top: 70%;
    animation-delay: -6s;
}

.s5 {
    right: 20%;
    top: 12%;
    width: 52px;
    height: 52px;
    font-size: 23px;
    animation-delay: -3s;
}

@keyframes floatSport {

    0%,100% {
        transform:
            translateY(0px)
            rotate(0deg);
    }

    50% {
        transform:
            translateY(-22px)
            rotate(8deg);
    }
}


/* ==========================================
   STREAMLIT CONTAINERS
========================================== */

[data-testid="stVerticalBlockBorderWrapper"] {
    background:
        linear-gradient(
            145deg,
            rgba(11,17,13,.90),
            rgba(7,10,8,.87)
        );

    border:
        1px solid rgba(241,196,0,.20) !important;

    border-radius: 18px;

    backdrop-filter: blur(12px);

    box-shadow:
        0 0 30px rgba(0,0,0,.35),
        inset 0 0 30px rgba(68,136,62,.025);
}


[data-testid="stChatMessage"] {
    background: rgba(10,15,11,.92);
    border: 1px solid rgba(241,196,0,.12);
    border-radius: 15px;
}


[data-testid="stChatInput"] {
    background: rgba(7,11,8,.95);
    border-radius: 14px;
}


.stButton > button {
    background:
        linear-gradient(
            135deg,
            #F1C400,
            #C9A500
        );

    color: #10120f;

    border: none;

    border-radius: 10px;

    font-weight: 900;
}

</style>


<div class="sports-space">

    <div class="sport s1">
        ⚽
    </div>

    <div class="sport s2">
        🏀
    </div>

    <div class="sport s3">
        🏎️
    </div>

    <div class="sport s4">
        🎾
    </div>

    <div class="sport s5">
        🏆
    </div>

</div>
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
# SCI-FI HQ VISUAL
# =========================================================

hq = """
<!DOCTYPE html>

<html>

<head>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    overflow: hidden;
    background: transparent;
    font-family: Arial, sans-serif;
    color: white;
}

.hq {

    position: relative;

    height: 610px;

    overflow: hidden;

    border-radius: 24px;

    border:
        1px solid rgba(241,196,0,.25);

    background:

        radial-gradient(
            circle at center,
            rgba(241,196,0,.08),
            transparent 32%
        ),

        linear-gradient(
            rgba(5,10,7,.88),
            rgba(3,6,4,.96)
        );

    box-shadow:
        inset 0 0 100px rgba(0,0,0,.85),
        0 0 45px rgba(0,0,0,.55);
}


/* HEADER */

.title {

    position: absolute;

    top: 20px;
    left: 30px;

    font-size: 30px;

    font-weight: 900;

    letter-spacing: 3px;
}

.yellow {
    color: #F1C400;
}

.green {
    color: #59BE52;
}

.sub {

    position: absolute;

    top: 60px;
    left: 32px;

    color: #69766D;

    font-size: 10px;

    letter-spacing: 2px;
}


/* CENTRAL CORE */

.core-wrap {

    position: absolute;

    left: 50%;
    top: 52%;

    transform:
        translate(-50%,-50%);

    width: 350px;
    height: 350px;
}


.ring1,
.ring2,
.ring3 {

    position: absolute;

    border-radius: 50%;
}


.ring1 {

    inset: 0;

    border:
        1px solid rgba(241,196,0,.30);

    animation:
        rotate 16s linear infinite;
}


.ring2 {

    inset: 30px;

    border:
        2px dashed rgba(75,190,70,.35);

    animation:
        reverseRotate 12s linear infinite;
}


.ring3 {

    inset: 65px;

    border:
        1px solid rgba(241,196,0,.7);

    box-shadow:
        0 0 30px rgba(241,196,0,.15);

    animation:
        pulse 2.6s ease-in-out infinite;
}


.core {

    position: absolute;

    left: 95px;
    top: 95px;

    width: 160px;
    height: 160px;

    border-radius: 50%;

    display: flex;

    align-items: center;
    justify-content: center;

    text-align: center;

    border:
        2px solid #F1C400;

    background:

        radial-gradient(
            circle,
            rgba(241,196,0,.8),
            rgba(68,136,62,.28) 35%,
            rgba(5,9,6,.96) 70%
        );

    box-shadow:
        0 0 25px #F1C400,
        0 0 75px rgba(241,196,0,.38);

    animation:
        corePulse 2s ease-in-out infinite;
}


.core-name {

    font-size: 20px;

    font-weight: 900;

    letter-spacing: 2px;
}


.core-status {

    color: #70E268;

    margin-top: 8px;

    font-size: 9px;

    letter-spacing: 1px;
}


/* AGENTS */

.agent {

    position: absolute;

    width: 255px;

    padding: 15px;

    border-radius: 14px;

    background:
        linear-gradient(
            135deg,
            rgba(13,20,15,.96),
            rgba(7,12,8,.92)
        );

    border:
        1px solid rgba(241,196,0,.24);

    box-shadow:
        0 0 22px rgba(0,0,0,.45);
}


.agent.online {
    border-color:
        rgba(81,213,76,.38);
}


.a1 {
    top: 140px;
    left: 4%;
}

.a2 {
    top: 275px;
    left: 4%;
}

.a3 {
    top: 410px;
    left: 4%;
}

.a4 {
    top: 140px;
    right: 4%;
}

.a5 {
    top: 275px;
    right: 4%;
}

.a6 {
    top: 410px;
    right: 4%;
}


.agent-title {

    font-size: 13px;

    font-weight: 900;
}


.agent-job {

    color: #718078;

    font-size: 9px;

    line-height: 1.5;

    margin-top: 6px;
}


.online-status {

    color: #6EE466;

    font-size: 9px;

    font-weight: 900;

    margin-top: 8px;
}


.planned-status {

    color: #F1C400;

    font-size: 9px;

    font-weight: 900;

    margin-top: 8px;
}


/* CONNECTIONS */

.connector {

    position: absolute;

    height: 1px;

    width: 180px;

    opacity: .65;

    background:

        linear-gradient(
            90deg,
            transparent,
            #F1C400,
            #44883E,
            transparent
        );

    box-shadow:
        0 0 8px rgba(241,196,0,.35);
}


.c1 {
    left: calc(50% - 340px);
    top: 210px;
}

.c2 {
    left: calc(50% - 340px);
    top: 340px;
}

.c3 {
    left: calc(50% - 340px);
    top: 470px;
}


.c4 {
    right: calc(50% - 340px);
    top: 210px;
}

.c5 {
    right: calc(50% - 340px);
    top: 340px;
}

.c6 {
    right: calc(50% - 340px);
    top: 470px;
}


/* ANIMATIONS */

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


@keyframes pulse {

    0%,100% {
        opacity: .35;
    }

    50% {
        opacity: 1;
    }
}


@keyframes corePulse {

    0%,100% {

        box-shadow:
            0 0 20px #F1C400,
            0 0 55px rgba(241,196,0,.25);
    }

    50% {

        box-shadow:
            0 0 35px #F1C400,
            0 0 100px rgba(241,196,0,.5);
    }
}

</style>

</head>


<body>

<div class="hq">


<div class="title">

<span class="yellow">
◉ BOOKIE
</span>

<span class="green">
OS
</span>

</div>


<div class="sub">

BOOKIECO ARTIFICIAL INTELLIGENCE OPERATIONS HQ

</div>



<div class="connector c1"></div>
<div class="connector c2"></div>
<div class="connector c3"></div>

<div class="connector c4"></div>
<div class="connector c5"></div>
<div class="connector c6"></div>



<div class="agent online a1">

<div class="agent-title">
🔎 WEEKLY MATCH SCOUT
</div>

<div class="agent-job">
Scans upcoming sport events and identifies the strongest marketing opportunities.
</div>

<div class="online-status">
● ONLINE
</div>

</div>



<div class="agent online a2">

<div class="agent-title">
🧠 BET RESEARCHER
</div>

<div class="agent-job">
Analyses teams, players, form, statistics and betting concepts.
</div>

<div class="online-status">
● ONLINE · AUTO
</div>

</div>



<div class="agent a3">

<div class="agent-title">
📣 MARKETING MANAGER
</div>

<div class="agent-job">
Creates the final BookieCo weekly marketing plan.
</div>

<div class="planned-status">
COMING NEXT
</div>

</div>



<div class="agent a4">

<div class="agent-title">
🎁 PROMOTION SELECTOR
</div>

<div class="agent-job">
Selects the best BookieCo promotion for each event.
</div>

<div class="planned-status">
PLANNED
</div>

</div>



<div class="agent a5">

<div class="agent-title">
🎨 CREATIVE DIRECTOR
</div>

<div class="agent-job">
Controls templates, graphics and creative direction.
</div>

<div class="planned-status">
PLANNED
</div>

</div>



<div class="agent a6">

<div class="agent-title">
✍️ SOCIAL MEDIA WRITER
</div>

<div class="agent-job">
Creates headlines, captions and social media copy.
</div>

<div class="planned-status">
PLANNED
</div>

</div>



<div class="core-wrap">

<div class="ring1"></div>
<div class="ring2"></div>
<div class="ring3"></div>


<div class="core">

<div>

<div class="core-name">
BOOKIEOS
</div>

<div class="core-status">
● CENTRAL CORE ONLINE
</div>

</div>

</div>

</div>


</div>

</body>

</html>
"""


components.html(
    hq,
    height=625,
    scrolling=False
)


# =========================================================
# COMMAND CONSOLE
# =========================================================

center_left, center, center_right = st.columns(
    [0.12, 1, 0.12]
)


with center:

    with st.container(border=True):

        st.subheader(
            "◉ BOOKIEOS COMMAND CONSOLE"
        )

        st.caption(
            "Command the BookieCo AI network."
        )


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


        text_prompt = st.chat_input(
            "Ask BookieOS..."
        )


        user_prompt = (
            text_prompt
            or voice_prompt
        )


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


                if use_scout:

                    try:

                        st.markdown(
                            "### 🔎 WEEKLY MATCH SCOUT"
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

Interesting ideas may include:

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

Do NOT provide betting odds.

Do NOT invent BookieCo odds.

Do NOT claim a market is available at BookieCo.

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
                            f"Agent error: {e}"
                        )


                else:

                    try:

                        response = (
                            client.responses.create(

                                model="gpt-5.6-luna",

                                instructions="""
You are BookieOS.

You are the central AI operating system for
BookieCo, a retail betting company in Cyprus.

ACTIVE AGENTS:

Weekly Match Scout
Bet Researcher

PLANNED AGENTS:

Marketing Manager
Promotion Selector
Creative Director
Social Media Writer

BookieOS does not currently have access to
BookieCo live betting odds.

Never invent odds.

Never claim a BookieCo market is available
unless it has been verified.

Answer Greek in Greek.

Answer English in English.

Keep responses concise.
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
