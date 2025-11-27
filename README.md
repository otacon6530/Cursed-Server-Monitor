# ServerMonitor

A Python-based server monitoring application that collects and stores system metrics (CPU, RAM, Disk usage).

---

## Features

- **Real-time server metrics collection** (CPU, RAM, Disk)
- **Curses-based UI** for live monitoring
- **Database backend failover:**  
  - Uses SQL Server if available  
  - Falls back to SQLite automatically if SQL Server is offline

---

## Getting Started

### Prerequisites

- Python 3.8+
- Microsoft SQL Server

### Installation

1. **Clone the repository:**
2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3. **Configure SQL Server (optional):**
   - Update `DB_CONFIG` in `classes/window.py` if your SQL Server instance or database name differs.

---

## Usage

### Start the Server
```bash
python -m servermonitor
```

---

## Development

### Running Tests

- To run the unit tests, execute:
  ```bash
  pytest --test
  ```

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).