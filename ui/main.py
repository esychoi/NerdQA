import pandas as pd
import streamlit as st

# Page configuration
st.set_page_config(page_title="Nerd Bot", page_icon="🧙")

with st.sidebar:
    st.title("Nerd Bot")
    # Theme selection
    theme = st.selectbox("Choose theme:", ["The Lord Of The Rings"])

    # Panel selection
    panel = st.radio("Choose a panel:", ["Chat", "Database"], horizontal=True)

# -------------------------
# CHAT PANEL
# -------------------------
if panel == "Chat":
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"Hi 👋! I'm NerdBot. Ask me anything about {theme}."}
        ]

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input(f"Type your question here."):
        # Display and store user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Echo response (temporary)
        response = f"Echo: {prompt}"

        # Display and store assistant response
        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

# -------------------------
# DATABASE PANEL
# -------------------------
elif panel == "Database":
    # Mock database data (TODO: replace with ChromaDB data later)
    data = [
        {
            "ID": "0",
            "Metadata": {"source": "the_fellowship.txt", "page": 1},
            "Text": "In a hole in the ground there lived a hobbit. \nThis was the beginning of an unexpected adventure.",
        },
        {
            "ID": "1",
            "Metadata": {"source": "the_fellowship.txt", "page": 2},
            "Text": "The One Ring is an ancient and powerful artifact created by Sauron.",
        },
        {
            "ID": "2",
            "Metadata": {"source": "middle_earth.txt", "page": 5},
            "Text": "The Fellowship travelled across Middle-earth to destroy the One Ring.",
        },
    ]

    df = pd.DataFrame(data)

    df["Metadata"] = df["Metadata"].map(
        lambda metadata: "\n".join(f"{key}: {value}" for key, value in metadata.items())
    )

    st.dataframe(df, hide_index=True, row_height=100)

    st.caption(f"{len(df)} chunks in this collection (mock data).")
