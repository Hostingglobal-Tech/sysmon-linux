# Bashrc Setup Guide for sysmon

## Overview
The `~/.bashrc` file has been updated with convenient aliases and functions for quick access to sysmon commands.

## Added Features

### 1. Quick Aliases

| Alias | Description | Command |
|-------|-------------|---------|
| `sysmon` | Default monitoring (60s interval) | `python3 sysmon.py` |
| `sysmon-once` | Show stats once and exit | `python3 sysmon.py --once` |
| `sysmon-fast` | Fast monitoring (5s interval) | `python3 sysmon.py -i 5` |
| `sysmon-no-thread` | Sequential mode (no threading) | `python3 sysmon.py --no-threading` |

### 2. Helper Function

**Command**: `sysmon-help`

Displays comprehensive help information including:
- Basic commands
- Custom options
- Python 3.14 features
- Performance testing examples
- Current Python/GIL status

## Activation

### For Current Session
```bash
source ~/.bashrc
```

### For New Terminals
The aliases will be automatically available in all new terminal sessions.

## Usage Examples

### Quick System Check
```bash
sysmon-once
```

### Fast Monitoring (5-second updates)
```bash
sysmon-fast
```

### Performance Comparison
```bash
# With threading (faster)
time sysmon-once

# Without threading (baseline)
time sysmon-no-thread
```

### Get Help
```bash
sysmon-help
```

### Custom Interval
```bash
sysmon -i 30    # 30-second updates
```

## Location in .bashrc

Lines **204-241** in `~/.bashrc`

```bash
# sysmon - Linux System Monitor (Python 3.14 Free-Threading Support)
alias sysmon='python3 /home/nmsglobal/DEVEL/CHATGPT5_PLAN/sysmon/sysmon.py'
alias sysmon-once='python3 /home/nmsglobal/DEVEL/CHATGPT5_PLAN/sysmon/sysmon.py --once'
alias sysmon-fast='python3 /home/nmsglobal/DEVEL/CHATGPT5_PLAN/sysmon/sysmon.py -i 5'
alias sysmon-no-thread='python3 /home/nmsglobal/DEVEL/CHATGPT5_PLAN/sysmon/sysmon.py --no-threading'
export PATH="$PATH:/home/nmsglobal/DEVEL/CHATGPT5_PLAN/sysmon"

# sysmon helper function
sysmon-help() {
    # ... (function definition)
}
```

## Integration with Other Tools

The sysmon aliases work seamlessly with other system tools:

```bash
# Pipe to grep
sysmon-once | grep CPU

# Save to file
sysmon-once > /tmp/system_status.txt

# Monitor in background
sysmon &

# Chain with other commands
sysmon-once && echo "System check complete"
```

## Python Version Detection

The `sysmon-help` function automatically detects and displays:
- Current Python version
- GIL status (Enabled/Disabled)
- Free-threading availability

This uses the existing `pyver` alias for consistent status reporting.

## Troubleshooting

### Aliases not working
```bash
# Reload bashrc
source ~/.bashrc
```

### Function not found
Functions are only available in interactive shells. If using scripts, call the command directly:
```bash
python3 /home/nmsglobal/DEVEL/CHATGPT5_PLAN/sysmon/sysmon.py --once
```

### Permission denied
```bash
# Ensure script is executable
chmod +x /home/nmsglobal/DEVEL/CHATGPT5_PLAN/sysmon/sysmon.py
```

## Uninstallation

To remove sysmon aliases:

1. Edit `~/.bashrc`
2. Remove lines 204-241
3. Reload: `source ~/.bashrc`

## Additional Resources

- **Main Documentation**: `README.md`
- **Python 3.14 Upgrade**: `PYTHON314_UPGRADE.md`
- **Project Directory**: `/home/nmsglobal/DEVEL/CHATGPT5_PLAN/sysmon`

## Version

**Date**: 2025-10-13
**sysmon Version**: 2.0.0
**Status**: ✅ Active and tested
