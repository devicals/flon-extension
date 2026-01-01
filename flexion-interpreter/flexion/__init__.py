"""
Flexion Language Interpreter
A Python library for parsing and working with Flexion (.flon) files
"""

from .flon import load, parse, get, pretty, set_env
from .converter import convert, convert_data

__version__ = "1.0.2"

# We use a class with staticmethods so that flon.load() 
# does not try to pass 'self' as an argument.
class flon:
    """Flexion parser module namespace"""
    load = staticmethod(load)
    parse = staticmethod(parse)
    get = staticmethod(get)
    pretty = staticmethod(pretty)
    _env = staticmethod(set_env)
    
    # Adding converters here because your test script calls flon.convert
    convert = staticmethod(convert)
    convert_data = staticmethod(convert_data)

__all__ = ['flon']