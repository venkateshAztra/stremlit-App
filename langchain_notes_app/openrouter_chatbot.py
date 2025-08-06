

import streamlit as st
from openai import OpenAI

# ✅ Set OpenRouter API key and base URL
client = OpenAI(
    api_key="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",  # 🔐 Replace with your actual OpenRouter key
    base_url="https://openrouter.ai/api/v1"
)

st.set_page_config(page_title="🧠 Chatbot via OpenRouter", layout="centered")
st.title("🤖 Chatbot via OpenRouter API")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Display previous messages
for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).write(msg["content"])

# User input box
if prompt := st.chat_input("Ask anything..."):
    # Show user message
    st.chat_message("user").write(prompt)

    # Add to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Send to OpenRouter
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",  # ✅ use "z-ai/glm-4.5" or another available model
            messages=st.session_state.messages,
            max_tokens=500
        )

        reply = response.choices[0].message.content

        # Show reply
        st.chat_message("assistant").write(reply)

        # Save to history
        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.error(f"❌ Error: {e}")
