#!/usr/bin/env python

""" Tranform Rita Store Products to Shopify """
import json
import time
import urllib2
import cStringIO
import base64
import requests
from PIL import Image

class TransToShopify():
    """ Tranform Rita Store Products to Shopify """

    def main(self):
        self.parse()
        #print inspect.getargspec(requests.post)

    def parse(self):
        """ Parse Products Data """
        api_url = 'https://akcy.myshopify.com/admin/'
        auth = ('***********', '************')

        with open('products.json') as json_file:
            datas = json.load(json_file)
            for item in datas:
                data = {
                    'product': {
                        'title': item['title'],
                        'body_html': item['body_html'],
                        'product_type': item['product_type'],
                        'images': item['images'],
                        'vendor': 'RITA',
                        'published': False
                    }
                }
                payload = json.dumps(data)
                url = api_url + 'products.json'
                headers = {'Content-Type': 'application/json'}
                #resp = requests.post(url, headers=headers, data=payload, auth=auth)
                resp = requests.post(url, headers=headers, data=payload)
                print resp.ok


if __name__ == '__main__':
    TransToShopify().main()
