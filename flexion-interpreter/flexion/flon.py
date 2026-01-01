import re
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Global environment settings
_env_settings = {
    'indent': 2
}

class FlexionParser:
    """
    A parser for Flexion (.flon) files.
    
    Usage:
        flon = FlexionParser()
        flon.load('path/to/file.flon')
        value = flon.get('root/panels')
        type_info = flon.get('root/panels/docs', 'type')
    """
    
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self._raw_content: str = ""
    
    def load(self, filepath: Union[str, Path]) -> 'FlexionParser':
        """Load a Flexion file from the given path."""
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return self.parse(content)
    
    def parse(self, content: str) -> 'FlexionParser':
        """Parse Flexion content from a string."""
        self._raw_content = content
        self.data = self._parse_content(content)
        return self
    
    def get(self, path: str, mode: str = 'value') -> Any:
        """Get data from the parsed Flexion structure."""
        if mode not in ('value', 'type'):
            raise ValueError("mode must be either 'value' or 'type'")
        
        parts = path.strip('/').split('/')
        current = self.data
        
        for i, part in enumerate(parts):
            if not isinstance(current, dict):
                raise KeyError(f"Cannot navigate to '{part}' in path '{path}'")
            
            if part not in current:
                raise KeyError(f"Path not found: '{path}' (missing '{part}')")
            
            current = current[part]
        
        if mode == 'type':
            return self._get_type(current)
        
        return self._get_value(current)
    
    def pretty(self, path: str, mode: str = 'value', indent: Optional[int] = None) -> str:
        """Get formatted data as a string."""
        if indent is None:
            indent = _env_settings['indent']
        
        data = self.get(path, mode)
        if isinstance(data, (dict, list)):
            return json.dumps(data, indent=indent, ensure_ascii=False)
        return str(data)
    
    def _get_value(self, data: Any) -> Any:
        """Extract the value from parsed data."""
        if isinstance(data, dict):
            if '_type' in data and '_value' in data:
                val = data['_value']
                if isinstance(val, dict):
                    return self._get_value(val)
                return val
            else:
                result = {}
                for key, value in data.items():
                    if not key.startswith('_'):
                        result[key] = self._get_value(value)
                return result
        return data
    
    def _get_type(self, data: Any) -> str:
        """Extract the type from parsed data."""
        if isinstance(data, dict):
            if '_type' in data:
                return data['_type']
            else:
                return 'item'
        
        if isinstance(data, bool):
            return 'bool'
        elif isinstance(data, int):
            return 'int'
        elif isinstance(data, float):
            return 'float'
        elif isinstance(data, str):
            return 'string'
        elif isinstance(data, list):
            return 'list'
        else:
            return 'unknown'
    
    def _parse_content(self, content: str) -> Dict[str, Any]:
        """Parse the Flexion content into a structured dictionary."""
        lines = []
        in_block_comment = False
        
        for line in content.split('\n'):
            stripped = line.strip()  # noqa: F841
            
            if '!! !!' in line:
                if not in_block_comment:
                    in_block_comment = True
                    before = line.split('!! !!')[0]
                    if before.strip():
                        lines.append(before)
                else:
                    in_block_comment = False
                    parts = line.split('!! !!', 1)
                    if len(parts) > 1 and parts[1].strip():
                        lines.append(parts[1])
                continue
            
            if in_block_comment:
                continue
            
            if '!' in line:
                in_quote = False
                escape_next = False
                for i, char in enumerate(line):
                    if escape_next:
                        escape_next = False
                        continue
                    if char == '\\':
                        escape_next = True
                        continue
                    if char == '"':
                        in_quote = not in_quote
                    elif char == '!' and not in_quote:
                        line = line[:i]
                        break
            
            if line.strip():
                lines.append(line)
        
        cleaned_content = '\n'.join(lines)
        
        result = {}
        items = self._extract_items(cleaned_content)
        
        for item_path, item_content in items.items():
            self._insert_nested_path(result, item_path, self._parse_item_content(item_content))
        
        return result
    
    def _insert_nested_path(self, root: Dict, path: str, value: Any):
        """Insert a value into a nested dictionary structure based on path."""
        parts = path.split('/')
        current = root
        
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        current[parts[-1]] = value
    
    def _extract_items(self, content: str) -> Dict[str, str]:
        """Extract top-level items (@name (...))."""
        items = {}
        i = 0
        
        while i < len(content):
            while i < len(content) and content[i] in ' \t\n\r':
                i += 1
            
            if i >= len(content):
                break
            
            if content[i] == '@':
                j = i + 1
                while j < len(content) and (content[j].isalnum() or content[j] in '/_-'):
                    j += 1
                
                name = content[i+1:j]
                
                while j < len(content) and content[j] in ' \t\n\r':
                    j += 1
                
                if j < len(content) and content[j] == '(':
                    paren_count = 1
                    k = j + 1
                    while k < len(content) and paren_count > 0:
                        if content[k] == '(':
                            paren_count += 1
                        elif content[k] == ')':
                            paren_count -= 1
                        k += 1
                    
                    if paren_count == 0:
                        body = content[j+1:k-1]
                        items[name] = body
                        i = k
                        continue
            
            i += 1
        
        return items
    
    def _parse_item_content(self, content: str) -> Dict[str, Any]:
        """Parse the content inside an item."""
        result = {}
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            if not stripped:
                i += 1
                continue
            
            colon_pos = stripped.find(':')
            if colon_pos == -1:
                i += 1
                continue
            
            label = stripped[:colon_pos].strip()
            rest = stripped[colon_pos+1:].strip()
            
            type_info = None
            value_part = rest
            
            if ':' in rest and not rest.startswith('object:'):
                second_colon = rest.find(':')
                potential_type = rest[:second_colon].strip()
                if potential_type in ['string', 'str', 'int', 'integer', 'float', 'decimal', 'double', 'bool', 'boolean', 'void', 'null', 'undefined', 'object', 'list', 'array', 'keyword']:
                    type_info = potential_type
                    value_part = rest[second_colon+1:].strip()
            
            if value_part.startswith('object:'):
                value_part = value_part[7:].strip()
                type_info = 'object'
            
            if value_part.startswith('('):
                obj_lines = []
                paren_count = 0
                
                for char in value_part:
                    if char == '(':
                        paren_count += 1
                    elif char == ')':
                        paren_count -= 1
                
                obj_lines.append(value_part[1:])
                
                j = i + 1
                while j < len(lines) and paren_count > 0:
                    current_line = lines[j]
                    for char in current_line:
                        if char == '(':
                            paren_count += 1
                        elif char == ')':
                            paren_count -= 1
                    obj_lines.append(current_line)
                    j += 1
                
                if obj_lines:
                    obj_lines[-1] = obj_lines[-1].rsplit(')', 1)[0]
                
                obj_str = '\n'.join(obj_lines)
                parsed_obj = self._parse_item_content(obj_str)
                
                result[label] = {
                    '_type': 'object',
                    '_value': parsed_obj,
                    **parsed_obj
                }
                
                i = j
            else:
                value = self._parse_value(value_part, type_info)
                result[label] = {
                    '_type': type_info or self._infer_type(value),
                    '_value': value
                }
                i += 1
        
        return result
    
    def _parse_value(self, value_str: str, type_hint: Optional[str] = None) -> Any:
        """Parse a value string into appropriate Python type."""
        value_str = value_str.strip()
        
        if value_str.startswith('"') and value_str.endswith('"'):
            return value_str[1:-1]
        
        if value_str.lower() == 'true':
            return True
        if value_str.lower() == 'false':
            return False
        
        if value_str.startswith('@') or value_str.startswith('#'):
            return value_str
        
        if type_hint in ('int', 'integer'):
            try:
                return int(value_str)
            except ValueError:
                pass
        if type_hint in ('float', 'decimal', 'double'):
            try:
                return float(value_str)
            except ValueError:
                pass
        
        try:
            if '.' in value_str:
                return float(value_str)
            return int(value_str)
        except ValueError:
            pass
        
        return value_str
    
    def _infer_type(self, value: Any) -> str:
        """Infer Flexion type from Python value."""
        if isinstance(value, bool):
            return 'bool'
        elif isinstance(value, int):
            return 'int'
        elif isinstance(value, float):
            return 'float'
        elif isinstance(value, str):
            if value.startswith('@') or value.startswith('#'):
                return 'keyword'
            return 'string'
        elif isinstance(value, dict):
            return 'object'
        elif isinstance(value, list):
            return 'list'
        else:
            return 'keyword'


# Module-level convenience functions
_global_parser = FlexionParser()

def load(filepath: Union[str, Path]) -> FlexionParser:
    """Load a Flexion file."""
    return _global_parser.load(filepath)

def parse(content: str) -> FlexionParser:
    """Parse Flexion content."""
    return _global_parser.parse(content)

def get(path: str, mode: str = 'value') -> Any:
    """Get data from the loaded Flexion structure."""
    return _global_parser.get(path, mode)

def pretty(path: str, mode: str = 'value', indent: Optional[int] = None) -> str:
    """Get formatted data as a string."""
    return _global_parser.pretty(path, mode, indent)

def set_env(variable_name: str, value: Any):
    """Set environment variable."""
    if variable_name not in _env_settings:
        raise ValueError(f"Unknown environment variable: {variable_name}")
    _env_settings[variable_name] = value


__all__ = ['FlexionParser', 'load', 'parse', 'get', 'pretty', 'set_env']