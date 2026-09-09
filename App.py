import asyncio
import streamlit as st
from openai import OpenAI

from weekly_match_scout import run_weekly_match_scout
from bet_researcher import run_bet_researcher
from bookieco_live_feed import BookieCoLiveFeed
from bookieco_browser import search_bookieco


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="BookieOS",
    page_icon="◉",
    layout="wide"
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

st.title("◉ BOOKIEOS")

st.caption(
    "BookieCo Artificial Intelligence Operating System"
)

st.divider()


# =========================================================
# LAYOUT
# =========================================================

main_column, agent_column = st.columns(
    [3, 1]
)


# =========================================================
# MAIN BOOKIEOS
# =========================================================

with main_column:

    st.subheader("BookieOS")

    st.caption(
        "Talk to BookieOS in English or Greek."
    )


    # -----------------------------------------------------
    # VOICE
    # -----------------------------------------------------

    voice_prompt = None

    audio = st.audio_input(
        "🎤 Talk to BookieOS"
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

            st.write(
                "🎙️",
                voice_prompt
            )

        except Exception as e:

            st.error(
                f"Voice error: {e}"
            )


    # -----------------------------------------------------
    # TEXT INPUT
    # -----------------------------------------------------

    text_prompt = st.chat_input(
        "Ask BookieOS..."
    )


    user_prompt = (
        text_prompt
        or voice_prompt
    )


    # -----------------------------------------------------
    # HANDLE REQUEST
    # -----------------------------------------------------

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

                "αγώνες εβδομάδας",
                "αγωνες εβδομαδας",
                "αγώνες αυτής της εβδομάδας",
                "αγωνες αυτης της εβδομαδας",
                "αγώνες επόμενης εβδομάδας",
                "αγωνες επομενης εβδομαδας"
            ]


            use_scout = any(
                word in lower_prompt
                for word in scout_words
            )


            # =================================================
            # WEEKLY MATCH SCOUT
            # =================================================

            if use_scout:

                with st.spinner(
                    "Weekly Match Scout is researching..."
                ):

                    try:

                        scout_report = (
                            run_weekly_match_scout(
                                user_prompt
                            )
                        )


                        st.markdown(
                            "### 🔎 Weekly Match Scout"
                        )

                        st.write(
                            scout_report
                        )


                        st.divider()


                        # =====================================
                        # AUTOMATIC BET RESEARCHER
                        # =====================================

                        with st.spinner(
                            "Bet Researcher is analysing the bets..."
                        ):

                            researcher_task = f"""
The Weekly Match Scout produced the report below.

Analyse EVERY proposed FOOTBALL betting market in the report.

For each proposed football bet:

1. Identify the match.
2. Identify the proposed betting market.
3. Research current information about the teams and players.
4. Decide whether the proposed bet makes sense.
5. Rate it:
   STRONG
   REASONABLE
   WEAK

6. Estimate the likely price profile:
   TOO LOW
   GOOD MARKETING RANGE
   HIGH RISK - HIGH PRICE
   UNKNOWN

Prefer interesting marketing bets that would likely be around
decimal odds 2.00 to 6.00.

Avoid boring bets that are likely below approximately 1.80
unless there is an exceptional reason.

If the proposed bet is too low or weak, suggest a more
interesting alternative.

Do NOT invent BookieCo odds.

BookieCo market availability is not yet verified.

SCOUT REPORT:

{scout_report}
"""


                            research_report = (
                                run_bet_researcher(
                                    researcher_task
                                )
                            )


                        st.markdown(
                            "### 🧠 Bet Researcher"
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

                    response = (
                        client.responses.create(

                            model="gpt-5.6-luna",

                            instructions="""
You are BookieOS.

You are the central AI assistant for BookieCo,
a retail betting company in Cyprus.

Connected agents:

Weekly Match Scout
Bet Researcher

Not connected yet:

Marketing Manager
Promotion Selector

Workflow:

User
→ BookieOS
→ specialist agent
→ BookieOS
→ User

The BookieCo live betting market connection
is currently being developed.

Never invent BookieCo odds.

Never claim that a betting market exists at
BookieCo unless it has been verified using
BookieCo data.

If the user speaks Greek, answer in Greek.

If the user speaks English, answer in English.

Keep answers clear and practical.
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
# AGENT PANEL
# =========================================================

with agent_column:

    st.subheader(
        "Live Agents"
    )


    st.write(
        "🔴 Marketing Manager"
    )

    st.caption(
        "NOT CONNECTED"
    )


    st.write(
        "🟢 Weekly Match Scout"
    )

    st.caption(
        "CONNECTED"
    )


    st.write(
        "🟢 Bet Researcher"
    )

    st.caption(
        "CONNECTED - AUTO"
    )


    st.write(
        "🔴 Promotion Selector"
    )

    st.caption(
        "NOT CONNECTED"
    )


    st.divider()


    # =====================================================
    # WEBSITE READER TEST
    # =====================================================

    st.subheader(
        "🌐 BookieCo Website Reader"
    )

    st.caption(
        "Testing BookieOS reading the public website."
    )


    if st.button(
        "🌐 Test Website Reader",
        use_container_width=True
    ):

        with st.spinner(
            "Opening BookieCo website..."
        ):

            try:

                website_text = (
                    search_bookieco(
                        "Olympiacos"
                    )
                )


                st.success(
                    "BookieCo website opened!"
                )


                st.text_area(
                    "What BookieOS can see:",
                    website_text,
                    height=400
                )


            except Exception as e:

                st.error(
                    f"Website reader error: {e}"
                )


    st.divider()


    # =====================================================
    # OLD API SEARCH TEST
    # =====================================================

    st.subheader(
        "🔎 BookieCo Match Search"
    )


    if st.button(
        "🔎 Search Olympiacos",
        use_container_width=True
    ):

        with st.spinner(
            "Searching BookieCo..."
        ):

            try:

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
                        "BookieCo search connected"
                    )


                    st.write(
                        "Matches found:",
                        result.get(
                            "matches_found",
                            0
                        )
                    )


                    for match in result.get(
                        "results",
                        []
                    ):

                        st.markdown(
                            f"**{match.get('name')}**"
                        )

                        st.write(
                            "BookieCo Match ID:",
                            match.get(
                                "match_id"
                            )
                        )

                        st.write(
                            "Competition:",
                            match.get(
                                "league_name"
                            )
                        )

                        st.write(
                            "Country/Category:",
                            match.get(
                                "category_name"
                            )
                        )

                        st.write(
                            "Status:",
                            match.get(
                                "status"
                            )
                        )

                        st.divider()


                else:

                    st.error(
                        "BookieCo search failed"
                    )

                    st.write(
                        result
                    )


            except Exception as e:

                st.error(
                    f"Search error: {e}"
                )


    st.divider()


    # =====================================================
    # LIVE FEED TEST
    # =====================================================

    st.subheader(
        "📡 BookieCo Live Feed"
    )


    if st.button(
        "🧪 Test Live Feed",
        use_container_width=True
    ):

        with st.spinner(
            "Listening to BookieCo..."
        ):

            try:

                feed = (
                    BookieCoLiveFeed()
                )


                result = asyncio.run(
                    feed.connect(
                        listen_seconds=8
                    )
                )


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
                        "BookieCo feed connected"
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


                    for match in result.get(
                        "matches",
                        []
                    ):

                        competitors = (
                            match.get(
                                "competitors",
                                []
                            )
                        )


                        if competitors:

                            st.write(
                                "⚽ "
                                + " vs ".join(
                                    competitors
                                )
                            )


                            st.caption(
                                "ID: "
                                + str(
                                    match.get(
                                        "match_id"
                                    )
                                )
                            )


                else:

                    st.error(
                        "BookieCo feed failed"
                    )

                    st.write(
                        result
                    )


            except Exception as e:

                st.error(
                    f"Live feed error: {e}"
                )


    st.divider()

    st.success(
        "BOOKIEOS ONLINE"
    )
