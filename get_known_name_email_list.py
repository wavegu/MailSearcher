# encoding=utf8 
import json
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

person_list = []
with open('src/citation_top_1000.json') as json_file:
	json_content = json_file.read()
	person_list = json.loads(json_content)

with open('known_name_email.txt', 'w') as known_name_email_file:
	for person_dict in person_list:
		if 'email' not in person_dict['contact']:
			person_dict['contact']['email'] = ''
		if not person_dict['contact']['email']:
			continue
		known_name_email_file.write(('%30s [%10s]\n') % (person_dict['name'], person_dict['contact']['email'].replace('\n', '')))