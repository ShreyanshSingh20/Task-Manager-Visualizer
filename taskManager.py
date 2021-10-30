import psutil
from datetime import datetime
import pandas as pd
import time
import os
import json
import csv
from elasticsearch import Elasticsearch, helpers
es = Elasticsearch(host = "localhost", port = 9200)
es = Elasticsearch()
        
def get_processes_info():
    
    processes = []
    for process in psutil.process_iter():
      
        with process.oneshot():
           
            pid = process.pid
            if pid == 0:
              
                continue
            
            name = process.name()
          
        
            try: 
                cores = len(process.cpu_affinity())
            except psutil.AccessDenied:
                cores = 0
            
            cpu_usage = process.cpu_percent()
            
            status = process.status()
            try: 
                memory_usage = process.memory_full_info().uss
            except psutil.AccessDenied:
                memory_usage = 0
           
            io_counters = process.io_counters()
            read_bytes = io_counters.read_bytes
            write_bytes = io_counters.write_bytes
            
            n_threads = process.num_threads()
           
            
            
        processes.append({
            'pid': pid, 'name': name,
            'cores': cores, 'cpu_usage': cpu_usage, 'status': status,
            'memory_usage': memory_usage, 'read_bytes': read_bytes, 'write_bytes': write_bytes,
            'n_threads': n_threads,
        })

    field_names = ['pid', 'name',  'cores', 'cpu_usage', 'status','memory_usage', 'read_bytes','write_bytes','n_threads']

    with open('output.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(processes)

    print(processes)

    with open('D:\zenatix\output.csv') as f:
        reader = csv.DictReader(f)
        helpers.bulk(es, reader, index='my-index', doc_type='my-type')




get_processes_info()



