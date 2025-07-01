"""
Test script for RAG PDF AI Agent
"""

import os
import sys
import tempfile
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.pdf_processor import PDFProcessor
from src.embeddings import EmbeddingManager
from src.vector_store import VectorStore
from src.rag_chain import RAGChain


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


def test_embeddings():
    """Test embedding functionality"""
    print("\nTesting Embeddings...")
    
    try:
        # Test HuggingFace embeddings (doesn't require API key)
        embedding_manager = EmbeddingManager(embedding_type="huggingface")
        print("✅ HuggingFace embeddings initialized successfully")
        
        # Test embedding generation
        test_query = "This is a test query"
        embedding = embedding_manager.embed_query(test_query)
        print(f"✅ Generated embedding with dimension: {len(embedding)}")
        
        return True
    except Exception as e:
        print(f"❌ Embeddings test failed: {e}")
        return False


def test_vector_store():
    """Test vector store functionality"""
    print("\nTesting Vector Store...")
    
    try:
        # Create embedding manager
        embedding_manager = EmbeddingManager(embedding_type="huggingface")
        
        # Create vector store
        vector_store = VectorStore(
            store_type="faiss",
            embedding_manager=embedding_manager,
            persist_directory="./test_data/vector_db"
        )
        print("✅ Vector Store initialized successfully")
        
        # Create sample documents
        from langchain.schema import Document
        documents = [
            Document(page_content="This is the first test document", metadata={"source": "test1"}),
            Document(page_content="This is the second test document", metadata={"source": "test2"}),
            Document(page_content="This is the third test document", metadata={"source": "test3"})
        ]
        
        # Create vector store from documents
        vector_store.create_vector_store(documents)
        print("✅ Vector store created with sample documents")
        
        # Test similarity search
        results = vector_store.similarity_search("test document", k=2)
        print(f"✅ Similarity search returned {len(results)} results")
        
        return True
    except Exception as e:
        print(f"❌ Vector Store test failed: {e}")
        return False


def test_rag_chain():
    """Test RAG chain functionality"""
    print("\nTesting RAG Chain...")
    
    # Check if OpenAI API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ OpenAI API key not found, skipping RAG chain test")
        return True
    
    try:
        # Create components
        embedding_manager = EmbeddingManager(embedding_type="openai")
        vector_store = VectorStore(
            store_type="faiss",
            embedding_manager=embedding_manager,
            persist_directory="./test_data/vector_db"
        )
        
        # Create sample documents
        from langchain.schema import Document
        documents = [
            Document(page_content="Python is a programming language", metadata={"source": "test1"}),
            Document(page_content="Machine learning is a subset of AI", metadata={"source": "test2"}),
            Document(page_content="RAG combines retrieval and generation", metadata={"source": "test3"})
        ]
        
        vector_store.create_vector_store(documents)
        
        # Create RAG chain
        rag_chain = RAGChain(vector_store=vector_store)
        print("✅ RAG Chain initialized successfully")
        
        # Test query
        response = rag_chain.query("What is Python?")
        print(f"✅ RAG query successful: {response['answer'][:100]}...")
        
        return True
    except Exception as e:
        print(f"❌ RAG Chain test failed: {e}")
        return False


def test_full_pipeline():
    """Test complete pipeline"""
    print("\nTesting Full Pipeline...")
    
    try:
        # Create sample PDF content (text only for testing)
        sample_content = """
        This is a sample PDF document for testing the RAG system.
        
        Chapter 1: Introduction
        This document contains information about artificial intelligence and machine learning.
        
        Chapter 2: Machine Learning
        Machine learning is a method of data analysis that automates analytical model building.
        
        Chapter 3: Deep Learning
        Deep learning is part of a broader family of machine learning methods.
        """
        
        # Test PDF processor
        processor = PDFProcessor()
        documents = processor.create_documents(sample_content, {"source": "sample.pdf"})
        
        # Test embeddings
        embedding_manager = EmbeddingManager(embedding_type="huggingface")
        
        # Test vector store
        vector_store = VectorStore(
            store_type="faiss",
            embedding_manager=embedding_manager,
            persist_directory="./test_data/vector_db_full"
        )
        vector_store.create_vector_store(documents)
        
        # Test similarity search
        results = vector_store.similarity_search("machine learning", k=2)
        print(f"✅ Full pipeline test successful: found {len(results)} relevant documents")
        
        return True
    except Exception as e:
        print(f"❌ Full pipeline test failed: {e}")
        return False


def cleanup_test_data():
    """Clean up test data"""
    import shutil
    
    test_dirs = ["./test_data"]
    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
            print(f"🧹 Cleaned up {test_dir}")


def main():
    """Run all tests"""
    print("🚀 Starting RAG PDF AI Agent Tests\n")
    
    tests = [
        test_pdf_processor,
        test_embeddings,
        test_vector_store,
        test_rag_chain,
        test_full_pipeline
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    # Cleanup
    cleanup_test_data()
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
