# encoding: utf-8


import re
import os
from mail_score import mail_score
from HTMLParser import HTMLParser

import sys

reload(sys)
sys.setdefaultencoding('utf8')


class SearchPageHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.isInItem = False
        self.urls = []
        self.titles = []
        self.currentTitle = ''

    def handle_data(self, data):
        if self.isInItem:
            self.currentTitle += data

    def get_title_url_dict(self):
        return zip(self.titles, self.urls)


class GooglePageHTMLParser(SearchPageHTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == "h3":
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "class" and value == "r":
                        self.isInItem = True
                        break
        if self.isInItem and tag == 'a':
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == 'href':
                        url = str(value).replace('/url?q=', '')
                        pos = url.find('&sa=')
                        if pos >= 0:
                            url = url[:pos]
                        self.urls.append(url)
                        break

    def handle_endtag(self, tag):
        if self.isInItem and tag == 'a':
            self.isInItem = False
            self.titles.append(self.currentTitle)
            self.currentTitle = ''


class BingPageHTMLParser(SearchPageHTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == "li":
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "class" and value == "b_algo":
                        self.isInItem = True
                        break
        if self.isInItem and tag == 'a':
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == 'href':
                        self.urls.append(str(value))
                        break

    def handle_endtag(self, tag):
        if self.isInItem and tag == 'a':
            self.isInItem = False
            self.titles.append(self.currentTitle)
            self.currentTitle = ''


class GoogleSearchPageMailParser(HTMLParser):
    """
    search for e-mail address from search page
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.data = ''
        self.isInSpan = False
        self.emails = []

    def handle_starttag(self, tag, attrs):
        if tag == 'span':
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "class" and value == "st":
                        self.isInSpan = True
                        self.data = ''
                        break

    def handle_endtag(self, tag):
        if tag == 'span':
            if self.data == '':
                return
            try:
                self.data = str(self.data).lower()
            except Exception as e:
                print e
                print self.data
                return []
            if self.data.find('@') < 0 and self.data.find(' at ') and self.data.find(' [at] ') < 0:
                return []

            rough_pattern = re.compile('[a-z0-9-\._]+(@| at | \[at\] )(([a-z0-9\-]+)(\.| dot | \. | \[dot\] ))+([a-z]+)')
            rough_match = rough_pattern.finditer(self.data)
            for rm in rough_match:
                pattern = re.compile('(([a-z0-9-_]+)(\.| dot | \. )?)+(@| at | \[at\] )(([a-z0-9\-]+)(\.| dot | \.  \[dot\] ))+([a-z]+)')
                match = pattern.finditer(rm.group())
                for m in match:
                    self.emails.append(m.group().replace(' dot ', '.').replace(' at ', '@').replace(' [at] ', '@'))

    def handle_data(self, data):
        if self.isInSpan:
            self.data += data

    def get_email_list(self):
        for email_a in self.emails:
            for email_b in self.emails:
                if email_a == email_b or email_b not in self.emails:
                    continue
                if email_a in email_b:
                    self.emails[self.emails.index(email_b)] = email_a
        return self.emails


def sort_mail(name, mail_list):
    list_len = len(mail_list)
    for i in range(list_len):
        for j in range(i):
            if mail_score(name, mail_list[i]) > mail_score(name, mail_list[j]):
                mail_list[i], mail_list[j] = mail_list[j], mail_list[i]
    return mail_list


# def parse_mails(engine_name):
#     mail_list_path = '../email_list/'
#     if not os.path.isdir(mail_list_path):
#         os.mkdir(mail_list_path)
#     search_result_path = '../' + engine_name + '_result/'
#     for person in os.listdir(search_result_path):
#         print person
#         pages_path = search_result_path + person + '/pages/'
#         if not os.path.isdir(pages_path):
#             continue
#         mail_list = []
#         for page in os.listdir(pages_path):
#             page_content = open(pages_path + page).read()
#             mail_parser = GoogleSearchPageMailParser()
#
#             mail_parser.feed(page_content)
#             mail_list += mail_parser.get_email_list()
#
#         output_file = open(mail_list_path + person + '.txt', 'w')
#         # mail_list = set(list(mail_list))
#         mail_list = sort_mail(person, mail_list)
#         for mail in mail_list:
#             output_file.write(mail + '\n')
#         output_file.close()


def parse_mails_from_search_page(engine_name):
    mail_list_path = '../email_list/'
    if not os.path.isdir(mail_list_path):
        os.mkdir(mail_list_path)
    search_result_path = '../' + engine_name + '_result/'
    counter = 0
    for person in os.listdir(search_result_path):
        counter += 1
        print '[' + str(counter) + ']', person
        if person + '.txt' in os.listdir(mail_list_path):
            continue
        if not os.path.isdir(search_result_path + person):
            continue
        search_page_path = search_result_path + person + '/search_page.html'
        search_page_content = open(search_page_path).read()

        mail_list = []
        mail_parser = GoogleSearchPageMailParser()
        mail_parser.feed(search_page_content)
        mail_list += mail_parser.get_email_list()

        output_file = open(mail_list_path + person + '.txt', 'w')
        mail_list = sort_mail(person, mail_list)
        for mail in mail_list:
            output_file.write(mail + '\t[')
            output_file.write(str(mail_score(person, mail)) + ']\n')
        output_file.close()


if __name__ == '__main__':
    # parser = GoogleSearchPageMailParser()
    # parser.handle_data(data)
    # print parser.emails
    parse_mails_from_search_page('google')