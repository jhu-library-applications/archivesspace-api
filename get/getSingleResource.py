import json
import requests
import argparse
import urllib3
import secret

secretVersion = input('To edit production server, enter secret file name: ')
if secretVersion != '':
    try:
        secret = __import__(secretVersion)
        print('Editing Production')
    except ImportError:
        print('Editing Development')
else:
    print('Editing Development')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--uri', help='URI of the child_dict to retrieve.')
args = parser.parse_args()

if args.uri:
    uri = args.uri
else:
    uri = input('Enter handle (\'/repositories/3/resources/855\'): ')

uri = '/repositories/3/archival_objects/257988'

baseURL = secret.baseURL
user = secret.user
password = secret.password
repository = secret.repository
verify = secret.verify

auth = requests.post(baseURL+'/users/'+user+'/login?password='+password, verify=verify).json()
session = auth['session']
print('Session: '+session)
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}

print(baseURL+uri)
output = requests.get(baseURL + uri, headers=headers, verify=verify).json()
repository = str(repository)
uri = uri.replace('/repositories/'+repository+'/', '').replace('/', '-')
f = open(uri+'.json', 'w')
results = (json.dump(output, f))
f.close()