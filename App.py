import asyncio
import streamlit as st
from openai import OpenAI

from weekly_match_scout import run_weekly_match_scout
from bet_researcher import run_bet_researcher
from bookieco_live_feed import BookieCoLiveFeed


# =========================================================
# PAGE
# =========================================================

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
    # PROCESS
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
            # AGENT 1 + AGENT 2
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

Analyse EVERY proposed football betting market.

For every bet:

- Research whether the idea makes sense.
- Rate it STRONG, REASONABLE or WEAK.
- Prefer interesting marketing bets.
- Prefer estimated decimal odds around 2.00 to 6.00.
- Avoid boring low-odds selections when possible.
- Suggest a better alternative when appropriate.

Never invent BookieCo odds.

Never claim that a market is available at BookieCo unless
actual BookieCo data verifies it.

BookieCo integration is currently being connected automatically.
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

CONNECTED:

- Weekly Match Scout
- Bet Researcher
- BookieCo data connector

The BookieCo connector can now search the company's
sports database for matches and retrieve BookieCo match IDs.

Full automatic market and odds verification is still being completed.

Never invent BookieCo odds or market availability.

NOT YET CONNECTED:

- Marketing Manager
- Promotion Selector

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
    # BOOKIECO SEARCH
    # =====================================================

    st.markdown(
        "**🔎 BookieCo Match Search**"
    )


    if st.button(
        "🔎 Search Olympiacos"
    ):

        with st.spinner(
            "Searching BookieCo..."
        ):

            feed = (
                BookieCoLiveFeed()
            )


            result = (
                feed.search_football_match(
                    "Olympia"
                )
            )


        if result.get(
            "success"
        ):

            st.success(
                "✅ BookieCo search connected"
            )


            st.write(
                "Football matches found:",
                result.get(
                    "matches_found",
                    0
                )
            )


            matches = (
                result.get(
                    "results",
                    []
                )
            )


            if matches:

                for match in matches:

                    st.markdown("---")


                    st.markdown(
                        "### ⚽ "
                        + str(
                            match.get(
                                "name",
                                "Unknown match"
                            )
                        )
                    )


                    st.write(
                        "**BookieCo Match ID:**",
                        match.get(
                            "match_id"
                        )
                    )


                    st.write(
                        "**Competition:**",
                        match.get(
                            "league_name"
                        )
                    )


                    st.write(
                        "**Country/Category:**",
                        match.get(
                            "category_name"
                        )
                    )


                    st.write(
                        "**Status:**",
                        match.get(
                            "status"
                        )
                    )


            else:

                st.warning(
                    "BookieCo responded successfully, "
                    "but no football matches were returned."
                )


        else:

            st.error(
                "❌ BookieCo search failed"
            )


            st.write(
                result.get(
                    "error",
                    "Unknown error"
                )
            )


    st.divider()


    # =====================================================
    # LIVE FEED
    # =====================================================

    st.markdown(
        "**📡 BookieCo Live Feed**"
    )


    if st.button(
        "🧪 Test Live Feed"
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

            summary = (
                result.get(
                    "summary",
                    {}
                )
            )


            st.success(
                "✅ BookieCo feed connected"
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


            for match in matches:

                competitors = (
                    match.get(
                        "competitors",
                        []
                    )
                )


                if len(
                    competitors
                ) >= 2:

                    name = (
                        str(
                            competitors[0]
                        )
                        + " vs "
                        + str(
                            competitors[1]
                        )
                    )

                else:

                    name = (
                        str(
                            competitors
                        )
                    )


                st.write(
                    "⚽ " + name
                )


                st.caption(
                    "Match ID: "
                    + str(
                        match.get(
                            "match_id"
                        )
                    )
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
