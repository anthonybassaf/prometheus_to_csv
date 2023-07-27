# CONFIGURATION TOOLS
import os

app_directory = os.path.dirname(os.path.abspath(__file__))
file_path_metrics = os.path.join(app_directory, "metrics_prod.yml")
file_dest_dir = os.path.join(app_directory, "tmp")

# CONFIGURATION PROMETHEUS
hostname_prometheus = "10.105.154.30"
port_prometheus = "9090"  # Replace with the port number on which Prometheus is running

# CONFIGURATION OUTPUT
prefixe_GlobalFilename = "ZZ_FINISH_FILE"

# CONFIGURATION REQUEST
step_interval = "5m"  # Replace with the desired step interval for Prometheus queries
myfrom = ""
myuntil = ""
