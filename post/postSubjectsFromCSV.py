import json
import requests
import time
import secret
import pandas as pd
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter filename (including \'.csv\'): ')

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

# Authenticate user information for ArchivesSpace.
auth = requests.post(baseURL+'/users/'+user+'/login?password='+password).json()
session = auth['session']
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}

# Convert CSV with subject information into DataFrame.
df = pd.read_csv(filename)

logForAllItems = []
for index, row in df.iterrows():
    # Get subject information from CSV.
    label = row['label']
    print('Gathering subject #{}: {}.'.format(index, label))
    subject_type = row['type']
    source = row['source']
    source_uri = row['uri']

    # Build JSON record for subject.
    subjectRecord = {}
    terms = []
    term = {'term': label, 'term_type': subject_type, 'vocabulary': '/vocabularies/1'}
    terms.append(term)
    subjectRecord['terms'] = terms
    subjectRecord['publish'] = True
    subjectRecord['jsonmodel_type'] = 'subject'
    subjectRecord['source'] = source
    subjectRecord['vocabulary'] = '/vocabularies/1'
    subjectRecord['authority_id'] = source_uri
    subjectRecord = json.dumps(subjectRecord)
    print('JSON created for {}.'.format(label))

    # Create dictionary for item log.
    itemLog = {}

    # Try to POST JSON to ArchivesSpace API subject endpoint.
    try:
        post = requests.post(baseURL+'/subjects', headers=headers, data=subjectRecord).json()
        # Get URI and add to item log
        uri = post['uri']
        print('Subject successfully created with URI: {}'.format(uri))
        itemLog = {'uri': uri, 'label': label}
        # Add item log to list of logs
        logForAllItems.append(itemLog)

    # If POST to ArchivesSpace fails, break loop.
    except requests.exceptions.JSONDecodeError:
        itemLog = {'uri': 'error', 'label': label}
        # Add item log to list of logs
        logForAllItems.append(itemLog)
        print('POST to AS failed, breaking loop.')
        break
    print('')

# Convert logForAllItems to DataFrame.
log = pd.DataFrame.from_dict(logForAllItems)

# Create CSV of all item logs.
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
subjectCSV = 'postNewSubjects_'+dt+'.csv'
log.to_csv(subjectCSV)
print('{} created.'.format(subjectCSV))

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))