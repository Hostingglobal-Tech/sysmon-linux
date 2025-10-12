# Code Style and Conventions

## Python Style Guidelines
The project follows standard Python conventions with specific patterns:

### Naming Conventions
- **Classes**: PascalCase (`SystemMonitor`)
- **Methods**: snake_case (`get_uptime`, `get_cpu_usage`, `format_display`)
- **Variables**: snake_case (`uptime_seconds`, `total_processes`, `high_cpu_count`)
- **Constants**: UPPER_CASE (`RED`, `GREEN`, `YELLOW`, `BLUE`, `BOLD`, `RESET`, `CLEAR`)
- **Private methods**: Not used in this project (all methods are public)

### Documentation Style
- **Module docstring**: Triple quotes with brief description
- **Class docstring**: Describes purpose and functionality
- **Method docstrings**: Google-style with Args and Returns sections
```python
def get_uptime(self):
    """Get system uptime and load average from /proc
    
    Returns:
        dict: Dictionary with uptime string and load average
    """
```

### Code Organization
- **Imports**: Standard library imports grouped at top
- **Class structure**: Single main class with logical method grouping:
  - Initialization (`__init__`)
  - Data collection methods (`get_*`)
  - Display methods (`format_display`)
  - Control methods (`run`, `stop`, `signal_handler`)

### Error Handling
- **Pattern**: Try-except blocks with graceful fallbacks
- **Default values**: Always provide sensible defaults when operations fail
- **Multiple fallbacks**: CPU usage calculation has multiple fallback methods

### Color and Display
- **ANSI codes**: Manual color code definitions (not using external libraries)
- **Conditional formatting**: Color disabled with `--no-color` flag
- **Clear screen**: Uses ANSI escape sequences for terminal control

### Code Structure Patterns
- **Single responsibility**: Each method handles one specific system metric
- **Error resilience**: All data collection methods return safe defaults on failure
- **Resource efficiency**: Direct `/proc` filesystem access over external tools