import requests
import secret
import csv
import argparse

secretVersion = input('To edit production server, enter secret filename: ')
if secretVersion != '':
    try:
        secret = __import__(secretVersion)
        print('Editing Production')
    except ImportError:
        print('Editing Development')
else:
    print('Editing Development')

types = []

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--keyword', help='Keyword to retrieve.')
parser.add_argument('-t', '--entity_type', choices=['accession', 'resource', 'subject', 'agent', 'location', 'archival_object'],
                    help='What entity_type of records do you want to search? Type out which of the following you want: '
                         'accession, resource, subject, agent, location, archival_object. optional - if not provided, '
                         'the script will ask for input')
args = parser.parse_args()

if args.keyword:
    keyword = args.keyword
else:
    keyword = input('Enter keyword to search: ')
if args.type:
    etype = args.type
    etype = etype.split(',')
    for item in etype:
        item = item.strip()
        item = '&entity_type[]='+item
        types.append(item)
else:
    etype = input('What record entity_type do you want to search? Type out what you want in a list: '
                  'accession, resource, subject, agent, location, archival_object. ')
    etype = etype.split(',')
    for item in etype:
        item = item.strip()
        item = '&entity_type[]='+item
        types.append(item)

types = ''.join(types)
print(types)


baseURL = secret.baseURL
user = secret.user
password = secret.password
repository = secret.repository

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}


endpoint = '/repositories/3/search?q='+keyword+types+'&page_size=2000&page=1'

results = requests.get(baseURL + endpoint, headers=headers).json()
results = results['results']

f = csv.writer(open(keyword+'Search.csv', 'w'))
f.writerow(['uri'])

for result in results:
    uri = result['uri']
    f.writerow([uri])

print(len(results))