import requests
import secret
import time
import csv

secretVersion = input('To edit production server, enter secret filename: ')
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

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}

endpoint = '/search?page=1&page_size=2000&entity_type[]=top_container&filter_term[]={"empty_u_sbool":true}&q="/repositories/3"'

results = requests.get(baseURL + endpoint, headers=headers).json()
results = results['results']

f = csv.writer(open('unassociatedTopContainer.csv', 'w'))
f.writerow(['uri'])

for result in results:
    uri = result['uri']
    f.writerow([uri])

print(len(results))