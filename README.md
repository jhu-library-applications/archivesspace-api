Python scripts used to perform various tasks with the ArchivesSpace API

## Authenticating to the API

All of these scripts require a secret.py file in the same directory that must contain the following text:

	base_url = '[ArchivesSpace API URL]'
	user = '[user name]'
	password = '[password]'
	repository = '[repository]'

This secret.py file will be ignored according to the repository's .gitignore file so that ArchivesSpace login details will not be inadvertently exposed through GitHub.

If you are using both a development server and a production server, you can create a separate secret.py file with a different name (e.g. secretProd.py) and containing the production server information. When running each of these scripts, you will be prompted to enter the file name (e.g 'secretProd' without '.py') of an alternate secret file. If you skip the prompt or incorrectly type the file name, the scripts will default to the information in the secret.py file. This ensures that you will only access the production server if you really intend to.

## Helpful links

- [ArchivesSpace JSON Schema List](https://archivesspace.github.io/archivesspace/doc/schema_list.html)
- [ArchivesSpace API Reference](https://archivesspace.github.io/archivesspace/api/)

