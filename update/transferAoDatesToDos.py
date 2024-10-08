import json
import requests
import secret
import time
import csv

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

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}
print('authenticated')

endpoint = '/repositories/'+repository+'/archival_objects?all_ids=true'

ids = requests.get(baseURL + endpoint, headers=headers).json()
ids.reverse()
print(len(ids))

# Generates a text file of AOs with DOs. Takes 2+ hours to generate so this code block is separate so the main portion of the script can be run more quickly.

# f=csv.writer(open('archivalObjectsWithDigitalObjects.csv', 'w'))
# f.writerow(['uri'])
# doAos = []
#
# for a_id in ids:
#     endpoint = '/repositories/'+repository+'/archival_objects/'+str(a_id)
#     output = requests.get(baseURL + endpoint, headers=headers).json()
#     try:
#         dates = output['dates']
#     except:
#         dates = ''
#     uri = output['uri']
#     instances = output['instances']
#     for instance in instances:
#         if instance['instance_type'] == 'digital_object':
#             doUri = instance['digital_object']['ref']
#             print(doUri)
#             f.writerow([uri])
#             doAos.append(uri)
#
# f2=open('archivalObjectsWithDigitalObjectsList.txt', 'w')
# f2.write(json.dumps(doAos))

f = csv.writer(open('DigitalObjectsDatesEdited.csv', 'w'))
f.writerow(['doUri']+['oldBegin']+['oldEnd']+['oldExpression']+['oldLabel']+['aoUri']+['newBegin']+['newEnd']+['newExpression']+['newLabel']+['post'])

doAos = json.load(open('archivalObjectsWithDigitalObjectsList.txt', 'w'))
for doAo in doAos:
    print(doAo)
    aoBegin = ''
    aoExpression = ''
    aoLabel = ''
    aoEnd = ''
    doBegin = ''
    doExpression = ''
    doLabel = ''
    doEnd = ''
    aoOutput = requests.get(baseURL + doAo, headers=headers).json()
    try:
        aoDates = aoOutput['dates']
        for aoDate in aoDates:
            try:
                aoBegin = aoDate['begin']
            except KeyError:
                aoBegin = ''
            try:
                aoEnd = aoDate['end']
            except KeyError:
                aoEnd = ''
            try:
                aoExpression = aoDate['expression']
            except KeyError:
                aoExpression = ''
            try:
                aoLabel = aoDate['label']
            except KeyError:
                aoLabel = ''
    except KeyError:
        aoBegin = ''
        aoExpression = ''
        aoLabel = ''
        aoEnd = ''
    try:
        instances = aoOutput['instances']
    except KeyError:
        continue
    for instance in instances:
        if instance['instance_type'] == 'digital_object':
            if aoBegin+aoExpression+aoLabel != '':
                doUri = instance['digital_object']['ref']
                doOutput = requests.get(baseURL + str(doUri), headers=headers).json()
                print('moving date from AO to DO')
                doDates = doOutput['dates']
                if not doDates:
                    print('no date', doDates)
                    doBegin = ''
                    doExpression = ''
                    doLabel = ''
                    doEnd = ''
                    doDates = []
                    doDate = {'begin': aoBegin, 'expression': aoExpression, 'label': aoLabel, 'date_type': 'single'}
                    if aoEnd != '':
                        doDate['end'] = aoEnd
                        doDate['date_type'] = 'range'
                    doDates.append(doDate)
                    doOutput['dates'] = doDates
                    output = json.dumps(doOutput)
                    doPost = requests.post(baseURL + doUri, headers=headers, data=output).json()
                    print(doPost)
                else:
                    print('existing date', doDates)
                    for doDate in doDates:
                        try:
                            doBegin = doDate['begin']
                        except KeyError:
                            doBegin = ''
                        try:
                            doEnd = doDate['end']
                        except KeyError:
                            doEnd = ''
                        try:
                            doExpression = doDate['expression']
                        except KeyError:
                            doExpression = ''
                        try:
                            doLabel = doDate['label']
                        except KeyError:
                            doLabel = ''
                        if aoBegin != '':
                            doDate['begin'] = aoBegin
                        if aoExpression != '':
                            doDate['expression'] = aoExpression
                        if aoLabel != '':
                            doDate['label'] = aoLabel
                        if aoEnd != '':
                            doDate['end'] = aoEnd
                    doOutput['dates'] = doDates
                    output = json.dumps(doOutput)
                    doPost = requests.post(baseURL + doUri, headers=headers, data=output).json()
                    print(doPost)
                f.writerow([doUri]+[doBegin]+[doEnd]+[doExpression]+[doLabel]+[doAo]+[aoBegin]+[aoEnd]+[aoExpression]+[aoLabel]+[doPost])

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))