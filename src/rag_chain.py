"""
RAG Chain Module
Implements the complete RAG (Retrieval Augmented Generation) pipeline
"""

import os
from typing import List, Optional, Dict, Any
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from src.vector_store import VectorStore
from src.embeddings import EmbeddingManager


class RAGChain:
    """Class for implementing RAG pipeline"""
    
    def __init__(self,
                 vector_store: VectorStore,
                 llm_type: str = "openai",
                 model_name: str = "gpt-3.5-turbo",
                 temperature: float = 0.7):
        """
        Initialize RAG chain
        
        Args:
            vector_store: VectorStore instance
            llm_type: Type of LLM to use
            model_name: Name of the model
            temperature: Temperature for generation
        """
        self.vector_store = vector_store
        self.llm_type = llm_type
        self.model_name = model_name
        self.temperature = temperature
        self.llm = self._initialize_llm()
        self.retrieval_qa = None
        self._setup_chain()
    
    def _initialize_llm(self):
        """Initialize the language model"""
        try:
            if self.llm_type == "openai":
                if not os.getenv("OPENAI_API_KEY"):
                    raise ValueError("OPENAI_API_KEY not found in environment variables")
                
                if "gpt-3.5" in self.model_name or "gpt-4" in self.model_name:
                    return ChatOpenAI(
                        model_name=self.model_name,
                        temperature=self.temperature,
                        openai_api_key=os.getenv("OPENAI_API_KEY")
                    )
                else:
                    return OpenAI(
                        model_name=self.model_name,
                        temperature=self.temperature,
                        openai_api_key=os.getenv("OPENAI_API_KEY")
                    )
            else:
                raise ValueError(f"Unsupported LLM type: {self.llm_type}")
                
        except Exception as e:
            raise Exception(f"Error initializing LLM: {str(e)}")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create custom prompt template for RAG"""
        template = """
        Gunakan konteks berikut untuk menjawab pertanyaan. Jika Anda tidak tahu jawabannya berdasarkan konteks yang diberikan, katakan bahwa Anda tidak tahu, jangan mencoba membuat jawaban.

        Konteks:
        {context}

        Pertanyaan: {question}
        
        Jawaban yang detail dan informatif:
        """
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
    
    def _setup_chain(self):
        """Setup the RAG retrieval chain"""
        try:
            if self.vector_store.vector_store is None:
                raise ValueError("Vector store not initialized")
            
            # Create custom prompt
            prompt = self._create_prompt_template()
            
            # Create retrieval QA chain
            self.retrieval_qa = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.vector_store.as_retriever(
                    search_kwargs={"k": 4}
                ),
                chain_type_kwargs={"prompt": prompt},
                return_source_documents=True
            )
            
        except Exception as e:
            raise Exception(f"Error setting up RAG chain: {str(e)}")
    
    def query(self, question: str, k: int = 4) -> Dict[str, Any]:
        """
        Query the RAG system
        
        Args:
            question: User question
            k: Number of documents to retrieve
            
        Returns:
            Dictionary with answer and source documents
        """
        try:
            if self.retrieval_qa is None:
                raise ValueError("RAG chain not initialized")
            
            # Update retriever with new k value
            self.retrieval_qa.retriever.search_kwargs = {"k": k}
            
            # Get response
            response = self.retrieval_qa({"query": question})
            
            return {
                "answer": response["result"],
                "source_documents": response["source_documents"],
                "question": question
            }
            
        except Exception as e:
            raise Exception(f"Error querying RAG system: {str(e)}")
    
    def get_relevant_documents(self, question: str, k: int = 4) -> List[Document]:
        """
        Get relevant documents for a question without generating answer
        
        Args:
            question: User question
            k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        try:
            return self.vector_store.similarity_search(question, k=k)
        except Exception as e:
            raise Exception(f"Error getting relevant documents: {str(e)}")
    
    def get_relevant_documents_with_scores(self, 
                                         question: str, 
                                         k: int = 4) -> List[tuple]:
        """
        Get relevant documents with similarity scores
        
        Args:
            question: User question
            k: Number of documents to retrieve
            
        Returns:
            List of tuples (document, score)
        """
        try:
            return self.vector_store.similarity_search_with_score(question, k=k)
        except Exception as e:
            raise Exception(f"Error getting relevant documents with scores: {str(e)}")
    
    def update_retriever_config(self, search_kwargs: Dict[str, Any]):
        """
        Update retriever configuration
        
        Args:
            search_kwargs: New search parameters
        """
        try:
            if self.retrieval_qa:
                self.retrieval_qa.retriever.search_kwargs.update(search_kwargs)
        except Exception as e:
            raise Exception(f"Error updating retriever config: {str(e)}")
    
    def get_chain_info(self) -> Dict[str, Any]:
        """
        Get information about the RAG chain
        
        Returns:
            Dictionary with chain information
        """
        return {
            "llm_type": self.llm_type,
            "model_name": self.model_name,
            "temperature": self.temperature,
            "vector_store_info": self.vector_store.get_store_info(),
            "chain_initialized": self.retrieval_qa is not None
        }
    
    def chat_with_history(self, 
                         question: str, 
                         chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Chat with conversation history context
        
        Args:
            question: Current question
            chat_history: List of previous Q&A pairs
            
        Returns:
            Dictionary with answer and updated history
        """
        try:
            # Add chat history context to question if provided
            if chat_history:
                context_question = f"Riwayat percakapan:\n"
                for entry in chat_history[-3:]:  # Keep last 3 exchanges
                    context_question += f"Q: {entry['question']}\nA: {entry['answer']}\n\n"
                context_question += f"Pertanyaan saat ini: {question}"
            else:
                context_question = question
            
            # Get response
            response = self.query(context_question)
            
            # Update chat history
            if chat_history is None:
                chat_history = []
            
            chat_history.append({
                "question": question,
                "answer": response["answer"]
            })
            
            return {
                "answer": response["answer"],
                "source_documents": response["source_documents"],
                "chat_history": chat_history
            }
            
        except Exception as e:
            raise Exception(f"Error in chat with history: {str(e)}")
