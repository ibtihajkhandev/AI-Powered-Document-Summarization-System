# 🤖 AI-Powered Document Summarization System

> AI-based NLP system that summarizes long documents into short, meaningful summaries using extractive techniques built with Python and NLTK.

---

## 📌 Project Overview

Organizations deal with large volumes of documents — reports, emails, and articles.
Manual summarization is time-consuming and inconsistent.
This system automatically extracts key sentences and produces a concise summary while preserving the most important information.

Built as **Task AI-INT-1** for the **Teyzix Core AI Internship (June 2026 Batch)**.

---

## ✨ Features

- ✅ Three input methods — direct text, `.txt` file, and `.pdf` file
- ✅ Full NLP preprocessing pipeline (lowercase → tokenize → remove stopwords → segment)
- ✅ Two summarization algorithms — **Frequency-Based** and **TF-IDF**
- ✅ Adjustable summary length (choose number of output sentences)
- ✅ Analytics module — word frequency, top keywords, sentence importance scores
- ✅ Export summary to `.txt` or `.pdf`
- ✅ Modular, readable, commented code — beginner-friendly

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| `nltk` | Tokenization, stopwords, sentence segmentation |
| `PyPDF2` | Extracting text from PDF files |
| `fpdf` | Exporting summary as a PDF |
| `collections` | Word frequency counting via Counter |
| `math` | IDF calculation using log() |
| `string / os` | Punctuation removal, file path handling |

---

## 📓 Notebook Cell Reference (Cells 1–9)

> Run cells **in order** from top to bottom in Google Colab.

| Cell | Module | What it does |
|---|---|---|
| Cell 1 | Install Libraries | Installs `nltk`, `PyPDF2`, `fpdf` using pip |
| Cell 2 | Imports & NLTK Data | Imports all modules; downloads `punkt` and `stopwords` |
| Cell 3 | Text Preprocessing | Lowercase, remove punctuation, tokenize, remove stopwords |
| Cell 4 | Data Input Module | Accepts text from direct input, `.txt` file, or `.pdf` file |
| Cell 5 | Frequency Summarizer | Scores sentences by raw word frequency; returns top N sentences |
| Cell 6 | TF-IDF Summarizer | Scores sentences using TF-IDF weighting; more accurate ranking |
| Cell 7 | Analytics Module | Word frequencies, top keywords, sentence importance scores |
| Cell 8 | Output & Export | Displays results; exports summary to `.txt` and `.pdf` |
| Cell 9 | Main Pipeline | Ties everything together — change your input here and run |

---

## 🚀 How to Run (Google Colab)

1. Open [Google Colab](https://colab.research.google.com)
2. Upload or copy the notebook cells in order
3. Run **Cell 1** to install all required libraries
4. Run **Cell 2** to import libraries and download NLTK data
5. Run **Cells 3 through 8** to load all functions into memory
6. In **Cell 9**, choose your input method and set `SUMMARY_SENTENCES`
7. Run **Cell 9** — results print in the output and files save to `/content/`

---

## 📂 Input Methods

### Option A — Direct Text (default)
```python
raw_text = input_from_text("""
Your long document text goes here ...
""")
```

### Option B — Load from `.txt` File
```python
# Upload file to Colab first, then:
raw_text = input_from_txt_file("/content/your_document.txt")
```

### Option C — Load from `.pdf` File
```python
# Upload PDF to Colab first, then:
raw_text = input_from_pdf_file("/content/your_document.pdf")
```

> Only one option should be active at a time. Comment out the others.

---

## ⚙️ Adjusting Summary Length

In **Cell 9**, change this variable:

```python
SUMMARY_SENTENCES = 4   # Change to any number between 1 and 10
```

---

## 📤 Output Files

| File | Description |
|---|---|
| `/content/summary_output.txt` | Plain text export of the TF-IDF summary |
| `/content/summary_output.pdf` | Formatted PDF export with title and summary |

Download both from the **Files panel** on the left side of Colab.

---

## 🧠 How the Summarization Works

### Method 1 — Frequency-Based
- Count how often each important word appears across the document
- Score each sentence by summing the frequencies of its words
- Select the top N highest-scoring sentences in original order

### Method 2 — TF-IDF
- **TF** → how often a word appears in a given sentence (normalized)
- **IDF** → penalizes words that appear in many sentences (not unique enough)
- Words common in one sentence but rare across the document score highest
- More accurate than plain frequency — avoids rewarding generic filler words

---

## 📊 Analytics Module Output

After summarization, Cell 9 automatically displays:

- Total word count (after cleaning)
- Unique word count
- Total sentence count
- Top 10 most frequent keywords
- Top 3 most important sentences with importance scores

---

## 📁 Project Structure
