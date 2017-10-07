# -*- coding: utf-8 -*-
import random, base64


class ProxyMiddleware(object):
    #代理IP列表
    proxyList = [ \
      'http://114.215.150.13:3128',
      'http://114.215.103.121:8081'
        ]

    def process_request(self, request, spider):
        # Set the location of the proxy
        pro_adr = random.choice(self.proxyList)
        print("USE PROXY -> " + pro_adr)
        request.meta['proxy'] = pro_adr