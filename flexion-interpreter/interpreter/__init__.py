"""
Flexion Language Interpreter
A Python library for parsing and working with Flexion (.flon) files
"""

from .flon import FlexionParser, load, parse, get, pretty, set_env
from .converter import convert, convert_data

__version__ = "1.0.0"
__all__ = ['flon', 'converter', 'FlexionParser']

# Create module-level namespaces
class FlonModule:
    """Flexion parser module"""
    FlexionParser = FlexionParser
    load = load
    parse = parse
    get = get
    pretty = pretty
    _env = set_env

class ConverterModule:
    """Format conversion module"""
    convert = convert
    convert_data = convert_data

# Module instances
flon = FlonModule()
converter = ConverterModule()