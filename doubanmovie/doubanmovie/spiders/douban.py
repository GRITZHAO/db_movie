# -*- coding: utf-8 -*-
import scrapy
from doubanmovie.items import DoubanmovieItem
from urllib import parse
from scrapy.http import HtmlResponse


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/review/best']

    def parse(self, response):
        article_url = response.xpath("//div[@class='article']/div[1]//a[@class='subject-img']/@href").extract()

        for arti_url in article_url:
            yield scrapy.Request(arti_url, callback=self.deail_parse)

        next_url = response.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href').extract_first()
        if next_url:
            yield scrapy.Request(parse.urljoin(response.url, next_url), callback=self.parse)

    def deail_parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        result = DoubanmovieItem()
        imag_url = response.xpath('//*[@id="mainpic"]/a/img/@src').get()
        title = response.xpath('//*[@id="content"]/h1/span[1]/text()').get()
        year = response.xpath('//*[@id="content"]/h1/span[2]/text()').get()
        star = response.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').get()
        comment = response.xpath('//*[@id="hot-comments"]//div/div/p/span/text()').get()
        result['title'] = title
        result['year'] = year
        result['star'] = star
        result['comment'] = comment
        result['image_url'] = imag_url

        yield result
