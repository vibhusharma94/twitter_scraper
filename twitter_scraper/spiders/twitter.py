# -*- coding: utf-8 -*-
import re
import json

import scrapy
from scrapy.linkextractor import LinkExtractor
from ..settings import PROJECT_ROOT
from bs4 import BeautifulSoup

from ..items import TwitterScraperItem


class TwitterSpider(scrapy.Spider):
    name = 'twitter'
    allowed_domain = ['twitter.com']
    twitter_domain = 'twitter.com'
    handle_regex = '^@?(\w){1,15}$'
    follower_xpath = '//*[@id="page-container"]/div[1]/div/div[2]/div/div/div[2]/div/div/ul/li[3]/a/span[3]'
    name_xpath = '//*[@id="page-container"]/div[2]/div/div/div[1]/div/div/div/div[1]/h1/a'

    start_urls = json.load(open(PROJECT_ROOT + '/urls.json'))

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        for link in links:
            if self.twitter_domain in link.url:
                text = link.url.replace("https://twitter.com/", "")
                if re.match(self.handle_regex, text):
                    yield scrapy.Request(link.url, callback=self.parse_profile, dont_filter=True)
    
    def parse_profile(self, response):
        data = TwitterScraperItem()
        
        html_content =  response.selector.xpath(self.follower_xpath).extract_first(default='')
        soup = BeautifulSoup(html_content)
        for item in  soup.findAll('span'):
            data['follower_count'] = dict(item.attrs)['data-count']

        html_content =  response.selector.xpath(self.name_xpath).extract_first(default='')
        soup = BeautifulSoup(html_content)
        for item in  soup.findAll('a'):
            data['profile_name'] = item.text
            data['handle'] = dict(item.attrs)['href'].replace("/", "")

        if int(data.get('follower_count', 0)) > 1000:
            return data




