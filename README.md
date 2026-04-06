# Playwright Excel Automation Pipeline

## Overview

This project implements an end-to-end automated data pipeline that integrates web automation, system scripting, and Excel-based data processing.

The pipeline performs:

* Automated data extraction via browser automation
* Scheduled execution through Windows Task Scheduler
* Cross-environment orchestration (Python → PowerShell → VBA)
* Structured logging across all layers
* Automated generation of pivot table reports

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

A structured logging mechanism is implemented across all components:

#### Python Layer

* Tracks workflow execution
* Logs success/failure of subprocess calls (PowerShell)
* Does not capture deep system errors intentionally (delegated downstream)

#### PowerShell Layer

* Logs execution steps (Excel open, macro execution)
* Captures runtime exceptions (e.g. COM errors)
* Acts as a bridge between Python and VBA

#### VBA Layer

* Logs detailed business logic execution
* Captures fine-grained errors during data processing
* Provides the most detailed debugging information

---

### Logging Flow

```text
Python → (status only)
   ↓
PowerShell → (execution + error summary)
   ↓
VBA → (detailed root cause)
```

This design ensures:

* Clear separation of concerns
* Minimal noise in higher layers
* Deep traceability when needed

---

### 3. Rolling Log Mechanism

All logging layers implement a rolling file strategy:

* Max file size: **2 MB**
* Max backups: **5 files**
* Format:

  * `py.log`, `py.log.1` ... `py.log.5`
  * `ps.log`, `ps.log.1` ... `ps.log.5`
  * `macro.log`, `macro.log.1` ... `macro.log.5`

Benefits:

* Prevents uncontrolled log growth
* Preserves recent history for debugging
* Suitable for long-running scheduled jobs

---

### 4. Scheduled Execution

The pipeline is fully automated using Windows Task Scheduler:

* Multiple daily triggers
* No manual intervention required
* Executes via PowerShell wrapper (`run.ps1`)

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

---

## Error Handling Strategy

The system follows a hierarchical error tracing model:

| Layer      | Responsibility                      |
| ---------- | ----------------------------------- |
| Python     | Detects failure (high-level status) |
| PowerShell | Captures execution errors           |
| VBA        | Provides detailed root cause        |

Example:

* Python logs: `PowerShell FAILED`
* PowerShell logs: COM exception
* VBA logs: exact processing error

