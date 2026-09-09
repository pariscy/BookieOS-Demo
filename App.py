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


            # ---------- MATCH SCOUT ROUTING ----------
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


            # ---------- WEEKLY MATCH SCOUT + AUTOMATIC BET RESEARCHER ----------
            if use_scout:

                with st.spinner("⚽ Weekly Match Scout is researching..."):

                    scout_result = run_weekly_match_scout(
                        client,
                        prompt
                    )


                with st.spinner("🔎 Bet Researcher is automatically analysing the Scout report..."):

                    researcher_task = f"""
The Weekly Match Scout produced the following report:

--- SCOUT REPORT START ---

{scout_result}

--- SCOUT REPORT END ---

Automatically analyse EVERY proposed football betting market in this report.

For each proposed football bet:

1. Identify the match.
2. Identify the proposed betting market.
3. Research whether the betting idea makes sense.
4. Check current team/player/statistical information when relevant.
5. Rate the proposed bet:
   - STRONG
   - REASONABLE
   - WEAK
6. Explain the reasoning briefly.
7. Clearly state that BookieCo market availability is NOT YET VERIFIED.

Do not skip proposed football bets.

Do not analyse Formula 1 or other non-football events as football betting markets.

Return the analysis in the same day-by-day order as the Scout report.
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


            # ---------- BOOKIEOS ----------
            else:

                response = client.responses.create(
                    model="gpt-5.6-luna",
                    instructions="""
You are BookieOS, the internal AI operating system for BookieCo.

Your job is to coordinate specialist AI agents and communicate with the user.

CONNECTED AGENTS:

1. Weekly Match Scout
- Finds upcoming sporting events.
- Produces weekly marketing recommendations.
- Proposes interesting football betting markets.

2. Bet Researcher
- Automatically analyses every football betting market proposed by the Weekly Match Scout.
- Researches whether the betting idea makes sense.
- Will later verify BookieCo's actual market availability and odds.

CURRENT AUTOMATIC WORKFLOW:

User
→ BookieOS
→ Weekly Match Scout
→ Bet Researcher
→ BookieOS
→ User

The user does NOT need to manually ask the Bet Researcher to analyse every match.

NOT YET CONNECTED:
- Marketing Manager
- Promotion Selector

IMPORTANT:
BookieCo's actual market catalogue and odds are NOT connected yet.

Therefore:
- Never claim a proposed betting market definitely exists at BookieCo.
- Never invent BookieCo odds.
- Bet Researcher analysis is research only until the BookieCo data connection is built.

The user may communicate in English or Greek.

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


# ---------- AGENTS PANEL ----------
with agents:

    st.subheader("⚡ LIVE AGENTS")


    st.markdown("**🤖 Marketing Manager**")
    st.warning("● NOT CONNECTED")


    st.markdown("**⚽ Weekly Match Scout**")
    st.success("● CONNECTED")


    st.markdown("**🔎 Bet Researcher**")
    st.success("● CONNECTED - AUTO")


    st.markdown("**📢 Promotion Selector**")
    st.warning("● NOT CONNECTED")


    st.divider()

    st.caption("SYSTEM STATUS")
    st.success("BOOKIEOS ONLINE")
