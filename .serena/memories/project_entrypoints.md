# Project Entrypoints and Usage

## Main Entrypoint
- **Primary executable**: `sysmon.py`
- **Interpreter**: Python 3.6+
- **Shebang**: `#!/usr/bin/env python3`

## Running Methods

### Direct Execution
```bash
# Default mode (60 second intervals, continuous monitoring)
./sysmon.py

# Custom interval
./sysmon.py -i 30

# Single display and exit
./sysmon.py --once

# No color output (for logging or unsupported terminals)
./sysmon.py -n
```

### Via Python Interpreter
```bash
python3 sysmon.py
python3 sysmon.py -i 10 --once
```

### Via npm Scripts (package.json)
```bash
npm start      # Runs: python3 sysmon.py
npm test       # Runs: python3 -m unittest test_sysmon.py (test file doesn't exist yet)
```

## Command Line Arguments

| Option | Long Form | Type | Default | Description |
|--------|-----------|------|---------|-------------|
| `-i` | `--interval` | int | 60 | Update interval in seconds |
| `-n` | `--no-color` | flag | False | Disable colored output |
| | `--once` | flag | False | Show statistics once and exit |
| `-v` | `--version` | flag | | Show version information |
| `-h` | `--help` | flag | | Show help message |

## Usage Examples

### System Administration
```bash
# Quick health check
sysmon --once

# Continuous monitoring with frequent updates
sysmon -i 10

# Log system stats without colors
sysmon -n -i 30 > system_monitor.log

# Background monitoring
nohup sysmon -i 60 > /var/log/sysmon.log 2>&1 &
```

### Development and Debugging
```bash
# High-frequency monitoring for performance testing
sysmon -i 5

# Single snapshot for scripts
sysmon --once | grep "CPU:"
```

## Program Flow
1. **Argument Parsing**: `parse_arguments()` processes command line options
2. **Monitor Creation**: `SystemMonitor` instance created with specified settings
3. **Execution Mode**:
   - **Once mode**: Single data collection and display, then exit
   - **Continuous mode**: Infinite loop with signal handling for graceful shutdown
4. **Data Collection**: Four main metrics collected per cycle:
   - Uptime and load average
   - CPU usage percentage  
   - Process information with high CPU detection
   - Memory statistics
5. **Display**: Formatted output with color coding and emojis

## Signal Handling
- **SIGINT (Ctrl+C)**: Graceful shutdown with cleanup message
- **Signal Handler**: `signal_handler()` method in SystemMonitor class