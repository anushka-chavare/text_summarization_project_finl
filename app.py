import re

from pypdf import PdfReader
import streamlit as st
from transformers import pipeline

# BART accepts at most 1024 tokens; ~600 words per chunk stays safely under it
CHUNK_WORDS = 600


@st.cache_resource
def load_model():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_model()


# ----------------------------
# FUNCTIONS
# ----------------------------
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    pages = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            pages.append(page_text)

    return "\n".join(pages)


def clean_text(text):
    """Fix common PDF extraction issues before summarizing."""
    text = re.sub(r"-\s*\n\s*", "", text)         # join words hyphenated across lines
    text = re.sub(r"\s*\n\s*", " ", text)          # line breaks -> spaces
    text = re.sub(r"[^\S ]+", " ", text)           # tabs and other whitespace
    text = re.sub(r" {2,}", " ", text)             # collapse repeated spaces
    return text.strip()


def split_into_chunks(text, max_words=CHUNK_WORDS):
    """Split text into chunks of whole sentences, each under max_words."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks, current, count = [], [], 0

    for sentence in sentences:
        words = sentence.split()
        # a single very long "sentence" (e.g. no punctuation) is cut into pieces
        while len(words) > max_words:
            if current:
                chunks.append(" ".join(current))
                current, count = [], 0
            chunks.append(" ".join(words[:max_words]))
            words = words[max_words:]
        if count + len(words) > max_words and current:
            chunks.append(" ".join(current))
            current, count = [], 0
        if words:
            current.append(" ".join(words))
            count += len(words)

    if current:
        chunks.append(" ".join(current))
    return chunks


def run_model(text, max_len):
    summary = summarizer(
        text,
        max_length=max_len,
        min_length=30,
        do_sample=False,
        truncation=True,
    )
    return summary[0]["summary_text"]


def summarize_text(text, max_len):
    """Clean, chunk, summarize each chunk, then combine. Returns (summary, chunk_count)."""
    text = clean_text(text)
    chunks = split_into_chunks(text)

    if len(chunks) == 1:
        return run_model(chunks[0], max_len), 1

    progress = st.progress(0, text="Summarizing chunks...")
    partial = []
    for i, chunk in enumerate(chunks, start=1):
        partial.append(run_model(chunk, max_len))
        progress.progress(i / len(chunks), text=f"Summarized chunk {i} of {len(chunks)}")
    progress.empty()

    combined = " ".join(partial)
    # summary of summaries, so the final length follows the slider
    if len(combined.split()) > max_len:
        combined = " ".join(run_model(c, max_len) for c in split_into_chunks(combined))
    return combined, len(chunks)

# ----------------------------
# UI
# ----------------------------
st.set_page_config(page_title="AI Summarizer", layout="centered")

st.title("📄 AI Text & PDF Summarizer")
st.write("Summarize text or upload a PDF using Transformers AI")

# Sidebar
st.sidebar.title("ℹ️ Model Info")
st.sidebar.write("Model: facebook/bart-large-cnn")
st.sidebar.write("Task: Abstractive Summarization")

# Summary length control
length = st.slider("✂️ Summary Length", 50, 200, 100)

# Tabs
tab1, tab2 = st.tabs(["✍️ Text Input", "📄 PDF Upload"])

# ----------------------------
# TAB 1: TEXT
# ----------------------------
with tab1:
    st.subheader("Enter Text")

    example = st.selectbox(
        "Try Example",
        [
            "AI is transforming industries by enabling automation and intelligent decision making.",
            "Machine learning is a subset of artificial intelligence that focuses on data-driven learning."
        ]
    )

    text = st.text_area("Input Text", value=example, height=200)

    if st.button("Summarize Text"):
        if text.strip():
            summary, n_chunks = summarize_text(text, length)

            st.subheader("🧠 Summary")
            st.write(summary)

            st.subheader("📊 Stats")
            st.write(f"Original Words: {len(text.split())}")
            st.write(f"Summary Words: {len(summary.split())}")
            st.write(f"Chunks Processed: {n_chunks}")

            st.download_button(
                "⬇️ Download Summary",
                summary,
                file_name="summary.txt"
            )
        else:
            st.warning("Please enter text")

# ----------------------------
# TAB 2: PDF
# ----------------------------
with tab2:
    st.subheader("Upload PDF File")

    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])

    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)

        if text.strip():
            st.subheader("📄 Extracted Text Preview")
            st.write(text[:1000] + "...")

            if st.button("Summarize PDF"):
                summary, n_chunks = summarize_text(text, length)

                st.subheader("🧠 Summary")
                st.write(summary)

                st.subheader("📊 Stats")
                st.write(f"Original Words: {len(text.split())}")
                st.write(f"Summary Words: {len(summary.split())}")
                st.write(f"Chunks Processed: {n_chunks}")

                st.download_button(
                    "⬇️ Download Summary",
                    summary,
                    file_name="pdf_summary.txt"
                )
        else:
            st.error("Could not extract text from PDF")