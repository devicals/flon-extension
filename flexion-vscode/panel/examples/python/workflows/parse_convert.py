from flexion import flon, converter

# Load FLON file
flon.load('config.flon')

# Query data
host = flon.get('root/database/host')
port = flon.get('root/database/port')

# Convert to JSON
converter.convert('config.flon', 'json')