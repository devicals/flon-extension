"""
Advanced Parsing Examples
Demonstrates complex use cases and patterns
"""

from flexion import flon
from typing import Dict, Any, List

# Example 1: Configuration Manager Class
print("=== Example 1: Configuration Manager ===")

class ConfigManager:
    """Manages application configuration from FLON files"""
    
    def __init__(self, config_file: str):
        flon.load(config_file)
        self.config = flon.get('root/config')
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value with optional default"""
        return self.config.get(key, default)
    
    def get_type(self, key: str) -> str:
        """Get the type of a config value"""
        return flon.get(f'root/config/{key}', 'type')
    
    def validate_required(self, *keys: str) -> List[str]:
        """Validate that required keys exist"""
        missing = []
        for key in keys:
            if key not in self.config:
                missing.append(key)
        return missing

# Usage
flon.parse("""
@root/config (
    host: "localhost"
    port: int: 8080
    debug: bool: true
)
""")

config = ConfigManager('dummy')  # Would use actual file
print(f"Host: {config.get('host')}")
print(f"Port: {config.get('port', 3000)}")
print(f"Missing keys: {config.validate_required('host', 'port', 'database')}")
print()

# Example 2: Schema Validator
print("=== Example 2: Schema Validator ===")

class SchemaValidator:
    """Validate data against a schema"""
    
    def __init__(self, schema_data: Dict[str, str]):
        self.schema = schema_data
    
    def validate(self, data: Dict[str, Any]) -> List[str]:
        """Validate data and return list of errors"""
        errors = []
        
        for field, expected_type in self.schema.items():
            if field not in data:
                errors.append(f"Missing required field: {field}")
                continue
            
            actual_value = data[field]
            actual_type = type(actual_value).__name__
            
            # Map Python types to Flexion types
            type_map = {
                'str': 'string',
                'int': 'int',
                'float': 'float',
                'bool': 'bool',
                'dict': 'object',
                'list': 'list'
            }
            
            flexion_type = type_map.get(actual_type, actual_type)
            
            if flexion_type != expected_type:
                errors.append(
                    f"Type mismatch for {field}: "
                    f"expected {expected_type}, got {flexion_type}"
                )
        
        return errors

# Usage
schema = {
    'username': 'string',
    'age': 'int',
    'email': 'string',
    'active': 'bool'
}

validator = SchemaValidator(schema)

# Valid data
valid_data = {
    'username': 'alice',
    'age': 30,
    'email': 'alice@example.com',
    'active': True
}

errors = validator.validate(valid_data)
print(f"Valid data errors: {errors if errors else 'None'}")

# Invalid data
invalid_data = {
    'username': 'bob',
    'age': '30',  # Wrong type (string instead of int)
    'active': True
    # Missing email
}

errors = validator.validate(invalid_data)
print(f"Invalid data errors: {errors}")
print()

# Example 3: Nested Data Navigator
print("=== Example 3: Nested Data Navigator ===")

class DataNavigator:
    """Navigate complex nested structures"""
    
    def __init__(self):
        self.data = None
    
    def load(self, content: str):
        """Load FLON content"""
        flon.parse(content)
        self.data = flon.get('root')
    
    def find_all(self, key: str) -> List[Any]:
        """Find all occurrences of a key in nested structure"""
        results = []
        self._search(self.data, key, results)
        return results
    
    def _search(self, obj: Any, key: str, results: List):
        """Recursively search for key"""
        if isinstance(obj, dict):
            if key in obj:
                results.append(obj[key])
            for value in obj.values():
                self._search(value, key, results)
        elif isinstance(obj, list):
            for item in obj:
                self._search(item, key, results)

# Usage
navigator = DataNavigator()
navigator.load("""
@root (
    user: object: (
        name: "Alice"
        email: "alice@example.com"
        settings: object: (
            theme: "dark"
            notifications: object: (
                email: bool: true
            )
        )
    )
    admin: object: (
        name: "Bob"
        email: "bob@example.com"
    )
)
""")

# Find all 'email' fields
emails = navigator.find_all('email')
print(f"Found emails: {emails}")

# Find all 'name' fields
names = navigator.find_all('name')
print(f"Found names: {names}")
print()

# Example 4: Dynamic Query Builder
print("=== Example 4: Dynamic Query Builder ===")

class QueryBuilder:
    """Build queries from FLON configuration"""
    
    def __init__(self, config_content: str):
        flon.parse(config_content)
        self.config = flon.get('root/query')
    
    def build_sql(self) -> str:
        """Generate SQL from config"""
        table = self.config.get('table', 'users')
        fields = self.config.get('fields', ['*'])
        where = self.config.get('where', {})
        limit = self.config.get('limit', None)
        
        # Build query
        fields_str = ', '.join(fields)
        query = f"SELECT {fields_str} FROM {table}"
        
        if where:
            conditions = [f"{k} = '{v}'" for k, v in where.items()]
            query += " WHERE " + " AND ".join(conditions)
        
        if limit:
            query += f" LIMIT {limit}"
        
        return query + ";"

# Usage
query_config = """
@root/query (
    table: "users"
    fields: list: ["id", "username", "email"]
    where: object: (
        active: "true"
        role: "admin"
    )
    limit: int: 10
)
"""

builder = QueryBuilder(query_config)
sql = builder.build_sql()
print(f"Generated SQL: {sql}")
print()

# Example 5: Multi-Environment Config
print("=== Example 5: Multi-Environment Config ===")

class EnvironmentConfig:
    """Manage configurations for multiple environments"""
    
    def __init__(self, base_path: str = 'configs'):
        self.configs = {}
        self.base_path = base_path
    
    def load_environment(self, env: str):
        """Load config for specific environment"""
        # In real use, would load from file
        # For demo, we'll parse inline
        if env == 'development':
            content = """
@root (
    debug: bool: true
    host: "localhost"
    port: int: 3000
)
"""
        elif env == 'production':
            content = """
@root (
    debug: bool: false
    host: "api.example.com"
    port: int: 443
)
"""
        else:
            content = """
@root (
    debug: bool: false
    host: "staging.example.com"
    port: int: 8080
)
"""
        
        flon.parse(content)
        self.configs[env] = flon.get('root')
    
    def get_config(self, env: str) -> Dict[str, Any]:
        """Get configuration for environment"""
        if env not in self.configs:
            self.load_environment(env)
        return self.configs[env]

# Usage
env_config = EnvironmentConfig()

for environment in ['development', 'staging', 'production']:
    config = env_config.get_config(environment)
    print(f"{environment.capitalize()}:")
    print(f"  Debug: {config['debug']}")
    print(f"  Host: {config['host']}")
    print(f"  Port: {config['port']}")
print()

# Example 6: Data Transformer
print("=== Example 6: Data Transformer ===")

class DataTransformer:
    """Transform FLON data into different formats"""
    
    @staticmethod
    def to_env_vars(data: Dict[str, Any], prefix: str = '') -> Dict[str, str]:
        """Convert nested dict to flat environment variables"""
        env_vars = {}
        
        for key, value in data.items():
            env_key = f"{prefix}{key}".upper()
            
            if isinstance(value, dict):
                nested = DataTransformer.to_env_vars(value, f"{env_key}_")
                env_vars.update(nested)
            else:
                env_vars[env_key] = str(value)
        
        return env_vars

# Usage
flon.parse("""
@root (
    database: object: (
        host: "localhost"
        port: int: 5432
    )
    cache: object: (
        ttl: int: 3600
    )
)
""")

data = flon.get('root')
env_vars = DataTransformer.to_env_vars(data)

print("Environment variables:")
for key, value in env_vars.items():
    print(f"  {key}={value}")