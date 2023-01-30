Python scripts used to perform various tasks with the ArchivesSpace API

## Authenticating to the API

All of these scripts require a secret.py file in the same directory that must contain the following text:

	baseURL = '[ArchivesSpace API URL]'
	user = '[user name]'
	password = '[password]'
	repository = '[repository]'

This secret.py file will be ignored according to the repository's .gitignore file so that ArchivesSpace login details will not be inadvertently exposed through GitHub.

If you are using both a development server and a production server, you can create a separate secret.py file with a different name (e.g. secretProd.py) and containing the production server information. When running each of these scripts, you will be prompted to enter the file name (e.g 'secretProd' without '.py') of an alternate secret file. If you skip the prompt or incorrectly type the file name, the scripts will default to the information in the secret.py file. This ensures that you will only access the production server if you really intend to.

## Helpful links

- [ArchivesSpace JSON Schema List](https://archivesspace.github.io/archivesspace/doc/schema_list.html)
- [ArchivesSpace API Reference](https://archivesspace.github.io/archivesspace/api/)

## Scripts

### create

#### [createDigitalObjects.py](/create/createDigitalObjects.py)
Creates a Digital Object JSON file from a CSV.
#### [eadToCsv.py](/create/eadToCsv.py)
Based on a specified file name and a specified file path, extracts selected elements from an EAD XML file and prints them to a CSV file.

### get

#### [getAccessionUDFs.py](/get/getAccessionUDFs.py)
Retrieves all user-defined fields from all accessions in the specified repository.

#### [getAccessions.py](/get/getAccessions.py)
Retrieves all accessions from a particular repository into a JSON file.

#### [getAllArchivalObjectTitles.py](/get/getAllArchivalObjectTitles.py)
Retrieves titles from all archival objects in a repository. Upon running the script, you will be prompted enter the resource ID (just the number, not the full URI).

#### [getArchivalObjectCountByResource.py](/get/getArchivalObjectCountByResource.py)
Retrieves a count of archival objects associated with a particular resource. Upon running the script, you will be prompted enter the resource ID (just the number, not the full URI).

#### [getArchivalObjectsByResource.py](/get/getArchivalObjectsByResource.py)
Retrieves all archival objects associated with a particular resource. Upon running the script, you will be prompted enter the resource ID (just the number, not the full URI).

#### [getArchivalObjectRefIdsForResource.py](/get/getArchivalObjectRefIdsForResource.py)
Retrieves the title, URI, ref_id, date expression, and level for all archival objects associated with a particular resource. Upon running the script, you will be prompted enter the resource ID (just the number, not the full URI).

#### [getArrayPropertiesFromPeople.py](/get/getArrayPropertiesFromPeople.py)
Retrieves specific properties, including properties that have arrays as values, from the JSON of ArchivesSpace agent_people records.

#### [getEntitiesNotPublished.py](/get/getEntitiesNotPublished.py)
Retrieves unpublished entities (where Publish = False) from ArchivesSpace and lists them in a CSV file.

Using the argparse module, the user enters in the terminal either "people," "corporate_entities," or "families" to search for unpublished entities under those categories. The CSV also prints several properties of the unpublished agent, which can be adjusted in the script based on information needs.

#### [getPropertiesFromResources.py](/get/getPropertiesFromResources.py)
Retrieves select properties from all resources in the repository.

#### [getPropertiesFromSingleResource.py](/get/getPropertiesFromSingleResource.py)
Based on user input, retrieves select properties from the specified resource.

#### [getSingleResource.py](/get/getSingleResource.py)
Based on user input, retrieves a single ArchivesSpace record based on the specified record's 'uri.'

#### [getTopContainerCountByResource.py](/get/getTopContainerCountByResource.py)
Retrieves a count of top containers associated with archival objects associated with a particular resource. Upon running the script, you will be prompted enter the resource ID (just the number, not the full URI).

#### [getTopContainerCountByResourceNoAOs.py](/get/getTopContainerCountByResourceNoAOs.py)
Retrieves a count of top containers directly associated (not through an archival object) with a particular resource. Upon running the script, you will be prompted enter the resource ID (just the number, not the full URI).

#### [getTopContainers.py](/get/getTopContainers.py)
Retrieves all top containers from a particular repository into a JSON file.

#### [getUnassociatedContainers.py](/get/getUnassociatedContainers.py)
Prints the URIs to a CSV file of all top containers that are not associated with a resource or archival object.

#### [getUrisAndIds.py](/get/getUrisAndIds.py)
For the specified record type, retrieves URI and the 'id_0,' 'id_1,' 'id_2,' 'id_3,' and a concatenated version of all the 'id' fields.

#### [getURIsFromKeywordSearch.py](/get/getURIsFromKeywordSearch.py)

You can choose one or more types of records (accession, resource, subject, agent, location, or archival_object) to search in ArchiveSpace by a certain keyword. This will return a CSV with the URIs of records with that keyword.

#### [getUserDefinedFieldsFromResources.py](/get/getUserDefinedFieldsFromResources.py)

This script searches the following user-defined fields in all resources and accessions for any values.

1. accessionAcknowledged
2. selector
3. assignedTo
4. appraisalLegacy
5. custodialHistory
6. electronicRecordLog
7. relatedMaterialsNote
8. archiveItSeeds
9. appraisal
10. accessionStatus

For records with values in any of its user-defined fields, its title, uri, and all user-defined fields will be recorded in a CSV called UserDefinedFieldsFromResources.csv.

#### [getPropertiesFromArchivalObjects.py](/get/getPropertiesFromArchivalObjects.py)
Retrieves specific properties from the JSON of ArchivesSpace archival_object records into a CSV file.

#### [getPropertiesFromDigitalObjects.py](/get/getPropertiesFromDigitalObjects.py)
Retrieves specific properties from the JSON of ArchivesSpace digital_object records into a CSV file.

#### [getPropertiesFromPeople.py](/get/getPropertiesFromPeople.py)
Retrieves specific properties from the JSON of ArchivesSpace agent_people records into a CSV file.

### post
#### [postContainersFromCSV.py](/post/postContainersFromCSV.py)
Creates instances of top_containers from a separate CSV file. The CSV file should have two columns, indicator and barcode. The directory where this file is stored must match the directory in the filePath variable. The script will prompt you first for the exact name of the CSV file, and then for the exact resource or accession to attach the containers to.

#### [postContainerLinksToRecords.py](/post/postContainerLinksToRecords.py)
Based on user input, posts containers to a specified record based on a specified CSV file.

#### [postContainerLinksToRecordsFromCSV.py](/post/postContainerLinksToRecordsFromCSV.py)
Based on user input, posts containers to a specified record based on a specified CSV file of top container and resource URIs.

#### [postCorporateAgentsFromCSV.py](/post/postCorporateAgentsFromCSV.py)
Based on user input, posts corporate agents based on a specified CSV file.

#### [postDigitalObjects.py](/post/postDigitalObjects.py)
Posts JSON files of digital objects to specified resource.

#### [postFamilyAgentsFromCSV.py](/post/postFamilyAgentsFromCSV.py)
Based on user input, posts family agents based on a specified CSV file.

#### [postNew.py](/post/postNew.py)
Posts new records to a generic API endpoint based the record type, 'agents/people' in this example. This script can be modified to accommodate other data types (e.g. 'repositories/[repo ID]/resources' or 'agents/corporate_entities'). 

It requires a properly formatted JSON file (specified where [JSON File] appears in the 'records' variable) for the particular ArchivesSpace record type you are trying to post.  

#### [postOverwrite.py](/post/postOverwrite.py)
Overwrites existing ArchivesSpace records based the 'uri' and can be used with any ArchivesSpace record type (e.g. resource, accession, subject, agent_people, agent_corporate_entity, archival_object, etc.). 

It requires a properly formatted JSON file (specified where [JSON File] appears in the 'records' variable) for the particular ArchivesSpace record type you are trying to post.

#### [postPeopleAgentsFromCSV.py](/post/postPeopleAgentsFromCSV.py)
Based on user input, posts people agents based on a specified CSV file.

#### [postSubjectsFromCSV.py](/post/postSubjectsFromCSV.py)
Based on user input, posts subjects based on a specified CSV file.

### update

#### [transferAoDatesToDos.py](/update/transferAoDatesToDos.py)
Transfers the date from an archival object to any attached digital objects.

#### [unpublishArchivalObjectsByResource.py](/update/unpublishArchivalObjectsByResource.py)
Un-publishes all archival objects associated with the specified resource. Upon running the script, you will be prompted enter the resource ID (just the number, not the full URI).

#### [updateKeywordInRecords.py](/update/updateKeywordInRecords.py)
This script searches the URIs selected by getURIsFromKeywordSearch.py and finds the relevant properties in that record with the keyword and replaces them. It most likely will NOT find the keyword in all records generated  by getURIsFromKeywordSearch.py, as this script will get a record if one of its related records has the keyword, rather than that record containing the keyword itself.

#### [updateResourceWithAgentOrSubjectLinks.py](/update/updateResourceWithAgentOrSubjectLinks.py)
Based on user input, posts agent or subject links to resources based on a specified CSV file.

#### [updateResourceWithCSV.py](/update/updateResourceWithCSV.py)
Based on user input, updates first level (['title']) and second level (['user_defined']['real_1']) elements for resources based on a specified CSV file.