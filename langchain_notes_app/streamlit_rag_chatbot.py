import streamlit as st
from rag_chain import build_chain

st.set_page_config(page_title="🧠 PDF Chatbot", layout="wide")
st.title("Chat with Your PDF")

uploaded_file = st.file_uploader("📄 Upload a PDF file", type="pdf")

if uploaded_file:
    # Save uploaded file to disk
    with open(f"langchain_notes_app/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("✅ File uploaded successfully!")

    # Load QA chain
    qa = build_chain(f"langchain_notes_app/{uploaded_file.name}")

    query = st.text_input("Ask a question based on the PDF:")

    if query:
        with st.spinner("🤖 Generating answer..."):
            result = qa.run(query)
            st.write("📎 Answer:", result)
