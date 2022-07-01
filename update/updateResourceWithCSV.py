import json
import requests
import secrets
import time
import csv


def first_level_update(key, value_source):
    uri = row['uri']
    value = row[value_source]
    if value != '':
        as_record = requests.get(baseURL+uri, headers=headers).json()
        as_record[key] = value
        as_record = json.dumps(as_record)
        post = requests.post(baseURL + uri, headers=headers, data=as_record).json()
        print(post)
    else:
        pass


def second_level_update(key, value_source, first_level):
    uri = row['uri']
    value = row[value_source]
    if value != '':
        as_record = requests.get(baseURL+uri, headers=headers).json()
        try:
            as_record[first_level][key] = value
        except:
            as_record[first_level] = {}
            as_record[first_level][key] = value
        as_record = json.dumps(as_record)
        post = requests.post(baseURL + uri, headers=headers, data=as_record).json()
        print(post)
    else:
        pass


startTime = time.time()

baseURL = secrets.baseURL
user = secrets.user
password = secrets.password

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}

filename = input('Enter filename (including \'.csv\'): ')

with open(filename) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        second_level_update('real_1', 'bib', 'user_defined')

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))