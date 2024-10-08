import json
import requests
import secret
import csv
import time
import argparse
from datetime import datetime

secretVersion = input('To edit production server, enter secret filename: ')
if secretVersion != '':
    try:
        secret = __import__(secretVersion)
        print('Editing Production')
    except ImportError:
        print('Editing Development')
else:
    print('Editing Development')

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='JSON file of records to post')
parser.add_argument('-e', '--endpoint', help='Endpoint for record entity_type')
args = parser.parse_args()

if args.file:
    file = args.file
else:
    file = input('Enter the JSON file of records to post (".json"): ')
if args.endpoint:
    endpoint = args.endpoint
else:
    endpoint = input('Endpoint for the record type ("resources", "agents"): ')

startTime = time.time()

baseURL = secret.baseURL
user = secret.user
password = secret.password
repository = secret.repository

auth = requests.post(baseURL+'/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}

dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')

f = csv.writer(open('postNew_'+dt+'.csv', 'w'))
f.writerow(['post'])

records = json.load(open(file))
for i in range(0, len(records)):
    record = json.dumps(records[i])
    post = requests.post(baseURL+'/'+endpoint, headers=headers, data=record).json()
    post = json.dumps(post)
    print(post)
    f.writerow([post])

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))