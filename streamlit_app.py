from dotenv import load_dotenv
load_dotenv()

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
st.title("ISTQB Syllabus - RAG Chat")

rag_or_error = get_rag_service()
if isinstance(rag_or_error, dict) and rag_or_error.get("error"):
    st.error(rag_or_error["error"])
    st.stop()

rag: RAGService = rag_or_error

if "history" not in st.session_state:
    st.session_state.history = []

with st.form(key="ask_form", clear_on_submit=True):
    query = st.text_area("Ask a question:", height=300)
    st.caption('Enter a question regarding the syllabus and see how the RAG service answers based on the indexed content from the PDF')
    submit = st.form_submit_button("Send")

st.text("Chat History:")

if submit and query:
    st.session_state.history.append({"role": "user", "text": query})
    with st.spinner("Thinking..."):
        try:
            answer = rag.answer(query)
        except Exception as e:
            answer = f"[ERROR] {e}"

    # Normalize empty/None answers so UI shows a message instead of blank
    if answer is None or (isinstance(answer, str) and answer.strip() == ""):
        answer = "[NO ANSWER RETURNED]"

    st.session_state.history.append({"role": "assistant", "text": answer})
    # `st.experimental_rerun()` may not exist in some Streamlit versions/environment.
    # Use it when available; otherwise stop execution so the app can re-run on next interaction.
    # Try to trigger a rerun if available; do not call `st.stop()` as fallback
    # because that halts rendering and prevents the updated history from showing.
    try:
        rerun = getattr(st, "experimental_rerun", None)
        if callable(rerun):
            rerun()
    except Exception:
        # ignore and allow Streamlit to continue the normal script run
        pass

for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['text']}")
    else:
        st.markdown(f"**Assistant:** {msg['text']}")
