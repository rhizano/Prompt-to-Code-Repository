"""
Vector Store Module
Handles vector database operations for similarity search
"""

import os
import pickle
from typing import List, Optional, Tuple
from langchain.vectorstores import FAISS, Chroma
from langchain.schema import Document
from src.embeddings import EmbeddingManager


class VectorStore:
    """Class for managing vector database operations"""
    
    def __init__(self, 
                 store_type: str = "faiss",
                 embedding_manager: Optional[EmbeddingManager] = None,
                 persist_directory: str = "./data/vector_db"):
        """
        Initialize vector store
        
        Args:
            store_type: Type of vector store ("faiss" or "chroma")
            embedding_manager: EmbeddingManager instance
            persist_directory: Directory to persist vector store
        """
        self.store_type = store_type
        self.persist_directory = persist_directory
        self.embedding_manager = embedding_manager or EmbeddingManager()
        self.vector_store = None
        
        # Create persist directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
    
    def create_vector_store(self, documents: List[Document]) -> None:
        """
        Create vector store from documents
        
        Args:
            documents: List of Document objects
        """
        try:
            if self.store_type == "faiss":
                self.vector_store = FAISS.from_documents(
                    documents=documents,
                    embedding=self.embedding_manager.embeddings
                )
            elif self.store_type == "chroma":
                self.vector_store = Chroma.from_documents(
                    documents=documents,
                    embedding=self.embedding_manager.embeddings,
                    persist_directory=self.persist_directory
                )
            else:
                raise ValueError(f"Unsupported vector store type: {self.store_type}")
                
        except Exception as e:
            raise Exception(f"Error creating vector store: {str(e)}")
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to existing vector store
        
        Args:
            documents: List of Document objects to add
        """
        try:
            if self.vector_store is None:
                self.create_vector_store(documents)
            else:
                self.vector_store.add_documents(documents)
                
        except Exception as e:
            raise Exception(f"Error adding documents: {str(e)}")
    
    def similarity_search(self, 
                         query: str, 
                         k: int = 4,
                         filter_dict: Optional[dict] = None) -> List[Document]:
        """
        Perform similarity search
        
        Args:
            query: Search query
            k: Number of results to return
            filter_dict: Optional filter for metadata
            
        Returns:
            List of similar documents
        """
        try:
            if self.vector_store is None:
                raise ValueError("Vector store not initialized")
            
            if filter_dict:
                return self.vector_store.similarity_search(
                    query=query,
                    k=k,
                    filter=filter_dict
                )
            else:
                return self.vector_store.similarity_search(query=query, k=k)
                
        except Exception as e:
            raise Exception(f"Error performing similarity search: {str(e)}")
    
    def similarity_search_with_score(self, 
                                   query: str, 
                                   k: int = 4) -> List[Tuple[Document, float]]:
        """
        Perform similarity search with scores
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of tuples (document, similarity_score)
        """
        try:
            if self.vector_store is None:
                raise ValueError("Vector store not initialized")
            
            return self.vector_store.similarity_search_with_score(query=query, k=k)
                
        except Exception as e:
            raise Exception(f"Error performing similarity search with score: {str(e)}")
    
    def save_vector_store(self, path: Optional[str] = None) -> None:
        """
        Save vector store to disk
        
        Args:
            path: Optional custom path to save
        """
        try:
            if self.vector_store is None:
                raise ValueError("Vector store not initialized")
            
            if self.store_type == "faiss":
                save_path = path or os.path.join(self.persist_directory, "faiss_index")
                self.vector_store.save_local(save_path)
            elif self.store_type == "chroma":
                # Chroma automatically persists to persist_directory
                if hasattr(self.vector_store, 'persist'):
                    self.vector_store.persist()
                    
        except Exception as e:
            raise Exception(f"Error saving vector store: {str(e)}")
    
    def load_vector_store(self, path: Optional[str] = None) -> None:
        """
        Load vector store from disk
        
        Args:
            path: Optional custom path to load from
        """
        try:
            if self.store_type == "faiss":
                load_path = path or os.path.join(self.persist_directory, "faiss_index")
                if os.path.exists(load_path):
                    self.vector_store = FAISS.load_local(
                        load_path,
                        embeddings=self.embedding_manager.embeddings
                    )
            elif self.store_type == "chroma":
                if os.path.exists(self.persist_directory):
                    self.vector_store = Chroma(
                        persist_directory=self.persist_directory,
                        embedding_function=self.embedding_manager.embeddings
                    )
                    
        except Exception as e:
            raise Exception(f"Error loading vector store: {str(e)}")
    
    def delete_vector_store(self) -> None:
        """Delete vector store and clean up"""
        try:
            if self.store_type == "chroma" and hasattr(self.vector_store, 'delete_collection'):
                self.vector_store.delete_collection()
            
            self.vector_store = None
            
        except Exception as e:
            raise Exception(f"Error deleting vector store: {str(e)}")
    
    def get_document_count(self) -> int:
        """
        Get number of documents in vector store
        
        Returns:
            Number of documents
        """
        try:
            if self.vector_store is None:
                return 0
            
            if self.store_type == "faiss":
                return self.vector_store.index.ntotal
            elif self.store_type == "chroma":
                return len(self.vector_store.get()['ids'])
            
            return 0
            
        except Exception as e:
            raise Exception(f"Error getting document count: {str(e)}")
    
    def get_store_info(self) -> dict:
        """
        Get information about vector store
        
        Returns:
            Dictionary with store information
        """
        return {
            "type": self.store_type,
            "persist_directory": self.persist_directory,
            "document_count": self.get_document_count(),
            "embedding_info": self.embedding_manager.get_model_info()
        }
