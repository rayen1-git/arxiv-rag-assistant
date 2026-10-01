# arXiv Research Assistant (RAG)

A retrieval-augmented generation system that ingests arXiv papers on a topic,
stores them in a local vector database, and answers questions with citations
back to the exact paper.

Built to be a portfolio-quality example of RAG done properly: real embeddings,
a real vector store, and an evaluation harness — not just a demo notebook.

## Why this project

Most "RAG demos" stop at "it works on my example." This one adds:

- **Real embeddings** (sentence-transformers, runs locally, no API key needed for retrieval)
- **A real vector database** (ChromaDB, persisted to disk)
- **Grounded generation** via the Groq API (Llama 3.3), with inline citations
- **An evaluation harness** that scores faithfulness, answer relevance, and latency,
  so you can say "89% of answers were fully grounded" instead of "it seemed good"

## Architecture

```
arXiv API  ─▶  fetch_arxiv.py   (pull papers for a topic)
              │
              ▼
         ingest.py             (chunk abstracts, embed, store in Chroma)
              │
              ▼
          rag.py                (embed query → retrieve top-k → ask the LLM)
              │
              ▼
        evaluate.py             (run a question set, score groundedness)
              │
              ▼
          app.py                (Streamlit chat UI over the whole pipeline)
```

## Setup

```bash
pip install -r requirements.txt
# Windows (cmd):        set GROQ_API_KEY=your-key-here
# Windows (PowerShell): $env:GROQ_API_KEY="your-key-here"
# Mac/Linux:            export GROQ_API_KEY="your-key-here"
```

## Usage

**1. Pull papers on a topic and build the vector store:**
```bash
python -m src.ingest --topic "retrieval augmented generation" --max-results 40
```

**2. Ask a question from the command line:**
```bash
python -m src.rag --question "What techniques reduce hallucination in RAG systems?"
```

**3. Run the evaluation harness:**
```bash
python -m src.evaluate --questions data/eval_questions.json
```

**4. Launch the chat UI:**
```bash
streamlit run app.py
```

## Project layout

```
arxiv-rag-assistant/
├── README.md
├── requirements.txt
├── config.py
├── app.py                    # Streamlit UI
├── data/
│   ├── chroma_db/            # persisted vector store (created on first run)
│   └── eval_questions.json   # sample eval set
├── notebooks/
│   └── quickstart.ipynb      # walk-through in notebook form
└── src/
    ├── __init__.py
    ├── fetch_arxiv.py        # pull + parse papers from the arXiv API
    ├── ingest.py              # chunk, embed, store
    ├── rag.py                 # retrieve + generate with citations
    └── evaluate.py            # faithfulness / relevance / latency scoring
```

## What to highlight in a write-up or LinkedIn post

- Show a before/after: manual literature search time vs. this tool
- Share your eval numbers (faithfulness %, avg latency) — concrete metrics beat "it works great"
- Mention the design choice to run embeddings locally (cheaper, no API rate limits on ingestion)
  while using the LLM only for the final generation step

## Notes / next steps

- Swap in a reranker (e.g. cross-encoder) between retrieval and generation for a quality bump
- Add hybrid search (BM25 + embeddings) for queries with exact technical terms
- Add contradiction detection across papers for a stronger differentiator
