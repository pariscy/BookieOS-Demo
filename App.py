import streamlit as st
from openai import OpenAI

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

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("Ask BookieOS anything..."):

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.write(prompt)

        # Send the conversation to the real AI
        try:
            response = client.responses.create(
                model="gpt-5.6-luna",
                instructions="""
You are BookieOS, the internal AI operating system for BookieCo.

You coordinate specialist AI agents for the company.

Current Marketing agents:
- Marketing Manager
- Weekly Match Scout
- Bet Researcher
- Promotion Selector

Be concise, professional and helpful.

IMPORTANT:
The specialist agents are not connected yet.
Never pretend that an agent has performed work when it has not.
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
            answer = "BookieOS could not contact the AI service. Error: " + str(e)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        with st.chat_message("assistant"):
            st.write(answer)


with agents:
    st.subheader("⚡ LIVE AGENTS")

    st.markdown("**🤖 Marketing Manager**")
    st.success("● READY")

    st.markdown("**⚽ Weekly Match Scout**")
    st.success("● READY")

    st.markdown("**🔎 Bet Researcher**")
    st.success("● READY")

    st.markdown("**📢 Promotion Selector**")
    st.success("● READY")

    st.divider()

    st.caption("SYSTEM STATUS")
    st.success("BOOKIEOS ONLINE")
