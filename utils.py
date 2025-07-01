"""
Utility functions for RAG PDF AI Agent
"""

import os
import hashlib
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Setup logging configuration
    
    Args:
        log_level: Logging level
        
    Returns:
        Logger instance
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('rag_pdf.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def validate_api_keys() -> Dict[str, bool]:
    """
    Validate required API keys
    
    Returns:
        Dictionary with API key validation status
    """
    return {
        "openai": bool(os.getenv("OPENAI_API_KEY")),
        "huggingface": bool(os.getenv("HUGGINGFACE_API_TOKEN"))
    }


def calculate_file_hash(file_content: bytes) -> str:
    """
    Calculate MD5 hash of file content
    
    Args:
        file_content: File content as bytes
        
    Returns:
        MD5 hash string
    """
    return hashlib.md5(file_content).hexdigest()


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def save_chat_history(chat_history: List[Dict[str, str]], 
                     filename: str = None) -> str:
    """
    Save chat history to JSON file
    
    Args:
        chat_history: List of chat exchanges
        filename: Optional custom filename
        
    Returns:
        Path to saved file
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_history_{timestamp}.json"
    
    filepath = os.path.join("data", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=2)
    
    return filepath


def load_chat_history(filepath: str) -> List[Dict[str, str]]:
    """
    Load chat history from JSON file
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        List of chat exchanges
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def clean_text(text: str) -> str:
    """
    Clean and normalize text
    
    Args:
        text: Input text
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters but keep basic punctuation
    import re
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
    
    return text.strip()


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to specified length
    
    Args:
        text: Input text
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def get_file_metadata(filepath: str) -> Dict[str, Any]:
    """
    Get file metadata
    
    Args:
        filepath: Path to file
        
    Returns:
        Dictionary with file metadata
    """
    try:
        stat = os.stat(filepath)
        return {
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "extension": os.path.splitext(filepath)[1].lower()
        }
    except OSError:
        return {}


def ensure_directory(directory: str) -> None:
    """
    Ensure directory exists, create if not
    
    Args:
        directory: Directory path
    """
    os.makedirs(directory, exist_ok=True)


def list_files_in_directory(directory: str, 
                          extension: str = None) -> List[str]:
    """
    List files in directory with optional extension filter
    
    Args:
        directory: Directory path
        extension: Optional file extension filter
        
    Returns:
        List of file paths
    """
    if not os.path.exists(directory):
        return []
    
    files = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            if extension is None or filename.lower().endswith(extension.lower()):
                files.append(filepath)
    
    return sorted(files)


def create_backup_name(original_name: str) -> str:
    """
    Create backup filename with timestamp
    
    Args:
        original_name: Original filename
        
    Returns:
        Backup filename
    """
    name, ext = os.path.splitext(original_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{name}_backup_{timestamp}{ext}"


def validate_pdf_file(file_content: bytes) -> bool:
    """
    Validate if file content is a valid PDF
    
    Args:
        file_content: File content as bytes
        
    Returns:
        True if valid PDF, False otherwise
    """
    # Check PDF header
    return file_content.startswith(b'%PDF-')


def get_system_info() -> Dict[str, Any]:
    """
    Get system information
    
    Returns:
        Dictionary with system information
    """
    import platform
    import psutil
    
    return {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "cpu_count": os.cpu_count(),
        "memory_total": psutil.virtual_memory().total,
        "memory_available": psutil.virtual_memory().available,
        "disk_usage": psutil.disk_usage('/').percent
    }
