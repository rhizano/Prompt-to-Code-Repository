@echo off
REM RAG PDF AI Agent Setup Script for Windows

echo 🚀 Setting up RAG PDF AI Agent...

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo ⚡ Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📋 Installing requirements...
pip install -r requirements.txt

REM Create necessary directories
echo 📁 Creating directories...
if not exist "data\uploads" mkdir data\uploads
if not exist "data\vector_db" mkdir data\vector_db

REM Copy environment file
echo 🔑 Setting up environment...
if not exist ".env" (
    copy .env.example .env
    echo ✅ Created .env file from template
    echo ⚠️ Please edit .env file and add your API keys
) else (
    echo ✅ .env file already exists
)

REM Run tests
echo 🧪 Running tests...
python test_rag.py

REM Check if tests passed
if %ERRORLEVEL% == 0 (
    echo ✅ All tests passed!
    echo.
    echo 🎉 Setup completed successfully!
    echo.
    echo Next steps:
    echo 1. Edit .env file and add your API keys
    echo 2. Run the application:
    echo    - Streamlit: streamlit run app.py
    echo    - FastAPI: python api.py
    echo    - Docker: docker-compose up
) else (
    echo ❌ Some tests failed. Please check the output above.
)

pause
