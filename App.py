import streamlit as st

st.set_page_config(
    page_title="BookieOS",
    page_icon="🤖",
    layout="wide"
)

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

    # Conversation memory
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

        # Temporary demo response
        response = (
            "Understood. This is currently the BookieOS demo interface. "
            "My AI brain and specialist agents will be connected next."
        )

        with st.chat_message("assistant"):
            st.write(response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })


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
