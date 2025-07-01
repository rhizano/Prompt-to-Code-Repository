"""
Simple test script for RAG PDF AI Agent - Basic functionality only
"""

import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.pdf_processor import PDFProcessor


def test_pdf_processor():
    """Test PDF processor functionality"""
    print("Testing PDF Processor...")
    
    try:
        processor = PDFProcessor()
        print("✅ PDF Processor initialized successfully")
        
        # Test with sample text
        sample_text = "This is a test document. " * 100
        documents = processor.create_documents(sample_text, {"source": "test"})
        print(f"✅ Created {len(documents)} documents from sample text")
        
        return True
    except Exception as e:
        print(f"❌ PDF Processor test failed: {e}")
        return False


def test_basic_imports():
    """Test basic imports"""
    print("Testing basic imports...")
    
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain.schema import Document
        print("✅ Basic LangChain imports successful")
        
        return True
    except Exception as e:
        print(f"❌ Basic imports test failed: {e}")
        return False


def main():
    """Run basic tests"""
    print("🚀 Starting Basic RAG PDF AI Agent Tests\n")
    
    tests = [
        test_basic_imports,
        test_pdf_processor
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Basic tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
