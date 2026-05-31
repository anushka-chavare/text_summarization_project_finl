import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq

st.title("Text Summarizer (Extractive NLP)")

text = st.text_area("Enter Text")

if st.button("Summarize"):

    if text.strip():

        sentences = sent_tokenize(text)

        stop_words = set(stopwords.words("english"))

        word_freq = {}

        for word in word_tokenize(text.lower()):
            if word.isalnum() and word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1

        sentence_scores = {}

        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in word_freq:
                    sentence_scores[sentence] = (
                        sentence_scores.get(sentence, 0)
                        + word_freq[word]
                    )

        summary = heapq.nlargest(
            3,
            sentence_scores,
            key=sentence_scores.get
        )

        st.subheader("Summary")
        st.write(" ".join(summary))