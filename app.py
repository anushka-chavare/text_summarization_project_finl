from transformers import pipeline
from PyPDF2 import PdfReader

# Load summarization model
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

# Read PDF file
reader = PdfReader(r"C:\Users\anush\OneDrive\Desktop\CPE\Weekly Diary finl.pdf")

text = ""

# Extract text from all pages
for page in reader.pages:
    extracted_text = page.extract_text()

    if extracted_text:
        text += extracted_text

# Limit text size (important for transformer models)
text = text[:2000]

# Generate summary
summary = summarizer(
    text,
    max_length=120,
    min_length=40,
    do_sample=False
)

# Print summary
print("\n========== SUMMARY ==========\n")
print(summary[0]['summary_text'])