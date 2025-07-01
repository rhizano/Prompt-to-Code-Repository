"""
Configuration file for RAG PDF AI Agent
"""

import os
from typing import Dict, Any

# Default configuration
DEFAULT_CONFIG = {
    "pdf_processing": {
        "chunk_size": 1000,
        "chunk_overlap": 200,
        "max_file_size": 10 * 1024 * 1024,  # 10MB
    },
    "embeddings": {
        "default_type": "huggingface",
        "openai_model": "text-embedding-ada-002",
        "huggingface_model": "sentence-transformers/all-MiniLM-L6-v2",
    },
    "vector_store": {
        "default_type": "faiss",
        "persist_directory": "./data/vector_db",
        "search_k": 4,
    },
    "llm": {
        "default_model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 1000,
    },
    "streamlit": {
        "page_title": "RAG PDF AI Agent",
        "page_icon": "📚",
        "layout": "wide",
    }
}


class Config:
    """Configuration class for the application"""
    
    def __init__(self, config_dict: Dict[str, Any] = None):
        """
        Initialize configuration
        
        Args:
            config_dict: Optional custom configuration dictionary
        """
        self.config = DEFAULT_CONFIG.copy()
        if config_dict:
            self._update_config(config_dict)
    
    def _update_config(self, config_dict: Dict[str, Any]):
        """Update configuration with custom values"""
        for key, value in config_dict.items():
            if key in self.config and isinstance(self.config[key], dict):
                self.config[key].update(value)
            else:
                self.config[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_pdf_config(self) -> Dict[str, Any]:
        """Get PDF processing configuration"""
        return self.config["pdf_processing"]
    
    def get_embedding_config(self) -> Dict[str, Any]:
        """Get embedding configuration"""
        return self.config["embeddings"]
    
    def get_vector_store_config(self) -> Dict[str, Any]:
        """Get vector store configuration"""
        return self.config["vector_store"]
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration"""
        return self.config["llm"]
    
    def get_streamlit_config(self) -> Dict[str, Any]:
        """Get Streamlit configuration"""
        return self.config["streamlit"]


# Global configuration instance
config = Config()
