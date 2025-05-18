"""
Common utility functions for the API.
"""

import json
from typing import Dict, Any, Union
from pathlib import Path

def load_json_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load JSON data from a file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dictionary containing the JSON data
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(data: Dict[str, Any], file_path: Union[str, Path]) -> None:
    """
    Save JSON data to a file.
    
    Args:
        data: Dictionary containing the data to save
        file_path: Path to save the JSON file
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
