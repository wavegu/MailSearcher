# encoding: utf-8


import re
import os
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


class MailParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.emails = []

    def handle_data(self, data):
        try:
            data = str(data).lower()
        except Exception as e:
            print e
            print data
            return []
        if data.find('@') < 0 and data.find(' at ') < 0:
            return []

        rough_pattern = re.compile('[a-z0-9-\. ]+(@| at )(([a-z0-9\-]+)(\.| dot | \. ))+([a-z]+)')
        rough_match = rough_pattern.finditer(data)
        for rm in rough_match:
            pattern = re.compile('(([a-z0-9-]+)(\.| dot | \. )?)+(@| at )(([a-z0-9\-]+)(\.| dot | \. ))+([a-z]+)')
            match = pattern.finditer(rm.group())
            for m in match:
                self.emails.append(m.group())
        self.emails = self.emails
        return self.emails

    def get_email_list(self):
        return self.emails


def parse_mails(engine_name):
    result_path = '../' + engine_name + '_result/'
    for person in os.listdir(result_path):
        print person
        pages_path = result_path + person + '/pages/'
        if not os.path.isdir(pages_path):
            continue
        mail_list = []
        for page in os.listdir(pages_path):
            page_content = open(pages_path + page).read()
            mail_parser = MailParser()

            mail_parser.feed(page_content)
            mail_list += mail_parser.get_email_list()

        output_file = open(result_path + person + '.mailist', 'w')
        # mail_list = set(list(mail_list))
        mail_list = sorted(mail_list)
        for mail in mail_list:
            output_file.write(mail + '\n')
        output_file.close()


if __name__ == '__main__':
    # parser = MailParser()
    # data = 'sakira@biken.osaka-u.ac.jp'
    # parser.handle_data(data)
    parse_mails('google')