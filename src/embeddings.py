"""
Text Embeddings Module
Handles text embedding generation using various embedding models
"""

import os
from typing import List, Optional
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.schema import Document


class EmbeddingManager:
    """Class for managing text embeddings"""
    
    def __init__(self, embedding_type: str = "openai", model_name: Optional[str] = None):
        """
        Initialize embedding manager
        
        Args:
            embedding_type: Type of embedding ("openai" or "huggingface")
            model_name: Optional specific model name
        """
        self.embedding_type = embedding_type
        self.model_name = model_name
        self.embeddings = self._initialize_embeddings()
    
    def _initialize_embeddings(self):
        """Initialize embedding model based on type"""
        try:
            if self.embedding_type == "openai":
                if not os.getenv("OPENAI_API_KEY"):
                    raise ValueError("OPENAI_API_KEY not found in environment variables")
                
                model = self.model_name or "text-embedding-ada-002"
                return OpenAIEmbeddings(
                    model=model,
                    openai_api_key=os.getenv("OPENAI_API_KEY")
                )
            
            elif self.embedding_type == "huggingface":
                model = self.model_name or "sentence-transformers/all-MiniLM-L6-v2"
                return HuggingFaceEmbeddings(
                    model_name=model,
                    model_kwargs={'device': 'cpu'},
                    encode_kwargs={'normalize_embeddings': True}
                )
            
            else:
                raise ValueError(f"Unsupported embedding type: {self.embedding_type}")
                
        except Exception as e:
            raise Exception(f"Error initializing embeddings: {str(e)}")
    
    def embed_documents(self, documents: List[Document]) -> List[List[float]]:
        """
        Generate embeddings for documents
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of embedding vectors
        """
        try:
            texts = [doc.page_content for doc in documents]
            return self.embeddings.embed_documents(texts)
        except Exception as e:
            raise Exception(f"Error embedding documents: {str(e)}")
    
    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a query
        
        Args:
            query: Query string
            
        Returns:
            Embedding vector
        """
        try:
            return self.embeddings.embed_query(query)
        except Exception as e:
            raise Exception(f"Error embedding query: {str(e)}")
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings
        
        Returns:
            Embedding dimension
        """
        try:
            # Test with a small text
            test_embedding = self.embed_query("test")
            return len(test_embedding)
        except Exception as e:
            raise Exception(f"Error getting embedding dimension: {str(e)}")
    
    def compare_embeddings(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculate similarity between two embeddings using cosine similarity
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score
        """
        try:
            import numpy as np
            
            # Convert to numpy arrays
            emb1 = np.array(embedding1)
            emb2 = np.array(embedding2)
            
            # Calculate cosine similarity
            cosine_sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
            return float(cosine_sim)
        except Exception as e:
            raise Exception(f"Error comparing embeddings: {str(e)}")
    
    def get_model_info(self) -> dict:
        """
        Get information about the current embedding model
        
        Returns:
            Dictionary with model information
        """
        return {
            "type": self.embedding_type,
            "model_name": self.model_name,
            "dimension": self.get_embedding_dimension()
        }
