import requests
import time
from datetime import datetime, timedelta
import csv
import sys
import yaml
import os
import argparse

# LOCAL
from Metric_qualif import *

import config_qualif as cfg

class CSVDataWriter(object):
    def __init__(self, filename, table_name):
        self.filename = filename
        self.table_name = table_name
        self.file = open("%s" %(self.filename), 'a+', newline='')
        self.writer = csv.writer(self.file, delimiter=';')

    def findAndWriteMetric(self, metric):
        # print(f"Query for metric {metric.name} before checking is: {metric.query}")

        if metric.query is None:
            print(f"Query for metric {metric.name} is None. Skipping...")
            return
        
        query = metric.query.strip()

        url = f"http://{cfg.hostname_prometheus}:{cfg.port_prometheus}/api/v1/query_range"
        params = {
            'query': query,
            'start': myfrom,
            'end': myuntil,
            'step': cfg.step_interval,
        }
        headers = {'Accept': 'application/json'}
        
        try:
            response = requests.get(url, params=params, headers=headers)
            # print("Response: ", response.text)  # This prints the raw response text
            # print("Response JSON: ", response.json())  # This prints the JSON response
         
            
            if response.status_code != 200:
                print(f"Request failed with status code {response.status_code}.")
                return

            data = response.json()

            if 'data' not in data or 'result' not in data['data']:
                print(f"'data' or 'result' key is missing in the response: {data}")
                return
        

            for result in data['data']['result']:
                metric_name = result['metric'].get('instance_short') # [{'metric': {'hostname': 'inin8oqt07'}, 'values': [[1688162400, '0'], ..... }]
                # print("Metric Name: ", metric_name)
                metric_values = result['values']
                # print("Metric Values: ", metric_values)
            
                for metric_value in metric_values:
                    my_time = metric_value[0]
                    my_value = metric_value[1]
                    try: 
                        self.writer.writerow(metric.toCSV(my_time, my_value, metric_name))
                        # print("Time: ", my_time, " Value: ", my_value)  # This prints each time-value pair
                    except Exception as e:
                        print("Error Occurred while writing to CSV: ", e)
        except Exception as e:
            print("Error Occurred: ", e)        
     
    def createNewMetrics(self, metric_from_file, my_date):
        name = metric_from_file['name']
        site = metric_from_file['site']
        mode = metric_from_file.get('mode', None)
        query = metric_from_file['query']
        availability_zone = metric_from_file.get('availability_zone', None)
        aggregates = metric_from_file.get('aggregates', None)
        memory = metric_from_file.get('memory', None)
        product_name = metric_from_file.get('product_name', None)
                
        metric_list = []

        # Create Metric based on different tables in the YAML file
        # if "CPU" in self.table_name:
        #     # print(f"Creating new metric with query: {query}\n")
        #     metric_list.append(Metric(name, site, mode, query, availability_zone, aggregates, memory, product_name))
        #     print("Creating New Metric: ", metric_list[-1].__dict__)
        # elif "DMI_INFO" in self.table_name:
        #     # print(f"Creating new metric with query: {query}\n")
        #     metric_list.append(Metric(name, site, mode, query, availability_zone, aggregates, memory, product_name))
        #     print("Creating New Metric: ", metric_list[-1].__dict__)
        # elif "POWER" in self.table_name:
        #     # print(f"Creating new metric with query: {query}\n")
        #     metric_list.append(Metric(name, site, mode, query, availability_zone, aggregates, memory, product_name))
        #     print("Creating New Metric: ", metric_list[-1].__dict__)
        # elif "RAM" in self.table_name:
        #     # print(f"Creating new metric with query: {query}\n")
        #     metric_list.append(Metric(name, site, mode, query, availability_zone, aggregates, memory, product_name))
        #     print("Creating New Metric: ", metric_list[-1].__dict__)
        # elif "VMS" in self.table_name:
        #     # print(f"Creating new metric with query: {query}\n")
        #     metric_list.append(Metric(name, site, mode, query, availability_zone, aggregates, memory, product_name))
        #     print("Creating New Metric: ", metric_list[-1].__dict__)
        if "TRIGRAMME" in self.table_name:
            # print(f"Creating new metric with query: {query}\n")
            metric_list.append(MetricTrigramme(name, site, mode, query, availability_zone, aggregates, memory, product_name, metric_from_file['trigramme']))
            print("Creating New Metric: ", metric_list[-1].__dict__)
        elif "SERVER" in self.table_name:
            if 'loop' in metric_from_file and "TRUE" in metric_from_file['loop']:
                print("Metric server with a loop")
                for num_server in metric_from_file['num_server'].split():
                    query = query.replace("${num_server}", num_server)
                    metric_list.append(MetricServer(name, site, mode, query, availability_zone, aggregates, memory, product_name, num_server))
            else:
                metric_list.append(MetricServer(name, site, mode, query, availability_zone, aggregates, memory, product_name, metric_from_file['num_server']))
        else:
            metric_list.append(MetricGlobale(name, site, mode, query, availability_zone, aggregates, memory, product_name))
        return metric_list

    def processMetric(self, table_name, metric_read, metric_from_file, my_date):
        print("\nTABLE: %s -- METRIC: %s -- Add metric to the CSV file %s_%s.csv" % (table_name, metric_read, table_name, my_date))
        metric_list = self.createNewMetrics(metric_from_file, my_date)
        print(f"\nCreating New Metric: ", metric_list[-1].__dict__)
        # print("Metric List: ", [metric.__dict__ for metric in metric_list], "\n")  # This prints all the attributes of the metrics in the list
        for metric in metric_list:
            # if isinstance(metric, (MetricTrigramme, MetricServer, MetricGlobale)):
            self.findAndWriteMetric(metric)

class CSVGlobaWriter(object):
    def __init__(self, filename):
        self.filename = filename
        self.file = open("%s" % self.filename, 'a+')
        self.writer = csv.writer(self.file, delimiter=';')

    def addFileRow(self, dataFilename):
        dataFilesize = os.stat(dataFilename).st_size
        self.writer.writerow([dataFilename.split('/')[-1], dataFilesize])
        return

def list_tables():
    try:
        with open(cfg.file_path_metrics) as metrics_file:
            metrics_yml = yaml.safe_load(metrics_file)
            tables = metrics_yml['TABLES']
            for table, metrics in tables.items():
                print(table)
                for metric in metrics:
                    print("  |-", metric)
    except IOError:
        print("Error while reading the metrics file. Does it exist?")
        raise

def parse_args():
    parser = argparse.ArgumentParser(usage="%(prog)s --startdate YYYYMMDD --enddate YYYYMMDD --tablename TABLE [optional] --metricname METRIC [optional] \n Use --list for an overview of Tables and metrics \n")
    parser.add_argument("--startdate", help="The start date of the period you want to collect")
    parser.add_argument("--enddate", help="The end date of the period you want to collect")
    parser.add_argument("--tablename", help="Specify a table name if you want only a file for this table, or leave it blank to get a list of available tables")
    parser.add_argument("--metricname", help="Specify a metric name if you want only a file for this metric (table name required)")
    parser.add_argument("--list", action='store_true', help="Lists all the tables and metrics available to collect")
    args = parser.parse_args()
    
    # check if only one date argument is provided
    if args.startdate and not args.enddate:
        args.enddate = args.startdate
    if args.enddate and not args.startdate:
        args.startdate = args.enddate
        
    # check if start date is later than end date
    if datetime.strptime(args.startdate, "%Y%m%d") > datetime.strptime(args.enddate, "%Y%m%d"):
        raise ValueError("Start date cannot be later than end date.")
    
    if args.startdate is None or args.enddate is None:
        print("Specify the date of the day you want to collect. Format YYYYMMDD \n")
        parser.print_usage()
        sys.exit(1)
    if args.metricname and not args.tablename:
        print("You cannot use args metric name without specifying a table name \n")
        parser.print_usage()
        sys.exit(1)
    if args.list == True:  # If --tablename was provided without a value
        list_tables()
        sys.exit(0)  # Exit after printing the tables
    return args

if __name__ == "__main__":
    os.makedirs(f"{cfg.app_directory}/csv_files", exist_ok=True)
    args = parse_args()
    start_date = datetime.strptime(args.startdate, "%Y%m%d")
    end_date = datetime.strptime(args.enddate, "%Y%m%d")

    while start_date <= end_date:
        my_date = start_date.strftime("%Y%m%d")
        myfrom = int(time.mktime(datetime.strptime("%s 00:00:00" % my_date, "%Y%m%d %H:%M:%S").timetuple()))
        myuntil = int(time.mktime(datetime.strptime("%s 23:59:59" % my_date, "%Y%m%d %H:%M:%S").timetuple()))

        try:
            os.makedirs(cfg.file_dest_dir, exist_ok=True)
            global_writer = CSVGlobaWriter("%s/%s_%s.txt" % (cfg.file_dest_dir.replace("\\", "/"), cfg.prefixe_GlobalFilename, my_date))

            with open(cfg.file_path_metrics) as metrics_file:
                metrics_yml = yaml.safe_load(metrics_file)

                if args.tablename:
                    table_name = args.tablename
                    csvDwriter = CSVDataWriter(f"{cfg.app_directory}/csv_files/{table_name}_{my_date}.csv", table_name)

                    if args.metricname:
                        csvDwriter.processMetric(table_name, args.metricname, metrics_yml['TABLES'][table_name][args.metricname], my_date)
                    else:
                        for metric_read in metrics_yml['TABLES'][table_name]:
                            csvDwriter.processMetric(table_name, metric_read, metrics_yml['TABLES'][table_name][metric_read], my_date)
                    csvDwriter.file.close()
                    global_writer.addFileRow(csvDwriter.filename)
                else:
                    for table_name in metrics_yml['TABLES']:
                        csvDwriter = CSVDataWriter("%s/csv_files/%s_%s.csv" % (cfg.app_directory, table_name, my_date), table_name)
                        for metric_read in metrics_yml['TABLES'][table_name]:
                            csvDwriter.processMetric(table_name, metric_read, metrics_yml['TABLES'][table_name][metric_read], my_date)
                        csvDwriter.file.close()
                        global_writer.addFileRow(csvDwriter.filename)

                global_writer.file.close()
        except IOError:
            print("Error while reading the metrics file. Does it exist?")
            raise

        start_date += timedelta(days=1)  # advance to next day