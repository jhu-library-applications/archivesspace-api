"""Creates a CSV with a count of archival objects by series and subseries for a particular resource. """

import requests
import secret
import time
import argparse
import pandas as pd
from datetime import datetime

secretVersion = input('To edit production server, enter secret file name: ')
if secretVersion != '':
    try:
        secret = __import__(secretVersion)
        print('Editing Production')
    except ImportError:
        print('Editing Development')
else:
    print('Editing Development')

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--a_id', help='resourceID of the child_dict to retrieve.')

args = parser.parse_args()

if args.a_id:
    resourceID = args.a_id
else:
    resourceID = input('Enter resource ID: ')

startTime = time.time()

base_url = secret.base_url
user = secret.user
password = secret.password
repository = secret.repository

repository = str(repository)
auth = requests.post(base_url+'/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}

def get_children_metadata(child_object):
    child_details = {}
    child_title = child_object['title']
    print(child_title)
    child_uri = child_object['uri']
    has_children = child_object['has_children']
    child_details['title'] = child_title
    child_details['uri'] = child_uri
    child_details['has_children'] = has_children
    if has_children is True:
        descendants = child_object['children']
        number_descendants = len(descendants)
        child_details['descendants'] = number_descendants
    else:
        descendants = None
    to_save.append(child_details)
    return descendants

to_save = []
endpoint = '/bulk_archival_object_updater/repositories/' + repository + '/resources/' + resourceID + '/small_tree'
print(endpoint)
output = requests.get(base_url + endpoint, headers=headers).json()
children = output['children']
for child in children:
    second_children = get_children_metadata(child)
    if second_children:
        for second in second_children:
            third_children = get_children_metadata(second)
            if third_children:
                for third in third_children:
                    fourth_children = get_children_metadata(third)
                    if fourth_children:
                        for fourth in fourth_children:
                            fifth_children = get_children_metadata(fourth)
                            print(len(fifth_children))

df = pd.DataFrame.from_records(to_save)
print(df.head)
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df.to_csv('archival_objects_'+dt+'.csv', index=False)


