# 📚 AI PDF Study Assistant

An AI-powered web application that helps students study from PDF documents.

Users can upload a PDF and use AI-powered tools to understand, summarize, and revise the material.

## ✨ Features

### 📄 PDF Upload
Upload a PDF document and extract its text for analysis.

### 💬 Ask Questions
Ask questions about the uploaded PDF and receive answers based only on the document content.

### 📝 Summary
Generate a concise study summary containing:
- Important concepts
- Definitions
- Key facts
- Headings
- Bullet points

### 🧠 Flashcards
Generate study flashcards from important information in the PDF.

### 💡 Explain
Get difficult concepts explained in simpler language with examples.

### 📖 Exam Notes
Generate concise revision notes containing important:
- Definitions
- Concepts
- Facts
- Information to memorize

### ❓ MCQ Generator
Generate multiple-choice questions with:
- 4 answer options
- Correct answers
- Explanations
- Adjustable difficulty

## 🛠️ Technologies

- Python
- Flask
- HTML
- CSS
- JavaScript
- Scikit-learn
- TF-IDF
- OpenRouter API
- Markdown
- PyMuPDF

## 🧩 How It Works

The application follows a Retrieval-Augmented Generation (RAG)-style workflow.

```text
PDF Upload
    ↓
PDF Text Extraction
    ↓
Text Chunking
    ↓
TF-IDF Embeddings
    ↓
Vector Similarity Search
    ↓
Relevant PDF Context
    ↓
OpenRouter AI Model
    ↓
Study Response