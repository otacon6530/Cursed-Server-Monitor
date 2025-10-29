# ServerMonitorApp

A cross-platform server monitoring and management CLI tool built with Python and Click.

## Features

- View system metrics: uptime, CPU usage, RAM usage, disk usage.
- Ping a remote host to check connectivity.
- List all services and their status (Windows and Linux supported).
- Run system commands.
- Query and update SQL Server metrics.
- Modular command structure for easy extension.

## Requirements

- Python 3.7+
- [Click](https://pypi.org/project/click/)
- [psutil](https://pypi.org/project/psutil/)
- [pyodbc](https://pypi.org/project/pyodbc/)
- (Windows) ODBC Driver for SQL Server
- (Linux) systemctl for service status

## Installation

1. Clone the repository:
    ```
    git clone https://dev.azure.com/StephensDev/StephensDev.com/_git/Cloud
    cd ServerMonitorApp
    ```

2. Create and activate a virtual environment:
    ```
    python -m venv env
    # On Windows
    .\env\Scripts\activate
    # On Linux/macOS
    source env/bin/activate
    ```

3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage 

servmon.exe [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  start  Starts the service to push client metrics to the central hub.
  test   Display system metrics (uptime, CPU, RAM, disk usage), ping a remote host, list all services and their status, and run all unit tests for core functions.
