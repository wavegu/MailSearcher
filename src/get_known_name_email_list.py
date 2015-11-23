import json


person_list = []
with open('src/citation_top_1000.json') as json_file:
	json_content = json_file.read()
	person_list = json.loads(json_content)

for person_dict in person_list:
	if 'email' not in person_dict:
		person_dict['email'] = ''
	if not person_dict['email']:
		continue
	print person_dict['name'], person_dict['email']	