# AI Text & PDF Summarizer

An AI-powered web application that summarizes long text and PDF documents using state-of-the-art transformer models from Hugging Face. The application provides an intuitive Streamlit interface for generating concise summaries from user-provided text or uploaded PDF files.

---

## Features

* Summarize raw text input
* Extract and summarize PDF documents
* Adjustable summary length
* Input vs. summary word count comparison
* Download generated summaries
* Interactive Streamlit web interface

---

## Technologies Used

* Python
* Streamlit
* Hugging Face Transformers
* PyPDF
* BART (`facebook/bart-large-cnn`)

---

## Model

The application uses **facebook/bart-large-cnn**, a transformer-based sequence-to-sequence model fine-tuned for abstractive text summarization.

---

## Project Structure

```
text_summarization_project/
│
├── app.py
├── requirements.txt
├── assets/
│   ├── text_input_ui.png
│   ├── pdf_input_ui.png
│   ├── text_output1.png
│   ├── text_output2.png
│   ├── pdf_output1.png
│   ├── pdf_output2.png
│   └── pdf_output3.png
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<anushka-chavare>/text_summarization_project_finl.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## Live Demo

https://textsummarizationprojectfinl.streamlit.app/

---

## Screenshots

### Text Input

![Text Input](assets/text_input_ui.png)

### PDF Upload

![PDF Upload](assets/pdf_input_ui.png)

### Generated Summary

![Summary](assets/text_output1.png)

---

## Applications

* Research paper summarization
* Article summarization
* Study notes condensation
* Document review
* Educational content analysis

---

## Future Enhancements

* URL summarization
* Multi-language summarization
* Export summary as PDF
* Support for very large documents using chunk-based processing
* OCR support for scanned PDFs

---

## Author

**Anushka Chavare**

GitHub: https://github.com/anushka-chavare

LinkedIn: https://www.linkedin.com/in/anushka-chavare/