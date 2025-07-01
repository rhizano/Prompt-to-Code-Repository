"""
PDF Processing Module
Handles PDF file upload, parsing, and text extraction
"""

import os
import tempfile
from typing import List, Optional
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


class PDFProcessor:
    """Class for processing PDF files"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize PDF processor
        
        Args:
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """
        Extract text from PDF file
        
        Args:
            pdf_file: PDF file object or path
            
        Returns:
            Extracted text content
        """
        try:
            if hasattr(pdf_file, 'read'):
                # File object
                pdf_reader = PyPDF2.PdfReader(pdf_file)
            else:
                # File path
                with open(pdf_file, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def process_uploaded_file(self, uploaded_file, save_path: str) -> str:
        """
        Process uploaded PDF file and save it
        
        Args:
            uploaded_file: Streamlit uploaded file object
            save_path: Path to save the file
            
        Returns:
            Path to saved file
        """
        try:
            # Create uploads directory if it doesn't exist
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Save uploaded file
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            return save_path
        except Exception as e:
            raise Exception(f"Error saving uploaded file: {str(e)}")
    
    def create_documents(self, text: str, metadata: Optional[dict] = None) -> List[Document]:
        """
        Create LangChain documents from text
        
        Args:
            text: Input text
            metadata: Optional metadata for documents
            
        Returns:
            List of Document objects
        """
        try:
            # Split text into chunks
            chunks = self.text_splitter.split_text(text)
            
            # Create documents
            documents = []
            for i, chunk in enumerate(chunks):
                doc_metadata = metadata.copy() if metadata else {}
                doc_metadata.update({"chunk_id": i, "chunk_size": len(chunk)})
                
                documents.append(Document(
                    page_content=chunk,
                    metadata=doc_metadata
                ))
            
            return documents
        except Exception as e:
            raise Exception(f"Error creating documents: {str(e)}")
    
    def process_pdf_to_documents(self, pdf_file, filename: str = None) -> List[Document]:
        """
        Complete pipeline: PDF to LangChain documents
        
        Args:
            pdf_file: PDF file object or path
            filename: Optional filename for metadata
            
        Returns:
            List of Document objects
        """
        try:
            # Extract text
            text = self.extract_text_from_pdf(pdf_file)
            
            # Create metadata
            metadata = {
                "source": filename or "unknown",
                "file_type": "pdf"
            }
            
            # Create and return documents
            return self.create_documents(text, metadata)
        except Exception as e:
            raise Exception(f"Error processing PDF to documents: {str(e)}")
    
    def get_file_info(self, pdf_file) -> dict:
        """
        Get information about PDF file
        
        Args:
            pdf_file: PDF file object or path
            
        Returns:
            Dictionary with file information
        """
        try:
            if hasattr(pdf_file, 'read'):
                pdf_reader = PyPDF2.PdfReader(pdf_file)
            else:
                with open(pdf_file, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
            
            info = {
                "num_pages": len(pdf_reader.pages),
                "metadata": pdf_reader.metadata,
                "encrypted": pdf_reader.is_encrypted
            }
            
            return info
        except Exception as e:
            raise Exception(f"Error getting file info: {str(e)}")
