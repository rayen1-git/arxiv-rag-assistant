"""Streamlit UI for the arXiv Research Assistant.

Run with:
    streamlit run app.py
"""
import streamlit as st

import config
from src.fetch_arxiv import fetch_papers
from src.ingest import build_vector_store
from src.rag import answer as rag_answer

st.set_page_config(page_title="arXiv Research Assistant", page_icon="📚", layout="centered")

st.title("📚 arXiv Research Assistant")
st.caption("Retrieval-augmented Q&A over real arXiv papers, with inline citations.")

with st.sidebar:
    st.header("1. Build a corpus")
    topic = st.text_input("Topic", value="retrieval augmented generation")
    max_results = st.slider("Number of papers", 10, 100, 20, step=10)
    full_text = st.checkbox("Index full PDF text (slower, much richer)", value=True)
    if st.button("Fetch + index papers", use_container_width=True):
        with st.spinner(f"Fetching up to {max_results} papers on '{topic}'..."):
            papers = fetch_papers(topic, max_results)
        if not papers:
            st.error("No papers found for that topic.")
        else:
            with st.spinner("Embedding and storing in vector database..."):
                build_vector_store(papers, full_text=full_text)
            st.success(f"Indexed {len(papers)} papers on '{topic}'.")

    st.divider()
    if not config.GROQ_API_KEY:
        st.warning("GROQ_API_KEY is not set. Set it in your terminal before asking questions.")

st.header("2. Ask a question")
question = st.text_input("Your question", placeholder="e.g. What reduces hallucination in RAG systems?")

if st.button("Ask", type="primary") and question:
    with st.spinner("Retrieving relevant papers and generating an answer..."):
        result = rag_answer(question)

    st.subheader("Answer")
    st.write(result["answer"])

    if result["sources"]:
        st.subheader("Sources used")
        for s in result["sources"]:
            page = f" (p.{s['page']})" if s.get("page") else ""
            st.markdown(f"- **[{s['arxiv_id']}]**{page} {s['title']} — [link]({s['url']})")
