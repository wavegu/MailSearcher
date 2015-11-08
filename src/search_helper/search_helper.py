from web_helper import WebHelper

from src.my_html_parser import *


class SearchHelper:

    __parser__ = None
    __SEARCH_ROOT_URL__ = ''
    __RESULT_DIR_PATH__ = ''

    def __init__(self):
        pass

    @classmethod
    def get_search_page_by_name(cls, name):
        """
        get html content of the search page as a bing_result of the given name
        :param name: name to be searched on search engine
        :return: html content of search page
        """
        name = str(name).replace(' ', '+')
        search_url = cls.__SEARCH_ROOT_URL__ + name
        return WebHelper.get_page_content_from_url(search_url)

    @classmethod
    def get_items_from_search_page(cls, page_content):
        """
        get titles and urls on the google search page
        >> for title, url in GoogleHelper.get_items_from_search_page():
        :param page_content:
        :return: zipped title_url_dict
        """
        search_page_parser = cls.__parser__()
        search_page_parser.feed(page_content)
        return search_page_parser.get_title_url_dict()


class GoogleHelper(SearchHelper):
    __parser__ = GooglePageHTMLParser
    __RESULT_DIR_PATH__ = '../google_result/'
    __SEARCH_ROOT_URL__ = 'https://www.google.com/search?hl=en&safe=off&q='


class BingHelper(SearchHelper):
    __parser__ = BingPageHTMLParser
    __RESULT_DIR_PATH__ = '../bing_result/'
    __SEARCH_ROOT_URL__ = 'https://cn.bing.com/search?q='


if __name__ == '__main__':
    # bing_result = GoogleHelper.get_google_search_page_by_name('jie tang mail')
    # resultFile = open('bing_result.html', 'w')
    # resultFile.write(bing_result)
    #
    # title_url_dict = GoogleHelper.get_google_items_from_search_page(bing_result)
    # for url, title in title_url_dict:
    #     print url, title

    content = WebHelper.get_page_content_from_url('http://www.google.com/search?q=jie+tang+tsinghua+email')
    result = open('bing_result.html', 'w')
    result.write(content)

    # proxy = urllib2.ProxyHandler({'http': 'http://megvii:face++@tel.lc.ignw.net:25'})
    # auth = urllib2.HTTPBasicAuthHandler()
    # opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
    # urllib2.install_opener(opener)
    # print 'ready to open'
    # conn = urllib2.urlopen('http://www.google.com')
    # print conn.read()