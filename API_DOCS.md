# Dokumentasi API

## Deskripsi
REST API untuk RAG PDF AI Agent yang memungkinkan integrasi dengan aplikasi lain.

## Base URL
```
http://localhost:8000
```

## Authentication
Saat ini tidak diperlukan authentication. Untuk production, disarankan menambahkan API key authentication.

## Endpoints

### 1. Health Check
**GET** `/health`

Mengecek status kesehatan API.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### 2. Upload PDF
**POST** `/upload`

Upload dan proses file PDF.

**Headers:**
- `Content-Type: multipart/form-data`

**Body:**
- `file`: PDF file (required)

**Response:**
```json
{
  "message": "File uploaded and processed successfully",
  "filename": "document.pdf",
  "chunks": 15,
  "size": 1048576
}
```

### 3. Query Documents
**POST** `/query`

Query dokumen menggunakan RAG.

**Headers:**
- `Content-Type: application/json`

**Body:**
```json
{
  "question": "What is the main topic of the document?",
  "k": 4
}
```

**Response:**
```json
{
  "answer": "The main topic is artificial intelligence and machine learning.",
  "sources": [
    {
      "content": "This document discusses AI and ML concepts...",
      "metadata": {
        "source": "document.pdf",
        "chunk_id": 0
      }
    }
  ],
  "question": "What is the main topic of the document?"
}
```

### 4. Chat with History
**POST** `/chat`

Chat dengan dokumen dengan riwayat percakapan.

**Headers:**
- `Content-Type: application/json`

**Body:**
```json
{
  "question": "Can you explain more about this topic?",
  "chat_history": [
    {
      "question": "What is AI?",
      "answer": "AI is artificial intelligence..."
    }
  ]
}
```

**Response:**
```json
{
  "answer": "Based on our previous discussion about AI...",
  "sources": [...],
  "chat_history": [
    {
      "question": "What is AI?",
      "answer": "AI is artificial intelligence..."
    },
    {
      "question": "Can you explain more about this topic?",
      "answer": "Based on our previous discussion about AI..."
    }
  ]
}
```

### 5. Get Status
**GET** `/status`

Mendapatkan status sistem.

**Response:**
```json
{
  "status": "active",
  "documents_count": 50,
  "embedding_model": "all-MiniLM-L6-v2",
  "vector_store_type": "faiss"
}
```

### 6. List Documents
**GET** `/documents`

Mendapatkan informasi dokumen yang telah diproses.

**Response:**
```json
{
  "document_count": 50,
  "store_info": {
    "type": "faiss",
    "persist_directory": "./data/vector_db",
    "document_count": 50,
    "embedding_info": {
      "type": "huggingface",
      "model_name": "sentence-transformers/all-MiniLM-L6-v2",
      "dimension": 384
    }
  }
}
```

### 7. Clear Documents
**DELETE** `/documents`

Menghapus semua dokumen dari vector store.

**Response:**
```json
{
  "message": "All documents cleared successfully"
}
```

### 8. Find Similar Documents
**GET** `/similar?query={query}&k={k}`

Mencari dokumen yang mirip tanpa generate jawaban.

**Parameters:**
- `query`: Search query (required)
- `k`: Number of documents to return (optional, default: 4)

**Response:**
```json
[
  {
    "content": "This section discusses machine learning algorithms...",
    "metadata": {
      "source": "document.pdf",
      "chunk_id": 5
    },
    "similarity_score": 0.85
  }
]
```

## Error Responses

Semua error response menggunakan format:
```json
{
  "detail": "Error message description"
}
```

**HTTP Status Codes:**
- `400`: Bad Request (invalid input)
- `500`: Internal Server Error
- `422`: Validation Error

## Example Usage

### Python
```python
import requests

# Upload PDF
with open('document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/upload',
        files={'file': f}
    )

# Query
response = requests.post(
    'http://localhost:8000/query',
    json={'question': 'What is this document about?'}
)
```

### cURL
```bash
# Upload PDF
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"

# Query
curl -X POST "http://localhost:8000/query" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
```

### JavaScript
```javascript
// Upload PDF
const formData = new FormData();
formData.append('file', pdfFile);

fetch('http://localhost:8000/upload', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));

// Query
fetch('http://localhost:8000/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    question: 'What is this document about?'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## Rate Limiting
Saat ini tidak ada rate limiting. Untuk production, disarankan mengimplementasi rate limiting untuk mencegah abuse.

## Deployment
Untuk deployment production:
1. Gunakan reverse proxy (nginx)
2. Setup HTTPS
3. Implementasi authentication
4. Setup monitoring dan logging
5. Gunakan production-grade database untuk vector storage
