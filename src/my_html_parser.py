import re
from HTMLParser import HTMLParser


class SearchPageHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.isInItem = False
        self.urls = []
        self.titles = []
        self.currentTitle = ''

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

    def handle_data(self, data):
        if self.isInItem:
            self.currentTitle += data

    def get_title_url_dict(self):
        return zip(self.titles, self.urls)


class MailParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.emails = []

    def handle_data(self, data):
        data = str(data).lower()
        pattern = re.compile(r'.*?(([a-zA-Z0-9]+\.?)+@([a-zA-Z0-9]+\.?)+\.(com|cn|edu)).*')
        match = pattern.match(data)
        if match:
            self.emails.append(match.group(1))
            print match.group(1)

    def get_email_list(self):
        return self.emails


if __name__ == '__main__':
    testcases = ['jietang@tsinghua.edu.cn']
    parser = MailParser()
    for testcase in testcases:
        parser.handle_data(testcase)