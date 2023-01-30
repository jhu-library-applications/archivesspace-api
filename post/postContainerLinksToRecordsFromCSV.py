import json
import requests
import secret
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

targetFile = input('Enter file name: ')

baseURL = secret.baseURL
user = secret.user
password = secret.password
repository = secret.repository

auth = requests.post(baseURL+'/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}

csvfile = csv.DictReader(open(targetFile))

f = csv.writer(open('containerLinksPostedFromCSV.csv', 'w'))
f.writerow(['topContainer']+['resource']+['post'])

for row in csvfile:
    uri = row['uri']
    resourceUri = row['resourceuri']
    link = baseURL+resourceUri
    asRecord = requests.get(link, headers=headers).json()
    instanceArray = asRecord['instances']
    top_container = {'ref': uri}
    sub_container = {'top_container': top_container}
    instance = {'sub_container': sub_container, 'instance_type': 'mixed_materials'}
    instanceArray.append(instance)
    asRecord['instances'] = instanceArray
    asRecord = json.dumps(asRecord)
    post = requests.post(link, headers=headers, data=asRecord).json()
    print(post)
    f.writerow([uri]+[resourceUri]+[post])