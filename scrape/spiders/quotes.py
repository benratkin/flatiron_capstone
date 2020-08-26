# -*- coding: utf-8 -*-
import scrapy
from scrape.item_loaders.quotes_item_loader import QuoteLoader
from scrape.items.quotes_item import Quote
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.common.exceptions import NoSuchElementException


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    # Used if no start_requests implemented
    # start_urls = []

    def start_requests(self):
        urls = ['http://quotes.toscrape.com/']
        for url in urls:
            # Instances of SeleniumRequest inherit from normal Scrapy.Request and only override the __init__ method
            # to define additional, custom arguments then pass all other args to super's __init__. Similar objects.
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        # Can be used to invoke scrapy shell at this point in crawl
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        # Can be used to view response as scrapy sees it
        # from scrapy.utils.response import open_in_browser
        # open_in_browser(response)

        self.driver = response.meta['driver']

        while True:
            # TODO: Missing page 10 in results I believe
            next_button = self.driver.find_element_by_css_selector('.next > a')
            print(next_button.get_attribute('href'))
            try:
                for quote in self.driver.find_elements_by_css_selector('.quote'):
                    # If using the 'il.add_x' functions below, must convert 'outerHTML' of webelement to Scrapy
                    # Selector object.
                    sel = Selector(text=quote.get_attribute('outerHTML'))
                    il = QuoteLoader(item=Quote(), selector=sel)
                    il.add_css('quote', '.text::text')
                    il.add_css('by', '.author::text')
                    quote_item = il.load_item()
                    # # Can use yield? Or should I just append items to a list and return list?
                    yield quote_item
                next_button.click()
            except NoSuchElementException:
                break
