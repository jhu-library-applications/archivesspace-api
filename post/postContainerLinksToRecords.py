import json
import requests
import secret
import csv

secretVersion = input('To edit production server, enter secret file: ')
if secretVersion != '':
    try:
        secret = __import__(secretVersion)
        print('Editing Production')
    except ImportError:
        print('Editing Development')
else:
    print('Editing Development')

targetFile = input('Enter file name: ')
targetRecord = input('Enter record type and resource_id (e.g. \'accessions/2049\'): ')

baseURL = secret.baseURL
user = secret.user
password = secret.password
repository = secret.repository

auth = requests.post(baseURL+'/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}

csv = csv.DictReader(open(targetFile))
link = baseURL+'/repositories/'+repository+'/'+targetRecord
asRecord = requests.get(link, headers=headers).json()
print(link)
f = open(targetRecord+'asRecordBackup.json', 'w')
json.dump(asRecord, f)
instanceArray = asRecord['instances']

for row in csv:
    uri = row['uri']
    print(uri)
    top_container = {'ref': uri}
    sub_container = {'top_container': top_container}
    instance = {'sub_container': sub_container, 'instance_type': 'mixed_materials'}
    instanceArray.append(instance)
asRecord['instances'] = instanceArray
f2 = open(targetRecord+'asRecordModified.json', 'w')
json.dump(asRecord, f2)
asRecord = json.dumps(asRecord)
post = requests.post(link, headers=headers, data=asRecord).json()
print(post)