from pathlib import Path

import scrapy


class AsicSpider(scrapy.Spider):
    name = "asic"

    def start_requests(self):
        urls = [
            'https://www.asicminervalue.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for asic in response.xpath('//tbody/tr'):
            
            yield{
            'modelo': asic.xpath('.//td[1]/div[1]/div[2]/a[1]/span[1]/text()').get() + " " + asic.xpath('.//td[1]/div[1]/div[2]/a[1]/span[2]/text()').get(),
            'hashrate' : asic.xpath('.//td[3]/div[1]/span[1]/text()').get() + asic.xpath('.//td[3]/div[1]/span[2]/text()').get(),
            'algoritmo' : asic.xpath('.//td[6]/div[1]/text()').get(),
            'rentabilidad' :  (asic.xpath('.//td[7]/div[1]/div[2]/span[1]/text()').get() or '') + (asic.xpath('.//td[7]/div[1]/div[2]/span[2]/text()').get() or ''),
        }
            
