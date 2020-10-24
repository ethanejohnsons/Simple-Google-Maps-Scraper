import scrapy
import time
from selenium import webdriver

"""
Author: Ethan Johnson
Last Modified: October 11th, 2020
File Name: spider.py
"""


class MapsSpider(scrapy.Spider):
    name = 'maps'
    start_urls = [
        'https://google.com/maps/search/child+fargo+moorhead',
        'https://google.com/maps/search/childcare+fargo+moorhead',
        'https://google.com/maps/search/daycare+fargo+moorhead',
        'https://google.com/maps/search/early+education+fargo+moorhead',
        'https://google.com/maps/search/early+childhood+fargo+moorhead',
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver = webdriver.Firefox()
        self.running_list_of_names = []
        self.count = 0
        self.MAX_RESULTS = 250

    def parse(self, response):
        self.driver.get(response.url)

        while True:
            time.sleep(5)

            results = self.driver.find_elements_by_xpath('//div[@class="section-result"]')
            for result in results:
                self.count += 1
                if (self.count > self.MAX_RESULTS):
                    return

                name = result.find_element_by_xpath('div/div/div/div/div/h3[@class="section-result-title"]/span').text
                if name in self.running_list_of_names:
                    continue

                self.running_list_of_names.append(name)
                website = ""
                try:
                    website = result.find_element_by_xpath('div/div/div/a').get_attribute('data-href')
                except:
                    print("no website :(")

                yield {
                    'name': name,
                    'address': result.find_element_by_xpath('div/div/div/span[@class="section-result-location"]').text,
                    'details': result.find_element_by_xpath('div/div/div/span[@class="section-result-details"]').text,
                    'phone': result.find_element_by_xpath(
                        'div/div/div/span[@class="section-result-info section-result-phone-number"]/span').text,
                    'website': website
                }

            next_page = self.driver.find_element_by_xpath('//button[@aria-label=" Next page "]')
            try:
                next_page.click()
            except:
                break
