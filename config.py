"""
Project configuration settings.

This file stores the host, ports, timeout,
monitoring interval, and logging settings.
"""

# Target server
TARGET_HOST = "127.0.0.1"

# TCP ports to monitor
TARGET_PORTS = [
    22,    # SSH
    80,    # HTTP
    443,   # HTTPS 
]

# Maximum time to wait for a connection
CONNECTION_TIMEOUT = 3

# Time between monitoring cycles (seconds)
MONITOR_INTERVAL = 60

# Maximum number of simultaneous connections
MAX_CONCURRENT_CHECKS = 10

# Logging settings
LOG_FILE = "logs/monitor.log"
LOG_LEVEL = "INFO"