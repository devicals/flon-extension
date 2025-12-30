# Flexion Language Support for VS Code

Provides syntax highlighting, code snippets, and language configuration for Flexion (.flon) files.

## Features

- **Syntax Highlighting**: Full syntax highlighting for all Flexion constructs
  - Path declarations
  - Templates
  - References
  - Types and values
  - Comments (single-line and block)

- **Code Snippets**: Quick snippets for common patterns
  - Path declarations
  - Templates
  - Objects and lists
  - Type annotations
  - Comments

- **Auto-Completion**: Auto-closing brackets and quotes

- **Code Folding**: Fold path declarations and nested structures

- **IntelliSense & Hovers**:
  - Hover over built-in types to see documentation.
  - Hover over values to see detected data types (string, int, float, bool).

- **Navigation**:
  - `Ctrl + Click` to jump to `#template` definitions or usage.
  - This does not work on `@paths/references` as intended behavior, however sometimes you may be able to still jump to `@reference` definitions. *This is cause of a bug, but will not be fixed.*

- **Formatting**:
  - Automatic indentation and cleanup via `Format Document`.

- **Diagnostics**:
  - Validation for undefined templates.

## Usage

Access the **Flexion Wiki** via the sidebar icon or by running the command `Flexion: Open Wiki` from the Command Palette (`Ctrl+Shift+P`).

### Snippets

Type the prefix and press Tab to expand:

| Prefix | Description |
|--------|-------------|
| `root` | Create @root path |
| `path` | Create path declaration |
| `template` | Define a template |
| `use-template` | Use a template |
| `obj` | Create object |
| `list` | Create list |
| `ref` | Create reference |
| `str`, `int`, `float`, `bool` | Typed values |

### Syntax Highlighting

The extension provides rich syntax highlighting for:
- **Blue**: Path declarations (@root, @path/name)
- **Purple**: Types (string, int, bool, etc.)
- **Green**: Strings
- **Orange**: Numbers
- **Blue**: Booleans
- **Gray**: Comments
- **Yellow**: Template names

## Requirements

VS Code version 1.75.0 or higher

## Contributing

Contributions are welcome! Please submit issues and pull requests to the GitHub repository.

## License

Copyright 2025 ~ 2026 Error Dev

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.