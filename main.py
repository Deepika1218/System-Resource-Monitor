
import psutil
import os
import time
import csv
import statistics
import matplotlib.pyplot as plt

from datetime import datetime


REPORT_FOLDER = "Reports"
CSV_FILE = os.path.join(REPORT_FOLDER, "system_monitor.csv")
SUMMARY_FILE = os.path.join(REPORT_FOLDER, "system_summary.txt")

CPU_CHART = os.path.join(REPORT_FOLDER, "cpu_usage.png")
RAM_CHART = os.path.join(REPORT_FOLDER, "ram_usage.png")
DISK_CHART = os.path.join(REPORT_FOLDER, "disk_usage.png")

CPU_THRESHOLD = 80
RAM_THRESHOLD = 80
DISK_THRESHOLD = 85


def get_cpu_usage():

    return psutil.cpu_percent(interval=1)


def get_memory_usage():

    memory = psutil.virtual_memory()

    total_memory = memory.total / (1024 ** 3)
    used_memory = memory.used / (1024 ** 3)
    available_memory = memory.available / (1024 ** 3)
    memory_percentage = memory.percent

    return total_memory, used_memory, available_memory, memory_percentage


def get_disk_usage():

    disk = psutil.disk_usage(os.path.abspath(os.sep))

    total_disk = disk.total / (1024 ** 3)
    used_disk = disk.used / (1024 ** 3)
    free_disk = disk.free / (1024 ** 3)
    disk_percentage = disk.percent

    return total_disk, used_disk, free_disk, disk_percentage


def save_to_csv(data):

    os.makedirs(REPORT_FOLDER, exist_ok=True)

    file_exists = os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "Timestamp",
                "CPU Usage (%)",
                "RAM Usage (%)",
                "Total RAM (GB)",
                "Used RAM (GB)",
                "Available RAM (GB)",
                "Disk Usage (%)",
                "Total Disk (GB)",
                "Used Disk (GB)",
                "Free Disk (GB)"
            ])

        writer.writerow(data)


def check_resource_alerts(cpu, ram, disk):

    alert_found = False

    print("\nRESOURCE ALERTS")
    print("------------------------------")

    if cpu > CPU_THRESHOLD:

        print(f"WARNING: High CPU usage: {cpu}%")
        alert_found = True

    if ram > RAM_THRESHOLD:

        print(f"WARNING: High RAM usage: {ram}%")
        alert_found = True

    if disk > DISK_THRESHOLD:

        print(f"WARNING: High Disk usage: {disk}%")
        alert_found = True

    if not alert_found:

        print("All system resources are within normal limits.")


def generate_resource_charts(timestamps, cpu_values, ram_values, disk_values):

    os.makedirs(REPORT_FOLDER, exist_ok=True)

    # CPU usage chart
    plt.figure(figsize=(10, 5))

    plt.plot(timestamps, cpu_values, marker="o", label="CPU Usage")

    plt.title("CPU Usage Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("CPU Usage (%)")

    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.savefig(CPU_CHART)
    plt.close()

    # RAM usage chart
    plt.figure(figsize=(10, 5))

    plt.plot(timestamps, ram_values, marker="o", label="RAM Usage")

    plt.title("RAM Usage Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("RAM Usage (%)")

    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.savefig(RAM_CHART)
    plt.close()

    # Disk usage chart
    plt.figure(figsize=(10, 5))

    plt.plot(timestamps, disk_values, marker="o", label="Disk Usage")

    plt.title("Disk Usage Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Disk Usage (%)")

    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.savefig(DISK_CHART)
    plt.close()

    print("\nResource charts generated successfully.")

    print("CPU Chart  :", CPU_CHART)
    print("RAM Chart  :", RAM_CHART)
    print("Disk Chart :", DISK_CHART)


def generate_summary_report():

    print("\nGenerating resource usage summary...")

    if not os.path.exists(CSV_FILE):

        print("CSV file not found. No monitoring data available.")
        return

    cpu_values = []
    ram_values = []
    disk_values = []
    timestamps = []

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            try:

                cpu_values.append(float(row["CPU Usage (%)"]))
                ram_values.append(float(row["RAM Usage (%)"]))
                disk_values.append(float(row["Disk Usage (%)"]))
                timestamps.append(row["Timestamp"])

            except (ValueError, KeyError):

                print("Skipping an invalid CSV record.")

    if not cpu_values:

        print("No valid monitoring records found.")
        return

    # Calculate statistics
    total_records = len(cpu_values)

    average_cpu = statistics.mean(cpu_values)
    maximum_cpu = max(cpu_values)

    average_ram = statistics.mean(ram_values)
    maximum_ram = max(ram_values)

    average_disk = statistics.mean(disk_values)
    maximum_disk = max(disk_values)

    report = [
        "==========================================",
        "       SYSTEM RESOURCE USAGE SUMMARY",
        "==========================================",
        "",
        f"Report Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"First Reading    : {timestamps[0]}",
        f"Last Reading     : {timestamps[-1]}",
        f"Total Records    : {total_records}",
        "",
        "CPU USAGE",
        "------------------------------------------",
        f"Average CPU Usage : {average_cpu:.2f}%",
        f"Maximum CPU Usage : {maximum_cpu:.2f}%",
        "",
        "RAM USAGE",
        "------------------------------------------",
        f"Average RAM Usage : {average_ram:.2f}%",
        f"Maximum RAM Usage : {maximum_ram:.2f}%",
        "",
        "DISK USAGE",
        "------------------------------------------",
        f"Average Disk Usage : {average_disk:.2f}%",
        f"Maximum Disk Usage : {maximum_disk:.2f}%",
        "",
        "==========================================",
        "             END OF REPORT",
        "=========================================="
    ]

    with open(SUMMARY_FILE, "w", encoding="utf-8") as file:

        file.write("\n".join(report))

    print("\n".join(report))

    print(f"\nSummary report saved at: {SUMMARY_FILE}")

    # Generate charts using historical CSV data
    generate_resource_charts(
        timestamps,
        cpu_values,
        ram_values,
        disk_values
    )


def monitor_system():

    print("\n======================================")
    print("    CONTINUOUS SYSTEM MONITOR")
    print("======================================")

    print("Monitoring interval: 5 seconds")
    print("CPU alert threshold:", CPU_THRESHOLD, "%")
    print("RAM alert threshold:", RAM_THRESHOLD, "%")
    print("Disk alert threshold:", DISK_THRESHOLD, "%")
    print("Press Ctrl + C to stop monitoring.")

    try:

        while True:

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cpu = get_cpu_usage()

            total_ram, used_ram, available_ram, ram_percent = get_memory_usage()

            total_disk, used_disk, free_disk, disk_percent = get_disk_usage()

            monitoring_data = [
                current_time,
                cpu,
                ram_percent,
                round(total_ram, 2),
                round(used_ram, 2),
                round(available_ram, 2),
                disk_percent,
                round(total_disk, 2),
                round(used_disk, 2),
                round(free_disk, 2)
            ]

            save_to_csv(monitoring_data)

            print("\n======================================")
            print(f"TIME: {current_time}")
            print("======================================")

            print(f"CPU Usage     : {cpu}%")

            print(f"RAM Usage     : {ram_percent}%")
            print(f"Total RAM     : {total_ram:.2f} GB")
            print(f"Used RAM      : {used_ram:.2f} GB")
            print(f"Available RAM : {available_ram:.2f} GB")

            print(f"Disk Usage    : {disk_percent}%")
            print(f"Total Disk    : {total_disk:.2f} GB")
            print(f"Used Disk     : {used_disk:.2f} GB")
            print(f"Free Disk     : {free_disk:.2f} GB")

            check_resource_alerts(cpu, ram_percent, disk_percent)

            print("\nData saved to CSV successfully.")
            print("======================================")

            time.sleep(5)

    except KeyboardInterrupt:

        print("\n\nMonitoring stopped by user.")
        print("System monitoring completed.")

    finally:

        generate_summary_report()


if __name__ == "__main__":

    monitor_system()
