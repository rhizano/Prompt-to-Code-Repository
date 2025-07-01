"""
Demo script untuk RAG PDF AI Agent
Menunjukkan penggunaan basic functionality
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def demo_pdf_processing():
    """Demo PDF processing capabilities"""
    print("🚀 Demo: PDF Processing")
    print("=" * 50)
    
    try:
        from src.pdf_processor import PDFProcessor
        
        # Initialize processor
        processor = PDFProcessor()
        print("✅ PDF Processor initialized")
        
        # Sample text (simulating PDF content)
        sample_text = """
        Artificial Intelligence (AI) adalah teknologi yang memungkinkan mesin untuk meniru kecerdasan manusia.
        Machine Learning adalah subset dari AI yang fokus pada algoritma yang dapat belajar dari data.
        Deep Learning adalah subset dari Machine Learning yang menggunakan neural networks dengan banyak layer.
        
        Natural Language Processing (NLP) adalah cabang AI yang berkaitan dengan interaksi antara komputer dan bahasa manusia.
        Computer Vision adalah bidang AI yang memungkinkan komputer untuk menginterpretasi dan memahami dunia visual.
        
        Retrieval Augmented Generation (RAG) adalah teknik yang menggabungkan retrieval dan generation untuk menghasilkan respons yang lebih akurat.
        """
        
        # Create documents
        documents = processor.create_documents(sample_text, {"source": "demo.pdf"})
        
        print(f"✅ Created {len(documents)} document chunks")
        print("\n📄 Sample Document Chunks:")
        
        for i, doc in enumerate(documents[:3], 1):
            print(f"\nChunk {i}:")
            print(f"Content: {doc.page_content[:100]}...")
            print(f"Metadata: {doc.metadata}")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False


def demo_basic_workflow():
    """Demo basic RAG workflow without external dependencies"""
    print("\n🚀 Demo: Basic RAG Workflow")
    print("=" * 50)
    
    try:
        from src.pdf_processor import PDFProcessor
        
        # Step 1: Process document
        processor = PDFProcessor()
        
        # Sample FAQ content
        faq_content = """
        Q: Apa itu Artificial Intelligence?
        A: Artificial Intelligence (AI) adalah teknologi yang memungkinkan mesin untuk meniru kemampuan kognitif manusia seperti belajar, reasoning, dan problem solving.
        
        Q: Apa perbedaan antara AI, Machine Learning, dan Deep Learning?
        A: AI adalah konsep yang lebih luas, Machine Learning adalah subset dari AI yang fokus pada algoritma yang belajar dari data, sedangkan Deep Learning adalah subset dari ML yang menggunakan neural networks.
        
        Q: Apa itu RAG?
        A: Retrieval Augmented Generation (RAG) adalah teknik yang menggabungkan pencarian informasi (retrieval) dengan generasi teks untuk menghasilkan jawaban yang lebih akurat dan kontekstual.
        
        Q: Bagaimana cara kerja RAG?
        A: RAG bekerja dengan mencari dokumen atau informasi yang relevan terlebih dahulu, kemudian menggunakan informasi tersebut untuk menghasilkan jawaban yang lebih baik.
        """
        
        documents = processor.create_documents(faq_content, {"source": "faq.pdf"})
        
        print(f"✅ Processed document into {len(documents)} chunks")
        
        # Step 2: Simulate simple retrieval
        query = "Apa itu RAG?"
        print(f"\n🔍 Query: {query}")
        
        # Simple keyword-based retrieval simulation
        relevant_docs = []
        query_words = query.lower().split()
        
        for doc in documents:
            content_lower = doc.page_content.lower()
            if any(word in content_lower for word in query_words):
                relevant_docs.append(doc)
        
        print(f"✅ Found {len(relevant_docs)} relevant documents")
        
        # Step 3: Show retrieved context
        print("\n📚 Retrieved Context:")
        for i, doc in enumerate(relevant_docs[:2], 1):
            print(f"\nRelevant Document {i}:")
            print(f"Content: {doc.page_content[:200]}...")
        
        # Step 4: Simple response generation (without LLM)
        print(f"\n🤖 Simulated Response:")
        print("Berdasarkan dokumen yang tersedia:")
        for doc in relevant_docs[:1]:
            if "RAG" in doc.page_content:
                # Extract answer from FAQ format
                lines = doc.page_content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip().startswith('A: ') and 'RAG' in line:
                        print(f"✨ {line.strip()[3:]}")
                        break
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False


def demo_project_structure():
    """Demo project structure and files"""
    print("\n🚀 Demo: Project Structure")
    print("=" * 50)
    
    try:
        project_root = Path(__file__).parent
        
        print("📁 Project Structure:")
        
        # Show main files
        main_files = [
            "app.py",
            "api.py", 
            "requirements.txt",
            "README.md",
            ".env.example"
        ]
        
        for file in main_files:
            filepath = project_root / file
            if filepath.exists():
                size = filepath.stat().st_size
                print(f"├── {file} ({size:,} bytes)")
            else:
                print(f"├── {file} (missing)")
        
        # Show src directory
        src_dir = project_root / "src"
        if src_dir.exists():
            print("├── src/")
            for file in src_dir.glob("*.py"):
                size = file.stat().st_size
                print(f"│   ├── {file.name} ({size:,} bytes)")
        
        # Show data directory structure
        data_dir = project_root / "data"
        print("└── data/")
        print("    ├── uploads/ (for PDF files)")
        print("    └── vector_db/ (for vector storage)")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False


def main():
    """Run all demos"""
    print("🎉 RAG PDF AI Agent - Demo")
    print("=" * 60)
    print("Demonstrating core functionality without external API dependencies")
    print()
    
    demos = [
        demo_pdf_processing,
        demo_basic_workflow,
        demo_project_structure
    ]
    
    success_count = 0
    
    for demo in demos:
        if demo():
            success_count += 1
        print()
    
    print("=" * 60)
    print(f"✅ Demo completed: {success_count}/{len(demos)} sections successful")
    
    if success_count == len(demos):
        print("🎉 All demos completed successfully!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Setup environment: cp .env.example .env")
        print("3. Add your API keys to .env file")
        print("4. Run the app: streamlit run app.py")
    else:
        print("⚠️ Some demos failed. Please check the error messages above.")


if __name__ == "__main__":
    main()
