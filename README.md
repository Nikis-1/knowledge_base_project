# Knowledge Base Search Engine (Multi-Document RAG)

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](#)

---

## 🌟 Project Overview
This project implements a **Retrieval-Augmented Generation (RAG)** pipeline using the **Gemini API** to create a multi-document, multi-format knowledge base search engine. Users can upload multiple PDF (`.pdf`) and text (`.txt`) documents, and the system synthesizes **concise, context-aware answers** to user queries based only on the content of the indexed documents.

The backend is built with **Python/Flask**, utilizing the `google-genai` library for all LLM and embedding operations.

---

## ✨ Features
- **Multi-Document Indexing**: Upload and query multiple documents simultaneously.
- **Multi-Format Support**: Ingests both PDF (`.pdf`) and plain text (`.txt`) files.
- **Persistent State**: Uses Flask sessions to remember indexed files until cleared.
- **LLM-Based RAG**: Leverages `text-embedding-004` for retrieval and `gemini-2.0-flash` for high-quality answer synthesis.
- **Optimized Retrieval**: Retrieves the **Top 3 most relevant text chunks** across all documents for improved answer accuracy.

---

## ⚙️ Prerequisites
Before running the application, you need:

- **Python 3.8+**
- **Gemini API Key** (from [Google AI Studio](https://aistudio.google.com/))

---

## 🚀 Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Nikis-1/knowledge_base_search_engine
cd knowledge_base_search_engine
```

### 2. Create and Activate Virtual Environment
**Windows:**
```bash
python -m venv kb_env
.\kb_env\Scripts ctivate
```

**macOS/Linux:**
```bash
python -m venv kb_env
source kb_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install Flask Werkzeug pypdf scikit-learn numpy google-genai
```

### 4. Run the Application
From the project root directory:
```bash
cd ..
python -m backend.app
```

Open your browser at: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 🌐 Usage

- **Upload**: Click “Choose Files” to select `.pdf` or `.txt` files, then click **Index & Upload**. Uploaded files appear in the “Current Indexed Knowledge Base.”  
- **Query**: Type a question related to the uploaded documents in “Ask a Question” and click **Search**.  
- **Clear Context**: Click **Clear All Context** to remove all indexed documents from the RAG pipeline.

---

## 📂 Project Structure
```graphql
knowledge_base_project/
├── backend/
│   ├── templates/
│   │   └── index.html      # Frontend interface
│   ├── app.py              # Main Flask app: routing, sessions, uploads
│   ├── main.py             # Flask backend query endpoint handler
|   ├── test_query.py       # RAG console test script
│   ├── pdf_loader.py       # File reading (.pdf/.txt) and chunking
│   └── vector_store.py     # Multi-Document RAG engine (embedding, retrieval, synthesis)
├── kb_env/                 # Python Virtual Environment
└── README.md               # This file
```

---

## 🔧 Technical Deep Dive (RAG Pipeline)
| Component | Technology/Method | Role |
|------------|------------------|------|
| Ingestion | pypdf, Python I/O | Reads text from files and splits into semantically rich chunks. |
| Embedding | text-embedding-004 | Converts text chunks and queries into dense vectors. |
| Vector Store | In-Memory (NumPy/Dict) | Stores vectors for fast lookup. |
| Retrieval | scikit-learn (cosine similarity) | Finds Top 3 chunks most relevant to the question. |
| Generation | gemini-2.0-flash | Synthesizes concise answers using retrieved chunks as context. |

---

## [Demo Video](https://drive.google.com/file/d/1Cqqfx_nbGAoET8vN1Zf3Z-VLBo4vtMV-/view?usp=sharing)

---

## 📝 Author
**Nikita Sanganeria** nikitasanganeria1@gmail.com

---

## 📄 License
**MIT License**
