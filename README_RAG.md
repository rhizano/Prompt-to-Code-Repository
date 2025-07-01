# RAG PDF AI Agent

🤖 **AI Agent untuk Retrieval Augmented Generation pada file PDF**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-green.svg)](https://langchain.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red.svg)](https://streamlit.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-orange.svg)](https://fastapi.tiangolo.com)

## 🚀 Quick Start

```bash
# Demo tanpa setup
git clone https://github.com/rhizano/Prompt-to-Code-Repository.git
cd Prompt-to-Code-Repository/rag-pdf
python demo.py
```

**Atau langsung jalankan aplikasi:**
```bash
pip install -r requirements.txt
streamlit run app.py
```

📖 **[Panduan Lengkap →](QUICKSTART.md)**

## ✨ Fitur Utama

- 📄 **Upload & Parse PDF** - Support multiple file formats
- 🧠 **AI-Powered Q&A** - Tanya jawab cerdas dengan dokumen
- 🔍 **Semantic Search** - Pencarian berdasarkan makna, bukan kata kunci
- 💬 **Chat Interface** - Interface chat yang user-friendly
- 🚀 **REST API** - Integrasi mudah dengan aplikasi lain
- 🐳 **Docker Ready** - Deploy dengan Docker
- 🔒 **No Lock-in** - Support multiple LLM providers

## 🛠️ Teknologi

| Komponen | Teknologi |
|----------|-----------|
| **Framework AI** | LangChain |
| **LLM** | OpenAI GPT, HuggingFace |
| **Vector DB** | FAISS, ChromaDB |
| **Web UI** | Streamlit |
| **API** | FastAPI |
| **PDF Processing** | PyPDF2 |
| **Embeddings** | OpenAI, Sentence Transformers |

## 📱 Screenshots

### Web Interface
```
┌─ RAG PDF AI Agent ────────────────────────────┐
│  📤 Upload PDF    💬 Chat    📋 History      │
├───────────────────────────────────────────────┤
│                                               │
│  [Drag & Drop PDF files here]                │
│                                               │
│  ✅ document1.pdf - 15 chunks processed      │
│  ✅ document2.pdf - 23 chunks processed      │
│                                               │
│  💬 Ask: "What is the main topic?"           │
│  🤖 Answer: "Based on the documents..."      │
│                                               │
└───────────────────────────────────────────────┘
```

## 🔧 Installation

### Method 1: Automated Setup
```bash
# Windows
setup.bat

# Linux/Mac  
bash setup.sh
```

### Method 2: Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup environment
cp .env.example .env
# Edit .env and add your API keys

# 3. Run application
streamlit run app.py
```

### Method 3: Docker
```bash
docker-compose up --build
```

## 🧪 Demo & Testing

### Live Demo
```bash
python demo.py
```

### Run Tests
```bash
# Basic test (no API keys required)
python test_basic.py

# Full test (requires OpenAI API key)
python test_rag.py
```

## 📚 Usage Examples

### Web Interface
1. Buka http://localhost:8501
2. Upload PDF di tab "Upload PDF"
3. Tanya jawab di tab "Chat dengan PDF"

### API Usage
```python
import requests

# Upload PDF
files = {'file': open('document.pdf', 'rb')}
response = requests.post('http://localhost:8000/upload', files=files)

# Query
data = {'question': 'Apa isi dokumen ini?'}
response = requests.post('http://localhost:8000/query', json=data)
print(response.json()['answer'])
```

### Python Integration
```python
from src.pdf_processor import PDFProcessor
from src.rag_chain import RAGChain

# Process PDF
processor = PDFProcessor()
documents = processor.process_pdf_to_documents('document.pdf')

# Create RAG chain
rag = RAGChain(vector_store)
response = rag.query("Apa topik utama dokumen?")
print(response['answer'])
```

## 🏗️ Arsitektur

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   PDF File  │───▶│ PDF Parser  │───▶│ Text Chunks │
└─────────────┘    └─────────────┘    └─────────────┘
                                               │
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Answer    │◀───│ LLM (GPT)   │◀───│ Embeddings  │
└─────────────┘    └─────────────┘    └─────────────┘
       ▲                                       │
       │           ┌─────────────┐    ┌─────────────┐
       └───────────│  RAG Chain  │◀───│ Vector DB   │
                   └─────────────┘    └─────────────┘
                          ▲                   │
                   ┌─────────────┐           │
                   │ User Query  │───────────┘
                   └─────────────┘
```

## 📁 Struktur Project

```
rag-pdf/
├── 🚀 app.py              # Streamlit web app
├── 🌐 api.py              # FastAPI REST API  
├── 📋 requirements.txt    # Dependencies
├── 🐳 Dockerfile         # Docker configuration
├── 📖 README.md          # This file
├── ⚡ QUICKSTART.md      # Quick start guide
├── 🧪 demo.py            # Demo script
├── src/                  # Core modules
│   ├── pdf_processor.py  # PDF handling
│   ├── embeddings.py     # Text embeddings
│   ├── vector_store.py   # Vector database
│   └── rag_chain.py      # RAG pipeline
└── data/                 # Data storage
    ├── uploads/          # Uploaded PDFs
    └── vector_db/        # Vector embeddings
```

## 🔒 Environment Variables

```bash
# Required for OpenAI models
OPENAI_API_KEY=sk-...

# Optional for HuggingFace models  
HUGGINGFACE_API_TOKEN=hf_...
```

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py --server.port 8501
python api.py  # FastAPI on port 8000
```

### Production (Docker)
```bash
docker-compose up -d
```

### Cloud Deployment
- **Streamlit Cloud**: Push to GitHub, deploy dari dashboard
- **Heroku**: Gunakan `Dockerfile` dan `docker-compose.yml`
- **AWS/GCP**: Deploy dengan container services

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push branch: `git push origin feature-name`
5. Submit Pull Request

## 📄 License

MIT License - bebas digunakan untuk project komersial dan non-komersial.

## 📞 Support

- 📚 **Dokumentasi**: [QUICKSTART.md](QUICKSTART.md) | [API_DOCS.md](API_DOCS.md)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/rhizano/Prompt-to-Code-Repository/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/rhizano/Prompt-to-Code-Repository/discussions)
- 📧 **Contact**: [@rhizano](https://github.com/rhizano)

---

⭐ **Star this repo if helpful!** | 🔗 **[GitHub Repository](https://github.com/rhizano/Prompt-to-Code-Repository)**
