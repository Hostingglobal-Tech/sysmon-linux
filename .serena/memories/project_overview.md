# System Monitor (sysmon) - Project Overview

## Project Purpose
This is a real-time Linux system monitoring tool called "sysmon" that displays CPU, memory, processes, and uptime information in a clean, colorful command-line interface. The tool is designed to help system administrators and developers quickly assess system health and identify resource-intensive processes.

## Key Features
- **Real-time System Monitoring**: System uptime, load average, CPU usage, process count, and memory usage
- **High CPU Process Detection**: Shows detailed information about processes using ≥90% CPU  
- **Performance Optimized**: Uses `/proc` filesystem for fast data collection with no external dependencies
- **Color-coded Display**: Resource usage levels are color-coded for quick visual assessment
- **CLI Interface**: Multiple command-line options for different monitoring scenarios

## Technical Architecture
- **Language**: Python 3.6+ (uses only standard library)
- **Platform**: Linux only (tested on Ubuntu, Debian, CentOS)
- **Data Sources**: `/proc` filesystem (`/proc/uptime`, `/proc/loadavg`, `/proc/stat`, `/proc/meminfo`) and `ps aux` command
- **Design Pattern**: Single class (`SystemMonitor`) with modular methods for different system metrics

## Project Structure
```
sysmon/
├── sysmon.py          # Main application (417 lines)
├── sysmon.py.broken   # Backup/broken version 
├── requirements.txt   # Dependencies (uses standard library only)
├── package.json       # Node.js package metadata for distribution
├── README.md          # Comprehensive documentation
├── LICENSE           # MIT License
└── .serena/          # Serena MCP configuration
```

## Development Status
- **Version**: 1.0.0 (Initial release)
- **License**: MIT
- **Repository**: https://github.com/Hostingglobal-Tech/sysmon-linux
- **Maintenance**: Active development project