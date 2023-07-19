# CONFIGURATION TOOLS
import os

app_directory = os.path.dirname(os.path.abspath(__file__))
file_path_metrics = os.path.join(app_directory, "metrics_cpu.yml")
file_dest_dir = os.path.join(app_directory, "csv_files")

# CONFIGURATION PROMETHEUS
hostname_prometheus = "192.168.210.44"  # Replace with the hostname or IP address of your Prometheus server
port_prometheus = "9090"  # Replace with the port number on which Prometheus is running

# CONFIGURATION OUTPUT
prefixe_GlobalFilename = "ZZ_FINISH_FILE"

# CONFIGURATION REQUEST
step_interval = "15s"  # Replace with the desired step interval for Prometheus queries
myfrom = ""
myuntil = ""