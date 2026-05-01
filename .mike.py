# CHUNK:  .mike
Reminders to the Gemini AI for Don's code projects

- Strict newline after every conditional/definition colon (:).
- Plain ASCII characters only; no Unicode punctuation.
- PEP-8 formatting except:
    - No empty lines or lines with whitespace only (except in docstrings)
- Classes have '''Manifest [N]: method_a method_b ... property_c''' where N is 
    the current count of methods & properties.
- Maintain "if 1:", "if 0:" blocks 
- Maintain "# CHUNK: ChunkName", "# END_CHUNK: ChunkName" blocks as these enable 
    simple code maintenance in the editor
- Triple quotes: Use ''' for all docstrings and multi-line strings.
- Quotes: Use " for all string definitions (e.g., 'a = "string"').
- Naming: CamelCase for classes/functions, snake_case for attributes/variables.
- Imports: Use 'import x' or 'import x as y'. Use x.y notation in code.
- Type annotations:  use type annotations wherever possible.
- Treat the provided code as a closed set.  Consider it mature code that cannot be 
    broken. Enhancement or "fix" requests must not omit any old code; if a method 
    isn't explicitly changed, include it exactly as-is.  I need the full class for 
    a copy-paste replacement.  No placeholders like "# ... existing code".

# END_CHUNK:  .mike
