"""
FastAPI REST API for RAG PDF AI Agent
Alternative API interface for the RAG system
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import tempfile
import os
from datetime import datetime

# Import RAG components
from src.pdf_processor import PDFProcessor
from src.embeddings import EmbeddingManager
from src.vector_store import VectorStore
from src.rag_chain import RAGChain

# Initialize FastAPI app
app = FastAPI(
    title="RAG PDF AI Agent API",
    description="REST API for RAG PDF processing and querying",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for RAG components
pdf_processor = None
embedding_manager = None
vector_store = None
rag_chain = None

# Pydantic models
class QueryRequest(BaseModel):
    question: str
    k: Optional[int] = 4

class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    question: str

class ChatRequest(BaseModel):
    question: str
    chat_history: Optional[List[Dict[str, str]]] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    chat_history: List[Dict[str, str]]

class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks: int
    size: int

class StatusResponse(BaseModel):
    status: str
    documents_count: int
    embedding_model: str
    vector_store_type: str


# Dependency to get RAG components
async def get_rag_components():
    """Dependency to ensure RAG components are initialized"""
    global pdf_processor, embedding_manager, vector_store, rag_chain
    
    if pdf_processor is None:
        pdf_processor = PDFProcessor()
    
    if embedding_manager is None:
        embedding_manager = EmbeddingManager(embedding_type="huggingface")
    
    if vector_store is None:
        vector_store = VectorStore(
            store_type="faiss",
            embedding_manager=embedding_manager,
            persist_directory="./data/vector_db"
        )
        # Try to load existing vector store
        try:
            vector_store.load_vector_store()
        except:
            pass
    
    return {
        "pdf_processor": pdf_processor,
        "embedding_manager": embedding_manager,
        "vector_store": vector_store,
        "rag_chain": rag_chain
    }


@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    await get_rag_components()


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "RAG PDF AI Agent API",
        "version": "1.0.0",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/upload", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    components: Dict = Depends(get_rag_components)
):
    """
    Upload and process PDF file
    
    Args:
        file: PDF file to upload
        
    Returns:
        Upload response with processing details
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Read file content
        content = await file.read()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Process PDF
            documents = components["pdf_processor"].process_pdf_to_documents(
                tmp_file_path, 
                file.filename
            )
            
            # Add to vector store
            components["vector_store"].add_documents(documents)
            components["vector_store"].save_vector_store()
            
            return UploadResponse(
                message="File uploaded and processed successfully",
                filename=file.filename,
                chunks=len(documents),
                size=len(content)
            )
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.post("/query", response_model=QueryResponse)
async def query_documents(
    request: QueryRequest,
    components: Dict = Depends(get_rag_components)
):
    """
    Query documents using RAG
    
    Args:
        request: Query request with question and optional k parameter
        
    Returns:
        Query response with answer and sources
    """
    try:
        # Initialize RAG chain if not already done
        if components["rag_chain"] is None:
            global rag_chain
            rag_chain = RAGChain(vector_store=components["vector_store"])
            components["rag_chain"] = rag_chain
        
        # Perform query
        response = components["rag_chain"].query(request.question, k=request.k)
        
        # Format sources
        sources = []
        for doc in response["source_documents"]:
            sources.append({
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "metadata": doc.metadata
            })
        
        return QueryResponse(
            answer=response["answer"],
            sources=sources,
            question=request.question
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying documents: {str(e)}")


@app.post("/chat", response_model=ChatResponse)
async def chat_with_documents(
    request: ChatRequest,
    components: Dict = Depends(get_rag_components)
):
    """
    Chat with documents using conversation history
    
    Args:
        request: Chat request with question and optional history
        
    Returns:
        Chat response with answer, sources, and updated history
    """
    try:
        # Initialize RAG chain if not already done
        if components["rag_chain"] is None:
            global rag_chain
            rag_chain = RAGChain(vector_store=components["vector_store"])
            components["rag_chain"] = rag_chain
        
        # Perform chat query
        response = components["rag_chain"].chat_with_history(
            request.question,
            request.chat_history or []
        )
        
        # Format sources
        sources = []
        for doc in response["source_documents"]:
            sources.append({
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "metadata": doc.metadata
            })
        
        return ChatResponse(
            answer=response["answer"],
            sources=sources,
            chat_history=response["chat_history"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")


@app.get("/status", response_model=StatusResponse)
async def get_status(components: Dict = Depends(get_rag_components)):
    """
    Get system status
    
    Returns:
        Status response with system information
    """
    try:
        doc_count = components["vector_store"].get_document_count()
        embedding_info = components["embedding_manager"].get_model_info()
        
        return StatusResponse(
            status="active",
            documents_count=doc_count,
            embedding_model=embedding_info["model_name"] or embedding_info["type"],
            vector_store_type=components["vector_store"].store_type
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")


@app.get("/documents")
async def list_documents(components: Dict = Depends(get_rag_components)):
    """
    List processed documents
    
    Returns:
        List of document information
    """
    try:
        doc_count = components["vector_store"].get_document_count()
        store_info = components["vector_store"].get_store_info()
        
        return {
            "document_count": doc_count,
            "store_info": store_info
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")


@app.delete("/documents")
async def clear_documents(components: Dict = Depends(get_rag_components)):
    """
    Clear all documents from vector store
    
    Returns:
        Success message
    """
    try:
        components["vector_store"].delete_vector_store()
        global rag_chain
        rag_chain = None
        components["rag_chain"] = None
        
        return {"message": "All documents cleared successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing documents: {str(e)}")


@app.get("/similar", response_model=List[Dict[str, Any]])
async def find_similar_documents(
    query: str,
    k: int = 4,
    components: Dict = Depends(get_rag_components)
):
    """
    Find similar documents without generating answer
    
    Args:
        query: Search query
        k: Number of documents to return
        
    Returns:
        List of similar documents with scores
    """
    try:
        results = components["vector_store"].similarity_search_with_score(query, k=k)
        
        similar_docs = []
        for doc, score in results:
            similar_docs.append({
                "content": doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content,
                "metadata": doc.metadata,
                "similarity_score": float(score)
            })
        
        return similar_docs
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding similar documents: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
