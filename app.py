"""
RAG PDF AI Agent - Streamlit Application
Main application for PDF RAG system with web interface
"""

import streamlit as st
import os
import tempfile
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import custom modules
from src.pdf_processor import PDFProcessor
from src.embeddings import EmbeddingManager
from src.vector_store import VectorStore
from src.rag_chain import RAGChain


# Page configuration
st.set_page_config(
    page_title="RAG PDF AI Agent",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #333;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 5px solid #28a745;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 5px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    if 'rag_chain' not in st.session_state:
        st.session_state.rag_chain = None
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = []
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []


def setup_rag_system(embedding_type="huggingface", vector_store_type="faiss"):
    """Setup the RAG system components"""
    try:
        # Initialize embedding manager
        embedding_manager = EmbeddingManager(embedding_type=embedding_type)
        
        # Initialize vector store
        vector_store = VectorStore(
            store_type=vector_store_type,
            embedding_manager=embedding_manager
        )
        
        # Try to load existing vector store
        vector_store.load_vector_store()
        
        return embedding_manager, vector_store
    except Exception as e:
        st.error(f"Error setting up RAG system: {str(e)}")
        return None, None


def process_uploaded_files(uploaded_files, pdf_processor, vector_store):
    """Process uploaded PDF files"""
    processed_docs = []
    
    for uploaded_file in uploaded_files:
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                tmp_file_path = tmp_file.name
            
            # Process PDF
            documents = pdf_processor.process_pdf_to_documents(
                tmp_file_path, 
                uploaded_file.name
            )
            
            processed_docs.extend(documents)
            
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
            st.session_state.processed_files.append({
                "name": uploaded_file.name,
                "size": uploaded_file.size,
                "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "chunks": len(documents)
            })
            
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
    
    if processed_docs:
        # Add documents to vector store
        try:
            vector_store.add_documents(processed_docs)
            vector_store.save_vector_store()
            return True
        except Exception as e:
            st.error(f"Error adding documents to vector store: {str(e)}")
            return False
    
    return False


def main():
    """Main application function"""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">📚 RAG PDF AI Agent</h1>', unsafe_allow_html=True)
    st.markdown("**Artificial Intelligence Agent untuk Retrieval Augmented Generation pada file PDF**")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Konfigurasi")
        
        # API Key check
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            st.success("✅ OpenAI API Key terdeteksi")
        else:
            st.warning("⚠️ OpenAI API Key tidak ditemukan")
            st.info("Gunakan HuggingFace embeddings sebagai alternatif")
        
        # Model selection
        st.subheader("Model Configuration")
        
        embedding_type = st.selectbox(
            "Embedding Model",
            ["huggingface", "openai"],
            index=0 if not openai_key else 1
        )
        
        vector_store_type = st.selectbox(
            "Vector Store",
            ["faiss", "chroma"],
            index=0
        )
        
        llm_model = st.selectbox(
            "Language Model",
            ["gpt-3.5-turbo", "gpt-4", "text-davinci-003"],
            index=0
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1
        )
        
        # System info
        st.subheader("📊 Status Sistem")
        if st.session_state.processed_files:
            st.info(f"📄 {len(st.session_state.processed_files)} file diproses")
            if st.session_state.vector_store:
                doc_count = st.session_state.vector_store.get_document_count()
                st.info(f"🗂️ {doc_count} dokumen dalam database")
        else:
            st.info("Belum ada file yang diproses")
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📤 Upload PDF", "💬 Chat dengan PDF", "📋 Riwayat File"])
    
    with tab1:
        st.markdown('<h2 class="sub-header">Upload dan Proses PDF</h2>', unsafe_allow_html=True)
        
        uploaded_files = st.file_uploader(
            "Pilih file PDF",
            type=["pdf"],
            accept_multiple_files=True,
            help="Upload satu atau beberapa file PDF untuk diproses"
        )
        
        if uploaded_files:
            st.info(f"📄 {len(uploaded_files)} file dipilih")
            
            # Show file details
            for file in uploaded_files:
                st.write(f"- **{file.name}** ({file.size:,} bytes)")
            
            if st.button("🚀 Proses File", type="primary"):
                with st.spinner("Memproses file PDF..."):
                    # Setup RAG system if not already done
                    if st.session_state.vector_store is None:
                        embedding_manager, vector_store = setup_rag_system(
                            embedding_type, vector_store_type
                        )
                        if vector_store:
                            st.session_state.vector_store = vector_store
                            st.session_state.embedding_manager = embedding_manager
                    
                    if st.session_state.vector_store:
                        # Process files
                        pdf_processor = PDFProcessor()
                        success = process_uploaded_files(
                            uploaded_files, 
                            pdf_processor, 
                            st.session_state.vector_store
                        )
                        
                        if success:
                            st.success("✅ File berhasil diproses dan ditambahkan ke database!")
                            st.rerun()
                        else:
                            st.error("❌ Gagal memproses file")
    
    with tab2:
        st.markdown('<h2 class="sub-header">Chat dengan Dokumen PDF</h2>', unsafe_allow_html=True)
        
        if not st.session_state.processed_files:
            st.info("📄 Upload file PDF terlebih dahulu untuk mulai chat")
        else:
            # Initialize RAG chain if not done
            if st.session_state.rag_chain is None and st.session_state.vector_store:
                try:
                    if embedding_type == "openai" and not openai_key:
                        st.error("OpenAI API Key diperlukan untuk menggunakan OpenAI models")
                    else:
                        with st.spinner("Inisialisasi AI agent..."):
                            rag_chain = RAGChain(
                                vector_store=st.session_state.vector_store,
                                model_name=llm_model,
                                temperature=temperature
                            )
                            st.session_state.rag_chain = rag_chain
                            st.success("✅ AI Agent siap!")
                except Exception as e:
                    st.error(f"Error initializing RAG chain: {str(e)}")
            
            if st.session_state.rag_chain:
                # Chat interface
                user_question = st.text_input(
                    "💬 Ajukan pertanyaan tentang dokumen:",
                    placeholder="Contoh: Apa isi utama dari dokumen ini?"
                )
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    ask_button = st.button("📨 Tanya", type="primary")
                with col2:
                    clear_history = st.button("🗑️ Hapus Riwayat")
                
                if clear_history:
                    st.session_state.chat_history = []
                    st.rerun()
                
                if ask_button and user_question:
                    with st.spinner("🤔 AI sedang berpikir..."):
                        try:
                            response = st.session_state.rag_chain.chat_with_history(
                                user_question,
                                st.session_state.chat_history
                            )
                            
                            st.session_state.chat_history = response["chat_history"]
                            
                            # Display answer
                            st.markdown("### 🤖 Jawaban AI:")
                            st.markdown(f'<div class="success-box">{response["answer"]}</div>', 
                                      unsafe_allow_html=True)
                            
                            # Display source documents
                            with st.expander("📚 Sumber Dokumen"):
                                for i, doc in enumerate(response["source_documents"]):
                                    st.markdown(f"**Sumber {i+1}:**")
                                    st.markdown(f"- File: {doc.metadata.get('source', 'Unknown')}")
                                    st.markdown(f"- Konten: {doc.page_content[:200]}...")
                                    st.markdown("---")
                        
                        except Exception as e:
                            st.error(f"Error getting response: {str(e)}")
                
                # Display chat history
                if st.session_state.chat_history:
                    st.markdown("### 💬 Riwayat Percakapan:")
                    for i, entry in enumerate(reversed(st.session_state.chat_history[-5:])):
                        with st.expander(f"Q{len(st.session_state.chat_history)-i}: {entry['question'][:50]}..."):
                            st.markdown(f"**👤 Pertanyaan:** {entry['question']}")
                            st.markdown(f"**🤖 Jawaban:** {entry['answer']}")
    
    with tab3:
        st.markdown('<h2 class="sub-header">Riwayat File yang Diproses</h2>', unsafe_allow_html=True)
        
        if st.session_state.processed_files:
            for i, file_info in enumerate(st.session_state.processed_files):
                with st.expander(f"📄 {file_info['name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Ukuran:** {file_info['size']:,} bytes")
                        st.write(f"**Diproses:** {file_info['processed_at']}")
                    with col2:
                        st.write(f"**Chunks:** {file_info['chunks']}")
                        
            # Clear all data button
            if st.button("🗑️ Hapus Semua Data", type="secondary"):
                if st.session_state.vector_store:
                    st.session_state.vector_store.delete_vector_store()
                st.session_state.vector_store = None
                st.session_state.rag_chain = None
                st.session_state.processed_files = []
                st.session_state.chat_history = []
                st.success("✅ Semua data berhasil dihapus!")
                st.rerun()
        else:
            st.info("📄 Belum ada file yang diproses")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "🚀 **RAG PDF AI Agent** - Dibuat dengan ❤️ menggunakan LangChain & Streamlit"
    )


if __name__ == "__main__":
    main()
