#!/usr/bin/env python

""" A spider for Products """
import json
import time
import random
import scrapy

class ProductsSpider(scrapy.Spider):
    """ A spider for Products """

    name = "products"
    start_urls = []
    with open('ritastore.json') as json_file:
        if json_file is not None:
            urls = json.load(json_file)
            for url in urls:
                start_urls.append(url["url"])

    def parse(self, response):

        product_type = ''
        types = response.css('#bd #j-product-desc ul>li.property-item')
        if types is not None:
            for typ in types:
                if typ is not None:
                    if typ.css('span.propery-title::text').extract_first() == 'Item Type:':
                        product_type = typ.css('span.propery-des::attr(title)').extract_first()

        images = []
        imgs = response.css('#bd #j-image-thumb-list img').xpath('@src').extract()
        if imgs is not None:
            for img in imgs:
                images.append({'src': self.fix_img(img)})

        variants = {}
        skus = response.css('#bd #j-product-info-sku ul>li.item-sku-image')
        if skus is not None:
            for sku in skus:
                sku_id = sku.css('a::attr(data-sku-id)').extract_first()
                sku_title = sku.css('a::attr(title)').extract_first()
                sku_image = self.fix_img(sku.css('a>img::attr(src)').extract_first())
                variants[sku_id] = {
                    'id': sku_id,
                    'title': sku_title,
                    'image': sku_image
                }

        def extract_with_css(query):
            """ extract with css """
            return response.css(query).extract_first().strip()

        sku_pros = []
        sku_products = extract_with_css('#bd #j-product-detail-bd .store-detail-wrap script::text')
        if sku_products is not None:
            pos1 = sku_products.index('var skuProducts=') + 16
            sku_products = sku_products[pos1:]
            pos2 = sku_products.index('var GaData') - 11
            sku_products = sku_products[0:pos2]
            if sku_products is not None:
                sku_pros = json.loads(sku_products.strip())

        if sku_pros is not None:
            for sk in sku_pros:
                sk_id = sk["skuPropIds"]
                sk["skuTitle"] = ''
                sk["skuImage"] = ''
                if sk_id in variants:
                    sk["skuTitle"] = variants[sk_id]['title']
                    sk["skuImage"] = variants[sk_id]['image']

        image = self.fix_img(extract_with_css('#bd #magnifier img::attr(src)'))
        body_html = extract_with_css('#bd #j-product-desc .product-property-main')
        body_html = body_html.replace("\n                                                                ", "")
        body_html = body_html.replace("\n                        ", "")
        body_html = body_html.replace("\n                    ", "")
        body_html = body_html.replace("\n        ", "")
        body_html = body_html.replace("\n    ", "")
        body_html = body_html.replace("\n", "")

        yield {
            'id': extract_with_css('#bd #hid-product-id::attr(value)'),
            'title': extract_with_css('#bd .product-name::text'),
            'price': extract_with_css('#bd #j-sku-discount-price::text'),
            'del_price': extract_with_css('#bd #j-sku-price::text'),
            'discount': extract_with_css('#bd .p-discount-rate::text'),
            'unit_odd': extract_with_css('#bd #oddUnitName_id::attr(value)'),
            'unit_multi': extract_with_css('#bd #multiUnitName_id::attr(value)'),
            'body_html': body_html,
            'image': image,
            'images': images,
            'product_type': product_type,
            'variants': variants,
            'skus': sku_pros
        }

        stop = random.randint(100, 200)
        print 'sleep'
        print stop
        print 'sleeping'
        time.sleep(stop)


    def fix_img(self, image):
        """ fix image src """
        if image is not None:
            pos = image.index('.jpg_')
            if pos > 0:
                image = image[0:pos] + '.jpg'
        return image
