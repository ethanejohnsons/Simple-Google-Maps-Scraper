import scrapy
import time

import reader
from selenium import webdriver

"""
Author: Ethan Johnson
Last Modified: October 29th, 2020
File Name: mapspider.py
"""


class MapSpider(scrapy.Spider):
    name = 'mapspider'
    start_urls = reader.read_from_file("searches.txt")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver = webdriver.Firefox()
        self.running_list_of_names = []
        self.count = 0
        self.MAX_RESULTS = 150

    def parse(self, response, **kwargs):
        self.driver.get(response.url)

        out = []

        # Loop through pages
        while True:
            time.sleep(5)

            index = 0
            num_results = len(self.driver.find_elements_by_xpath('//div[@class="section-result"]'))

            page = self.do_page(num_results, index)
            for p in page:
                out.append(p)

            # Click the next button to go to the next page
            try:
                self.driver.find_element_by_xpath('//button[@aria-label=" Next page "]').click()
            except:
                break

        for o in out:
            yield o

    def do_page(self, num_results, index):
        while index < num_results:
            time.sleep(2)
            try:
                result = self.driver.find_elements_by_xpath('//div[@class="section-result"]')[index]
                index += 1
            except:
                return

            self.driver.execute_script("arguments[0].scrollIntoView();", result)

            # Get the name and check for duplicates
            name = result.find_element_by_xpath('div/div/div/div/div/h3[@class="section-result-title"]/span').text
            if name in self.running_list_of_names:
                continue

            # Checks if the max number of results has been reached
            self.count += 1
            if self.count > self.MAX_RESULTS:
                return

            details = result.find_element_by_xpath('div/div/div/span[@class="section-result-details"]').text
            phone = result.find_element_by_xpath(
                'div/div/div/span[@class="section-result-info section-result-phone-number"]/span').text

            # Attempts to find a website
            self.running_list_of_names.append(name)
            website = ""
            try:
                website = result.find_element_by_xpath('div/div/div/a').get_attribute('data-href')
            except:
                print("no website :(")

            # Get the address
            time.sleep(1)
            result.click()
            time.sleep(4)
            address = self.driver.find_element_by_xpath('//button[contains(@aria-label, "Address:")]/div/div/div[contains(@class, "gm2-body-2")]').text
            print("CLICK================================================")
            print("CLICK================================================")
            print("CLICK================================================")
            print("CLICK================================================")
            print("CLICK================================================")
            print("CLICK================================================")
            print("CLICK================================================")
            print("CLICK================================================")
            time.sleep(1)
            self.driver.find_element_by_xpath('//span[contains(text(), "Back to results")]').click()
            # self.driver.back()
            time.sleep(1)

            # Yields the results
            yield {'name': name, 'address': address, 'details': details, 'phone': phone, 'website': website}
