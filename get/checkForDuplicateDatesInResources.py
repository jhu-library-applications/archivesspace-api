import requests
import secret
import time
import csv

secretVersion = input('To edit production server, enter secret file name: ')
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

endpoint = '/repositories/'+repository+'/resources?all_ids=true'

ids = requests.get(baseURL+endpoint, headers=headers).json()

records = []
f = csv.writer(open('duplicateBeginEndDates.csv', 'w'))
f2 = csv.writer(open('asDates.csv', 'w'))
f.writerow(['uri']+['begin']+['end']+['expression']+['entity_type'])
f2.writerow(['uri']+['begin']+['end']+['expression']+['entity_type'])
counter = 0
for r_id in ids:
    endpoint = '/repositories/'+repository+'/resources/'+str(r_id)
    output = requests.get(baseURL+endpoint, headers=headers).json()
    for date in output['dates']:
        counter = counter + 1
        print(counter)
        try:
            begin = date['begin']
        except KeyError:
            begin = ''
        try:
            end = date['end']
        except KeyError:
            end = ''
        try:
            expression = date['expression']
        except KeyError:
            expression = ''
        if begin == end and begin != '':
            f.writerow([output['uri']]+[begin]+[end]+[expression]+[date['date_type']])
        else:
            f2.writerow([output['uri']]+[begin]+[end]+[expression]+[date['date_type']])

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))