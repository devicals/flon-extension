"""
Format Conversion Examples
Demonstrates converting between FLON and JSON formats
"""

from interpreter import converter
from pathlib import Path

# Example 1: Convert file FLON to JSON
print("=== Example 1: FLON to JSON (File) ===")
output = converter.convert('data.flon', 'json')
print(f"Created: {output}")
print()

# Example 2: Convert file JSON to FLON
print("=== Example 2: JSON to FLON (File) ===")
output = converter.convert('data.json', 'flon')
print(f"Created: {output}")
print()

# Example 3: Convert with custom output name
print("=== Example 3: Custom Output Name ===")
output = converter.convert('config.flon', 'json', 'my-config.json')
print(f"Created: {output}")
print()

# Example 4: Convert string data FLON to JSON
print("=== Example 4: String Data FLON to JSON ===")
flon_content = """
@root (
    name: "Test Application"
    version: "1.0.0"
    settings: object: (
        debug: bool: true
        port: int: 8080
    )
)
"""

output = converter.convert_data(flon_content, 'json', 'output.json')
print(f"Created: {output}")

# Read and display the result
with open(output, 'r') as f:
    print("Content:")
    print(f.read())
print()

# Example 5: Convert string data JSON to FLON
print("=== Example 5: String Data JSON to FLON ===")
json_content = '''
{
  "name": "Sample App",
  "version": "2.0.0",
  "active": true,
  "config": {
    "host": "localhost",
    "port": 3000
  }
}
'''

output = converter.convert_data(json_content, 'flon', 'output.flon')
print(f"Created: {output}")

# Read and display the result
with open(output, 'r') as f:
    print("Content:")
    print(f.read())
print()

# Example 6: Batch conversion
print("=== Example 6: Batch Conversion ===")
def batch_convert_directory(directory, target_format):
    """Convert all files in a directory"""
    source_ext = '.json' if target_format == 'flon' else '.flon'
    
    for file in Path(directory).glob(f'*{source_ext}'):
        print(f"Converting {file.name}...")
        try:
            output = converter.convert(str(file), target_format)
            print(f"  -> Created {output}")
        except Exception as e:
            print(f"  -> Error: {e}")

# Usage (commented out to avoid actual execution)
# batch_convert_directory('./configs', 'json')
print("Batch conversion function defined")
print()

# Example 7: Round-trip conversion
print("=== Example 7: Round-trip Conversion ===")
original_flon = """
@test (
    value: int: 42
    text: "Hello"
)
"""

# FLON -> JSON
print("Original FLON -> JSON")
converter.convert_data(original_flon, 'json', 'temp.json')

# JSON -> FLON
print("JSON -> FLON (round-trip)")
with open('temp.json', 'r') as f:
    json_data = f.read()

converter.convert_data(json_data, 'flon', 'temp-roundtrip.flon')

# Display result
with open('temp-roundtrip.flon', 'r') as f:
    print("\nRound-trip result:")
    print(f.read())
print()

# Example 8: Error handling in conversion
print("=== Example 8: Error Handling ===")
try:
    converter.convert('nonexistent.flon', 'json')
except FileNotFoundError as e:
    print(f"Caught error: {e}")

try:
    converter.convert('data.flon', 'invalid_format')
except ValueError as e:
    print(f"Caught error: {e}")

# Cleanup temporary files
print("\n=== Cleanup ===")
for temp_file in ['temp.json', 'temp-roundtrip.flon', 'output.json', 'output.flon']:
    if Path(temp_file).exists():
        Path(temp_file).unlink()
        print(f"Removed {temp_file}")