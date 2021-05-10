#!/usr/bin/env python

from google.oauth2.credentials import Credentials
from google.cloud import bigquery


location = "US"
dataset = "palak_us"
table = 'gb_hsbc_ucm_workflow_workitem'

client = bigquery.Client(location=location)


print(client.project, dataset, table)
import csv
import json
import functools
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed


query = f" SELECT column_name, data_type, is_nullable FROM {dataset}.INFORMATION_SCHEMA.COLUMNS WHERE  table_name='{table}'"
query_job = client.query(query)

schema = {}
# for col in cols:
for row in query_job:
    schema[row['column_name']]= {
        'data_type':row['data_type'],
        'is_nullable':row['is_nullable']
    }

# get count
query_job = client.query(f"SELECT count(*) FROM {dataset}.{table}")
for row in query_job:
    records_count = int(row[0])
    
def get_col_info(key):
    # unique value count
    query = f"SELECT count(distinct {key}),max({key}),min({key}) FROM {dataset}.{table}"
    query_job = client.query(query)  # Make an API request.
    for row in query_job:
        unique_count = int(row[0])
        value_max = str(row[1])
        value_min = str(row[2])
    # value set
    query = f"SELECT {key},count(*) FROM {dataset}.{table} group by {key} order by count(*) desc limit 10"
    query_job = client.query(query)  # Make an API request.
    values={}
    for row in query_job:
        # probability of each value
        values[str(row[key])]=round(int(row[1])/records_count, 3)
    schema[key]['values']= values
    # max and min
    query = f"SELECT max({key}),min({key}) FROM {dataset}.{table}"
    query_job = client.query(query)  # Make an API request.
    res = {
        'unique_count': unique_count,
        'value_max': value_max,
        'value_min': value_min,
        'values': values
    }
    print(key,res)
    return res

with ThreadPoolExecutor(max_workers = 10) as executor:
    tasks = {executor.submit(get_col_info, key):key for key in schema}
    for future in as_completed(tasks):
        key = tasks[future]
        try:
            data = future.result()
        except Exception as exc:
            print(' generated an exception: %s' % (exc))
        else:
            schema[key].update(data)


schema['__most_unique_col'] =  max(schema, key=lambda x: schema[x].get('unique_count'))
schema['__most_unique_count'] = schema[schema['__most_unique_col']].get('unique_count')
schema['__count'] = records_count

json_object = json.dumps(schema, indent = 4)
json_filename = f"{table}.json"
with open(json_filename, "w") as outfile:
    outfile.write(json_object)

print(f"Jobs done! Check {json_filename}")