#!/usr/bin/env python3
"""
Linux System Monitor
Real-time monitoring of system resources: uptime, CPU, processes, memory
"""

import os
import sys
import time
import signal
import argparse
import subprocess
from datetime import datetime, timedelta


class SystemMonitor:
    """Main system monitor class that collects and displays system stats"""
    
    def __init__(self, interval=60, use_color=True):
        """Initialize the system monitor
        
        Args:
            interval: Update interval in seconds
            use_color: Whether to use colored output
        """
        self.interval = interval
        self.use_color = use_color
        self.running = True
        
        # Color codes
        if use_color:
            self.RED = '\033[91m'
            self.GREEN = '\033[92m'
            self.YELLOW = '\033[93m'
            self.BLUE = '\033[94m'
            self.BOLD = '\033[1m'
            self.RESET = '\033[0m'
            self.CLEAR = '\033[H\033[2J\033[3J'
        else:
            self.RED = self.GREEN = self.YELLOW = self.BLUE = ''
            self.BOLD = self.RESET = self.CLEAR = ''
    
    def get_uptime(self):
        """Get system uptime and load average from /proc
        
        Returns:
            dict: Dictionary with uptime string and load average
        """
        try:
            # Get uptime
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
            
            # Convert to human-readable format
            uptime_td = timedelta(seconds=int(uptime_seconds))
            days = uptime_td.days
            hours = uptime_td.seconds // 3600
            minutes = (uptime_td.seconds % 3600) // 60
            
            if days > 0:
                uptime_str = f"{days}d {hours}h {minutes}m"
            else:
                uptime_str = f"{hours}h {minutes}m"
            
            # Get load average
            with open('/proc/loadavg', 'r') as f:
                loadavg_line = f.readline().strip()
                loads = loadavg_line.split()[:3]
                load_avg = f"{loads[0]}, {loads[1]}, {loads[2]}"
            
            return {
                'uptime': uptime_str,
                'load_avg': load_avg
            }
        except Exception:
            return {
                'uptime': "N/A",
                'load_avg': "N/A"
            }
    
    def get_cpu_usage(self):
        """Get CPU usage percentage using /proc/stat
        
        Returns:
            dict: Dictionary with CPU usage stats
        """
        try:
            # Read /proc/stat twice with a small interval
            def read_cpu_stats():
                with open('/proc/stat', 'r') as f:
                    line = f.readline()
                    fields = line.split()
                    # cpu  user nice system idle iowait irq softirq steal guest guest_nice
                    return [int(x) for x in fields[1:]]
            
            # First reading
            cpu1 = read_cpu_stats()
            
            # Wait for a brief moment
            time.sleep(1.0)  # 1 second for better accuracy
            
            # Second reading
            cpu2 = read_cpu_stats()
            
            # Calculate differences for each field
            diffs = [cpu2[i] - cpu1[i] for i in range(len(cpu1))]
            
            # Sum all time (user, nice, system, idle, iowait, irq, softirq)
            total_time = sum(diffs[:7])  # Only use first 7 fields
            
            if total_time == 0:
                # No time passed or no change, return low usage
                return {'percent': 0.0, 'cores': os.cpu_count()}
            
            # Idle time is idle + iowait
            idle_time = diffs[3] + diffs[4]  # idle + iowait
            
            # CPU usage = (total - idle) / total * 100
            cpu_usage = ((total_time - idle_time) / total_time) * 100
            
            return {
                'percent': round(max(0, min(100, cpu_usage)), 1),
                'cores': os.cpu_count()
            }
            
        except Exception as e:
            # Fallback to top command
            try:
                result = subprocess.run(['top', '-bn1'], capture_output=True, text=True, timeout=2)
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if '%Cpu(s):' in line and 'id' in line:
                            # Extract idle percentage
                            parts = line.split(',')
                            for part in parts:
                                if 'id' in part:
                                    idle_val = float(part.strip().split()[0])
                                    return {
                                        'percent': round(100 - idle_val, 1),
                                        'cores': os.cpu_count()
                                    }
            except:
                pass
            
            # Final fallback
            return {'percent': 0.0, 'cores': os.cpu_count() or 1}
    
    def get_process_info(self):
        """Get process information from /proc and ps
        
        Returns:
            dict: Dictionary with total processes, high CPU count and process names
        """
        try:
            # Count all process directories in /proc
            proc_dirs = [d for d in os.listdir('/proc') if d.isdigit()]
            total_processes = len(proc_dirs)
            
            high_cpu_count = 0
            high_cpu_processes = []
            
            # Try multiple times to catch high CPU processes (since ps is fast)
            for attempt in range(3):
                try:
                    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, timeout=1)
                    
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        # Skip header line
                        for line in lines[1:]:
                            fields = line.split(None, 10)  # Split into max 11 parts
                            if len(fields) >= 11:
                                try:
                                    cpu_percent = float(fields[2])  # Third column is %CPU
                                    if cpu_percent >= 90.0:
                                        # Get process name (11th field)
                                        command = fields[10]
                                        process_name = command.split()[0]  # First word of command
                                        
                                        # If it's a path, get just the filename
                                        if '/' in process_name:
                                            process_name = process_name.split('/')[-1]
                                        
                                        # Check if we already have this process (avoid duplicates)
                                        existing = next((p for p in high_cpu_processes if p['pid'] == fields[1]), None)
                                        if not existing:
                                            high_cpu_processes.append({
                                                'name': process_name,
                                                'cpu': cpu_percent,
                                                'pid': fields[1]
                                            })
                                except (ValueError, IndexError):
                                    pass
                    
                    # Small delay between attempts
                    if attempt < 2:
                        time.sleep(0.1)
                        
                except subprocess.TimeoutExpired:
                    continue
            
            # Remove ps command itself if it appears
            high_cpu_processes = [p for p in high_cpu_processes if p['name'] != 'ps']
            high_cpu_count = len(high_cpu_processes)
                    
            return {
                'total': total_processes,
                'running': high_cpu_count,
                'high_cpu_list': high_cpu_processes
            }
        except Exception:
            return {'total': 0, 'running': 0, 'high_cpu_list': []}
    
    def get_memory_info(self):
        """Get memory information from /proc/meminfo
        
        Returns:
            dict: Dictionary with memory statistics
        """
        try:
            with open('/proc/meminfo', 'r') as f:
                lines = f.readlines()
            
            mem_info = {}
            for line in lines:
                parts = line.split()
                if parts[0] == 'MemTotal:':
                    mem_info['total'] = int(parts[1])
                elif parts[0] == 'MemFree:':
                    mem_info['free'] = int(parts[1])
                elif parts[0] == 'MemAvailable:':
                    mem_info['available'] = int(parts[1])
                elif parts[0] == 'Buffers:':
                    mem_info['buffers'] = int(parts[1])
                elif parts[0] == 'Cached:':
                    mem_info['cached'] = int(parts[1])
            
            # Calculate used memory
            used = mem_info['total'] - mem_info.get('available', mem_info['free'])
            percent = (used / mem_info['total']) * 100
            
            return {
                'total_mb': mem_info['total'] // 1024,
                'used_mb': used // 1024,
                'free_mb': mem_info.get('available', mem_info['free']) // 1024,
                'percent': round(percent, 1)
            }
        except Exception:
            return {
                'total_mb': 0,
                'used_mb': 0,
                'free_mb': 0,
                'percent': 0
            }
    
    def format_display(self, data):
        """Format and display the collected data
        
        Args:
            data: Dictionary containing all system statistics
        """
        # Clear screen
        print(self.CLEAR, end='')
        
        # Header
        print(f"{self.BOLD}{'='*50}{self.RESET}")
        print(f"{self.BOLD}    LINUX SYSTEM MONITOR{self.RESET}")
        print(f"{self.BOLD}{'='*50}{self.RESET}")
        print(f"Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'-'*50}")
        
        # Uptime and Load Average
        uptime_info = data['uptime']
        print(f"{self.GREEN}⏱  Uptime:{self.RESET} {uptime_info['uptime']}")
        print(f"{self.BLUE}📈 Load Average:{self.RESET} {uptime_info['load_avg']}")
        
        # CPU Usage
        cpu = data['cpu']
        if cpu['percent'] > 80:
            cpu_color = self.RED
        elif cpu['percent'] > 50:
            cpu_color = self.YELLOW
        else:
            cpu_color = self.GREEN
        print(f"{cpu_color}💻 CPU:{self.RESET} {cpu['percent']}% ({cpu['cores']} cores)")
        
        # Processes
        proc = data['processes']
        print(f"{self.BLUE}📊 Processes:{self.RESET} {proc['total']} total, {proc['running']} high CPU (≥90%)")
        
        # Show high CPU processes if any
        if proc['running'] > 0 and proc.get('high_cpu_list'):
            for p in proc['high_cpu_list']:
                print(f"   └─ {self.RED}{p['name']}{self.RESET} (PID {p['pid']}, {p['cpu']}% CPU)")
        
        # Memory
        mem = data['memory']
        if mem['percent'] > 80:
            mem_color = self.RED
        elif mem['percent'] > 60:
            mem_color = self.YELLOW
        else:
            mem_color = self.GREEN
        print(f"{mem_color}💾 Memory:{self.RESET} {mem['used_mb']}MB / {mem['total_mb']}MB ({mem['percent']}%)")
        
        # Footer
        print(f"{'-'*50}")
        print(f"Refresh interval: {self.interval}s | Press Ctrl+C to exit")
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C signal
        
        Args:
            signum: Signal number
            frame: Current stack frame
        """
        self.stop()
    
    def stop(self):
        """Stop the monitor gracefully"""
        self.running = False
        print("\n\nSystem Monitor stopped.")
        sys.exit(0)
    
    def run(self):
        """Main monitoring loop"""
        # Register signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        
        while self.running:
            try:
                # Collect data
                data = {
                    'uptime': self.get_uptime(),
                    'cpu': self.get_cpu_usage(),
                    'processes': self.get_process_info(),
                    'memory': self.get_memory_info()
                }
                
                # Display data
                self.format_display(data)
                
                # Wait for next update
                time.sleep(self.interval)
                
            except KeyboardInterrupt:
                self.stop()
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)


def parse_arguments():
    """Parse command line arguments
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Linux System Monitor - Real-time system statistics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sysmon                    # Default: 60s interval
  sysmon -i 30             # 30 seconds interval
  sysmon -i 5 -n           # 5 seconds, no color
  sysmon --once            # Show once and exit
        """
    )
    
    parser.add_argument('-i', '--interval', 
                       type=int, 
                       default=60,
                       help='Update interval in seconds (default: 60)')
    
    parser.add_argument('-n', '--no-color',
                       action='store_true',
                       help='Disable colored output')
    
    parser.add_argument('--once',
                       action='store_true',
                       help='Show statistics once and exit')
    
    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_arguments()
    
    # Create monitor instance
    monitor = SystemMonitor(
        interval=args.interval,
        use_color=not args.no_color
    )
    
    if args.once:
        # Single display mode
        data = {
            'uptime': monitor.get_uptime(),
            'cpu': monitor.get_cpu_usage(),
            'processes': monitor.get_process_info(),
            'memory': monitor.get_memory_info()
        }
        monitor.format_display(data)
    else:
        # Continuous monitoring mode
        print("Starting System Monitor...")
        print(f"Update interval: {args.interval} seconds")
        print("Press Ctrl+C to stop\n")
        time.sleep(2)
        monitor.run()


if __name__ == '__main__':
    main()