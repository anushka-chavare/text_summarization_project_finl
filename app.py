import streamlit as st
from transformers import pipeline
from pypdf import PdfReader

# ----------------------------
# MODEL
# ----------------------------
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# ----------------------------
# FUNCTIONS
# ----------------------------
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    return text

def summarize_text(text, max_len):
    if len(text.split()) > 800:
        text = " ".join(text.split()[:800])  # safety limit

    summary = summarizer(
        text,
        max_length=max_len,
        min_length=30,
        do_sample=False
    )
    return summary[0]["summary_text"]

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
            summary = summarize_text(text, length)

            st.subheader("🧠 Summary")
            st.write(summary)

            st.subheader("📊 Stats")
            st.write(f"Original Words: {len(text.split())}")
            st.write(f"Summary Words: {len(summary.split())}")

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
                summary = summarize_text(text, length)

                st.subheader("🧠 Summary")
                st.write(summary)

                st.subheader("📊 Stats")
                st.write(f"Original Words: {len(text.split())}")
                st.write(f"Summary Words: {len(summary.split())}")

                st.download_button(
                    "⬇️ Download Summary",
                    summary,
                    file_name="pdf_summary.txt"
                )
        else:
            st.error("Could not extract text from PDF")