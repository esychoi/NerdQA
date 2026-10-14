import pandas as pd
import requests
import streamlit as st

# GLOBAL VARIABLES
THEME_MAPPING = {"The Lord Of the Rings": "LOTR"}
API_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(page_title="Nerd Bot", page_icon="🧙")

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
    if prompt := st.chat_input(f"Type your question here."):
        # Display and store user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Call LLM
        with st.chat_message("assistant"):
            with st.spinner("*NerdBot is thinking...*"):
                response = requests.post(f"{API_URL}/completion", json={"user_prompt": prompt}, timeout=60)
                answer = response.json()["response"]

            st.markdown(answer)

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
