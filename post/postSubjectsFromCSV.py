import json
import requests
import time
import csv
import secret

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

targetFile = input('Enter file name: ')

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth['session']
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}

f = csv.writer(open('postNewSubjects.csv', 'w'))
f.writerow(['sortName']+['uri'])

csvfile = csv.DictReader(open(targetFile))

for row in csvfile:
    subjectRecord = {}
    terms = []
    term = {'term': row['label'], 'term_type': row['type'], 'vocabulary': '/vocabularies/1'}
    terms.append(term)

    subjectRecord['terms'] = terms
    subjectRecord['publish'] = True
    subjectRecord['jsonmodel_type'] = 'subject'
    subjectRecord['source'] = 'fast'
    subjectRecord['vocabulary'] = '/vocabularies/1'
    subjectRecord['authority_id'] = row['uri']
    subjectRecord = json.dumps(subjectRecord)
    print(subjectRecord)
    post = requests.post(baseURL + '/subjects', headers=headers, data=subjectRecord).json()
    print(json.dumps(post))
    uri = post['uri']
    f.writerow([row['label']]+[uri])

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))