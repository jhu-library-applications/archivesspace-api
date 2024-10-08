import json
import requests
import secret
import time
import csv
from datetime import datetime

secretVersion = input('To edit production server, enter the name of the secret file: ')
if secretVersion != '':
    try:
        secret = __import__(secretVersion)
        print('Editing Production')
    except ImportError:
        print('Editing Development')
else:
    print('Editing Development')

startTime = time.time()

baseURL = secret.baseURL
user = secret.user
password = secret.password
repository = secret.repository

auth = requests.post(baseURL+'/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}

urisBibs = csv.DictReader(open(''))

dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
f = csv.writer(open('bibNumberPush'+dt+'.csv', 'w'))
f.writerow(['uri']+['existingValue']+['bibNum'])

for row in urisBibs:
    uri = row['asURI']
    bibNum = row['bibNum']
    print(uri)
    record = requests.get(baseURL+uri, headers=headers).json()
    try:
        print(record['user_defined'])
        record['user_defined']['real_1'] = bibNum
        existingValue = 'Y'
    except:
        value = {'real_1': row['bibNum']}
        record['user_defined'] = value
        print(value)
        existingValue = 'N'
    record = json.dumps(record)
    post = requests.post(baseURL+uri, headers=headers, data=record)
    print(post)
    f.writerow([uri]+[existingValue]+[bibNum]+[post])

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))