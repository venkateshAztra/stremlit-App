import streamlit as st
from openai import OpenAI
from datetime import datetime
import time

import os
# --- Page Config ---
st.set_page_config(page_title="OpenRouter Chatbot", layout="centered")

# --- Dark Mode Toggle ---
dark_mode = st.toggle("🌙 Dark Mode")
if dark_mode:
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #121212;
            color: #f0f0f0;
        }
        .stChatMessage {
            background-color: #1e1e1e;
            color: #f0f0f0;
        }
        .user-msg, .bot-msg {
            color: #f0f0f0;
        }
        .stCaption, .stMarkdown {
            color: #ccc;
        }
        </style>
    """, unsafe_allow_html=True)


# --- Custom Styling (Light or Dark) ---
st.markdown("""
    <style>
    .user-msg {
        background-color: #ffe6e6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .bot-msg {
        background-color: #e6f2e6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- OpenRouter Setup ---
# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key="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"
# )


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)

st.title("🤖 OpenRouter-Powered Chatbot")

# --- Model Selector ---
model_choice = st.selectbox(
    "Select a model",
    ["openai/gpt-3.5-turbo", "openai/gpt-4", "mistralai/mixtral-8x7b"],
    index=0
)

# --- Initialize Session ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]
    st.session_state.timestamps = []

# --- Clear Chat Button ---
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]
    st.session_state.timestamps = []
    st.experimental_rerun()

# --- Display Chat History with Timestamps ---
for i, msg in enumerate(st.session_state.messages[1:]):
    role = msg["role"]
    icon = "👤" if role == "user" else "🤖"
    timestamp = st.session_state.timestamps[i] if i < len(st.session_state.timestamps) else ""

    with st.chat_message(role):
        st.markdown(f"{icon} {msg['content']}")
        st.caption(f"🕒 {timestamp}")

# --- User Input ---
user_input = st.chat_input("Type your message...")

if user_input:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.timestamps.append(timestamp)

    with st.chat_message("user"):
        st.markdown(user_input)
        st.caption(f"🕒 {timestamp}")

    # --- Typing Animation Simulation ---
    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown("🤖 typing...")
        time.sleep(1.5)

        # --- OpenRouter API Call ---
        response = client.chat.completions.create(
            model=model_choice,
            messages=st.session_state.messages,
        )

        reply = response.choices[0].message.content

        typing_placeholder.markdown(reply)
        reply_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state.timestamps.append(reply_timestamp)

# --- Download Chat Buttons ---
if len(st.session_state.messages) > 1:
    chat_log = ""
    for i, msg in enumerate(st.session_state.messages[1:]):
        role = msg["role"]
        timestamp = st.session_state.timestamps[i]
        sender = "You" if role == "user" else "Assistant"
        chat_log += f"[{timestamp}] {sender}: {msg['content']}\n\n"

    st.download_button("💾 Download as TXT", chat_log, file_name="chat_history.txt")

    # PDF requires ReportLab
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    def generate_pdf():
        from io import BytesIO
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        elements = []

        for i, msg in enumerate(st.session_state.messages[1:]):
            role = msg["role"]
            timestamp = st.session_state.timestamps[i]
            sender = "You" if role == "user" else "Assistant"
            elements.append(Paragraph(f"<b>[{timestamp}] {sender}:</b> {msg['content']}", styles["Normal"]))
            elements.append(Spacer(1, 12))

        doc.build(elements)
        buffer.seek(0)
        return buffer

    st.download_button(
        "📄 Download as PDF",
        data=generate_pdf(),
        file_name="chat_history.pdf",
        mime="application/pdf"
    )
