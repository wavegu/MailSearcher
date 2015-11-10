import json
import os
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')


email_miss_counter = 0


class Person:

    def __init__(self, person_dict):
        global email_miss_counter
        self.name = person_dict['name']
        if 'email' not in person_dict['contact']:
            self.email = ''
            email_miss_counter += 1
            # pass
        else:
            email_addr = str(person_dict['contact']['email']).lower().replace(' at ', '@').replace(' dot ', '.').replace(' ', '').replace('\n', '')
            self.email = email_addr


class MyTest:

    def __init__(self):
        self.people = []

    def get_test_people_list(self, file_path):
        self.people = [str(name).replace('\n', '') for name in open(file_path).readlines()]
        return self.people

    def display(self):
        for person in self.people:
            print person
        print len(self.people)


if __name__ == '__main__':
    testCase = MyTest()
    testCase.get_test_people_list('../normal_name_list.txt')
    testCase.display()