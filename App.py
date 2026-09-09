import asyncio
import json
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


main, agents = st.columns(
    [2.3, 1]
)


# =========================================================
# MAIN BOOKIEOS
# =========================================================

with main:

    st.subheader(
        "🤖 BookieOS"
    )

    st.info(
        "Good afternoon, Paris.\n\n"
        "BookieOS is online. What would you like me to do?"
    )


    # ---------- MEMORY ----------

    if "messages" not in st.session_state:
        st.session_state.messages = []


    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )


    # =====================================================
    # VOICE
    # =====================================================

    audio = st.audio_input(
        "🎤 Talk to BookieOS"
    )

    voice_prompt = None


    if audio:

        try:

            with st.spinner(
                "🎤 Listening..."
            ):

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

        except Exception as e:

            st.error(
                "Voice transcription error: "
                + str(e)
            )


    # =====================================================
    # TEXT INPUT
    # =====================================================

    prompt = st.chat_input(
        "Ask BookieOS anything..."
    )


    if voice_prompt:

        prompt = voice_prompt


    # =====================================================
    # PROCESS
    # =====================================================

    if prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })


        with st.chat_message(
            "user"
        ):

            st.write(
                prompt
            )


        try:

            prompt_lower = (
                prompt.lower()
            )


            # =================================================
            # ROUTING
            # =================================================

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


            # =================================================
            # AGENT 1
            # =================================================

            if use_scout:

                with st.spinner(
                    "⚽ Weekly Match Scout is researching..."
                ):

                    scout_result = (
                        run_weekly_match_scout(
                            client,
                            prompt
                        )
                    )


                # =================================================
                # BOOKIECO LIVE DATA
                # =================================================

                with st.spinner(
                    "📡 Checking BookieCo live markets..."
                ):

                    feed = (
                        BookieCoLiveFeed()
                    )


                    try:

                        feed_result = (
                            asyncio.run(
                                feed.connect(
                                    listen_seconds=10
                                )
                            )
                        )

                    except Exception as e:

                        feed_result = {
                            "success": False,
                            "error": str(e)
                        }


                # =================================================
                # BUILD CLEAN BOOKIECO SNAPSHOT
                # =================================================

                bookieco_snapshot = []


                if feed_result.get(
                    "success"
                ):

                    for match in (
                        feed.reader.matches.values()
                    ):

                        match_id = (
                            match.get(
                                "match_id"
                            )
                        )


                        markets = (
                            feed.reader.get_markets(
                                match_id
                            )
                        )


                        clean_markets = []


                        for market in markets:

                            clean_markets.append({

                                "market_type_id":
                                    market.get(
                                        "market_type_id"
                                    ),

                                "special":
                                    market.get(
                                        "special"
                                    ),

                                "is_suspended":
                                    market.get(
                                        "is_suspended"
                                    ),

                                "selections":
                                    market.get(
                                        "selections",
                                        []
                                    )
                            })


                        bookieco_snapshot.append({

                            "match_id":
                                match_id,

                            "competitors":
                                match.get(
                                    "competitors",
                                    []
                                ),

                            "start_time":
                                match.get(
                                    "start_time"
                                ),

                            "number_of_markets":
                                match.get(
                                    "number_of_markets"
                                ),

                            "markets":
                                clean_markets
                        })


                # Keep the data sent to the AI manageable
                bookieco_text = json.dumps(
                    bookieco_snapshot,
                    ensure_ascii=False
                )


                # =================================================
                # AGENT 2
                # =================================================

                with st.spinner(
                    "🔎 Bet Researcher is analysing and checking BookieCo..."
                ):

                    researcher_task = f"""
The Weekly Match Scout produced this report:

========================
SCOUT REPORT
========================

{scout_result}

========================
END SCOUT REPORT
========================


Below is a LIVE SNAPSHOT received directly from BookieCo's betting feed.

========================
BOOKIECO LIVE DATA
========================

{bookieco_text}

========================
END BOOKIECO DATA
========================


Analyse EVERY proposed football bet from the Scout report.

For each match:

1. Identify the Scout's proposed betting market.

2. Research whether the betting idea makes statistical sense.

3. Rate it:

STRONG
REASONABLE
WEAK

4. Estimate the price profile:

TOO LOW
GOOD MARKETING RANGE
HIGH RISK - HIGH PRICE
UNKNOWN

5. Prefer interesting marketing bets likely to fall roughly between
decimal odds 2.00 and 6.00.

6. If the proposed market looks too low or weak, suggest a better
alternative.

7. Check the BOOKIECO LIVE DATA for the same match.

8. If the exact match appears in the BookieCo data, report:

BOOKIECO MATCH:
FOUND

and show the BookieCo match ID.

9. If the match does not appear in this live snapshot, report:

BOOKIECO MATCH:
NOT FOUND IN CURRENT LIVE SNAPSHOT

Do NOT claim that BookieCo does not offer the match.
The current WebSocket snapshot may not contain every event.

10. marketTypeId 3 is known to represent the standard 1X2 market.

For marketTypeId 3:
- outcome 1 = Home
- outcome X = Draw
- outcome 2 = Away

You may report the actual BookieCo odds from this market when present.

11. For OTHER marketTypeIds:

DO NOT guess what the market name means yet.

We have not yet connected BookieCo's full market-type dictionary.

Therefore do NOT claim an advanced proposed bet is verified only because
an unknown marketTypeId exists.

Use:

ADVANCED MARKET VERIFICATION:
WAITING FOR MARKET TYPE MAPPING

12. Never invent BookieCo odds.

13. Never invent BookieCo market names.

14. If actual BookieCo data verifies something, clearly distinguish it
from your web research.

Return everything in the same Monday-Sunday order as the Scout report.
"""


                    researcher_result = (
                        run_bet_researcher(
                            client,
                            researcher_task
                        )
                    )


                # =================================================
                # FINAL RESULT
                # =================================================

                answer = (
                    "⚽ **Weekly Match Scout report**"
                    "\n\n"
                    + scout_result
                    + "\n\n---\n\n"
                    + "🔎 **Automatic Bet Researcher analysis**"
                    "\n\n"
                    + researcher_result
                )


            # =================================================
            # NORMAL BOOKIEOS
            # =================================================

            else:

                response = (
                    client.responses.create(

                        model="gpt-5.6-luna",

                        instructions="""
You are BookieOS, the internal AI operating system for BookieCo.

CONNECTED AGENTS:

1. Weekly Match Scout
2. Bet Researcher

AUTOMATIC WORKFLOW:

User
→ BookieOS
→ Weekly Match Scout
→ BookieCo live market feed
→ Bet Researcher
→ BookieOS
→ User

The Bet Researcher now receives a live BookieCo data snapshot.

IMPORTANT:

The live BookieCo connection is working.

However, the complete mapping between BookieCo marketTypeId values
and human-readable betting-market names is not connected yet.

Therefore:

- Never guess market names from unknown marketTypeId values.
- Never invent BookieCo odds.
- marketTypeId 3 is known to be standard 1X2.
- Advanced market availability still requires market-type mapping.

NOT YET CONNECTED:

- Marketing Manager
- Promotion Selector

LANGUAGE:

If the user speaks Greek, respond in Greek.

If the user speaks English, respond in English.

Be concise and professional.
""",

                        input=[
                            {
                                "role":
                                    message["role"],

                                "content":
                                    message["content"]
                            }

                            for message
                            in st.session_state.messages
                        ]
                    )
                )


                answer = (
                    response.output_text
                )


        except Exception as e:

            answer = (
                "BookieOS encountered an error: "
                + str(e)
            )


        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })


        with st.chat_message(
            "assistant"
        ):

            st.write(
                answer
            )


# =========================================================
# AGENTS PANEL
# =========================================================

with agents:

    st.subheader(
        "⚡ LIVE AGENTS"
    )


    st.markdown(
        "**🤖 Marketing Manager**"
    )

    st.warning(
        "● NOT CONNECTED"
    )


    st.markdown(
        "**⚽ Weekly Match Scout**"
    )

    st.success(
        "● CONNECTED"
    )


    st.markdown(
        "**🔎 Bet Researcher**"
    )

    st.success(
        "● CONNECTED - AUTO"
    )


    st.markdown(
        "**📢 Promotion Selector**"
    )

    st.warning(
        "● NOT CONNECTED"
    )


    st.divider()


    # =====================================================
    # BOOKIECO FEED TEST
    # =====================================================

    st.markdown(
        "**📡 BookieCo Market Feed**"
    )


    if st.button(
        "🧪 Test BookieCo Live Feed"
    ):

        with st.spinner(
            "Connecting to BookieCo..."
        ):

            feed = (
                BookieCoLiveFeed()
            )


            try:

                result = (
                    asyncio.run(
                        feed.connect(
                            listen_seconds=8
                        )
                    )
                )

            except Exception as e:

                result = {
                    "success": False,
                    "error": str(e)
                }


        if result.get(
            "success"
        ):

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


            matches = result.get(
                "matches",
                []
            )


            if matches:

                st.markdown(
                    "### ⚽ Matches found"
                )


                for match in matches:

                    competitors = (
                        match.get(
                            "competitors",
                            []
                        )
                    )


                    match_id = (
                        match.get(
                            "match_id"
                        )
                    )


                    number_of_markets = (
                        match.get(
                            "number_of_markets"
                        )
                    )


                    if len(
                        competitors
                    ) >= 2:

                        match_name = (
                            str(
                                competitors[0]
                            )
                            + " vs "
                            + str(
                                competitors[1]
                            )
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
                        + str(
                            number_of_markets
                        )
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


    st.divider()

    st.caption(
        "SYSTEM STATUS"
    )

    st.success(
        "BOOKIEOS ONLINE"
    )
