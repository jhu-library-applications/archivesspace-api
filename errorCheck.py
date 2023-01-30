import json
import requests
import secret
import time

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

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password, verify=False).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}
print('authenticated')
repository =['5']
for repo in repository:
    endpoint = '/repositories/'+repo+'/resources'
    ids = requests.get(baseURL+endpoint, headers=headers, verify=False).json()
    print(ids)
    # for a_id in ids:
    #     a_id = str(a_id)
    #     endpoint = '/repositories/'+repo+'/resources/'+a_id
    #     output = requests.get(baseURL+endpoint, headers=headers, verify=False).json()
    #     f = open(a_id+'_resources.json', 'w')
    #     results = (json.dump(output, f))
    #     f.close()


elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))