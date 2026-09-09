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

    st.subheader("🤖 BookieOS")

    st.info(
        "Good afternoon, Paris.\n\n"
        "BookieOS is online. What would you like me to do?"
    )


    # =====================================================
    # CHAT MEMORY
    # =====================================================

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
    # PROCESS MESSAGE
    # =====================================================

    if prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })


        with st.chat_message("user"):

            st.write(prompt)


        try:

            prompt_lower = (
                prompt.lower()
            )


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
            # WEEKLY MATCH SCOUT
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
                # CURRENT BOOKIECO SNAPSHOT
                # =================================================

                with st.spinner(
                    "📡 Checking BookieCo live markets..."
                ):

                    feed = BookieCoLiveFeed()


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


                bookieco_snapshot = []


                if feed_result.get("success"):

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


                bookieco_text = json.dumps(
                    bookieco_snapshot,
                    ensure_ascii=False
                )


                # =================================================
                # BET RESEARCHER
                # =================================================

                with st.spinner(
                    "🔎 Bet Researcher is analysing..."
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


Below is a live BookieCo snapshot:

========================
BOOKIECO LIVE DATA
========================

{bookieco_text}

========================
END BOOKIECO DATA
========================


Analyse EVERY proposed football bet.

For each proposed bet:

- Research whether it makes statistical sense.
- Rate it STRONG, REASONABLE or WEAK.
- Prefer interesting marketing bets.
- General target estimated decimal odds: 2.00 to 6.00.
- Avoid boring low-price bets when possible.
- Suggest a better alternative when appropriate.
- Never invent BookieCo odds.
- Never invent BookieCo markets.

marketTypeId 3 is confirmed as standard football 1X2.

For marketTypeId 3:

1 = Home
X = Draw
2 = Away

Other BookieCo marketTypeId values are not mapped yet.

Do not guess their meaning.

If an advanced market cannot yet be verified, say:

ADVANCED MARKET VERIFICATION:
WAITING FOR MARKET TYPE MAPPING
"""


                    researcher_result = (
                        run_bet_researcher(
                            client,
                            researcher_task
                        )
                    )


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

Connected:

- Weekly Match Scout
- Bet Researcher
- BookieCo live-data connector

Not yet connected:

- Marketing Manager
- Promotion Selector

BookieCo marketTypeId 3 is confirmed as standard 1X2.

Never invent BookieCo odds or market availability.

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


        with st.chat_message("assistant"):

            st.write(answer)


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
    # BOOKIECO SEARCH TEST
    # =====================================================

    st.markdown(
        "**📡 BookieCo Market Feed**"
    )


    if st.button(
        "🔎 Search BookieCo: Olympiacos"
    ):

        with st.spinner(
            "Searching BookieCo for Olympiacos..."
        ):

            search_feed = (
                BookieCoLiveFeed()
            )


            search_result = (
                search_feed.search_match(
                    "Olympia"
                )
            )


        if search_result.get(
            "success"
        ):

            matches_found = (
                search_result.get(
                    "matches_found",
                    0
                )
            )


            st.success(
                "✅ BookieCo search connected"
            )


            st.write(
                "Matches found:",
                matches_found
            )


            results = (
                search_result.get(
                    "results",
                    []
                )
            )


            if results:

                for result in results:

                    match = (
                        result.get(
                            "match",
                            {}
                        )
                    )


                    competitors = (
                        match.get(
                            "competitors",
                            []
                        )
                    )


                    match_id = (
                        result.get(
                            "match_id"
                        )
                    )


                    market_1x2 = (
                        result.get(
                            "market_1x2"
                        )
                    )


                    st.markdown("---")


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

                        match_name = (
                            str(
                                competitors
                            )
                        )


                    st.markdown(
                        "### ⚽ "
                        + match_name
                    )


                    st.write(
                        "BookieCo Match ID:",
                        match_id
                    )


                    st.write(
                        "Available markets:",
                        match.get(
                            "number_of_markets"
                        )
                    )


                    # =====================================
                    # REAL 1X2 ODDS
                    # =====================================

                    if market_1x2:

                        st.markdown(
                            "#### 💰 Real BookieCo 1X2 Odds"
                        )


                        odds = {}


                        for selection in (
                            market_1x2.get(
                                "selections",
                                []
                            )
                        ):

                            outcome = (
                                selection.get(
                                    "outcome"
                                )
                            )

                            odd = (
                                selection.get(
                                    "odds"
                                )
                            )

                            odds[
                                outcome
                            ] = odd


                        st.write(
                            "🏠 Home:",
                            odds.get("1")
                        )


                        st.write(
                            "🤝 Draw:",
                            odds.get("X")
                        )


                        st.write(
                            "✈️ Away:",
                            odds.get("2")
                        )


                    else:

                        st.warning(
                            "Match found, but 1X2 odds were not included in the search response."
                        )


            else:

                st.warning(
                    "BookieCo responded, but no matching events were parsed."
                )


        else:

            st.error(
                "❌ BookieCo search failed"
            )


            st.write(
                search_result.get(
                    "error",
                    "Unknown error"
                )
            )


    st.divider()


    # =====================================================
    # NORMAL LIVE FEED TEST
    # =====================================================

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


            summary = (
                result.get(
                    "summary",
                    {}
                )
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


            matches = (
                result.get(
                    "matches",
                    []
                )
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

                        match_name = (
                            str(
                                competitors
                            )
                        )


                    st.write(
                        "⚽ "
                        + match_name
                    )


                    st.caption(
                        "Match ID: "
                        + str(
                            match_id
                        )
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
