# Technology Stack and Dependencies

## Core Technology
- **Language**: Python 3.6+
- **Dependencies**: None (uses only Python standard library)
- **Platform**: Linux only (requires `/proc` filesystem)

## Standard Library Modules Used
- `os` - Operating system interface and CPU count
- `sys` - System-specific parameters and exit functionality  
- `time` - Time-related functions and sleep
- `signal` - Signal handling for graceful shutdown
- `argparse` - Command-line argument parsing
- `subprocess` - Running external commands (`ps aux`, `top`)
- `datetime` - Date and time manipulation for uptime calculation

## Optional Dependencies (Currently Commented Out)
```python
# psutil>=5.9.0        # For more detailed system information
# colorama>=0.4.6      # For Windows terminal color support  
# rich>=13.0.0         # For advanced terminal UI
```

## Development Dependencies (Currently Commented Out)
```python
# pytest>=7.0.0        # For running tests
# pyinstaller>=5.0     # For creating standalone executables
```

## System Requirements
- **OS**: Linux with `/proc` filesystem access
- **Python**: 3.6 or higher
- **Permissions**: Read access to `/proc` directory
- **Terminal**: ANSI color code support (optional, can disable with `-n` flag)

## Distribution
- **Package Manager**: npm (Node.js ecosystem) via package.json
- **Installation Methods**: 
  - Direct execution: `./sysmon.py`
  - System-wide: `sudo cp sysmon.py /usr/local/bin/sysmon`
  - Global npm install: `npm install -g sysmon-linux`