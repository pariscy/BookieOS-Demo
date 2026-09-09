import streamlit as st
from openai import OpenAI

from weekly_match_scout import run_weekly_match_scout
from sports_news_monitor import run_sports_news_monitor
from competitor_watch import run_competitor_watch
from sports_calendar import run_sports_calendar
from bet_researcher import run_bet_researcher
from marketing_manager import run_marketing_manager


st.set_page_config(
    page_title="BookieOS",
    page_icon="◉",
    layout="wide"
)


client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


# =========================================================
# SESSION STATE
# =========================================================

if "sports_news_report" not in st.session_state:
    st.session_state.sports_news_report = None

if "competitor_report" not in st.session_state:
    st.session_state.competitor_report = None

if "sports_calendar_report" not in st.session_state:
    st.session_state.sports_calendar_report = None

if "calendar_promo_ideas" not in st.session_state:
    st.session_state.calendar_promo_ideas = None


# =========================================================
# HEADER
# =========================================================

st.title("◉ BOOKIEOS")
st.caption("BookieCo Artificial Intelligence Operating System")
st.divider()


main_column, agent_column = st.columns([3, 1])


# =========================================================
# MAIN BOOKIEOS
# =========================================================

with main_column:

    st.subheader("BookieOS")
    st.caption("Ask BookieOS in English or Greek.")

    voice_prompt = None

    audio = st.audio_input(
        "🎤 Talk to BookieOS"
    )

    if audio is not None:

        try:

            transcription = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio,
                language="el"
            )

            voice_prompt = transcription.text

            st.write(
                "🎙️",
                voice_prompt
            )

        except Exception as e:

            st.error(
                f"Voice error: {e}"
            )


    text_prompt = st.chat_input(
        "Ask BookieOS..."
    )

    user_prompt = text_prompt or voice_prompt


    if user_prompt:

        with st.chat_message("user"):
            st.write(user_prompt)


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
            # WEEKLY MARKETING WORKFLOW
            # =================================================

            if use_scout:

                try:

                    with st.spinner(
                        "🔎 Weekly Match Scout is researching..."
                    ):

                        scout_report = run_weekly_match_scout(
                            client,
                            user_prompt
                        )


                    st.markdown(
                        "### 🔎 Weekly Match Scout"
                    )

                    st.write(
                        scout_report
                    )

                    st.divider()


                    with st.spinner(
                        "🧠 Bet Researcher is analysing..."
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

Market availability will be verified by another system
in the future.

If an idea is weak, suggest a better betting angle.


SCOUT REPORT:

{scout_report}
"""


                        research_report = run_bet_researcher(
                            client,
                            researcher_task
                        )


                    st.markdown(
                        "### 🧠 Bet Researcher"
                    )

                    st.write(
                        research_report
                    )

                    st.divider()


                    with st.spinner(
                        "📣 Marketing Manager is building the weekly plan..."
                    ):

                        marketing_report = run_marketing_manager(
                            scout_report,
                            research_report
                        )


                    st.markdown(
                        "### 📣 Marketing Manager"
                    )

                    st.write(
                        marketing_report
                    )


                    st.success(
                        "Marketing analysis complete."
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

AUTOMATIC MARKETING WORKFLOW:

1. Weekly Match Scout
2. Bet Researcher
3. Marketing Manager

INDEPENDENT MANUAL AGENTS:

4. Sports News Monitor

Checks important current sports developments.

5. Competitor Watch

Checks current public marketing activity from
betting competitors relevant to Cyprus.

6. Sports Calendar

Looks approximately 90 days ahead for major sporting
events that BookieCo should prepare marketing for.

The Sports Calendar also has an OPTIONAL Promo Ideas tool.

Promo Ideas are creative concepts only.

They are NOT existing BookieCo promotions and must
never be presented as approved or active promotions.

PLANNED AGENTS:

- Promotion Selector
- Creative Director
- Social Media Writer

BookieOS currently does NOT have access to
BookieCo live betting markets or odds.

Never invent odds.

Never claim that a betting market is available
at BookieCo unless it has actually been verified.

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
# RIGHT PANEL
# =========================================================

with agent_column:

    st.subheader(
        "Live Agents"
    )


    st.write(
        "🟢 🔎 Weekly Match Scout"
    )

    st.caption(
        "CONNECTED"
    )


    st.write(
        "🟢 🧠 Bet Researcher"
    )

    st.caption(
        "CONNECTED · AUTO"
    )


    st.write(
        "🟢 📣 Marketing Manager"
    )

    st.caption(
        "CONNECTED · AUTO"
    )


    st.write(
        "🟢 🚨 Sports News Monitor"
    )

    st.caption(
        "CONNECTED · MANUAL"
    )


    st.write(
        "🟢 🏆 Competitor Watch"
    )

    st.caption(
        "CONNECTED · MANUAL"
    )


    st.write(
        "🟢 📅 Sports Calendar"
    )

    st.caption(
        "CONNECTED · MANUAL"
    )


    st.divider()


    # =====================================================
    # SPORTS NEWS
    # =====================================================

    st.subheader(
        "🚨 Sports Intelligence"
    )

    st.caption(
        "Check major injuries, suspensions and important sports news."
    )


    if st.button(
        "🚨 Check Sports News",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Checking current sports news..."
            ):

                standalone_news_request = """
Perform a standalone current sports intelligence check.

Do NOT wait for a Weekly Match Scout report.

Search current sports news and identify only important
developments that could realistically matter to BookieCo.

Focus especially on:

- major football injuries
- important suspensions
- star players ruled out
- doubtful important players
- expected major player returns
- goalkeeper injuries
- manager changes
- major transfers
- match postponements
- match cancellations
- major squad problems
- important lineup developments

Give extra attention to:

- Cyprus football
- Cyprus teams in European competitions
- Greek teams
- Champions League
- Europa League
- Conference League
- Premier League
- La Liga
- Serie A
- Bundesliga
- major international football

Also mention major Formula 1 or basketball news if it is
important enough to affect betting or marketing interest.

Do NOT fill the report with minor stories.

Only show genuinely useful developments.

Clearly mark each item as:

🔴 MAJOR
🟠 WATCH
🟢 UPDATE

Include:

TEAM / EVENT
NEWS
WHY IT MATTERS
STATUS

If there are no important developments, say so clearly.
"""


                st.session_state.sports_news_report = (
                    run_sports_news_monitor(
                        client,
                        standalone_news_request
                    )
                )


        except Exception as e:

            st.error(
                f"Sports News Monitor error: {e}"
            )


    if st.session_state.sports_news_report:

        with st.container(
            border=True
        ):

            st.markdown(
                "### Latest Alerts"
            )

            st.write(
                st.session_state.sports_news_report
            )


    else:

        with st.container(
            border=True
        ):

            st.caption(
                "No sports intelligence check has been run yet."
            )


    st.divider()


    # =====================================================
    # COMPETITOR WATCH
    # =====================================================

    st.subheader(
        "🏆 Competitor Intelligence"
    )

    st.caption(
        "Check recent promotions and marketing activity from competitors."
    )


    if st.button(
        "🏆 Check Competitors",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Checking competitor activity..."
            ):

                st.session_state.competitor_report = (
                    run_competitor_watch(
                        client
                    )
                )


        except Exception as e:

            st.error(
                f"Competitor Watch error: {e}"
            )


    if st.session_state.competitor_report:

        with st.container(
            border=True
        ):

            st.markdown(
                "### Latest Competitor Report"
            )

            st.write(
                st.session_state.competitor_report
            )


    else:

        with st.container(
            border=True
        ):

            st.caption(
                "No competitor check has been run yet."
            )


    st.divider()


    # =====================================================
    # SPORTS CALENDAR
    # =====================================================

    st.subheader(
        "📅 Sports Calendar"
    )

    st.caption(
        "Look ahead 90 days for major marketing opportunities."
    )


    if st.button(
        "📅 Check Next 90 Days",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Building the 90-day sports calendar..."
            ):

                st.session_state.sports_calendar_report = (
                    run_sports_calendar(
                        client
                    )
                )

                # Clear old promo ideas whenever a new
                # calendar is generated.
                st.session_state.calendar_promo_ideas = None


        except Exception as e:

            st.error(
                f"Sports Calendar error: {e}"
            )


    if st.session_state.sports_calendar_report:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 90-Day Marketing Radar"
            )

            st.write(
                st.session_state.sports_calendar_report
            )


        # =================================================
        # OPTIONAL PROMO IDEAS
        # =================================================

        if st.button(
            "💡 Create Promo Ideas",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "Creating special-event promo ideas..."
                ):

                    promo_task = f"""
You are helping BookieCo brainstorm SPECIAL EVENT
promotion concepts.

BookieCo is a retail betting company in Cyprus.

Below is a 90-Day Sports Calendar created using
current sports research.

Your job is to identify ONLY the events that genuinely
deserve a special BookieCo campaign or promotion.

Do NOT create promotions for every event.

Special promotions should be reserved for major
opportunities.

Examples could include:

- major European football finals
- major Cyprus football opportunities
- major Greek football opportunities
- major international matches
- Formula 1 showcase weekends
- EuroLeague Final Four
- major tournament stages
- other exceptional sporting occasions

Be creative.

You may invent NEW promotional concepts.

However:

EVERY promotion you create is ONLY A CONCEPT.

It is NOT an active BookieCo promotion.

It is NOT approved.

It has NOT been checked against BookieCo rules.

It has NOT been checked against Cyprus advertising
or betting regulations.

It must therefore be clearly labelled:

⚠️ CONCEPT ONLY — NEEDS REVIEW

Do NOT invent BookieCo odds.

Do NOT claim any market currently exists at BookieCo.

Do NOT copy competitor promotions.

Think about concepts that could be exciting for
retail betting customers in Cyprus.

Possible types of ideas include:

- event-specific betting promotions
- prediction challenges
- score-related concepts
- goal-related concepts
- player-related concepts
- bet-builder concepts
- race-weekend concepts
- tournament concepts
- multi-day special-event campaigns
- shop-focused activations
- creative sports marketing mechanics

The concept does NOT need to be limited to these examples.

For every selected opportunity give:

EVENT:

DATE:

WHY THIS EVENT DESERVES A SPECIAL PROMO:

PROMO NAME:

PROMO CONCEPT:

HOW IT WOULD WORK:

WHY CUSTOMERS MAY FIND IT INTERESTING:

MARKETING POTENTIAL:
HIGH / MEDIUM / LOW

RECOMMENDED CONTENT:

Choose any that make sense:

- Instagram/Facebook Post
- Story
- Reel

PREPARATION TIME:

STATUS:
⚠️ CONCEPT ONLY — NEEDS REVIEW

At the end create:

SPECIAL EVENT PROMO SHORTLIST

Choose the BEST 3 concepts from the entire calendar.

Rank them:

🥇
🥈
🥉

Quality is much more important than quantity.


90-DAY SPORTS CALENDAR:

{st.session_state.sports_calendar_report}
"""


                    promo_response = client.responses.create(
                        model="gpt-5.6-luna",
                        input=promo_task
                    )


                    st.session_state.calendar_promo_ideas = (
                        promo_response.output_text
                    )


            except Exception as e:

                st.error(
                    f"Promo Ideas error: {e}"
                )


        if st.session_state.calendar_promo_ideas:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### 💡 Special Event Promo Ideas"
                )

                st.warning(
                    "Concepts only — these are not approved BookieCo promotions."
                )

                st.write(
                    st.session_state.calendar_promo_ideas
                )


    else:

        with st.container(
            border=True
        ):

            st.caption(
                "No 90-day calendar check has been run yet."
            )


    st.divider()


    # =====================================================
    # FUTURE AGENTS
    # =====================================================

    st.write(
        "⚪ 🎁 Promotion Selector"
    )

    st.caption(
        "WAITING FOR COMPANY FILES"
    )


    st.write(
        "⚪ 🎨 Creative Director"
    )

    st.caption(
        "PLANNED"
    )


    st.write(
        "⚪ ✍️ Social Media Writer"
    )

    st.caption(
        "PLANNED"
    )


    st.divider()


    st.success(
        "BOOKIEOS ONLINE"
    )
