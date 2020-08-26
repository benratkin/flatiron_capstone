import re
import scrapy
from scrapy import Selector, FormRequest, Request
from scrapy_selenium import SeleniumRequest
from scrape.item_loaders.washington_ut_record_loader import RecordLoader
from scrape.items.record_item import Record
from scrapy.utils.response import open_in_browser


class WashingtonUtSpider(scrapy.Spider):
    name = 'washington_ut'
    base_url = 'http://eweb.washco.utah.gov:8080/recorder'

    def start_requests(self):

        data = {'guest' : 'true'}
        yield FormRequest(url=f'{self.base_url}/web/loginPOST.jsp', formdata=data, callback=self.fill_form)

    def fill_form(self, response):
        print(response.url)
        data = {
            'RecordingDateIDStart': '04/29/2020',
            'RecordingDateIDEnd': '04/30/2020',
            'AllDocuments': 'ALL',
        }
        yield FormRequest(url=f'{self.base_url}/eagleweb/docSearchPOST.jsp', formdata=data, callback=self.paginate)

    def paginate(self, response):
        print(response.url)
        for element in response.css('#searchResultsTable > tbody > tr > td > strong > a'):
            yield Request(url=f"{self.base_url}/eagleweb/{element.attrib['href']}", callback=self.parse_detail)

        if elements := response.css(".pagelinks a:contains('Next')"):
            print('entered pagination loop')
            print(f"{self.base_url}/..{elements[0].attrib['href']}")
            yield Request(url=f"{self.base_url}/..{elements[0].attrib['href']}", callback=self.paginate)

    # def login_paginate(self, response):
    #     self.driver = response.meta['driver']
    #
    #     # Locate form elements
    #     start = self.driver.find_element_by_css_selector('#RecordingDateIDStart')
    #     end = self.driver.find_element_by_css_selector('#RecordingDateIDEnd')
    #     submit = self.driver.find_element_by_css_selector('input[type="submit"][ value="Search"]')
    #
    #     # Populate form elements
    #     start.send_keys('04/29/2020')
    #     end.send_keys('05/30/2020')
    #
    #     # click submit
    #     submit.click()
    #     link = self.driver.find_element_by_link_text('Last').get_attribute('href')
    #     num_pages = int(re.findall('page=\d', link)[0].split('=')[1])
    #
    #     for i in range(num_pages):
    #         # TODO: Buggy, rewrite this. Watch browser to see issue.
    #         url = f'http://eweb.washco.utah.gov:8080/recorder/eagleweb/docSearchResults.jsp?searchId=0&page={i + 1}'
    #         yield Request(url=url, callback=self.parse_page)

    # def parse_page(self, response):
        # Current approach
        # records = self.driver.find_elements_by_css_selector('#searchResultsTable > tbody > tr')
        # for record in records:
        #     link_url = record.find_element_by_css_selector(
        #         '#searchResultsTable > tbody > tr > td > strong > a').get_attribute('href')
        #     sel = Selector(text=record.get_attribute('outerHTML'))
        #     il = RecordLoader(item=Record(), selector=sel)
        #     il.add_css('doc_id', 'td > strong > a::text')
        #     il.add_css('doc_type_text', 'td > strong > a::text')
        #     il.add_css('recording_date', 'td:nth-child(2) > a::text')
        #     il.add_css('grantor', 'table > tbody >tr > td::text')
        #     il.add_css('grantee', 'table > tbody >tr > td::text')
        #     yield Request(url=link_url, callback=self.parse_detail, cb_kwargs={'item': il.load_item()})

        # Approach 1
        # records = self.driver.find_elements_by_css_selector('#searchResultsTable > tbody > tr')
        # links_to_records = {
        #     record.find_element_by_css_selector('td > strong > a').get_attribute('href'): record for record in records
        # }
        # for link, record in links_to_records.items():
        #     sel = Selector(text=record.get_attribute('outerHTML'))
        #     il = RecordLoader(item=Record(), selector=sel)
        #     il.add_css('doc_id', 'td > strong > a::text')
        #     il.add_css('doc_type_text', 'td > strong > a::text')
        #     il.add_css('recording_date', 'td:nth-child(2) > a::text')
        #     il.add_css('grantor', 'table > tbody >tr > td::text')
        #     il.add_css('grantee', 'table > tbody >tr > td::text')
        #     yield SeleniumRequest(url=link, callback=self.parse_detail, cb_kwargs={'item': il.load_item()})

        # Approach 2
        # record_elements = self.driver.find_elements_by_css_selector('#searchResultsTable > tbody > tr')
        # records = [record.get_attribute('outerHTML') for record in record_elements]
        # records = self.driver.find_elements_by_css_selector('#searchResultsTable > tbody > tr')
        # for record in records:
        #     link_url = record.find_element_by_css_selector(
        #         '#searchResultsTable > tbody > tr > td > strong > a').get_attribute('href')
        #     sel = Selector(text=record.get_attribute('outerHTML'))
        #     il = RecordLoader(item=Record(), selector=sel)
        #     il.add_css('doc_id', 'td > strong > a::text')
        #     il.add_css('doc_type_text', 'td > strong > a::text')
        #     il.add_css('recording_date', 'td:nth-child(2) > a::text')
        #     il.add_css('grantor', 'table > tbody >tr > td::text')
        #     il.add_css('grantee', 'table > tbody >tr > td::text')
        #     yield Request(url=link_url, callback=self.parse_detail, cb_kwargs={'item': il.load_item()})

    def parse_detail(self, response):
        print(response.url)
        il = RecordLoader(item=Record(), response=response)
        il.add_css('doc_id', "span:contains('Entry Number') + span span::text")
        il.add_css('doc_type_text', '#middle::text')
        il.add_css('recording_date', "span:contains('Recording Date') + span span::text")
        # il.add_css('grantor', '')
        # il.add_css('grantee', '')
        il.add_css('parcel_id', '#presentation > table > tbody > tr:nth-child(3) > td > fieldset > table.tableHtmlLayout > tbody > tr > td > table > tbody > tr.tableRow1 > td:nth-child(1) > span::text')
        il.add_css('fee', '#presentation > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(2) > td:nth-child(1) > span.field > span::text')
        il.add_css('consideration', '#presentation > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(2) > td:nth-child(2) > span.field > span::text')
        il.add_css('instrument_date', "span:contains('Recording Date') + span span::text")
        il.add_css('account_id', '#presentation > table > tbody > tr:nth-child(3) > td > fieldset > table.tableHtmlLayout > tbody > tr > td > table > tbody > tr.tableRow1 > td:nth-child(2) > span::text')

        # Not available for this county
        # 'doc_type_code'

        record_item = il.load_item()
        yield record_item
