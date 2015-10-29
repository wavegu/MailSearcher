# encoding: utf-8


import re
import os
from HTMLParser import HTMLParser


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
        if tag == "li":
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "class" and value == "g":
                        self.isInItem = True
                        break
        if self.isInItem and tag == 'a':
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == 'href':
                        url = str(value).replace('/url?q=', '')
                        url = url[:url.find('&sa=')]
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
        data = str(data).lower()
        # print data
        pattern = re.compile('([a-zA-Z0-9]+)(@| at )(([a-zA-Z0-9]+)( ?\. ?| dot ))+(com|edu|cn)')
        match = pattern.finditer(data)
        for m in match:
            print m.group()
            self.emails.append(m.group())
        self.emails = list(set(self.emails))
        return self.emails

    def get_email_list(self):
        return list(set(self.emails))


def parse_mails():
    result_path = '../bing_result/'
    for person in os.listdir(result_path):
        print person
        pages_path = result_path + person + '/pages/'
        if not os.path.isdir(pages_path):
            continue
        mail_list = []
        for page in os.listdir(pages_path):
            print page
            page_content = open(pages_path + page).read()
            mail_parser = MailParser()
            mail_parser.feed(page_content)
            mail_list += mail_parser.get_email_list()
        output_file = open(result_path + person + '.mailist', 'w')
        mail_list = set(list(mail_list))
        for mail in mail_list:
            output_file.write(mail + '\n')
        output_file.close()


if __name__ == '__main__':
    # parser = MailParser()
    # data = '&nbsp; jietang at tsinghua . edu . cn'
    # parser.handle_data(data)
    parse_mails()