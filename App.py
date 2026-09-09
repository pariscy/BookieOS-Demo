import streamlit as st
from openai import OpenAI
from weekly_match_scout import run_weekly_match_scout


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


    # If voice was used, use the spoken text as the prompt
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

            # Decide whether this request belongs to the Match Scout
            prompt_lower = prompt.lower()

            scout_words = [
                "weekly match scout",
                "match scout",
                "matches",
                "match",
                "fixtures",
                "football",
                "next week",
                "champions league",
                "premier league",
                "europa league",
                "conference league",
                "la liga",
                "serie a",
                "bundesliga",
                "formula 1",
                "f1",

                # Greek routing words
                "αγώνες",
                "αγώνα",
                "ποδόσφαιρο",
                "επόμενη εβδομάδα",
                "ερχόμενη εβδομάδα",
                "τσάμπιονς λιγκ",
                "γιουρόπα λιγκ",
                "κόνφερενς λιγκ",
                "φόρμουλα 1"
            ]

            use_scout = any(
                word in prompt_lower
                for word in scout_words
            )


            # ---------- WEEKLY MATCH SCOUT ----------
            if use_scout:

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

Current Marketing agents:

- Marketing Manager
- Weekly Match Scout
- Bet Researcher
- Promotion Selector

The Weekly Match Scout is connected.

The other specialist agents are not connected yet.

The user may communicate with you in English or Greek.

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
    st.warning("● NOT CONNECTED")


    st.markdown("**📢 Promotion Selector**")
    st.warning("● NOT CONNECTED")


    st.divider()

    st.caption("SYSTEM STATUS")
    st.success("BOOKIEOS ONLINE")
