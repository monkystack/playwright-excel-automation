# Playwright Excel Automation Pipeline

## Overview

This project implements an end-to-end automated data pipeline that integrates web automation, system scripting, and Excel-based data processing.

The pipeline:

* Logs into a web system using Playwright
* Queries and exports outbound data
* Downloads Excel files automatically
* Processes the data using Excel VBA
* Generates pivot table reports
* Runs on a schedule via Windows Task Scheduler

---

## Architecture

The system is designed as a multi-layer automation pipeline:

```text
Playwright (Python)
        ↓
Download Excel (Data.xlsx)
        ↓
PowerShell Orchestration
        ↓
Excel VBA Processing
        ↓
Pivot Table Output
```

Each layer is decoupled and communicates through file-based interfaces and subprocess calls.

---

## Key Features

### 1. Cross-Technology Integration

This project bridges multiple environments:

* **Python + Playwright** → web automation & data extraction
* **PowerShell** → orchestration and system-level execution
* **Excel VBA** → data transformation and reporting

This demonstrates a full-stack automation workflow beyond a single language ecosystem.

---

### 2. Layered Logging System (Core Design)

The pipeline implements layered logging across Python, PowerShell, and VBA, where:

* Each layer records its own details
* Only high-level success/failure signals are passed upstream
* Logs are persisted with rolling file strategy (2 MB per file, 5 backups)

This ensures clear separation of concerns, minimal noise in higher layers, and deep traceability when debugging is needed.

---

### 3. Scheduled Execution

The pipeline is fully automated using Windows Task Scheduler:

* Multiple daily triggers
* No manual intervention required
* Executes via PowerShell wrapper (run.ps1)
* 
---

## Project Structure

```text
playwright_project/
│
├── main.py
├── config.py
│
├── pages/
├── utils/
│
├── scripts/
│   ├── run.ps1
│   └── open_vba.ps1
│
├── excel_tool/
│   └── AnalyseTool.xlsm
│
├── scheduler/
│   └── scheduled_task.xml
│
└── logs/   (excluded from version control)
```

---

## Data Handling

* Input (`Data.xlsx`) and generated pivot tables are stored **outside the project directory**
* This ensures:

  * Clean repository structure
  * No large file commits
  * Separation between code and runtime data

---

## Configuration

Sensitive information such as credentials and URLs are stored in:

```python
config.py
```

These values are intentionally masked in this repository.
