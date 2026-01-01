import json
from pathlib import Path
from typing import Any, Dict, Optional, Union
from .flon import FlexionParser

def convert(filepath: Union[str, Path], target_type: str, output_name: Optional[str] = None) -> str:
    """
    Convert a file between FLON and JSON formats.
    
    Args:
        filepath: Path to the input file (.flon or .json)
        target_type: Target format ('flon' or 'json')
        output_name: Optional output filename (auto-generated if not provided)
    
    Returns:
        Path to the output file
    """
    filepath = Path(filepath)
    target_type = target_type.lower()
    
    if target_type not in ('flon', 'json'):
        raise ValueError("target_type must be either 'flon' or 'json'")
    
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    # Read and parse input
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Convert
    if target_type == 'json':
        # FLON to JSON
        parser = FlexionParser()
        parser.parse(content)
        output_data = parser._get_value(parser.data)
        
        if output_name is None:
            output_name = filepath.stem + '.json'
        
        output_path = filepath.parent / output_name
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    else:
        # JSON to FLON
        data = json.loads(content)
        
        if output_name is None:
            output_name = filepath.stem + '.flon'
        
        output_path = filepath.parent / output_name
        flon_content = _dict_to_flon(data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(flon_content)
    
    return str(output_path)


def convert_data(content: str, target_type: str, output_name: Optional[str] = None) -> str:
    """
    Convert data between FLON and JSON formats.
    
    Args:
        content: Input data as string (FLON or JSON)
        target_type: Target format ('flon' or 'json')
        output_name: Optional output filename (default: output.flon or output.json)
    
    Returns:
        Path to the output file
    """
    target_type = target_type.lower()
    
    if target_type not in ('flon', 'json'):
        raise ValueError("target_type must be either 'flon' or 'json'")
    
    # Convert
    if target_type == 'json':
        # FLON to JSON
        parser = FlexionParser()
        parser.parse(content)
        output_data = parser._get_value(parser.data)
        
        if output_name is None:
            output_name = 'output.json'
        
        with open(output_name, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    else:
        # JSON to FLON
        data = json.loads(content)
        
        if output_name is None:
            output_name = 'output.flon'
        
        flon_content = _dict_to_flon(data)
        
        with open(output_name, 'w', encoding='utf-8') as f:
            f.write(flon_content)
    
    return output_name


def _dict_to_flon(data: Any, level: int = 0, parent_key: str = 'root') -> str:
    """Convert a dictionary to FLON format."""
    indent = '    ' * level
    lines = []
    
    if level == 0:
        lines.append(f"@{parent_key} (")
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{indent}    {key}: object: (")
                lines.append(_dict_to_flon(value, level + 2, key).rstrip())
                lines.append(f"{indent}    )")
            elif isinstance(value, list):
                lines.append(f"{indent}    {key}: list: [")
                for item in value:
                    if isinstance(item, dict):
                        lines.append(f"{indent}        (")
                        lines.append(_dict_to_flon(item, level + 3, key).rstrip())
                        lines.append(f"{indent}        )")
                    else:
                        lines.append(f"{indent}        {_format_value(item)}")
                lines.append(f"{indent}    ]")
            elif isinstance(value, bool):
                lines.append(f"{indent}    {key}: bool: {str(value).lower()}")
            elif isinstance(value, int):
                lines.append(f"{indent}    {key}: int: {value}")
            elif isinstance(value, float):
                lines.append(f"{indent}    {key}: float: {value}")
            elif isinstance(value, str):
                lines.append(f"{indent}    {key}: string: \"{value}\"")
            else:
                lines.append(f"{indent}    {key}: {_format_value(value)}")
    
    if level == 0:
        lines.append(")")
    
    return '\n'.join(lines)


def _format_value(value: Any) -> str:
    """Format a value for FLON output."""
    if isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        return f'"{value}"'
    else:
        return str(value)


__all__ = ['convert', 'convert_data']