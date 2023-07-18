import requests
import time
import datetime
import csv
import sys
import yaml
import os
import argparse

# LOCAL
from Metric_vms import *

import config as cfg

class CSVDataWriter(object):
    def __init__(self, filename, table_name):
        self.filename = filename
        self.table_name = table_name
        self.file = open("%s" %(self.filename), 'a+', newline='')
        self.writer = csv.writer(self.file, delimiter=';')

    def findAndWriteMetric(self, metric):
        query = metric.query
        url = f"http://{cfg.hostname_prometheus}:{cfg.port_prometheus}/api/v1/query_range"
        params = {
            'query': query,
            'start': myfrom,
            'end': myuntil,
            'step': cfg.step_interval,
        }
        headers = {'Accept': 'application/json'}

        response = requests.get(url, params=params, headers=headers)
        data = response.json()


        for result in data['data']['result']:
            metric_name = result['metric']
            ### [{'metric': {'hostname': 'inin8oqt07'}, 'values': [[1688162400, '0'], ..... }]
            metric_values = result['values']
            
            for metric_value in metric_values:
                my_time = metric_value[0]
                my_value = metric_value[1]
                metric_name = result['metric'].get('hostname')  # Extract the hostname here
                site = metric.site
                availability_zone = metric.availability_zone
                aggregates = metric.aggregates
                self.writer.writerow(metric.toCSV(my_time, my_value, metric_name, site, availability_zone, aggregates))
                
     
    def createNewMetrics(self, metric_from_file, my_date):
        name = metric_from_file['name']
        site = metric_from_file['site']
        availability_zone = metric_from_file['availability_zone']
        aggregates = metric_from_file['aggregates']
        vms_value = metric_from_file['query']      
                
        metric_list = []

        if "TRIGRAMME" in self.table_name:
            metric_list.append(MetricTrigramme(name, site, availability_zone, aggregates, vms_value))
            # metric_list.append(MetricTrigramme(name, site, cpu_usage_value, ram_usage_value, vms_value, energy_value, metric_from_file['trigramme']))
        elif "SERVER" in self.table_name:
            if 'loop' in metric_from_file and "TRUE" in metric_from_file['loop']:
                print("Metric server with a loop")
                for num_server in metric_from_file['num_server'].split():
                    query = query.replace("${num_server}", num_server)
                    metric_list.append(MetricServer(name, site, availability_zone, aggregates, vms_value, num_server))
                    # metric_list.append(MetricTrigramme(name, site, cpu_usage_value, ram_usage_value, vms_value, energy_value, metric_from_file['trigramme'], num_server))
            else:
                metric_list.append(MetricServer(name, site, availability_zone, aggregates, vms_value, metric_from_file['num_server']))
                # metric_list.append(MetricTrigramme(name, site, cpu_usage_value, ram_usage_value, vms_value, energy_value, metric_from_file['trigramme'], metric_from_file['num_server']))
        else:
            metric_list.append(MetricGlobale(name, site, availability_zone, aggregates, vms_value))
            # metric_list.append(MetricTrigramme(name, site, cpu_usage_value, ram_usage_value, vms_value, energy_value))
        return metric_list

    def processMetric(self, table_name, metric_read, metric_from_file, my_date):
        print("TABLE: %s -- METRIC: %s -- Add metric to the CSV file" % (table_name, metric_read))
        metric_list = self.createNewMetrics(metric_from_file, my_date)
        for metric in metric_list:
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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("metricdate", help="The date of the day you want to collect")
    parser.add_argument("--tablename", help="Specify a table name if you want only a file for this table")
    parser.add_argument("--metricname", help="Specify a metric name if you want only a file for this metric (table name required)")
    args = parser.parse_args()
    if args.metricname and not args.tablename:
        parser.error("You cannot use args metric name without specifying a table name")
    return args


if __name__ == "__main__":
    args = parse_args()
    my_date = args.metricdate

    myfrom = int(time.mktime(datetime.datetime.strptime("%s 00:00:00" % my_date, "%Y%m%d %H:%M:%S").timetuple()))
    myuntil = int(time.mktime(datetime.datetime.strptime("%s 23:59:59" % my_date, "%Y%m%d %H:%M:%S").timetuple()))

    try:
        os.makedirs(cfg.file_dest_dir, exist_ok=True)
        global_writer = CSVGlobaWriter("%s/%s_%s.txt" % (cfg.file_dest_dir.replace("\\", "/"), cfg.prefixe_GlobalFilename, my_date))


        with open(cfg.file_path_metrics) as metrics_file:
            metrics_yml = yaml.safe_load(metrics_file)

            if args.tablename:
                table_name = args.tablename
                os.makedirs(f"{cfg.app_directory}/tmp", exist_ok=True)
                csvDwriter = CSVDataWriter(f"{cfg.app_directory}/tmp/{table_name}_{my_date}.csv", table_name)

                if args.metricname:
                    csvDwriter.processMetric(table_name, args.metricname, metrics_yml['TABLES'][table_name][args.metricname], my_date)
                else:
                    for metric_read in metrics_yml['TABLES'][table_name]:
                        csvDwriter.processMetric(table_name, metric_read, metrics_yml['TABLES'][table_name][metric_read], my_date)
                csvDwriter.file.close()
                global_writer.addFileRow(csvDwriter.filename)
            else:
                for table_name in metrics_yml['TABLES']:
                    csvDwriter = CSVDataWriter("%s/tmp/%s_%s.csv" % (cfg.app_directory, table_name, my_date), table_name)
                    for metric_read in metrics_yml['TABLES'][table_name]:
                        csvDwriter.processMetric(table_name, metric_read, metrics_yml['TABLES'][table_name][metric_read], my_date)
                    csvDwriter.file.close()
                    global_writer.addFileRow(csvDwriter.filename)

            global_writer.file.close()
    except IOError:
        print("Error while reading the metrics file. Does it exist?")
        raise