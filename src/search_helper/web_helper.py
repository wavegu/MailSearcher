# encoding: utf-8

import urllib2
import socket


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
            proxy = urllib2.ProxyHandler({'http': 'http://megvii:face++@tel.lc.ignw.net:25'})
            auth = urllib2.HTTPBasicAuthHandler()
            opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
            urllib2.install_opener(opener)
            conn = urllib2.urlopen(page_url, timeout=10)
            page_content = conn.read()
            return page_content
        except urllib2.URLError or urllib2.HTTPError as e:
            print '[Error]@WebHelper.get_page_content_from_url:', page_url
            print e
            return None
