# encoding: utf-8

import urllib2
from proxy_helper import ProxyHelper

proxyHelper = ProxyHelper()


class WebHelper:

    def __init__(self):
        pass

    @classmethod
    def get_page_content_from_url(cls, page_url):
        """
        get html content from web page with given url
        :param page_url: url of the page to be read
        :return: page_content
        """
        print 'getting content from [' + page_url + ']'
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1 WOW64 rv:23.0) Gecko/20130406 Firefox/23.0')]
        try:
            proxy_id = 'http://:@' + proxyHelper.choose_proxy()
            print 'proxy_id is', proxy_id
            proxy = urllib2.ProxyHandler({'http': proxy_id})
            auth = urllib2.HTTPBasicAuthHandler()
            opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
            urllib2.install_opener(opener)
            print 'url ready'
            conn = urllib2.urlopen(page_url)
            page_content = conn.read()
            return page_content
        except urllib2.URLError or urllib2.HTTPError as e:
            print '[Error]@WebHelper.get_page_content_from_url:', page_url
            print e
            return None


if __name__ == '__main__':
    page_content = WebHelper.get_page_content_from_url('http://www.google.com')
    with open('test_result.html', 'w') as result_file:
        result_file.write(page_content)