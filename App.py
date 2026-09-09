import asyncio
import streamlit as st
from openai import OpenAI

from weekly_match_scout import run_weekly_match_scout
from bet_researcher import run_bet_researcher
from bookieco_live_feed import BookieCoLiveFeed


st.set_page_config(
    page_title="BookieOS",
    page_icon="🤖",
    layout="wide"
)


# ---------- OPENAI ----------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# ---------- HEADER ----------
st.title("◉ BOOKIEOS")
st.caption("BookieCo Artificial Intelligence Operating System")

st.divider()


# ---------- LAYOUT ----------
main, agents = st.columns([2.3, 1])


# =========================================================
# MAIN BOOKIEOS AREA
# =========================================================

with main:

    st.subheader("🤖 BookieOS")

    st.info(
        "Good afternoon, Paris.\n\n"
        "BookieOS is online. What would you like me to do?"
    )


    # ---------- CHAT MEMORY ----------
    if "messages" not in st.session_state:
        st.session_state.messages = []


    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])


    # ---------- VOICE INPUT ----------
    audio = st.audio_input("🎤 Talk to BookieOS")

    voice_prompt = None


    if audio:

        try:

            with st.spinner("🎤 Listening..."):

                transcription = client.audio.transcriptions.create(
                    model="gpt-4o-mini-transcribe",
                    file=audio,
                    language="el"
                )

                voice_prompt = transcription.text

        except Exception as e:

            st.error(
                "Voice transcription error: "
                + str(e)
            )


    # ---------- TEXT INPUT ----------
    prompt = st.chat_input(
        "Ask BookieOS anything..."
    )


    if voice_prompt:
        prompt = voice_prompt


    # ---------- PROCESS REQUEST ----------
    if prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })


        with st.chat_message("user"):
            st.write(prompt)


        try:

            prompt_lower = prompt.lower()


            scout_words = [

                "weekly match scout",
                "match scout",
                "find matches",
                "find fixtures",
                "best matches",
                "matches next week",
                "fixtures next week",
                "football next week",

                "formula 1",
                "f1",

                "champions league",
                "europa league",
                "conference league",

                # Greek
                "βρες αγώνες",
                "βρες μου αγώνες",
                "καλύτερους αγώνες",
                "αγώνες επόμενης εβδομάδας",
                "επόμενη εβδομάδα",
                "ποδόσφαιρο",
                "φόρμουλα 1"
            ]


            use_scout = any(
                word in prompt_lower
                for word in scout_words
            )


            # =====================================================
            # AGENT 1 + AUTOMATIC AGENT 2
            # =====================================================

            if use_scout:

                with st.spinner(
                    "⚽ Weekly Match Scout is researching..."
                ):

                    scout_result = run_weekly_match_scout(
                        client,
                        prompt
                    )


                with st.spinner(
                    "🔎 Bet Researcher is automatically analysing the recommendations..."
                ):

                    researcher_task = f"""
The Weekly Match Scout produced this report:

--------------------
SCOUT REPORT
--------------------

{scout_result}

--------------------
END SCOUT REPORT
--------------------

Analyse EVERY proposed football betting market in the report.

For every proposed bet:

1. Identify the match.
2. Identify the proposed betting market.
3. Research whether the betting idea makes statistical sense.
4. Check relevant current team or player information.

5. Rate the bet:

STRONG
REASONABLE
WEAK

6. Estimate the likely price profile:

TOO LOW
GOOD MARKETING RANGE
HIGH RISK - HIGH PRICE
UNKNOWN

7. BookieCo prefers interesting marketing bets.

As a general target, prefer bets that would likely have decimal odds
around 2.00 to 6.00.

Avoid bets that would probably be below approximately 1.80 unless
there is an exceptional reason.

8. If the proposed bet is too low or weak, suggest a better,
more interesting alternative.

9. Do NOT invent BookieCo odds.

10. BookieCo's actual market availability has not yet been verified
by this research step.

Analyse all football recommendations automatically.

Do not require the user to ask you about each match individually.
"""


                    researcher_result = run_bet_researcher(
                        client,
                        researcher_task
                    )


                answer = (
                    "⚽ **Weekly Match Scout report**\n\n"
                    + scout_result
                    + "\n\n---\n\n"
                    + "🔎 **Automatic Bet Researcher analysis**\n\n"
                    + researcher_result
                )


            # =====================================================
            # NORMAL BOOKIEOS
            # =====================================================

            else:

                response = client.responses.create(

                    model="gpt-5.6-luna",

                    instructions="""
You are BookieOS, the internal AI operating system for BookieCo.

Your job is to coordinate specialist AI agents and communicate
with the user.

CONNECTED AGENTS:

1. Weekly Match Scout

The Weekly Match Scout:
- Researches upcoming sporting events.
- Creates weekly marketing recommendations.
- Prioritises the Cyprus audience.
- Gives additional priority to Cyprus and Greek teams.
- Checks Formula 1.
- Proposes interesting football betting markets.

2. Bet Researcher

The Bet Researcher:
- Automatically receives the Weekly Match Scout report.
- Analyses every proposed football betting market.
- Researches whether the betting angle makes sense.
- Looks for more interesting alternatives when a proposed bet
  is too low.
- Will verify BookieCo's real markets and odds once the live
  market integration is completed.

AUTOMATIC WORKFLOW:

User
→ BookieOS
→ Weekly Match Scout
→ Bet Researcher
→ BookieOS
→ User

The user does NOT need to manually ask the Bet Researcher
to analyse every match.

BOOKIECO DATA:

The BookieCo live market-feed connection is currently being built.

Never invent BookieCo odds.
Never invent BookieCo market availability.

NOT YET CONNECTED:

- Marketing Manager
- Promotion Selector

LANGUAGE:

If the user speaks Greek, respond in Greek.
If the user speaks English, respond in English.

Be concise, professional and helpful.
""",

                    input=[
                        {
                            "role": message["role"],
                            "content": message["content"]
                        }
                        for message in st.session_state.messages
                    ]
                )


                answer = response.output_text


        except Exception as e:

            answer = (
                "BookieOS encountered an error: "
                + str(e)
            )


        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })


        with st.chat_message("assistant"):
            st.write(answer)


# =========================================================
# AGENTS PANEL
# =========================================================

with agents:

    st.subheader("⚡ LIVE AGENTS")


    # ---------- MARKETING MANAGER ----------
    st.markdown("**🤖 Marketing Manager**")
    st.warning("● NOT CONNECTED")


    # ---------- WEEKLY MATCH SCOUT ----------
    st.markdown("**⚽ Weekly Match Scout**")
    st.success("● CONNECTED")


    # ---------- BET RESEARCHER ----------
    st.markdown("**🔎 Bet Researcher**")
    st.success("● CONNECTED - AUTO")


    # ---------- PROMOTION SELECTOR ----------
    st.markdown("**📢 Promotion Selector**")
    st.warning("● NOT CONNECTED")


    # =====================================================
    # BOOKIECO LIVE MARKET FEED
    # =====================================================

    st.divider()

    st.markdown("**📡 BookieCo Market Feed**")


    if st.button("🧪 Test BookieCo Live Feed"):

        with st.spinner("Connecting to BookieCo..."):

            feed = BookieCoLiveFeed()

            try:

                result = asyncio.run(
                    feed.connect(
                        listen_seconds=8
                    )
                )

            except Exception as e:

                result = {
                    "success": False,
                    "error": str(e)
                }


        if result.get("success"):

            st.success(
                "✅ BookieCo feed connected"
            )


            summary = result.get(
                "summary",
                {}
            )


            st.write(
                "Matches received:",
                summary.get(
                    "matches_loaded",
                    0
                )
            )


            st.write(
                "Markets received:",
                summary.get(
                    "markets_loaded",
                    0
                )
            )


            # ---------- SHOW MATCHES ----------

            matches = result.get(
                "matches",
                []
            )


            if matches:

                st.markdown("### ⚽ Matches found")


                for match in matches:

                    competitors = match.get(
                        "competitors",
                        []
                    )

                    match_id = match.get(
                        "match_id"
                    )

                    number_of_markets = match.get(
                        "number_of_markets"
                    )


                    if len(competitors) >= 2:

                        match_name = (
                            str(competitors[0])
                            + " vs "
                            + str(competitors[1])
                        )

                    else:

                        match_name = str(
                            competitors
                        )


                    st.write(
                        "⚽ " + match_name
                    )

                    st.caption(
                        "Match ID: "
                        + str(match_id)
                        + " | Markets: "
                        + str(number_of_markets)
                    )


            else:

                st.warning(
                    "Connected, but no matches were found."
                )


        else:

            st.error(
                "❌ BookieCo feed connection failed"
            )

            st.write(
                result.get(
                    "error",
                    "Unknown error"
                )
            )


    # ---------- SYSTEM STATUS ----------

    st.divider()

    st.caption("SYSTEM STATUS")

    st.success("BOOKIEOS ONLINE")
