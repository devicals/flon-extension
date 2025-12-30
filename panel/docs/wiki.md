# Flexion (.flon) - Flexible Object Notation

## Overview

Flexion is a flexible, human-readable data serialization format that combines the best features of JSON, YAML, and custom configuration languages. It uses the `.flon` file extension.

**Key Features:**
- Optional type annotations
- Multiple bracket styles (interchangeable)
- Templates for reusable structures
- Path-based organization
- Reference system for linking data
- Flexible formatting (commas and newlines are interchangeable)
- Comments and block comments

---

## Basic Syntax

### Comments

```flon
! This is a single-line comment

!! 
This is a 
block comment
!!
```

### Path Declarations

All data is organized under paths using the `@` symbol:

```flon
@root (
    key: value
)

@root/nested/path (
    data: "here"
)
```

The `@root` path is the top level. Paths use `/` as separators.

---

## Data Types

### Type Annotations

Types are optional and placed between the label and value:

```flon
name: string: "Jane Doe"
age: int: 35
active: bool: true
price: float: 19.99
```

### Supported Types

| Type | Aliases | Example |
|------|---------|---------|
| `string` | `str` | `"text"` |
| `keyword` | `unquoted` | `alphanumeric_underscore_only` |
| `integer` | `int` | `42` |
| `float` | `decimal`, `double` | `3.14` |
| `boolean` | `bool` | `true`, `false` |
| `object` | - | `{ key: value }` |
| `list` | `array` | `[1, 2, 3]` |
| `void` | `null`, `undefined` | (no value) |

### Type Detection

If no type is specified, Flexion auto-detects:

```flon
name: "Jane"        ! Detected as string
age: 35             ! Detected as int
price: 19.99        ! Detected as float
active: true        ! Detected as bool
city: Anytown       ! Detected as string (keyword)
```

### Keywords vs Strings

**Keywords** are unquoted alphanumeric text (with underscores allowed):

```flon
city: keyword: Anytown    ! Value is "Anytown" (string)
city: Anytown             ! Auto-detected as string
```

If a string value doesn't need quotes and has no special characters, quotes can be omitted.

> A keyword value being detected as a string is **intended behavior**.

---

## Values

### Simple Values

```flon
@root (
    id: "12345"
    count: 42
    active: true
    price: 29.99
)
```

### Objects

Objects use `()`, `[]`, or `{}` interchangeably. Opening and closing brackets must match:

```flon
address: object: (
    street: "123 Main St"
    city: "Anytown"
    zip: "12345"
)

! All of these are valid:
address: object: { ... }
address: object: [ ... ]
address: ( ... )
```

### Lists/Arrays

Lists can be inline or multi-line:

```flon
! Inline
tags: ["json", "example", "data"]

! Multi-line (commas optional with newlines)
tags: [
    "json"
    "example"
    "data"
]

! Type annotation for list items
numbers: list::int: [1, 2, 3, 4, 5]
```

### Void/Null Values

```flon
metadata: void           ! No value needed
data: null               ! Also valid
info: undefined          ! Also valid
```

---

## Advanced Features

### Unlabeled Items

Use `_` as a label for items that don't need a label:

```flon
phoneNumbers: (
    _: object: [
        type: "home"
        number: "555-1234"
    ]
)
```

### References

Link to other paths using `@`:

```flon
@root (
    mainData: @data_section
    metadata: @metadata_value
)

@data_section (
    info: "This is referenced"
)

@metadata_value (
    _: void
)
```

References can be simplified if unique:
- `@root/phones` can be written as `@phones` if no other `@phones` exists

### Type Alternatives

Use `|` (or) to specify multiple possible types:

```flon
coordinates: object | list: {
    latitude: 40.7128
    longitude: -74.0060
}

coordinates: object|list: (
    latitude: 40.7128
    longitude: -74.0060
)

! Both are valid.
```

---

## Evaluated Expressions

Flexion supports dynamic value calculation using the `$(...)` syntax. These are calculated at runtime by the interpreter.

### Usage

```flon
@root (
    sum: int: $(10 + 5)             ! Evaluates to 15
    fullName: string: $("A" + "B")  ! Evaluates to "AB"
    isAllowed: bool: $(!true)       ! Evaluates to false
    ratio: float: $(10 / 3.0)       ! Evaluates to 3.333...
)

---

## Templates

Templates allow you to define reusable structures without repeating labels and types.

### Defining Templates

```flon
@templates contact_info (
    type: keyword
    number: string
)
```

### Using Templates

Template usage is indicated with `#`:

```flon
@root/contacts (
    #contact_info (
        home, "555-1234"
    )
    
    #contact_info (
        mobile, "555-5678"
    )
)
```

Values are matched to template fields in order. Multiple formatting options:

```flon
#contact_info (
    mobile, "555-5678"
)

! Or with newlines
#contact_info (
    mobile
    "555-5678"
)
```

---

## Formatting Rules

### Commas

Commas are optional when items are separated by newlines:

```flon
! Both valid
tags: ["a", "b", "c"]

tags: [
    "a"
    "b"
    "c"
]
```

### Whitespace

Whitespace is flexible:

```flon
name:string:"Jane"     ! Compact
name: string: "Jane"   ! Readable
```

### Brackets

All bracket types are interchangeable, but must match:

```flon
data: ( ... )    ! Valid
data: { ... }    ! Valid
data: [ ... ]    ! Valid
data: ( ... }    ! INVALID - mismatched
```

---

## Complete Example

```flon
@templates phone_entry (
    type: keyword
    number: string
)

@root (
    id: string: "12345-abc-def"
    isActive: bool: true
    age: 35
    name: "Jane Doe"
    
    address: object: (
        street: "123 Main St"
        city: keyword: Anytown
        zipCode: string: 12345
        isRural: bool: false
    )
    
    phoneNumbers: @phones
    tags: list::string: ["flon", "example", "data", "structure"]
    metadata: @metadata_value
    
    coordinates: object|list: {
        latitude: float: 40.7128
        longitude: -74.0060
    }
)

@root/phones (
    _: [
        #phone_entry (
            home, "555-1234"
        )
        
        #phone_entry (
            mobile, "555-5678"
        )
    ]
)

@metadata_value (
    _: void
)
```

---

## Python Interpreter API

### Basic Usage

```python
from flexion import Flexion

# Load from file
flon = Flexion('data.flon')

# Or parse from string
flon = Flexion()
flon.parse(content)
```

### Accessing Data

```python
# Get value at path
name = flon.get('root/name')
city = flon.get('root/address/city')

# With default value
country = flon.get('root/address/country', 'Unknown')
```

### Type Information

```python
# Get type of value
type_name = flon.get_type('root/age')  # Returns: 'int'
```

### Checking Existence

```python
# Check if path exists
if flon.exists('root/email'):
    email = flon.get('root/email')
```

### Listing Keys

```python
# Get all keys at a path
keys = flon.keys('root')           # ['id', 'name', 'age', ...]
address_keys = flon.keys('root/address')  # ['street', 'city', 'zipCode']
```

### Export to Dictionary

```python
# Get entire structure as dict
data = flon.to_dict()
```

### Complete Example

```python
from flexion import Flexion

# Load file
flon = Flexion('user_data.flon')

# Access nested data
user_name = flon.get('root/name')
street = flon.get('root/address/street')

# Check types
print(f"Age type: {flon.get_type('root/age')}")

# List available keys
print(f"Root keys: {flon.keys('root')}")

# Safe access with defaults
email = flon.get('root/email', 'no-email@example.com')

# Export everything
all_data = flon.to_dict()
```

---

## Error Handling

```python
from flexion import Flexion, FlexionError

try:
    flon = Flexion('data.flon')
    value = flon.get('root/some/path')
except FlexionError as e:
    print(f"Parsing error: {e}")
except FileNotFoundError:
    print("File not found")
```

---

## Design Philosophy

Flexion is designed to be:

1. **Flexible**: Multiple ways to express the same thing
2. **Human-readable**: Clear syntax with optional verbosity
3. **Type-safe**: Optional type annotations for validation
4. **Efficient**: Templates reduce repetition
5. **Organized**: Path-based structure keeps data organized
6. **Forgiving**: Commas, quotes, and whitespace are flexible

---

## Comparison with JSON

| Feature | JSON | Flexion |
|---------|------|---------|
| Comments | ❌ | ✅ |
| Trailing commas | Required | Optional |
| Type annotations | ❌ | ✅ (optional) |
| Templates | ❌ | ✅ |
| References | ❌ | ✅ |
| Flexible brackets | ❌ | ✅ |
| Quoted keys | Required | Optional |

---

## Best Practices

1. **Use type annotations** for critical fields that need validation
2. **Create templates** for repeated structures
3. **Use references** to avoid duplication
4. **Organize with paths** to keep related data together
5. **Add comments** to document complex structures
6. **Use keywords** for simple string values without special characters
7. **Be consistent** with formatting style within a file

---

## License

MIT