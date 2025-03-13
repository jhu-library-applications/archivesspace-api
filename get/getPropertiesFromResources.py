import csv
import time

import requests

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

startTime = time.time()

baseURL = secret.baseURL
user = secret.user
password = secret.password
repository = secret.repository
verify = secret.verify

auth = requests.post(baseURL+'/users/'+user+'/login?password='+password, verify=verify).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}

endpoint = '/repositories/'+repository+'/resources?all_ids=true'

ids = requests.get(baseURL + endpoint, headers=headers, verify=verify).json()

f = csv.writer(open('resourceProperties.csv', 'w'))
f.writerow(['title']+['uri']+['bib_number']+['entity_type']+['value'])

total = len(ids)
for resource_id in ids:
    print('a_id', id, total, 'records remaining')
    total -= 1
    endpoint = '/repositories/'+repository+'/resources/'+str(resource_id)
    output = requests.get(baseURL + endpoint, headers=headers, verify=verify).json()

    title = output['title']
    uri = output['uri']
    try:
        bib_number = output['user_defined']['real_1']
    except:
        bib_number = ''
    try:
        agents = output['linked_agents']
        for agent in agents:
            agentUri = agent['ref']
            agentOutput = requests.get(baseURL + agentUri, headers=headers, verify=verify).json()
            agentName = agentOutput['title']
            f.writerow([title]+[uri]+[bib_number]+['name']+[agentName])
    except:
        pass
    try:
        subjects = output['subjects']
        for subject in subjects:
            subjectUri = subject['ref']
            subjectOutput = requests.get(baseURL + subjectUri, headers=headers, verify=verify).json()
            subjectName = subjectOutput['title']
            f.writerow([title]+[uri]+[bib_number]+['subject']+[subjectName])
    except:
        pass
    for note in output['notes']:
        abstract = ''
        scopecontent = ''
        acqinfo = ''
        custodhist = ''
        bioghist = ''
        accessrestrict = ''
        relatedmaterial = ''
        try:
            if note['entity_type'] == 'abstract':
                abstract = note['content'][0]

                f.writerow([title]+[uri]+[bib_number]+['abstract']+[abstract])
            if note['entity_type'] == 'scopecontent':
                scopecontentSubnotes = note['subnotes']
                for subnote in scopecontentSubnotes:
                    scopecontent = scopecontent + subnote['content'] + ' '
                f.writerow([title]+[uri]+[bib_number]+['scopecontent']+[scopecontent])
            if note['entity_type'] == 'acqinfo':
                acqinfoSubnotes = note['subnotes']
                for subnote in acqinfoSubnotes:
                    acqinfo = acqinfo + subnote['content'] + ' '
                f.writerow([title]+[uri]+[bib_number]+['acqinfo']+[acqinfo])
            if note['entity_type'] == 'custodhist':
                custodhistSubnotes = note['subnotes']
                for subnote in custodhistSubnotes:
                    custodhist = custodhist + subnote['content'] + ' '
                f.writerow([title]+[uri]+[bib_number]+['custodhist']+[custodhist])
            if note['entity_type'] == 'bioghist':
                bioghistSubnotes = note['subnotes']
                for subnote in bioghistSubnotes:
                    bioghist = bioghist + subnote['content'] + ' '
                f.writerow([title]+[uri]+[bib_number]+['bioghist']+[bioghist])
            if note['entity_type'] == 'accessrestrict':
                accessrestrictSubnotes = note['subnotes']
                for subnote in accessrestrictSubnotes:
                    accessrestrict = accessrestrict + subnote['content'] + ' '
                f.writerow([title]+[uri]+[bib_number]+['accessrestrict']+[accessrestrict])
            if note['entity_type'] == 'relatedmaterial':
                relatedmaterialSubnotes = note['subnotes']
                for subnote in relatedmaterialSubnotes:
                    relatedmaterial = relatedmaterial + subnote['content'] + ' '
                f.writerow([title]+[uri]+[bib_number]+['relatedmaterial']+[relatedmaterial])
        except:
            f.writerow([title]+[uri]+[bib_number]+['']+[custodhist])

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))
