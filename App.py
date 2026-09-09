import streamlit as st
import streamlit.components.v1 as components
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
# COLORS
# =========================================================

YELLOW = "#F1C400"
GREEN = "#44883E"
DARK = "#050806"


# =========================================================
# STREAMLIT CSS
# =========================================================

st.markdown(
    """
<style>

html,
body,
.stApp {
    background: #030604 !important;
}

header {
    background: transparent !important;
}

#MainMenu,
footer {
    visibility: hidden;
}

.block-container {
    max-width: 1800px;
    padding-top: 0.4rem;
    padding-bottom: 3rem;
}


/* BACKGROUND GLOW */

.stApp {
    background:

        radial-gradient(
            circle at 50% 0%,
            rgba(241,196,0,.07),
            transparent 30%
        ),

        radial-gradient(
            circle at 10% 40%,
            rgba(68,136,62,.07),
            transparent 25%
        ),

        linear-gradient(
            180deg,
            #071009,
            #020403
        ) !important;
}


/* CONSOLE */

[data-testid="stVerticalBlockBorderWrapper"] {

    background:
        linear-gradient(
            145deg,
            rgba(9,15,11,.96),
            rgba(4,8,5,.96)
        );

    border:
        1px solid rgba(241,196,0,.28) !important;

    border-radius: 14px;

    box-shadow:
        0 0 30px rgba(0,0,0,.55);
}


[data-testid="stChatMessage"] {

    background:
        rgba(7,13,9,.96);

    border:
        1px solid rgba(241,196,0,.12);

    border-radius: 12px;
}


[data-testid="stChatInput"] {

    background:
        rgba(7,11,8,.98);

    border-radius: 10px;
}


.stButton > button {

    background:
        linear-gradient(
            135deg,
            #F1C400,
            #C7A200
        );

    color: #111;

    border: none;

    border-radius: 8px;

    font-weight: 900;
}


.stButton > button:hover {

    background: #FFD724;

    color: #111;

    border: none;
}


h1,
h2,
h3 {
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
# MAIN HQ INTERFACE
# =========================================================

dashboard = """
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
   MAIN HUD
====================================================== */

.hud {

    position: relative;

    width: 100%;
    height: 860px;

    overflow: hidden;

    border-radius: 18px;

    border:
        1px solid rgba(241,196,0,.32);

    background:

        radial-gradient(
            circle at 50% 48%,
            rgba(241,196,0,.08),
            transparent 24%
        ),

        radial-gradient(
            circle at 50% 48%,
            rgba(68,136,62,.07),
            transparent 40%
        ),

        repeating-linear-gradient(
            90deg,
            rgba(241,196,0,.025) 0,
            rgba(241,196,0,.025) 1px,
            transparent 1px,
            transparent 70px
        ),

        repeating-linear-gradient(
            0deg,
            rgba(68,136,62,.025) 0,
            rgba(68,136,62,.025) 1px,
            transparent 1px,
            transparent 70px
        ),

        linear-gradient(
            180deg,
            #07100A,
            #020403
        );

    box-shadow:

        inset 0 0 140px rgba(0,0,0,.95),

        0 0 60px rgba(0,0,0,.7);
}


/* ======================================================
   BACKGROUND PARTICLES
====================================================== */

.stars {

    position: absolute;

    inset: 0;

    opacity: .25;

    background-image:

        radial-gradient(
            white 1px,
            transparent 1px
        );

    background-size:
        110px 110px;

    animation:
        stars 35s linear infinite;
}


/* ======================================================
   HEADER
====================================================== */

.brand {

    position: absolute;

    top: 20px;
    left: 30px;

    z-index: 10;
}


.brand-main {

    font-size: 28px;

    font-weight: 900;

    letter-spacing: 3px;
}


.yellow {
    color: #F1C400;
}


.green {
    color: #59C653;
}


.brand-sub {

    margin-top: 4px;

    font-size: 8px;

    color: #758078;

    letter-spacing: 2px;
}


.top-center {

    position: absolute;

    top: 19px;

    left: 50%;

    transform:
        translateX(-50%);

    text-align: center;
}


.top-title {

    color: #F1C400;

    font-size: 27px;

    font-weight: 900;

    letter-spacing: 4px;
}


.top-sub {

    color: #62CA59;

    font-size: 8px;

    letter-spacing: 2px;

    margin-top: 3px;
}


.system-online {

    margin-top: 9px;

    display: inline-block;

    padding: 5px 13px;

    border:
        1px solid rgba(90,210,80,.4);

    color: #70E568;

    font-size: 8px;

    letter-spacing: 1.5px;

    background:
        rgba(30,80,30,.10);
}


.clock {

    position: absolute;

    top: 20px;
    right: 30px;

    text-align: right;

    color: #7E8B81;

    font-size: 8px;

    letter-spacing: 1px;
}


.clock strong {

    display: block;

    color: #F1C400;

    font-size: 19px;

    margin-top: 4px;
}


/* ======================================================
   PANEL
====================================================== */

.panel {

    position: absolute;

    background:

        linear-gradient(
            145deg,
            rgba(8,16,10,.96),
            rgba(3,8,5,.96)
        );

    border:
        1px solid rgba(241,196,0,.27);

    box-shadow:
        0 0 20px rgba(0,0,0,.55);
}


.panel-heading {

    color: #F1C400;

    font-size: 10px;

    font-weight: 900;

    letter-spacing: 1px;

    margin-bottom: 12px;
}


/* ======================================================
   SPORTS MENU
====================================================== */

.sports {

    left: 28px;

    top: 105px;

    width: 175px;

    height: 310px;

    padding: 15px;
}


.sport-item {

    padding: 9px 4px;

    border-bottom:
        1px solid rgba(255,255,255,.04);

    color: #9FAAA2;

    font-size: 10px;

    letter-spacing: .5px;
}


.sport-item.active {

    color: #F1C400;

    background:
        rgba(241,196,0,.05);
}


.sport-icon {

    display: inline-block;

    width: 25px;

    color: #65CD5B;
}


/* ======================================================
   AGENTS
====================================================== */

.agents {

    left: 28px;

    top: 432px;

    width: 330px;

    height: 385px;

    padding: 15px;
}


.agent {

    position: relative;

    padding: 10px 8px;

    margin-bottom: 7px;

    min-height: 48px;

    border-bottom:
        1px solid rgba(255,255,255,.04);
}


.agent-icon {

    position: absolute;

    left: 2px;

    top: 8px;

    width: 34px;
    height: 34px;

    border-radius: 50%;

    display: flex;

    justify-content: center;
    align-items: center;

    border:
        1px solid rgba(241,196,0,.30);

    background:
        rgba(241,196,0,.05);
}


.agent-info {

    margin-left: 46px;
}


.agent-name {

    color: #EEF2EE;

    font-size: 9px;

    font-weight: 900;
}


.agent-job {

    color: #647068;

    font-size: 7px;

    margin-top: 4px;
}


.online {

    position: absolute;

    right: 3px;

    top: 15px;

    color: #69E661;

    font-size: 7px;

    font-weight: 900;
}


.planned {

    position: absolute;

    right: 3px;

    top: 15px;

    color: #F1C400;

    font-size: 7px;

    font-weight: 900;
}


/* ======================================================
   DATA PANEL
====================================================== */

.data {

    left: 220px;

    top: 105px;

    width: 245px;

    height: 215px;

    padding: 15px;
}


.wave {

    height: 65px;

    display: flex;

    align-items: end;

    gap: 3px;

    border-bottom:
        1px solid rgba(241,196,0,.12);

    padding-bottom: 8px;
}


.wave span {

    display: block;

    flex: 1;

    background:

        linear-gradient(
            #F1C400,
            #44883E
        );

    animation:
        bars 2s ease-in-out infinite alternate;
}


.wave span:nth-child(2n) {
    animation-delay: -.4s;
}

.wave span:nth-child(3n) {
    animation-delay: -.8s;
}


.data-line {

    display: flex;

    justify-content: space-between;

    margin-top: 11px;

    color: #7B877F;

    font-size: 8px;
}


.data-line strong {

    color: #65D65D;
}


/* ======================================================
   CORE
====================================================== */

.core-wrap {

    position: absolute;

    left: 52%;
    top: 47%;

    transform:
        translate(-50%,-50%);

    width: 520px;
    height: 520px;
}


.ring {

    position: absolute;

    border-radius: 50%;
}


.ring1 {

    inset: 0;

    border:
        1px solid rgba(241,196,0,.23);

    border-top-color:
        #F1C400;

    border-bottom-color:
        #44883E;

    animation:
        rotate 22s linear infinite;
}


.ring2 {

    inset: 35px;

    border:
        2px dashed rgba(68,136,62,.32);

    animation:
        reverseRotate 16s linear infinite;
}


.ring3 {

    inset: 75px;

    border:
        1px solid rgba(241,196,0,.45);

    animation:
        rotate 12s linear infinite;
}


.ring4 {

    inset: 115px;

    border:
        1px solid rgba(68,136,62,.38);

    box-shadow:
        0 0 35px rgba(68,136,62,.13);

    animation:
        pulse 2.4s ease-in-out infinite;
}


.globe {

    position: absolute;

    left: 145px;
    top: 145px;

    width: 230px;
    height: 230px;

    border-radius: 50%;

    overflow: hidden;

    border:
        2px solid #F1C400;

    background:

        repeating-linear-gradient(
            90deg,
            transparent,
            transparent 18px,
            rgba(241,196,0,.10) 19px
        ),

        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 18px,
            rgba(68,136,62,.10) 19px
        ),

        radial-gradient(
            circle at 40% 35%,
            rgba(255,225,60,.65),
            rgba(80,130,55,.25) 35%,
            rgba(4,10,6,.97) 70%
        );

    box-shadow:

        0 0 35px rgba(241,196,0,.60),

        0 0 90px rgba(241,196,0,.22),

        inset -30px -20px 40px rgba(0,0,0,.75);

    animation:
        globePulse 3s ease-in-out infinite;
}


.globe::before {

    content: "";

    position: absolute;

    width: 400px;
    height: 100%;

    background:

        repeating-linear-gradient(
            90deg,
            transparent,
            transparent 30px,
            rgba(241,196,0,.10) 31px
        );

    animation:
        globeMove 12s linear infinite;
}


.core-label {

    position: absolute;

    left: 50%;
    top: 50%;

    transform:
        translate(-50%,-50%);

    z-index: 4;

    text-align: center;
}


.core-bookie {

    font-size: 25px;

    font-weight: 900;

    color: #F1C400;

    letter-spacing: 2px;
}


.core-os {

    color: #5ED05A;
}


.core-small {

    font-size: 7px;

    color: #C4CCC5;

    letter-spacing: 2px;

    margin-top: 8px;
}


/* ======================================================
   SPORTS ORBIT
====================================================== */

.orbit {

    position: absolute;

    width: 54px;
    height: 54px;

    border-radius: 50%;

    display: flex;

    align-items: center;
    justify-content: center;

    font-size: 23px;

    border:
        1px solid rgba(241,196,0,.28);

    background:
        rgba(6,12,8,.80);

    box-shadow:
        0 0 15px rgba(241,196,0,.10);

    animation:
        float 6s ease-in-out infinite;
}


.football {

    left: 5px;
    top: 130px;
}


.basketball {

    right: 8px;
    top: 135px;

    animation-delay: -1.2s;
}


.tennis {

    left: 10px;
    bottom: 120px;

    animation-delay: -2.5s;
}


.f1 {

    right: 10px;
    bottom: 125px;

    animation-delay: -3.6s;
}


/* ======================================================
   RIGHT UPCOMING
====================================================== */

.upcoming {

    right: 28px;

    top: 105px;

    width: 300px;

    height: 255px;

    padding: 15px;
}


.event {

    padding: 11px 2px;

    border-bottom:
        1px solid rgba(255,255,255,.05);
}


.event-title {

    font-size: 9px;

    color: #EEF2EE;
}


.event-sub {

    margin-top: 4px;

    color: #657068;

    font-size: 7px;
}


/* ======================================================
   RIGHT INTELLIGENCE
====================================================== */

.intel {

    right: 28px;

    top: 377px;

    width: 300px;

    height: 195px;

    padding: 15px;
}


.intel-row {

    margin-top: 13px;
}


.intel-label {

    display: flex;

    justify-content: space-between;

    font-size: 8px;

    color: #7D897F;
}


.progress {

    height: 5px;

    margin-top: 5px;

    background:
        rgba(255,255,255,.05);
}


.progress div {

    height: 100%;

    background:

        linear-gradient(
            90deg,
            #44883E,
            #F1C400
        );
}


/* ======================================================
   RIGHT STATUS
====================================================== */

.status {

    right: 28px;

    top: 590px;

    width: 300px;

    height: 227px;

    padding: 15px;
}


.status-row {

    display: flex;

    justify-content: space-between;

    padding: 10px 0;

    border-bottom:
        1px solid rgba(255,255,255,.04);

    color: #77837B;

    font-size: 8px;
}


.status-row strong {

    color: #65DA5D;
}


/* ======================================================
   BOTTOM CENTER NETWORK
====================================================== */

.network {

    position: absolute;

    left: 390px;

    right: 360px;

    bottom: 24px;

    height: 92px;

    border:
        1px solid rgba(241,196,0,.22);

    background:
        rgba(5,11,7,.80);

    padding: 12px;
}


.network-title {

    color: #F1C400;

    font-size: 8px;

    letter-spacing: 1.5px;
}


.network-items {

    display: grid;

    grid-template-columns:
        repeat(5,1fr);

    gap: 8px;

    margin-top: 13px;
}


.network-item {

    border:
        1px solid rgba(68,136,62,.25);

    padding: 11px 5px;

    text-align: center;

    color: #8C9990;

    font-size: 7px;
}


.network-item.active {

    color: #F1C400;

    border-color:
        rgba(241,196,0,.35);
}


/* ======================================================
   ANIMATIONS
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


@keyframes pulse {

    0%,100% {
        opacity: .35;
    }

    50% {
        opacity: 1;
    }
}


@keyframes globePulse {

    0%,100% {

        box-shadow:
            0 0 30px rgba(241,196,0,.45),
            0 0 70px rgba(241,196,0,.17);
    }

    50% {

        box-shadow:
            0 0 45px rgba(241,196,0,.8),
            0 0 120px rgba(68,136,62,.27);
    }
}


@keyframes globeMove {

    from {
        transform:
            translateX(-100px);
    }

    to {
        transform:
            translateX(100px);
    }
}


@keyframes float {

    0%,100% {
        transform:
            translateY(0);
    }

    50% {
        transform:
            translateY(-15px);
    }
}


@keyframes stars {

    from {
        background-position: 0 0;
    }

    to {
        background-position: 110px 110px;
    }
}


@keyframes bars {

    from {
        height: 15%;
    }

    to {
        height: 100%;
    }
}

</style>

</head>


<body>

<div class="hud">

<div class="stars"></div>


<!-- HEADER -->

<div class="brand">

    <div class="brand-main">

        <span class="yellow">
            BOOKIE
        </span>

        <span class="green">
            CO
        </span>

    </div>

    <div class="brand-sub">
        MORE THAN BETTING
    </div>

</div>


<div class="top-center">

    <div class="top-title">

        BOOKIE<span class="green">OS</span>

    </div>

    <div class="top-sub">
        AI OPERATIONS SYSTEM
    </div>

    <div class="system-online">
        ● SYSTEM ONLINE
    </div>

</div>


<div class="clock">

    LARNACA · CYPRUS

    <strong id="clock">
        00:00:00
    </strong>

    BOOKIECO HQ

</div>



<!-- SPORTS -->

<div class="panel sports">

    <div class="panel-heading">
        SPORTS NETWORK
    </div>

    <div class="sport-item active">
        <span class="sport-icon">⚽</span>
        FOOTBALL
    </div>

    <div class="sport-item">
        <span class="sport-icon">🏀</span>
        BASKETBALL
    </div>

    <div class="sport-item">
        <span class="sport-icon">🎾</span>
        TENNIS
    </div>

    <div class="sport-item">
        <span class="sport-icon">🏎</span>
        FORMULA 1
    </div>

    <div class="sport-item">
        <span class="sport-icon">🚴</span>
        CYCLING
    </div>

    <div class="sport-item">
        <span class="sport-icon">🥊</span>
        COMBAT SPORTS
    </div>

    <div class="sport-item">
        <span class="sport-icon">🎮</span>
        ESPORTS
    </div>

</div>



<!-- LIVE DATA -->

<div class="panel data">

    <div class="panel-heading">
        SPORTS INTELLIGENCE
    </div>

    <div class="wave">

        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>

    </div>

    <div class="data-line">

        <span>
            WEEKLY SCOUT
        </span>

        <strong>
            READY
        </strong>

    </div>

    <div class="data-line">

        <span>
            BET RESEARCH
        </span>

        <strong>
            READY
        </strong>

    </div>

    <div class="data-line">

        <span>
            NETWORK STATUS
        </span>

        <strong>
            STABLE
        </strong>

    </div>

</div>



<!-- AGENTS -->

<div class="panel agents">

    <div class="panel-heading">
        AI AGENTS
    </div>


    <div class="agent">

        <div class="agent-icon">
            🔎
        </div>

        <div class="agent-info">

            <div class="agent-name">
                WEEKLY MATCH SCOUT
            </div>

            <div class="agent-job">
                Finds upcoming marketing events
            </div>

        </div>

        <div class="online">
            ● ONLINE
        </div>

    </div>


    <div class="agent">

        <div class="agent-icon">
            🧠
        </div>

        <div class="agent-info">

            <div class="agent-name">
                BET RESEARCHER
            </div>

            <div class="agent-job">
                Analyses teams and betting ideas
            </div>

        </div>

        <div class="online">
            ● ONLINE
        </div>

    </div>


    <div class="agent">

        <div class="agent-icon">
            📣
        </div>

        <div class="agent-info">

            <div class="agent-name">
                MARKETING MANAGER
            </div>

            <div class="agent-job">
                Creates weekly content plan
            </div>

        </div>

        <div class="planned">
            NEXT
        </div>

    </div>


    <div class="agent">

        <div class="agent-icon">
            🎁
        </div>

        <div class="agent-info">

            <div class="agent-name">
                PROMOTION SELECTOR
            </div>

            <div class="agent-job">
                Selects BookieCo promotions
            </div>

        </div>

        <div class="planned">
            PLANNED
        </div>

    </div>


    <div class="agent">

        <div class="agent-icon">
            🎨
        </div>

        <div class="agent-info">

            <div class="agent-name">
                CREATIVE DIRECTOR
            </div>

            <div class="agent-job">
                Designs campaign direction
            </div>

        </div>

        <div class="planned">
            PLANNED
        </div>

    </div>


    <div class="agent">

        <div class="agent-icon">
            ✍
        </div>

        <div class="agent-info">

            <div class="agent-name">
                SOCIAL MEDIA WRITER
            </div>

            <div class="agent-job">
                Creates headlines and captions
            </div>

        </div>

        <div class="planned">
            PLANNED
        </div>

    </div>

</div>



<!-- CENTRAL CORE -->

<div class="core-wrap">

    <div class="ring ring1"></div>

    <div class="ring ring2"></div>

    <div class="ring ring3"></div>

    <div class="ring ring4"></div>


    <div class="orbit football">
        ⚽
    </div>

    <div class="orbit basketball">
        🏀
    </div>

    <div class="orbit tennis">
        🎾
    </div>

    <div class="orbit f1">
        🏎
    </div>


    <div class="globe"></div>


    <div class="core-label">

        <div class="core-bookie">

            BOOKIE<span class="core-os">CO</span>

        </div>

        <div class="core-small">

            BOOKIEOS CENTRAL INTELLIGENCE

        </div>

    </div>

</div>



<!-- UPCOMING -->

<div class="panel upcoming">

    <div class="panel-heading">
        UPCOMING EVENTS
    </div>


    <div class="event">

        <div class="event-title">
            🔎 Weekly Match Scout
        </div>

        <div class="event-sub">
            Run the Scout to discover this week's priority events.
        </div>

    </div>


    <div class="event">

        <div class="event-title">
            ⚽ Football
        </div>

        <div class="event-sub">
            Major fixtures · Cyprus · Greece · Europe
        </div>

    </div>


    <div class="event">

        <div class="event-title">
            🏎 Formula 1
        </div>

        <div class="event-sub">
            Grand Prix weekends automatically considered
        </div>

    </div>


    <div class="event">

        <div class="event-title">
            🏀 Basketball
        </div>

        <div class="event-sub">
            Major international events
        </div>

    </div>

</div>



<!-- INTELLIGENCE -->

<div class="panel intel">

    <div class="panel-heading">
        MARKETING INTELLIGENCE
    </div>


    <div class="intel-row">

        <div class="intel-label">

            <span>
                MATCH DISCOVERY
            </span>

            <span>
                ONLINE
            </span>

        </div>

        <div class="progress">

            <div style="width:100%"></div>

        </div>

    </div>


    <div class="intel-row">

        <div class="intel-label">

            <span>
                BET RESEARCH
            </span>

            <span>
                ONLINE
            </span>

        </div>

        <div class="progress">

            <div style="width:100%"></div>

        </div>

    </div>


    <div class="intel-row">

        <div class="intel-label">

            <span>
                MARKETING MANAGER
            </span>

            <span>
                NEXT
            </span>

        </div>

        <div class="progress">

            <div style="width:35%"></div>

        </div>

    </div>

</div>



<!-- STATUS -->

<div class="panel status">

    <div class="panel-heading">
        SYSTEM STATUS
    </div>


    <div class="status-row">

        <span>
            BOOKIEOS CORE
        </span>

        <strong>
            ONLINE
        </strong>

    </div>


    <div class="status-row">

        <span>
            ACTIVE AGENTS
        </span>

        <strong>
            2
        </strong>

    </div>


    <div class="status-row">

        <span>
            DEPARTMENT
        </span>

        <strong>
            MARKETING
        </strong>

    </div>


    <div class="status-row">

        <span>
            NETWORK
        </span>

        <strong>
            STABLE
        </strong>

    </div>


    <div class="status-row">

        <span>
            NEXT AGENT
        </span>

        <strong>
            MANAGER
        </strong>

    </div>

</div>



<!-- NETWORK -->

<div class="network">

    <div class="network-title">
        BOOKIECO AI NETWORK
    </div>


    <div class="network-items">

        <div class="network-item active">
            DATA
        </div>

        <div class="network-item">
            IDEAS
        </div>

        <div class="network-item active">
            MARKETING
        </div>

        <div class="network-item">
            PEOPLE
        </div>

        <div class="network-item">
            RESULTS
        </div>

    </div>

</div>


</div>


<script>

function updateClock() {

    const now =
        new Date();

    document.getElementById(
        "clock"
    ).innerText =
        now.toLocaleTimeString(
            "en-GB",
            {
                hour12:false
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
    dashboard,
    height=875,
    scrolling=False
)


# =========================================================
# REAL BOOKIEOS COMMAND CONSOLE
# =========================================================

left_space, console, right_space = st.columns(
    [0.12, 1, 0.12]
)


with console:

    with st.container(
        border=True
    ):

        st.markdown(
            "### ◉ BOOKIEOS COMMAND CONSOLE"
        )

        st.caption(
            "Communicate with the BookieCo AI network."
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
        # INPUT
        # =================================================

        text_prompt = st.chat_input(
            "Type a command for BookieOS..."
        )


        user_prompt = (
            text_prompt
            or voice_prompt
        )


        # =================================================
        # HANDLE COMMAND
        # =================================================

        if user_prompt:

            with st.chat_message(
                "user"
            ):

                st.write(
                    user_prompt
                )


            with st.chat_message(
                "assistant"
            ):


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

                    word
                    in lower_prompt

                    for word
                    in scout_words
                )


                # =========================================
                # SCOUT WORKFLOW
                # =========================================

                if use_scout:

                    try:

                        st.markdown(
                            "### 🔎 WEEKLY MATCH SCOUT"
                        )


                        st.caption(
                            "Scanning upcoming sporting events..."
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


                        # =================================
                        # BET RESEARCHER
                        # =================================

                        st.markdown(
                            "### 🧠 BET RESEARCHER"
                        )


                        st.caption(
                            "Analysing Scout recommendations..."
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
statistics and betting concepts.

PLANNED AGENTS:

Marketing Manager
Promotion Selector
Creative Director
Social Media Writer

BookieOS currently does NOT have access to
BookieCo live betting markets or odds.

Never invent odds.

Never claim that a betting market exists at
BookieCo unless verified.

If the user speaks Greek, answer in Greek.

If the user speaks English, answer in English.

Keep answers concise and practical.
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
