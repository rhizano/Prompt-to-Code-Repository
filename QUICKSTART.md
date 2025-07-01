# Quick Start Guide - RAG PDF AI Agent

## 🚀 Get Started in 5 Minutes

### Option 1: Quick Demo (No Setup Required)
```bash
# Clone and demo
git clone https://github.com/rhizano/Prompt-to-Code-Repository.git
cd Prompt-to-Code-Repository/rag-pdf
python demo.py
```

### Option 2: Full Application Setup

#### Step 1: Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

#### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your API keys:
# OPENAI_API_KEY=your_openai_api_key_here
# HUGGINGFACE_API_TOKEN=your_huggingface_token_here
```

#### Step 4: Run Application
```bash
# Option A: Streamlit Web Interface
streamlit run app.py

# Option B: FastAPI REST API
python api.py
```

## 🛠️ Advanced Setup

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Access applications:
# Streamlit: http://localhost:8501
# FastAPI: http://localhost:8001
```

### Manual Installation
```bash
# If automated setup fails, run manually:
# Windows:
setup.bat

# Linux/Mac:
bash setup.sh
```

## 🧪 Testing

### Basic Functionality Test
```bash
python test_basic.py
```

### Full Feature Test (requires API keys)
```bash
python test_rag.py
```

## 📖 Usage Examples

### Web Interface
1. Open http://localhost:8501
2. Upload PDF files in "Upload PDF" tab
3. Ask questions in "Chat dengan PDF" tab

### API Usage
```python
import requests

# Upload PDF
with open('document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/upload',
        files={'file': f}
    )

# Query document
response = requests.post(
    'http://localhost:8000/query',
    json={'question': 'What is this document about?'}
)
print(response.json()['answer'])
```

## 🔧 Troubleshooting

### Common Issues

**1. "Could not import sentence_transformers"**
```bash
pip install sentence-transformers torch
```

**2. "OpenAI API key not found"**
- Add your OpenAI API key to `.env` file
- Or use HuggingFace embeddings (no API key required)

**3. "Module not found" errors**
```bash
pip install -r requirements.txt
```

**4. Port already in use**
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Getting API Keys

**OpenAI API Key:**
1. Visit https://platform.openai.com/api-keys
2. Create new API key
3. Add to `.env` file

**HuggingFace Token (Optional):**
1. Visit https://huggingface.co/settings/tokens
2. Create new token
3. Add to `.env` file

## 📚 Documentation

- [API Documentation](API_DOCS.md)
- [Full README](README.md)
- [Docker Guide](docker-compose.yml)

## 🆘 Support

If you encounter issues:
1. Check this troubleshooting guide
2. Run `python demo.py` to verify basic functionality
3. Check GitHub Issues: https://github.com/rhizano/Prompt-to-Code-Repository/issues
4. Create new issue with error details
