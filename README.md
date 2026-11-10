
# Python System Resource Monitor

A Python-based system monitoring tool that continuously tracks CPU, RAM, and disk usage. It records resource utilization, generates threshold-based alerts, stores historical readings in CSV format, and creates analytical reports and visualizations.

## Features

- Monitor CPU, RAM, and disk utilization.
- Collect system resource readings continuously.
- Generate alerts when resource usage crosses configured thresholds.
- Store historical monitoring data in a CSV file.
- Generate a summary report with average and maximum resource usage.
- Create CPU, RAM, and disk usage charts using Matplotlib.
- Stop monitoring gracefully using Ctrl + C.

## Technologies Used

- Python 3
- psutil
- CSV
- Matplotlib
- Statistics
- Git and GitHub

## Project Structure

```text
System-Resource-Monitor/
│
├── Reports/
│   ├── system_monitor.csv
│   ├── system_summary.txt
│   ├── cpu_usage.png
│   ├── ram_usage.png
│   └── disk_usage.png
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Deepika1218/System-Resource-Monitor.git
```

2. Navigate to the project directory:

```bash
cd System-Resource-Monitor
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Run the Project

```bash
python main.py
```

The application continuously monitors system resources and records readings at regular intervals.

Press `Ctrl + C` to stop monitoring and generate the summary report and charts.

## Generated Reports

The application generates the following files inside the Reports folder:

- `system_monitor.csv` – Historical resource utilization data.
- `system_summary.txt` – Summary of resource usage.
- `cpu_usage.png` – CPU utilization chart.
- `ram_usage.png` – RAM utilization chart.
- `disk_usage.png` – Disk utilization chart.

## Learning Outcomes

Through this project, I practised:

- Python functions and modules.
- System monitoring using psutil.
- File handling and CSV operations.
- Exception handling.
- Data analysis using Python statistics.
- Data visualization using Matplotlib.
- Git and GitHub version control.

## Author

Deepika Kodati

GitHub: [Deepika1218](https://github.com/Deepika1218)
