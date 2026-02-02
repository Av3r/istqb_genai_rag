import streamlit as st
from openai import OpenAI
from app.config import load_settings
from app.rag import RAGService

@st.cache_resource
def get_rag_service():
    try:
        settings = load_settings()
    except Exception as e:
        return {"error": str(e)}

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return RAGService(client, settings)

st.set_page_config(page_title="RAG Chat", layout="wide")
st.title("RAG Chat")

rag_or_error = get_rag_service()
if isinstance(rag_or_error, dict) and rag_or_error.get("error"):
    st.error(rag_or_error["error"])
    st.stop()

rag: RAGService = rag_or_error

if "history" not in st.session_state:
    st.session_state.history = []

with st.form(key="ask_form", clear_on_submit=True):
    query = st.text_input("Ask a question:")
    submit = st.form_submit_button("Send")

if submit and query:
    st.session_state.history.append({"role": "user", "text": query})
    with st.spinner("Thinking..."):
        try:
            answer = rag.answer(query)
        except Exception as e:
            answer = f"[ERROR] {e}"
    st.session_state.history.append({"role": "assistant", "text": answer})
    st.experimental_rerun()

for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['text']}")
    else:
        st.markdown(f"**Assistant:** {msg['text']}")
