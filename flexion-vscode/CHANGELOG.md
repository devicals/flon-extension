# Change Log

All notable changes to the "flexion-language" extension will be documented in this file.
All dates are formatted DD/MM/YYYY.

## [1.10.0] - 01/01/2026
### Added
- **Improved List Parsing**: The internal panel parser now supports Flexion lists `list: [...]` for configuration.

### Changed
- **Unified Icons**: All icons are now the same as the sidebar "flon" icon.

### Fixed
- **Label Parsing**: Fixed a bug where labels containing hyphens (e.g., `comparison-commented`) were ignored by the panel engine.
- **Bracket Counting**: Replaced regex-based block detection with a robust bracket-counting algorithm to prevent nested objects from "leaking" into the sidebar.

## [1.9.2] - 31/12/2025
### Changed
- **Icon**: Updated panel/sidebar icon from the "F" to "flon" (without it rendering as a filled square).

## [1.9.0] - 31/12/2025
- Minor Panel Bug Fixes

### Changed
- **TOC Tabs**: TOC tabs are now merged with the original markdown tabs.

## [1.8.2] - 31/12/2025
- Minor Bug Fixes

## [1.8.0] - 30/12/2025
### Added
- **Evaluated Expressions**: Introduced `$(...)` syntax for dynamic values.
  - Supports arithmetic (`ex: int: $(5 + 5)`)
  - Supports string concatenation (`ex: string: $("hello" + " world")`)
  - Supports boolean logic (`ex: bool: $(!false)`)
- **Expression Hovers**: Hovering over an expression now displays the expected resulting type based on the preceding type annotation.
- **Enhanced Syntax Highlighting**: Expressions now have distinct coloring for operators and delimiters.

## [1.7.0] - 30/12/2025
### Added
- Dynamic Panel Engine
- **Table of Contents (TOC) Tabs**: Markdown files with `jump: true` now automatically generate a collapsible "Table of Contents" sub-tab in the sidebar, allowing direct navigation to specific headers.
- **Virtual Read-Only Files**: Examples opened from the sidebar are now served via a custom `flexion-sample://` URI scheme, preventing accidental edits or overwrites to extension resources.
- UI De-cluttering

### Changed
- **Panel Logic**: Moved from a hardcoded sidebar structure to a lightweight Flexion-based parser that handles path-based navigation within the definition file.
- **Navigation Flow**: "Wiki Page" navigation now resets the scroll position to the top of the preview when clicked.

## [1.5.1] - 30/12/2025
- Minor Bug Fixes

## [1.5.0] - 30/12/2025
### Fixed
- **Minimap Fix**: Resolved issue where comments appeared "giant" on the minimap due to improper grammar boundaries.
- **Hovers**: Expanded hover tooltips to include all type aliases (str, integer, decimal, null, etc.).
- **Value Detection**: Improved value detection logic in hovers (keywords correctly show as string).

### Added
- **Autocomplete**: Real-time IntelliSense suggestions for all Flexion types.
- **Advanced Sidebar**: Collapsible Help and Feedback panel with separate sections for Documentation and Examples.
- **Comparison Example**: Added a dedicated JSON vs FLON comparison guide.

## [1.3.0] - 29/12/2025
### Fixed
- **Validation**: Comments (`!`) are now correctly ignored by the template validator; no more fake errors in comments.
- **Sidebar**: Fixed "Open Wiki" and Sidebar links which were previously unresponsive.
- **Path Resolution**: Correctly handles nested paths like `@root/phones` and standalone references like `@phones`.

### Added
- **Reverse Navigation**: Ctrl+Clicking a `@templates` definition now jumps to its first usage.

## [1.2.0] - 29/12/2025
### Added
- **IntelliSense Hover**: Hover over types (string, int, etc.) to see descriptions.
- **Type Detection**: Hover over values (like "123" or "true") to see their interpreted data type.
- **Template Validation**: Real-time error checking for missing template definitions.

## [1.0.0] - 29/12/2025
- Initial Release

### Added
- Syntax highlighting for Flexion files
- Code snippets for common patterns
- Language configuration with auto-closing pairs
- Comment support (! and !! !!)
- Bracket matching and auto-closing
- Code folding support