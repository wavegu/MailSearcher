import urllib2
from my_html_parser import SearchPageHTMLParser


class GoogleHelper:

    GOOGLE_SEARCH_ROOT_URL = 'http://www.google.com/search?q='

    def __init__(self):
        pass

    @classmethod
    def get_page_content_from_url(cls, page_url):
        """
        get html content from web page with given url
        :param url: url of the page to be read
        :return: page_content
        """
        print 'getting content from [' + page_url + ']'
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        try:
            res = opener.open(page_url).read()
        except urllib2.URLError or urllib2.HTTPError:
            print '[HTTP error]', page_url
            return None
        return res

    @classmethod
    def get_google_search_page_by_name(cls, name):
        """
        get html content of the google search page as a result of the given name
        :param name: name to be searched on Google
        :return: html content of google search page
        """
        name = str(name).replace(' ', '+')
        google_search_url = GoogleHelper.GOOGLE_SEARCH_ROOT_URL + name
        return cls.get_page_content_from_url(google_search_url)

    @classmethod
    def get_google_items_from_search_page(cls, page_content):
        """
        get titles and urls on the google search page
        >> for title, url in GoogleHelper.get_google_items_from_search_page():
        :param page_content:
        :return: zipped title_url_dict
        """
        parser = SearchPageHTMLParser()
        parser.feed(page_content)
        return parser.get_title_url_dict()


if __name__ == '__main__':
    result = GoogleHelper.get_google_search_page_by_name('jie tang mail')
    resultFile = open('result.html', 'w')
    resultFile.write(result)

    title_url_dict = GoogleHelper.get_google_items_from_search_page(result)
    for url, title in title_url_dict:
        print url, title
    # print len(url_title_dict)