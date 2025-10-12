# sysmon - Linux System Monitor

A real-time Linux system monitoring tool that displays CPU, memory, processes, and uptime information in a clean, colorful interface.

## Features

**Real-time System Monitoring**
- System uptime and load average
- CPU usage percentage (accurate calculation)
- Process count with high CPU process detection (>=90%)
- Memory usage with color-coded alerts
- Color-coded display based on resource usage levels

**High CPU Process Detection**
- Shows detailed information about processes using >=90% CPU
- Displays process name, PID, and exact CPU percentage
- Helps quickly identify resource-hungry applications

**Python 3.14 Free-Threading Support**
- Multi-threaded parallel data collection for faster updates
- Automatic detection of Python 3.14 free-threading mode (GIL disabled)
- True parallel execution on multi-core systems when GIL is disabled
- Backward compatible with standard Python (GIL enabled)

**Performance Optimized**
- Uses `/proc` filesystem for fast data collection
- Parallel data collection reduces wait time (especially with Python 3.14t)
- No external dependencies beyond standard Python libraries
- Lightweight and efficient

## Installation

### Quick Start

1. Clone or download the script:
```bash
cd /path/to/sysmon
chmod +x sysmon.py
```

2. Run directly:
```bash
./sysmon.py
```

### System-wide Installation

```bash
sudo cp sysmon.py /usr/local/bin/sysmon
sudo chmod +x /usr/local/bin/sysmon
```

## Usage

### Basic Usage
```bash
# Default: updates every 60 seconds with multi-threading
sysmon

# Custom interval (e.g., 5 seconds)
sysmon -i 5

# Single display and exit
sysmon --once

# No color output
sysmon -n

# Disable multi-threading (sequential data collection)
sysmon --no-threading
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --interval` | Update interval in seconds | 60 |
| `-n, --no-color` | Disable colored output | False |
| `--no-threading` | Disable multi-threading for data collection | False |
| `--once` | Display once and exit | False |
| `-h, --help` | Show help message | - |

## Examples

### Monitor with 10-second updates
```bash
sysmon -i 10
```

### Quick system check
```bash
sysmon --once
```

### Continuous monitoring without colors (for logs)
```bash
sysmon -n -i 30 > system_monitor.log
```

### Test Python 3.14 free-threading performance
```bash
# With threading (default, parallel data collection)
time sysmon --once

# Without threading (sequential data collection)
time sysmon --once --no-threading

# Compare performance difference
```

### Run with Python 3.14 free-threading build
```bash
# If you have python3.14t installed
python3.14t sysmon.py --once

# Or with pyenv
pyenv local 3.14.0t
python sysmon.py
```

## Output Example

```
==================================================
    LINUX SYSTEM MONITOR
==================================================
Last Update: 2024-01-19 15:30:45
Threading: Enabled | Python Mode: Standard (GIL Enabled)
--------------------------------------------------
Uptime: 5d 3h 45m
Load Average: 1.25 1.18 1.05
CPU: 75.5% (4 cores)
Processes: 245 total, 2 high CPU (>=90%)
   └─ stress-ng (PID 12345, 95.2% CPU)
   └─ python3 (PID 12346, 92.1% CPU)
Memory: 4096MB / 8192MB (50.0%)
--------------------------------------------------
Refresh interval: 60s | Press Ctrl+C to exit
```

### With Python 3.14 Free-Threading Mode
```
==================================================
    LINUX SYSTEM MONITOR
==================================================
Last Update: 2024-01-19 15:30:45
Threading: Enabled | Python Mode: Free-threading (GIL Disabled)
--------------------------------------------------
Uptime: 5d 3h 45m
Load Average: 1.25 1.18 1.05
CPU: 75.5% (4 cores)
Processes: 245 total, 0 high CPU (>=90%)
Memory: 4096MB / 8192MB (50.0%)
--------------------------------------------------
Refresh interval: 60s | Press Ctrl+C to exit
```

## System Requirements

- **OS**: Linux (tested on Ubuntu, Debian, CentOS)
- **Python**: 3.6 or higher (3.14+ recommended for free-threading support)
- **Permissions**: Read access to `/proc` filesystem

### Recommended for Best Performance
- **Python 3.14t**: Free-threading build (GIL disabled) for true parallel execution
  ```bash
  # Install Python 3.14 free-threading build with pyenv
  pyenv install 3.14.0t
  pyenv local 3.14.0t
  ```

## How It Works

The tool reads system information directly from the Linux `/proc` filesystem and uses system commands:
- `/proc/uptime` - System uptime
- `/proc/loadavg` - Load average information
- `/proc/stat` - CPU usage calculation
- `/proc/meminfo` - Memory statistics
- `ps aux` - Real-time process CPU usage for high CPU detection (≥90%)

### Multi-Threading Architecture

By default, `sysmon` uses Python's `ThreadPoolExecutor` to collect data in parallel:
1. **Uptime collection** - Reads `/proc/uptime` and `/proc/loadavg`
2. **CPU monitoring** - Calculates CPU usage from `/proc/stat`
3. **Process scanning** - Scans `/proc` and runs `ps aux` for high CPU processes
4. **Memory analysis** - Reads `/proc/meminfo`

These four tasks run simultaneously, reducing total collection time from ~1+ second to near-instant.

### Python 3.14 Free-Threading Benefits

When running with Python 3.14 free-threading build (`python3.14t`):
- **True Parallelism**: No Global Interpreter Lock (GIL) means all 4 threads execute simultaneously
- **Multi-Core Utilization**: Each thread can run on a separate CPU core
- **Faster Updates**: Parallel data collection is significantly faster on multi-core systems
- **Backward Compatible**: Works seamlessly with standard Python (GIL enabled)

To check if you're running in free-threading mode:
```bash
python3 -c "import sysconfig; print('Free-threading:', sysconfig.get_config_var('Py_GIL_DISABLED') == 1)"
```

## Color Coding

Memory usage is color-coded for quick status assessment:
- **Green**: < 60% usage (healthy)
- **Yellow**: 60-80% usage (moderate)
- **Red**: > 80% usage (high)

## Troubleshooting

### Permission Denied
If you encounter permission errors, ensure you have read access to `/proc`:
```bash
ls -la /proc/uptime
```

### No Color in Terminal
Some terminals may not support ANSI color codes. Use the `-n` flag to disable colors.

### High CPU Usage
If monitoring at very short intervals (< 5 seconds), consider increasing the interval to reduce system load.

## Development

### Running Tests
```bash
python3 -m unittest test_sysmon.py
```

### Contributing
Feel free to submit issues or pull requests for improvements.

## License

MIT License - Feel free to use and modify as needed.

## Author

System Monitor CLI Tool - Created as part of Linux system administration toolkit.

## Version

**2.0.0** - Python 3.14 Free-Threading Support
- Added multi-threaded parallel data collection
- Automatic detection of Python 3.14 free-threading mode
- New `--no-threading` option for sequential data collection
- Display threading and GIL status in output
- Performance improvements with parallel execution

**1.0.0** - Initial release with core monitoring features