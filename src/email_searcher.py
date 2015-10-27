import os
import urllib2
from google_helper import GoogleHelper
from my_html_parser import MailParser


RESULT_DIR_PATH = '../result/'


class EmailSearcher:

    def __init__(self):
        self.names = []
        self.mailParser = MailParser()

    def run(self, filename):
        self.names = open(filename).readlines()
        for name in self.names:
            name = name.replace('\n', '')
            dir_path = RESULT_DIR_PATH + name + '/'
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)

            content_file = open(dir_path + 'content.txt', 'w')
            search_page_cache_file = open(dir_path + 'search_page.html', 'w')
            try:
                search_page_content = GoogleHelper.get_google_search_page_by_name(name + ' email')
                search_page_cache_file.write(search_page_content)

                title_url_dict = GoogleHelper.get_google_items_from_search_page(search_page_content)
                for title, url in title_url_dict:
                    print url
                    try:
                        page_content = GoogleHelper.get_page_content_from_url(url)
                        if page_content is None:
                            continue
                        self.mailParser.feed(page_content)
                        email_list = list(set(self.mailParser.get_email_list()))
                        for email in email_list:
                            content_file.write(email + '\n')
                    except urllib2.HTTPError:
                        print '[HTTP_error]', url
                        continue
                    finally:
                        pass
            finally:
                content_file.close()
                search_page_cache_file.close()
                print name, 'OK...'


if __name__ == '__main__':
    searcher = EmailSearcher()
    searcher.run('../resource/names.list')