from typing import Any

import pandas as pd
import requests
import streamlit as st

# GLOBAL VARIABLES
THEME_MAPPING = {"The Lord Of the Rings": "LOTR"}
API_URL = "http://localhost:8000"


# UTILS FUNCTIONS
def stream_answer(theme: str, user_prompt: str, k: int = 4, filter: dict[str, Any] | None = None):
    with requests.post(
        f"{API_URL}/completion/ragchat/{theme}",
        json={"user_prompt": user_prompt, "k": k, "filter": filter},
        stream=True,
        timeout=(10, 300),
    ) as response:
        response.raise_for_status()
        response.encoding = "utf-8"
        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                yield chunk


# Page configuration
st.set_page_config(page_title="NerdBot", page_icon="🧙")

# -------------------------
# SIDE PANEL
# -------------------------
with st.sidebar:
    st.title("Nerd Bot")
    # Theme selection
    theme = st.selectbox("Choose theme:", list(THEME_MAPPING.keys()))

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
    if user_prompt := st.chat_input(f"Type your question here."):
        # Display and store user message
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Stream assistant response
        with st.chat_message("assistant"):
            with st.spinner("*NerdBot is thinking...*"):
                try:
                    answer = st.write_stream(stream_answer(THEME_MAPPING[theme], user_prompt))
                except requests.RequestException as e:
                    st.error(f"Could not get a response from NerdBot: {e}")
                    answer = None

        if answer is not None:
            st.session_state.messages.append({"role": "assistant", "content": answer})

# -------------------------
# DATABASE PANEL
# -------------------------
elif panel == "Database":
    try:
        response = requests.get(f"{API_URL}/documents/{THEME_MAPPING[theme]}", timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch documents from the API: {e}")

    df = pd.DataFrame(data["response"])
    df = df.rename(columns={"ids": "ID", "documents": "Text", "metadatas": "Metadata"})

    df["Metadata"] = df["Metadata"].map(
        lambda metadata: "\n".join(f"{key}: {value}" for key, value in metadata.items())
    )

    st.dataframe(df, hide_index=True, column_order=["ID", "Metadata", "Text"], row_height=100)

    st.caption(f"{len(df)} chunks in this collection.")
