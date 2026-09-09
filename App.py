import streamlit as st
from openai import OpenAI
from weekly_match_scout import run_weekly_match_scout
from bet_researcher import run_bet_researcher


st.set_page_config(
    page_title="BookieOS",
    page_icon="🤖",
    layout="wide"
)


# Connect BookieOS to OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# ---------- HEADER ----------
st.title("◉ BOOKIEOS")
st.caption("BookieCo Artificial Intelligence Operating System")

st.divider()


# ---------- LAYOUT ----------
main, agents = st.columns([2.3, 1])


with main:
    st.subheader("🤖 BookieOS")

    st.info(
        "Good afternoon, Paris.\n\n"
        "BookieOS is online. What would you like me to do?"
    )


    # ---------- CHAT MEMORY ----------
    if "messages" not in st.session_state:
        st.session_state.messages = []


    # Show previous messages
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
            st.error("Voice transcription error: " + str(e))


    # ---------- TEXT INPUT ----------
    prompt = st.chat_input("Ask BookieOS anything...")


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


            # ---------- ROUTING WORDS ----------

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


            researcher_words = [
                "bet researcher",
                "research this bet",
                "research the bet",
                "check this bet",
                "check this market",
                "bet type",
                "bet market",
                "bet builder",
                "player shots",
                "player cards",
                "corners",
                "cards",
                "does this bet make sense",
                "analyse this bet",
                "analyze this bet",

                # Greek
                "έλεγξε το στοίχημα",
                "έλεγξε αυτό το στοίχημα",
                "έλεγξε την αγορά",
                "τύπος στοιχήματος",
                "αγορά στοιχήματος",
                "bet builder",
                "κόρνερ",
                "κάρτες",
                "σουτ παίκτη",
                "ανάλυσε το στοίχημα"
            ]


            use_researcher = any(
                word in prompt_lower
                for word in researcher_words
            )

            use_scout = any(
                word in prompt_lower
                for word in scout_words
            )


            # ---------- BET RESEARCHER ----------
            if use_researcher:

                with st.spinner("🔎 Bet Researcher is working..."):

                    researcher_result = run_bet_researcher(
                        client,
                        prompt
                    )

                answer = (
                    "🔎 **Bet Researcher report**\n\n"
                    + researcher_result
                )


            # ---------- WEEKLY MATCH SCOUT ----------
            elif use_scout:

                with st.spinner("⚽ Weekly Match Scout is working..."):

                    scout_result = run_weekly_match_scout(
                        client,
                        prompt
                    )

                answer = (
                    "⚽ **Weekly Match Scout report**\n\n"
                    + scout_result
                )


            # ---------- BOOKIEOS ----------
            else:

                response = client.responses.create(
                    model="gpt-5.6-luna",
                    instructions="""
You are BookieOS, the internal AI operating system for BookieCo.

Your job is to coordinate specialist AI agents and communicate with the user.

CURRENT CONNECTED AGENTS:

1. Weekly Match Scout
Purpose:
Research upcoming sporting events and recommend strong marketing opportunities.

2. Bet Researcher
Purpose:
Research proposed betting ideas, analyse whether the betting angle makes sense,
and eventually verify whether the market exists at BookieCo.

NOT YET CONNECTED:

- Marketing Manager
- Promotion Selector

IMPORTANT:
BookieCo's actual market catalogue and odds are NOT connected yet.

Therefore:
- Never claim that a proposed betting market is definitely available at BookieCo.
- Never invent BookieCo odds.
- The Bet Researcher may research the idea, but BookieCo availability still requires a future data connection.

The user may communicate in English or Greek.

If the user speaks Greek, respond in Greek.

If the user speaks English, respond in English.

Be concise, professional and helpful.

Never pretend that an unconnected agent has completed work.
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


# ---------- AGENTS PANEL ----------
with agents:

    st.subheader("⚡ LIVE AGENTS")


    st.markdown("**🤖 Marketing Manager**")
    st.warning("● NOT CONNECTED")


    st.markdown("**⚽ Weekly Match Scout**")
    st.success("● CONNECTED")


    st.markdown("**🔎 Bet Researcher**")
    st.success("● CONNECTED")


    st.markdown("**📢 Promotion Selector**")
    st.warning("● NOT CONNECTED")


    st.divider()

    st.caption("SYSTEM STATUS")
    st.success("BOOKIEOS ONLINE")
