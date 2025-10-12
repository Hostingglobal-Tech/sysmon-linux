# Suggested Development Commands

## Running the Application
```bash
# Make executable
chmod +x sysmon.py

# Run with default settings (60s interval)
./sysmon.py

# Run with custom interval
./sysmon.py -i 30

# Single display and exit
./sysmon.py --once

# Disable colors
./sysmon.py -n

# Show help
./sysmon.py -h
```

## Development Commands
```bash
# Run via Python interpreter
python3 sysmon.py

# Run via npm scripts (if npm is available)
npm start
npm test  # Runs: python3 -m unittest test_sysmon.py
```

## Installation Commands
```bash
# System-wide installation
sudo cp sysmon.py /usr/local/bin/sysmon
sudo chmod +x /usr/local/bin/sysmon

# Then run from anywhere
sysmon -i 10
```

## Testing Commands
```bash
# Unit tests (referenced in package.json but test file doesn't exist)
python3 -m unittest test_sysmon.py

# Manual testing
./sysmon.py --once  # Quick single run test
```

## Useful Linux System Commands
```bash
# Check /proc filesystem access
ls -la /proc/uptime /proc/loadavg /proc/stat /proc/meminfo

# Monitor system resources manually
top -bn1
ps aux
free -h
uptime

# Check Python version
python3 --version

# Find Python executable
which python3
```

## Git Commands
```bash
# Status
git status

# Add changes
git add .

# Commit
git commit -m "Description"

# View logs
git log --oneline
```

## Development Tools
**Note**: This project currently has no linting, formatting, or testing configuration files. Consider adding:
- **Linting**: `flake8`, `pylint`, or `ruff`
- **Formatting**: `black` or `autopep8`  
- **Testing**: `pytest` with actual test files
- **Type checking**: `mypy` with type hints