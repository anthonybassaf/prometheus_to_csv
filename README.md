# prometheus_to_csv
This repository includes Python scripts to convert Prometheus metric data to CSV format. The code fetches the metric data from a Prometheus server, processes it, and writes it to a CSV file. The project consists of 4 main files:


- collect_qualif.py
- Metric_qualif.py
- config_qualif.py
- metrics_qualif.yml

## File Details
**collect_qualif.py**: This is the main script that carries out the operation of fetching metrics data, processing it, and writing it to a CSV file. The script fetches metrics based on specified tables and metrics names. If no table or metric name is specified, it fetches all available metrics.

**Metric_qualif.py**: This script defines various metric classes with their respective features. The Metric class is the base class, and there are other specific metric classes like MetricTrigramme, MetricServer, and MetricGlobale.

**config_qualif.py**: This script contains the configuration information like the Prometheus server hostname, port, the step interval for metrics fetching, file paths, and other necessary configuration details.

**metrics_qualif.yml**: This YAML file contains a list of tables and associated metrics that the script can fetch from the Prometheus server.

## Installation 
1. Clone the repository:
`git clone https://github.com/anthony.assaf/prometheus_to_csv.git`
2. Change into the repository's directory:
`cd prometheus_to_csv` 
3. Install the required Python libraries:
`pip install -r requirements.txt`


## Usage
You need to provide the date of the metrics you want to collect in the format YYYYMMDD. Optional parameters include a specific table name and a specific metric name. If these are not provided, the script fetches all metrics. There's also an option to list all the available tables and metrics.

- To list all available tables and metrics: 
`python collect_qualif.py --list`
**Use `python3` if you are using Python3.x version**
- To collect metrics for a specific date, table, and metric:
`python collect_qualif.py --metricdate YYYYMMDD --tablename TABLENAME --metricname METRICNAME`
**Replace 'YYYYMMDD' with the date, 'TABLENAME' with the table name, and 'METRICNAME' with the metric name** 

`python collect_qualif.py --metricdate YYYYMMDD [--tablename TABLE] [--metricname METRIC] [--list]
--metricdate YYYYMMDD: Specify the date of the metrics you want to collect.
--tablename TABLE: Specify a table name if you want only a file for this table.
--metricname METRIC: Specify a metric name if you want only a file for this metric. Note: You must specify a table name if you specify a metric name.
--list: Lists all the tables and metrics available to collect.`

The output will be CSV files written in the directory specified in config_qualif.py, and these CSV files will contain the fetched metrics data.

## Dependencies
Python 3.6+
All the packages and dependencies are listed in *requirements.txt*

Please ensure that the necessary Python packages are installed. You can install them with pip:

`pip install -r requirements.txt`

## Note

Please make sure to update the Prometheus server details and other necessary information in config_qualif.py before running the collect_qualif.py script.
