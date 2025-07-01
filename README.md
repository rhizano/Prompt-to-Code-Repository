# Prompt-to-Code-Repository

Collection of AI-powered coding projects and experiments.

## Projects

### RAG PDF AI Agent

AI Agent untuk melakukan Retrieval Augmented Generation (RAG) pada file PDF menggunakan LangChain dan Python. Project ini memungkinkan users untuk mengupload file PDF dan mengajukan pertanyaan tentang konten dalam file tersebut.

#### Fitur
- Upload dan parsing file PDF
- Text chunking dan embedding
- Vector database untuk pencarian semantik
- RAG pipeline dengan LangChain
- Interface web dengan Streamlit
- Support untuk multiple PDF files

#### Teknologi yang Digunakan
- **Python 3.8+**
- **LangChain** - Framework untuk LLM applications
- **OpenAI GPT** - Large Language Model
- **FAISS/ChromaDB** - Vector database
- **Streamlit** - Web interface
- **PyPDF2** - PDF processing
- **Sentence Transformers** - Text embeddings

#### Setup dan Instalasi

##### 1. Clone Repository
```bash
git clone https://github.com/rhizano/Prompt-to-Code-Repository.git
cd Prompt-to-Code-Repository/rag-pdf
```

##### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

##### 3. Setup Environment Variables
```bash
cp .env.example .env
```
Edit file `.env` dan tambahkan API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
HUGGINGFACE_API_TOKEN=your_huggingface_token_here
```

##### 4. Jalankan Aplikasi
```bash
streamlit run app.py
```

#### Struktur Project
```
rag-pdf/
├── app.py                 # Main Streamlit application
├── src/
│   ├── __init__.py
│   ├── pdf_processor.py   # PDF processing utilities
│   ├── embeddings.py      # Text embedding functions
│   ├── vector_store.py    # Vector database operations
│   └── rag_chain.py       # RAG pipeline implementation
├── data/
│   ├── uploads/           # Uploaded PDF files
│   └── vector_db/         # Vector database storage
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
```

#### Cara Penggunaan

1. **Upload PDF**: Upload file PDF melalui interface web
2. **Processing**: Sistem akan memproses dan membuat embeddings
3. **Query**: Ajukan pertanyaan tentang konten PDF
4. **Response**: Dapatkan jawaban berdasarkan konten PDF

#### API Endpoints

Jika ingin menggunakan sebagai API:
- `POST /upload` - Upload PDF file
- `POST /query` - Query terhadap PDF content
- `GET /documents` - List uploaded documents

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - [@rhizano](https://github.com/rhizano)

Project Link: [https://github.com/rhizano/Prompt-to-Code-Repository](https://github.com/rhizano/Prompt-to-Code-Repository)
