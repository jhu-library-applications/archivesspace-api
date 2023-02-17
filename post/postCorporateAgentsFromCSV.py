import json
import requests
import secret
import time
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

auth = requests.post(baseURL+'/users/'+user+'/login?password='+password).json()
session = auth['session']
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}


def add_field_to_record(field_name, record_dict):
    value = row.get(field_name)
    if value:
        value = value.strip()
        record_dict[field_name] = value
    else:
        pass


# Convert CSV with corporate entity information into DataFrame.
df = pd.read_csv(filename)

logForAllItems = []
for index, row in df.iterrows():
    # Get agent information from CSV.
    sort_name = row['sort_name']
    print('Gathering corporate entity #{}: {}.'.format(index, sort_name))

    agentRecord = {'publish': True, 'jsonmodel_type': 'agent_corporate_entity'}
    names = []
    name = {'jsonmodel_type': 'name_corporate_entity'}
    add_field_to_record('primary_name', name)
    add_field_to_record('subordinate_name_1', name)
    add_field_to_record('subordinate_name_2', name)
    add_field_to_record('qualifier', name)
    add_field_to_record('sort_name', name)
    add_field_to_record('authority_id', name)
    add_field_to_record('source', name)
    add_field_to_record('rules', name)
    add_field_to_record('name_order', name)
    add_field_to_record('use_dates', name)
    names.append(name)
    agentRecord['names'] = names

    dates = []
    date = {}
    add_field_to_record('jsonmodel_type', date)
    add_field_to_record('date_label', date)
    add_field_to_record('date_type', date)
    add_field_to_record('date_begin', date)
    add_field_to_record('date_end', date)
    if date:
        dates.append(date)
        agentRecord['dates_of_existence'] = dates

    notes = []
    note = {}
    subnotes = []
    subnote = {}
    add_field_to_record('jsonmodel_type', note)
    add_field_to_record('publish_note', note)
    add_field_to_record('content', subnote)
    add_field_to_record('publish_subnote', subnote)
    if subnote:
        subnotes.append(subnote)
        note['subnotes'] = subnotes
    if note:
        notes.append(note)
        agentRecord['notes'] = notes

    agentRecord = json.dumps(agentRecord)
    print('JSON created for {}.'.format(sort_name))

    # Create dictionary for item log.
    itemLog = {}

    # Try to POST JSON to ArchivesSpace API corporate entities' endpoint.
    try:
        post = requests.post(baseURL+'/agents/corporate_entities', headers=headers, data=agentRecord).json()
        print(json.dumps(post))
        uri = post['uri']
        print('Corporate entity successfully created with URI: {}'.format(uri))
        itemLog = {'uri': uri, 'sort_name': sort_name}
        # Add item log to list of logs
        logForAllItems.append(itemLog)

    # If POST to ArchivesSpace fails, break loop.
    except requests.exceptions.JSONDecodeError:
        itemLog = {'uri': 'error', 'sort_name': sort_name}
        # Add item log to list of logs
        logForAllItems.append(itemLog)
        print('POST to AS failed, breaking loop.')
        break
    print('')


# Convert logForAllItems to DataFrame.
log = pd.DataFrame.from_dict(logForAllItems)

# Create CSV of all item logs.
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
corporateCSV = 'postNewCorporateEntities_'+dt+'.csv'
log.to_csv(corporateCSV)
print('{} created.'.format(corporateCSV))

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))