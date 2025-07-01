#!/bin/bash

# RAG PDF AI Agent Setup Script

echo "🚀 Setting up RAG PDF AI Agent..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "⚡ Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📋 Installing requirements..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/uploads
mkdir -p data/vector_db

# Copy environment file
echo "🔑 Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo "⚠️ Please edit .env file and add your API keys"
else
    echo "✅ .env file already exists"
fi

# Run tests
echo "🧪 Running tests..."
python test_rag.py

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Edit .env file and add your API keys"
    echo "2. Run the application:"
    echo "   - Streamlit: streamlit run app.py"
    echo "   - FastAPI: python api.py"
    echo "   - Docker: docker-compose up"
else
    echo "❌ Some tests failed. Please check the output above."
fi
