# Linux Network Monitor

A simple Python project to monitor network ports on a Linux system.

This project checks if selected TCP ports are available. It runs checks at regular intervals and saves the results as JSON logs.

## Project Goals

The main goals of this project are:

- Check the status of important TCP ports.
- Handle network errors and connection timeouts.
- Use asynchronous programming to check ports faster.
- Save monitoring results in structured JSON logs.
- Run the monitor as a background service with Systemd.

## Project Structure

```text
linux-network-monitor/
│
├── monitor.py
├── config.py
├── logger.py
├── tests/
│   ├── test_logger.py
│   └── test_monitor.py
├── logs/
├── systemd/
│   └── network-monitor.service
├── README.md
├── requirements.txt
└── .gitignore
```

## Requirements

- Python 3.10 or newer
- Linux
- uv or Python virtual environment
- pytest for running tests
- Systemd for background service management

## Configuration

The `config.py` file contains the main settings:

- `TARGET_HOST`: The host to monitor.
- `TARGET_PORTS`: The TCP ports to check.
- `CONNECTION_TIMEOUT`: Maximum waiting time for a connection.
- `MONITOR_INTERVAL`: Time between monitoring cycles.
- `MAX_CONCURRENT_CHECKS`: Maximum number of concurrent checks.
- `LOG_FILE`: Path to the log file.

The default configuration checks ports 22, 80, and 443 on `127.0.0.1`.

## Why Asyncio?

I used `asyncio` because the monitor needs to check multiple network ports.

A normal program may wait for each connection before checking the next one. This can take more time.

With `asyncio`, the program can wait for multiple network operations at the same time. It does not need to stop all other tasks while waiting for one connection.

I also used `asyncio.gather()` to run the port checks together.

The `Semaphore` controls the number of active checks. This helps prevent too many connections from running at the same time.

## Error Handling

The monitor handles different network errors:

- `TIMEOUT`: The connection takes too long.
- `REFUSED`: The connection is refused.
- `DNS_ERROR`: The hostname cannot be resolved.
- `NETWORK_ERROR`: Another network error happens.
- `ONLINE`: The connection is successful.

The program also records the response time for each check.

## Structured Logging

The project uses Python's standard `logging` module.

The `logger.py` file uses a custom JSON formatter.

Each log entry contains:

- Timestamp
- Log level
- Message
- Host
- Port
- Connection status
- Response time
- Error information

Logs are saved in `logs/monitor.log` and are also displayed in the terminal.

## Installation

Clone the repository:

```bash
git clone https://github.com/mobinaesfani-mygit/linux-network-Monitor.git
cd linux-network-Monitor
```

Create a virtual environment:

```bash
uv venv
```

Install the required packages:

```bash
uv pip install --python .venv/bin/python -r requirements.txt
```

## Run the Monitor

Run the script with:

```bash
.venv/bin/python monitor.py
```

The monitor checks the configured ports and repeats the checks every 60 seconds.

To stop the program manually, press `Ctrl + C`.


## Run as a Systemd Service

Systemd can run the monitor in the background.

It can also start the service automatically when Linux starts.

### 1. Configure the service file

Open the service file:

```bash
nano systemd/network-monitor.service
```

Update `WorkingDirectory` and `ExecStart` with the correct project path on your system.

### 2. Copy the service file

```bash
sudo cp systemd/network-monitor.service /etc/systemd/system/
```

### 3. Reload Systemd

```bash
sudo systemctl daemon-reload
```

### 4. Start the service

```bash
sudo systemctl start network-monitor
```

### 5. Enable automatic startup

```bash
sudo systemctl enable network-monitor
```

### 6. Check the service status

```bash
sudo systemctl status network-monitor
```

The expected status is:

```text
Active: active (running)
```

### 7. View service logs

```bash
sudo journalctl -u network-monitor -f
```

### Other useful commands

Stop the service:

```bash
sudo systemctl stop network-monitor
```

Restart the service:

```bash
sudo systemctl restart network-monitor
```

Disable automatic startup:

```bash
sudo systemctl disable network-monitor
```

## What I Learned

During this project, I worked with:

- Python asynchronous programming
- TCP connections and network errors
- Exception handling
- Structured logging with JSON
- Unit testing and mocking
- Linux Systemd services
- Git branches and commit management

This project helped me understand how Python can be used to monitor network services on Linux.

## AI Used

AI tools were used as a learning assistant during this project.

I used AI to:

- Learn about asynchronous programming and Systemd.
- Review code and understand errors.
- Get help with test cases and debugging.

