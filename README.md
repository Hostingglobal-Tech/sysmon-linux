# sysmon - Linux System Monitor

A real-time Linux system monitoring tool that displays CPU, memory, processes, and uptime information in a clean, colorful interface.

## Features

🖥️ **Real-time System Monitoring**
- ⏱️ System uptime and load average
- 💻 CPU usage percentage (accurate calculation)
- 📊 Process count with high CPU process detection (≥90%)
- 💾 Memory usage with color-coded alerts
- 🎨 Color-coded display based on resource usage levels

🔍 **High CPU Process Detection**
- Shows detailed information about processes using ≥90% CPU
- Displays process name, PID, and exact CPU percentage
- Helps quickly identify resource-hungry applications

⚡ **Performance Optimized**
- Uses `/proc` filesystem for fast data collection
- No external dependencies beyond standard Python libraries
- Lightweight and efficient

## Installation

### Quick Start

1. Clone or download the script:
```bash
cd /home/nmsglobal/DEVEL/CHATGPT5_PLAN/sysmon
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
# Default: updates every 60 seconds
sysmon

# Custom interval (e.g., 5 seconds)
sysmon -i 5

# Single display and exit
sysmon --once

# No color output
sysmon -n
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --interval` | Update interval in seconds | 60 |
| `-n, --no-color` | Disable colored output | False |
| `--once` | Display once and exit | False |
| `-v, --version` | Show version information | - |
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

## Output Example

```
==================================================
    LINUX SYSTEM MONITOR
==================================================
Last Update: 2024-01-19 15:30:45
--------------------------------------------------
⏱  Uptime: 5d 3h 45m
📈 Load Average: 1.25 1.18 1.05
💻 CPU: 75.5% (4 cores)
📊 Processes: 245 total, 2 high CPU (≥90%)
   └─ stress-ng (PID 12345, 95.2% CPU)
   └─ python3 (PID 12346, 92.1% CPU)
💾 Memory: 4096MB / 8192MB (50.0%)
--------------------------------------------------
Refresh interval: 60s | Press Ctrl+C to exit
```

## System Requirements

- **OS**: Linux (tested on Ubuntu, Debian, CentOS)
- **Python**: 3.6 or higher
- **Permissions**: Read access to `/proc` filesystem

## How It Works

The tool reads system information directly from the Linux `/proc` filesystem and uses system commands:
- `/proc/uptime` - System uptime
- `/proc/loadavg` - Load average information
- `/proc/stat` - CPU usage calculation
- `/proc/meminfo` - Memory statistics
- `ps aux` - Real-time process CPU usage for high CPU detection (≥90%)

## Color Coding

Memory usage is color-coded for quick status assessment:
- 🟢 **Green**: < 60% usage (healthy)
- 🟡 **Yellow**: 60-80% usage (moderate)
- 🔴 **Red**: > 80% usage (high)

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

1.0.0 - Initial release with core monitoring features