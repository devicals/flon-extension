"""
Basic Usage Examples
Demonstrates fundamental operations with the Flexion interpreter
"""

from interpreter import flon

# Example 1: Loading from a file
print("=== Example 1: Load from File ===")
flon.load('config.flon')
config = flon.get('root/config')
print("Config:", config)
print()

# Example 2: Parsing from a string
print("=== Example 2: Parse from String ===")
content = """
@root (
    app: "MyApp"
    version: "1.0.0"
    debug: bool: true
)
"""

flon.parse(content)
app_name = flon.get('root/app')
debug_mode = flon.get('root/debug')
print(f"App: {app_name}")
print(f"Debug: {debug_mode}")
print()

# Example 3: Getting specific values
print("=== Example 3: Get Specific Values ===")
flon.parse("""
@database (
    host: "localhost"
    port: int: 5432
    credentials: object: (
        username: "admin"
        password: "secret"
    )
)
""")

host = flon.get('database/host')
port = flon.get('database/port')
username = flon.get('database/credentials/username')

print(f"Connecting to {host}:{port} as {username}")
print()

# Example 4: Type checking
print("=== Example 4: Type Checking ===")
flon.parse("""
@data (
    count: int: 42
    price: float: 19.99
    active: bool: true
    name: string: "Product"
)
""")

print(f"count is: {flon.get('data/count', 'type')}")
print(f"price is: {flon.get('data/price', 'type')}")
print(f"active is: {flon.get('data/active', 'type')}")
print(f"name is: {flon.get('data/name', 'type')}")
print()

# Example 5: Pretty printing
print("=== Example 5: Pretty Printing ===")
flon.parse("""
@users (
    alice: object: (
        id: int: 1
        email: "alice@example.com"
        active: bool: true
    )
    bob: object: (
        id: int: 2
        email: "bob@example.com"
        active: bool: false
    )
)
""")

print("Default indent (2 spaces):")
print(flon.pretty('users'))
print()

print("Custom indent (4 spaces):")
print(flon.pretty('users', indent=4))
print()

# Example 6: Setting environment variables
print("=== Example 6: Environment Variables ===")
flon._env('indent', 4)
print("Indent set to 4, pretty output:")
print(flon.pretty('users'))
print()

# Example 7: Working with lists
print("=== Example 7: Lists ===")
flon.parse("""
@api (
    endpoints: list: ["/users", "/posts", "/comments"]
    ports: list: [8080, 8081, 8082]
)
""")

endpoints = flon.get('api/endpoints')
ports = flon.get('api/ports')

for endpoint, port in zip(endpoints, ports):
    print(f"Endpoint {endpoint} on port {port}")
print()

# Example 8: Error handling
print("=== Example 8: Error Handling ===")
try:
    value = flon.get('nonexistent/path')
except KeyError as e:
    print(f"Caught error: {e}")

try:
    value = flon.get('users', 'invalid_mode')
except ValueError as e:
    print(f"Caught error: {e}")