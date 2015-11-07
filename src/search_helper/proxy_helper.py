from scrapy.http import Request
import string, random
from pymongo import MongoClient
from bson import ObjectId
import urllib, socket
import time


class ProxyHelper:

    def __init__(self):
        self.proxies = []
        self.request20proxy = 'http://erwx.daili666.com/ip/?tid=558045424788230&num=20&foreign=only'
        self.request1proxy = 'http://erwx.daili666.com/ip/?tid=558045424788230&num=1&foreign=only'
        proxy = urllib.urlopen(self.request20proxy)
        for line in proxy.readlines():
            if self.test_proxy(line.strip()):
                self.proxies.append(line.strip())
        print 'proxis is', self.proxies

    def choose_proxy(self):
        if self.proxies:
            random.shuffle(self.proxies)
            return self.proxies[0]
        proxy = urllib.urlopen(self.request1proxy)
        proxy_candidate = proxy.readlines()[0].strip()
        while not self.test_proxy(proxy_candidate):
            proxy = urllib.urlopen(self.request1proxy)
            proxy_candidate = proxy.readlines()[0].strip()
        self.proxies.append(proxy_candidate)
        print "Proxy " + proxy_candidate + " is added."
        return proxy_candidate

    @classmethod
    def test_proxy(cls, proxy):
        print 'testing', proxy
        socket.setdefaulttimeout(3.0)
        test_url = 'http://www.google.com'
        try:
            f = urllib.urlopen(test_url, proxies={'http': 'http://:@' + str(proxy)})
        except Exception as e:
            print "Proxy " + proxy + " fails!", e
            return False
        if f.getcode() != 200:
            print "Proxy " + proxy + " fails!", type(f.getcode())
            return False
        print proxy, 'ok...'
        return True

if __name__ == '__main__':
    proxyHelper = ProxyHelper()
    proxy_ip = proxyHelper.choose_proxy()
    print proxy_ip