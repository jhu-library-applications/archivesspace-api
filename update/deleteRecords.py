import json
import requests
from datetime import datetime
import time
import argparse
import secret
import pandas as pd
import urllib3

startTime = time.time()

secretVersion = input('To edit production server, enter secret filename: ')
if secretVersion != '':
    try:
        secret = __import__(secretVersion)
        print('Editing Production')
    except ImportError:
        print('Editing Development')
else:
    print('Editing Development')

# import secret
base_url = secret.base_url
user = secret.user
password = secret.password
repo = secret.repository
verify = secret.verify

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='filename to retrieve')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter file name as filename.csv: ')

s = requests.Session()

# authenticate
auth = s.post(base_url+'/users/'+user+'/login?password='+password, verify=verify).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session,
           'Content_Type': 'application/json'}

df = pd.read_csv(filename)
total_count = len(df)
print(total_count)

log = []
for count, row in df.iterrows():
    item_log = row.copy()
    uri = row['uri']
    print(count, uri)
    full_link = base_url+uri
    try:
        delete_response = s.delete(full_link, headers=headers, verify=verify).json()
    except requests.exceptions.RequestException as e:
        item_log['error'] = e
        print(e)
        log.append(item_log)
        continue

    status = delete_response['status']
    item_log['post_status'] = status
    print(status)
    log.append(item_log)

log = pd.DataFrame.from_dict(log)
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
log.to_csv('logOfDeletedRecords_'+dt+'.csv', index=False)

# Show script runtime
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Post complete.  Total script run time: ', '%d:%02d:%02d' % (h, m, s))
