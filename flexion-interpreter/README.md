# Flexion Language Guide

Welcome to the Flexion Language documentation. This guide provides an exhaustive overview of the Flexion syntax, data structures, VS Code extension features, and the Python Interpreter API.

Flexion is a flexible, human-readable data serialization format that combines the best features of JSON, YAML, and custom configuration languages. It uses the `.flon` file extension.

---

## Introduction

Flexion is designed to be cleaner and more intuitive than JSON while maintaining full compatibility with modern data requirements. 

**Key Features:**
- Optional type annotations for data validation.
- Multiple bracket styles (`()`, `[]`, `{}`) are completely interchangeable.
- Template system for defining reusable data structures.
- Path-based organization for logical data grouping.
- Reference system for linking data across different sections.
- Evaluated expressions for dynamic value calculation.
- Flexible formatting where commas and newlines are interchangeable.
- Support for single-line and block comments.

---

## Basic Syntax

### Path Declarations (Items)

Items are the primary containers in Flexion, defined with the `@` symbol. All data must be organized under a path. The `@root` path is typically the top-level container.

```flon
@root (
    key: value
)

@root/nested/path (
    data: "value"
)
```

Paths use the forward slash `/` as a separator to create hierarchical structures.

### Comments

Flexion supports single-line and block comments to document data structures.

```flon
! This is a single-line comment

!! 
This is a 
block comment
!!
```

---

## Data Types

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

### Type Annotations

Types are optional and placed between the label and the value. Specifying types is a best practice for critical fields requiring validation.

```flon
name: string: "Jane Doe"
age: int: 35
active: bool: true
price: float: 19.99
```

### Type Detection

If no type is specified, the Flexion interpreter auto-detects the type based on the value's format:

```flon
name: "Jane"        ! Detected as string
age: 35             ! Detected as int
price: 19.99        ! Detected as float
active: true        ! Detected as bool
city: Anytown       ! Detected as string (keyword)
```

### Keywords vs Strings

**Keywords** are unquoted alphanumeric strings (underscores allowed). If a string value does not contain special characters or spaces, quotes can be omitted.

```flon
city: keyword: Anytown    ! Value is "Anytown" (string)
city: Anytown             ! Auto-detected as string
```

**Note:** A keyword value being detected and displayed as a `string` by tooltips or the interpreter is intended behavior.

---

## Values and Structures

### Simple Values

Simple values include strings, numbers, booleans, and null-equivalents.

```flon
@root (
    id: "12345"
    count: 42
    active: true
    price: 29.99
)
```

### Objects

Objects can use `()`, `[]`, or `{}` interchangeably. The only requirement is that the opening and closing brackets must match.

```flon
address: object: (
    street: "123 Main St"
    city: "Anytown"
    zip: "12345"
)

! All of these are valid and identical:
address: object: { ... }
address: object: [ ... ]
address: ( ... )
```

### Lists and Arrays

Lists can be formatted inline or across multiple lines. When using multiple lines, commas between items are optional.

```flon
! Inline
tags: ["json", "example", "data"]

! Multi-line
tags: [
    "json"
    "example"
    "data"
]

! Typed list items
numbers: list::int: [1, 2, 3, 4, 5]
```

### Void, Null, and Undefined

These types represent an empty or null value. The "void" keyword is treated as the type; any value provided is ignored and set to undefined.

```flon
metadata: void           ! No value needed
data: null               ! Also valid
info: undefined          ! Also valid
```

---

## Advanced Features

### Unlabeled Items

The underscore `_` is used as a label for items that do not require a specific name, often used within nested objects or lists.

```flon
phoneNumbers: (
    _: object: [
        type: "home"
        number: "555-1234"
    ]
)
```

### References

References allow you to link one path to another using the `@` symbol. This avoids data duplication and allows for complex relational modeling.

```flon
@root (
    mainData: @data_section
    metadata: @metadata_value
)

@data_section (
    info: "This data is referenced above"
)

@metadata_value (
    _: void
)
```

References can be simplified to the unique portion of the path (e.g., `@phones` instead of `@root/phones`) if no naming collisions exist.

### Type Alternatives

Use the pipe `|` symbol to specify multiple valid types for a single field.

```flon
coordinates: object | list: {
    latitude: 40.7128
    longitude: -74.0060
}
```

### Evaluated Expressions

Flexion supports dynamic value calculation using the `$(...)` syntax. These are calculated at runtime by the interpreter.

```flon
@root (
    sum: int: $(10 + 5)             ! Evaluates to 15
    fullName: string: $("A" + "B")  ! Evaluates to "AB"
    isAllowed: bool: $(!true)       ! Evaluates to false
    ratio: float: $(10 / 3.0)       ! Evaluates to 3.333...
)
```

**Expression Logic Rules:**
1. The expression should return a value compatible with the defined type.
2. Expressions can be used anywhere a standard value is accepted.
3. Strings within expressions must be double-quoted.

### Templates

Templates allow you to define reusable structures, reducing the need to repeat labels and types.

**Defining Templates:**
Templates are defined using the `@templates` keyword.

```flon
@templates contact_info (
    type: keyword
    number: string
)
```

**Using Templates:**
Template usage is indicated with the `#` symbol. Values are matched to template fields in the order they are defined.

```flon
@root/contacts (
    #contact_info (home, "555-1234")
    #contact_info (mobile, "555-5678")
)

! Multi-line formatting for templates
#contact_info (
    mobile
    "555-5678"
)
```

---

## Formatting Rules

### Interoperability
- **Commas:** Optional when items are separated by newlines.
- **Whitespace:** Flexible. `key:type:value` is as valid as `key : type : value`.
- **Brackets:** All styles are interchangeable but must match. `( ... }` is invalid.

---

## VS Code Extension Features

### Syntax Highlighting
- **Blue:** Path declarations and references.
- **Purple:** Data types.
- **Green:** String values.
- **Orange:** Numeric values.
- **Gray:** Comments.
- **Yellow:** Template names.

### IntelliSense and Hovers
- **Type Hovers:** Hover over built-in types (string, int, etc.) to see documentation.
- **Value Hovers:** Hover over values to see the type detected by the interpreter.
- **Expression Hovers:** Hover over `$(...)` to see the evaluated result type.
- **Autocomplete:** Type `:` to see all available data types.

### Navigation and Validation
- **Go to Definition:** `Ctrl+Click` on an `@reference` to go to the declaration.
- **Template Navigation:** `Ctrl+Click` on a `#template` to jump to the `@templates` definition.
- **Diagnostics:** Real-time error checking for undefined templates or missing references.

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
    age: $(20 + 15)
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
        #phone_entry (home, "555-1234")
        #phone_entry (mobile, "555-5678")
    ]
)

@metadata_value (
    _: void
)
```

---

## Python Interpreter API

### Basic Usage

The interpreter allows for programmatic interaction with `.flon` files.

```python
from flexion import flon

# Load from file
flon.load('data.flon')

# Parse from string
flon.parse(content)
```

### Accessing Data

Data is accessed using path notation.

```python
# Get value at path
name = flon.get('root/name')
city = flon.get('root/address/city')

# With default value fallback
country = flon.get('root/address/country', default='Unknown')
```

### Type Information

```python
# Get the defined or detected type of a value
type_name = flon.get_type('root/age')  # Returns: 'int'
```

### Listing and Existence

```python
# Check if a path exists
if flon.exists('root/email'):
    email = flon.get('root/email')

# Get all keys at a specific path
root_keys = flon.keys('root')
```

### Format Conversion

The interpreter includes a `converter` module for bidirectional JSON support.

```python
from interpreter import converter

# Convert FLON file to JSON
converter.convert('data.flon', 'json')

# Convert JSON string to FLON file
converter.convert_data(json_content, 'flon', 'output.flon')
```

---

## Design Philosophy

Flexion is designed to be:
1. **Flexible:** Multiple ways to express the same data.
2. **Human-readable:** Clear syntax with minimal visual noise.
3. **Type-safe:** Optional annotations for robust validation.
4. **Efficient:** Templates and references reduce data repetition.
5. **Organized:** Path-based structures keep related data together.
6. **Forgiving:** Flexible rules for commas, quotes, and whitespace.

---

## Comparison with JSON

| Feature | JSON | Flexion |
|---------|------|---------|
| Comments | No | Yes (Line and Block) |
| Trailing Commas | Forbidden | Optional |
| Type Annotations | No | Yes (Optional) |
| Templates | No | Yes |
| References | No | Yes |
| Expressions | No | Yes |
| Flexible Brackets | No | Yes |
| Quoted Keys | Required | Optional (Keywords) |

---

## Best Practices

1. **Use Type Annotations:** Apply them to critical fields that require strict validation.
2. **Leverage Templates:** Create templates for any structure that repeats more than twice.
3. **Reference Data:** Use `@` references to link shared configuration values instead of duplicating them.
4. **Organize with Paths:** Use descriptive paths (`@auth/users/profiles`) to group related data.
5. **Comment Complex Logic:** Use block comments to explain the purpose of complex data blocks.
6. **Consistent Indentation:** While Flexion is flexible, consistent indentation improves readability.

---

## License

MIT - Copyright 2025 ~ 2026 Error Dev