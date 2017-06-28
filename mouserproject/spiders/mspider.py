# -*- coding: utf-8 -*-
import scrapy
from mouserproject.items import MouserprojectItem


class MosesepiderSpider(scrapy.Spider):
    name = 'mspider'
    start_urls = ['http://eu.mouser.com/Electromechanical/Audio-Devices/_/N-awp3d/']

    def parse(self, response):
        for item in response.xpath('//a[contains(@id, "MfrPartNumberLink")]/@href').extract():
            full_url = 'http://eu.mouser.com/' + ''.join(item.split('../')[4:])
            yield scrapy.Request(full_url, callback=self.parse_item)

        next_page = response.xpath('(//a[contains(., "Next")])[1]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_item(self, response):
        item = MouserprojectItem()
        item['ven_part_id'] = response.xpath('//div[@id="divMouserPartNum"]/text()').extract_first().strip()
        item['mfg_part_id'] = response.xpath('//div[@id="divManufacturerPartNum"]/h1/text()').extract_first().strip()
        item['description'] = response.xpath('//div[@id="divDes"]/text()').extract_first().strip()
        item['category'] = response.xpath('(//td[@class="ProductDetailData"]/span)[1]/text()').extract_first()
        item['inventory'] = response.xpath('(//div[contains(@class, "av-col2")])[1]/text()').re_first(r'\d+\.?\d*')
        item['lead_time'] = response.xpath('(//div[contains(@class, "av-col2")])[3]/text()').extract_first().strip()
        # item['price'] = response.xpath('(//span[contains(@id, "Price")])[1]/text()').extract_first()
        item['price'] = []
        for row in response.xpath('//div[contains(@class, "PriceBreaks")]/div[@class="row" and not(@id)]'):
            qty = row.xpath('div[a]/a/text()').extract_first()
            cost_price = row.xpath('.//span[contains(@id, "Price") and not(@title) and not(a)]/text()').extract_first()
            item['price'].append({"qty": qty, "cost_price": cost_price})
        item['link'] = response.url
        yield item
