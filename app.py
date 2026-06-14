#____ CELL 1: Install required librarie ____

!pip install nltk PyPDF2 fpdf

# CELL 2: Import all libraries we will use

import nltk  # (Natural Language Toolkit)
import string  # import for removing punctuation
import math    # import for mathematical calculation if need
import os
from collections import Counter, defaultdict

# PyPDF2 is used to read text from PDF files
import PyPDF2

# fpdf is used to export summary as a PDF file
from fpdf import FPDF

# Download NLTK resources (only needed once)
nltk.download('punkt')           # For sentence and word tokenization
nltk.download('stopwords')       # Common words like "the", "is", "and"
nltk.download('punkt_tab')       # Updated tokenizer tables

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

print("All libraries imported successfully!")

 # ___CELL 3: TEXT Preprocessing Function___

 def process_text(text): # this function process and clean text

     # step 1: convert lowercase, for example, APPLE and apple treated as the same
     lower_case = text.lower()

     # step 2: remove punctuation
     cl_text = lower_case.translate(str.maketrans('', '', string.punctuation))

     # step 3: tokenize, split text into words
     tk_words = word_tokenize(cl_text)

     # step 4: filter them out english stopwords
     stop_words = set(stopwords.words('english'))
     filtered_words = [word for word in tk_words if word not in stop_words and word.isalpha()]

     return filtered_words



def Sentence_segmentation(text): # this function tokenizes Splits the full text into individual sentences

      sentence = sent_tokenize(text)

      return sentence

  # === Testing ===
 sample_test = "A company collected customer feedback from emails and reports. A data science team processed the text, removed stop words, extracted key insights, and generated short summaries for management."

print("\ntokenize words:",process_text(sample_test))
print("\ntokenize sentences:",Sentence_segmentation(sample_test))

# cell 4: data input function

def input_from_text(text): # this function takes input from text
  if not text.strip():
    raise ValueError("Input text cannot be empty. Please provide text") # raise error if input is empty
  return text.strip()

def input_from_textfile(filepath): # this function takes input from text file
  if not os.path.isfile(filepath):
    raise FileNotFoundError(f"File not found: {filepath}")
  with open(filepath, 'r') as file:
    text = file.read()

  if not text.strip():
    raise ValueError("Input text cannot be empty.Please provide text")
    print(f"Loaded text file: {filepath}")

  return text

def input_from_pdf(filepath): # this function takes input from pdf file
  if not os.path.isfile(filepath):
    raise FileNotFoundError(f"File not found: {filepath}")


  text = ''
  with open(filepath, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)

     # Loop through every page in the PDF
    for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "

  if not text.strip():
    raise ValueError("Could not extract text from PDF")

  print(f"Loaded PDF: {filepath} ({len(pdf_reader.pages)} pages)")
  return text


print('input function ready')

# cell 5: Frequency-Based Extractive Summarization

def frequency_based_summary(text, num_sentences=3):

    # Get clean words (no stopwords, lowercase)
    clean_words = process_text(text)

    # Count frequency of each word
    word_freq = Counter(clean_words)

    # Get all sentences from original text
    sentences = Sentence_segmentation(text)
    # value Erroe raise if length of sentence zero or space  
    if len(sentences) == 0:
        raise ValueError("No sentences found in the text.")

    # Cap summary length — can't summarize more sentences than we have
    num_sentences = min(num_sentences, len(sentences))


    # Score each sentence
    sentence_scores = {}
    for sentence in sentences:
        # Lowercase the sentence for word matching
        words_in_sentence = word_tokenize(sentence.lower())
        score = 0
        for word in words_in_sentence:
            if word in word_freq:
                score += word_freq[word]  # Add frequency of each word
        sentence_scores[sentence] = score

    # Sort sentences by score (highest first) and pick top N
    ranked_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    top_sentences = ranked_sentences[:num_sentences]

    # Keep original order of sentences in the summary
    summary_sentences = [s for s in sentences if s in top_sentences]
    summary = ' '.join(summary_sentences)

    return summary, sentence_scores


print(" Frequency-based summarizer ready!")

# CELL 6: TF-IDF Based Summarization

def tfidf_based_summary(text, num_sentences=3): #  Extractive summarization using TF-IDF scoring.
                                                #  TF  = Term Frequency  → how often a word appears in a sentence
 # Get all sentences from original text         #  IDF = Inverse Document Frequency → penalizes words common in ALL sentence
  sentences = Sentence_segmentation(text)

 # value Erroe raise if length of sentence zero or space
  if len(sentences) == 0:
    raise ValueError("No sentences found in the text.")

  num_sentences = min(num_sentences, len(sentences))
  # Filter english words
  stop_words = set(stopwords.words('english'))

  # step 1: Tokenize Each Sentence
  tokenized_sentences = []
  for sentence in sentences:
    words = word_tokenize(sentence.lower())
    clean_sent = [i for i in words if i.isalpha() and i not in stop_words]
    tokenized_sentences.append(clean_sent)

  total_sentences = len(sentences)

 # Step 2: Calculate TF for each word in each sentence
  tf_sr = []
  for token in tokenized_sentences:
    tf = {}
    total = len(token) if len(token) > 0 else 1
    word_count = Counter(token)
    for word, count in word_count.items():
      tf[word] = count / total
    tf_sr.append(tf)

   # Step 3: Calculate IDF for each word
  idf = {}
  all_words = set(word for tokens in tokenized_sentences for word in token)

  for word in all_words:
    count = sum(1 for tokens in tokenized_sentences if word in tokens)
    idf[word] = math.log(total_sentences / (count + 1))

 # Step 4: Score each sentence using TF-IDF
  sentence_scores = {}
  for i, sentence in enumerate(sentences):
    score = 0
    for word, tf_val in tf_sr[i].items():
      score += tf_val * idf.get(word, 0)  # TF × IDF
    sentence_scores[sentence] = score

 # Pick top N sentences, preserve original order
  top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
  summary_sentences = [s for s in sentences if s in top_sentences]
  summary = ' '.join(summary_sentences)

  return summary, sentence_scores

print("TF-IDF summarizer ready!")

# CELL 7: Analytics Module
# Word frequency, keywords, sentence importance

def analyze_text(text, top_n=10):
    """
    Performs text analytics:
    - Word frequency distribution
    - Top N most important keywords
    - Sentence importance scores
    
    Parameters:
    - text: input document
    - top_n: how many top keywords to show
  
    """
    
    clean_words = process_text(text)
    sentences = Sentence_segmentation(text)
    
    # Word Frequency 
    word_freq = Counter(clean_words)
  
    # Top N Keywords 
    top_keywords = word_freq.most_common(top_n)
    
    # Sentence Importance Score (using frequency method) 
    _, sentence_scores = frequency_based_summary(text, num_sentences=len(sentences))
    
    # Sort sentences by importance
    ranked = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    
    analytics = {
        "total_words": len(clean_words),
        "unique_words": len(word_freq),
        "total_sentences": len(sentences),
        "word_frequency": dict(word_freq),
        "top_keywords": top_keywords,
        "sentence_ranking": ranked
    }
    
    return analytics


def display_analytics(analytics):
    """
    Prints analytics results in a clean readable format.
    """
    print("=" * 55)
    print("            📊 TEXT ANALYTICS REPORT")
    print("=" * 55)
    print(f"  📝 Total Words (cleaned)  : {analytics['total_words']}")
    print(f"  🔤 Unique Words           : {analytics['unique_words']}")
    print(f"  📄 Total Sentences        : {analytics['total_sentences']}")
    
    print("\n  🔑 Top Keywords:")
    for i, (word, freq) in enumerate(analytics['top_keywords'], 1):
        print(f"     {i:>2}. {word:<20} (freq: {freq})")
    
    print("\n  📈 Top 3 Most Important Sentences:")
    for i, (sentence, score) in enumerate(analytics['sentence_ranking'][:3], 1):
        short = sentence[:80] + "..." if len(sentence) > 80 else sentence
        print(f"     {i}. [{score:.2f}] {short}")
    print("=" * 55)


print("Analytics module ready!")

# CELL 8: Output and File Export
# Show results, export to .txt or .pdf

def display_summary(original_text, summary, method_name="Frequency"):
    """
    Prints original text vs summary side by side for comparison.
    """
    original_words = len(original_text.split())
    summary_words = len(summary.split())
    reduction = round((1 - summary_words / original_words) * 100, 1) if original_words > 0 else 0
    
    print("=" * 60)
    print(f"  📄 SUMMARIZATION RESULT  [{method_name}]")
    print("=" * 60)
    print(f"\n  Original : {original_words} words")
    print(f"  Summary  : {summary_words} words  ({reduction}% reduction)\n")
    print("─" * 60)
    print("  ORIGINAL TEXT (first 300 chars):")
    print(f"  {original_text[:300]}...")
    print("\n─" * 8)
    print("  SUMMARY:")
    print(f"  {summary}")
    print("=" * 60)


def export_to_txt(summary, original_text, filepath="/content/summary_output.txt"):
    """
    Saves the summary and original text to a .txt file.
    Default save location is /content/ in Colab.
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("AI-POWERED DOCUMENT SUMMARIZATION SYSTEM\n")
        f.write("Teyzix Core Internship — Task AI-INT-1\n")
        f.write("=" * 50 + "\n\n")
        f.write("ORIGINAL TEXT:\n")
        f.write(original_text + "\n\n")
        f.write("=" * 50 + "\n\n")
        f.write("GENERATED SUMMARY:\n")
        f.write(summary + "\n")
    
    print(f"Summary exported to TXT: {filepath}")


def export_to_pdf(summary, original_text, filepath="/content/summary_output.pdf"):
    """
    Saves the summary to a nicely formatted PDF using fpdf.
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(0, 10, "AI Document Summarization System", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, "Teyzix Core Internship - Task AI-INT-1", ln=True, align='C')
    pdf.ln(5)
    
    # Original Text Section 
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 8, "Original Text (Preview):", ln=True)
    pdf.set_font("Arial", size=10)
    
    # Limit to first 600 characters for PDF preview
    preview = original_text[:600] + "..." if len(original_text) > 600 else original_text
    # multi_cell handles long text with line wrapping
    pdf.multi_cell(0, 6, preview)
    pdf.ln(5)
    
    # --- Summary Section ---
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 8, "Generated Summary:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, summary)
    
    # Save the PDF
    pdf.output(filepath)
    print(f"Summary exported to PDF: {filepath}")


print("Output module ready!")

# Cell 9: Testing

raw_text = input_from_text("""
Artificial Intelligence (AI) is rapidly transforming every sector of the modern world.
From healthcare to finance, AI systems are automating complex tasks and improving efficiency.
Machine learning, a subset of AI, allows systems to learn from data without being explicitly programmed.
Deep learning uses neural networks to recognize patterns in large datasets.
Natural Language Processing (NLP) enables machines to understand and generate human language.
AI-powered chatbots are now used in customer service to handle thousands of queries simultaneously.
Self-driving cars rely on AI algorithms to navigate roads safely.
In medicine, AI is helping diagnose diseases like cancer faster and more accurately than humans.
The global AI market is expected to reach trillions of dollars in the coming decade.
However, AI also raises important ethical questions around bias, privacy, and job displacement.
Governments worldwide are working on regulations to ensure responsible AI development.
Education systems are adapting to prepare students for an AI-driven economy.
Open-source AI tools have democratized access to powerful models for researchers and developers.
The future of AI holds immense promise but requires careful and thoughtful governance.
""")
print("\n METHOD 1: Frequency-Based Summarization")
freq_summary, _ = frequency_based_summary(raw_text, num_sentences=4)
display_summary(raw_text, freq_summary, method_name="Frequency-Based")

print("\n METHOD 2: TF-IDF Summarization")
tfidf_sum, _ = tfidf_based_summary(raw_text, num_sentences=4)
display_summary(raw_text, tfidf_sum, method_name="TF-IDF")

print("\n🔹 ANALYTICS REPORT:")
analytics = analyze_text(raw_text, top_n=10)
display_analytics(analytics)

export_to_pdf(tfidf_sum, raw_text)
export_to_txt(tfidf_sum, raw_text)

print('Saved File ')

# input from pdf

pdf_summery = input_from_pdf("/content/sample_article.pdf")

# show TF_IDF Base Summery
print("\nMETHOD 2: TF-IDF Summarization")
tfidf_sum, _ = tfidf_based_summary(pdf_summery, num_sentences=6)
display_summary(pdf_summery, tfidf_sum, method_name="TF-IDF")

export_to_pdf(tfidf_sum, pdf_summery)
export_to_txt(tfidf_sum, pdf_summery)

print('saved file')





