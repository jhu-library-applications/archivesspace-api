import requests
import secrets
import pandas as pd
import argparse
from datetime import datetime

secretsVersion = input('To edit production server, enter secrets file name: ')
if secretsVersion != '':
    try:
        secrets = __import__(secretsVersion)
        print('Editing Production')
    except ImportError:
        print('Editing Development')
else:
    print('Editing Development')

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='file_name to retrieve')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter file name as filename.csv: ')

baseURL = secrets.baseURL
user = secrets.user
password = secrets.password
repository = secrets.repository
verify = True

df_1 = pd.read_csv(filename)
itemList = df_1.record_uri.to_list()


def collect_property(dictionary, ao_property, name=None):
    if dictionary is not None:
        value = dictionary.get(ao_property)
        if value is not None:
            if name:
                tiny_dict[name] = value
            else:
                tiny_dict[ao_property] = value


auth = requests.post(baseURL+'/users/'+user+'/login?password='+password,
                     verify=verify).json()
session = auth['session']
print(auth)
print(session)
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}
all_items = []
for count, item in enumerate(itemList):
    tiny_dict = {}
    print(count)
    print(baseURL+item)
    output = requests.get(baseURL+item, headers=headers, verify=verify).json()
    collect_property(output, 'uri')
    collect_property(output, 'title')
    dates = output.get('dates')
    for date in dates:
        collect_property(date, 'expression')
        collect_property(date, 'begin')
        collect_property(date, 'end')
        collect_property(date, 'date_type')
        collect_property(date, 'label')
    instances = output.get('instances')
    for instance in instances:
        sub_container = instance.get('sub_container')
        if sub_container:
            top_container = sub_container.get('top_container')
            collect_property(top_container, 'ref', 'container')
        digital_object = instance.get('digital_object')
        collect_property(digital_object, 'ref', 'digital')
    all_items.append(tiny_dict)


df = pd.DataFrame.from_dict(all_items)
print(df.head)
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df.to_csv('archival_objects_'+dt+'.csv', index=False)