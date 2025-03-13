import requests
import secret
import pandas as pd
from datetime import datetime
import time

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

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}
print('authenticated')

endpoint = '/subjects?all_ids=true'

subject_ids = requests.get(baseURL+endpoint, headers=headers).json()
total_subjects = len(subject_ids)
print('Total of {} subjects.'.format(total_subjects))

all_items = []
for subject_id in subject_ids:
    print(subject_id)
    subject_dict = {}
    endpoint = '/subjects/'+str(subject_id)
    output = requests.get(baseURL+endpoint, headers=headers).json()

    uri = output['uri']
    title = output['title']
    authority_id = output.get('authority_id')
    source = output.get('source')
    terms = output['terms'][0]
    term_type = terms.get('term_type')
    print(term_type)
    subject_dict['uri'] = uri
    subject_dict['title'] = title
    subject_dict['authority_id'] = authority_id
    subject_dict['source'] = source
    subject_dict['term_type'] = term_type
    all_items.append(subject_dict)

df = pd.DataFrame.from_records(all_items)
print(df.head(15))
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df.to_csv('subjectProperties_'+dt+'.csv', index=False)

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))
