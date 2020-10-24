# Simple Google Maps Scraper
This project is a simple google maps scraper that can be used for compiling a list of specific types of locations.
The example `searches.txt` file contains a list of searches for child-centered businesses in the Fargo-Moorhead area.

## Setup
To setup your python environment to run this project, you must install [Scrapy](https://scrapy.org/) and [Selenium](https://selenium-python.readthedocs.io/).
To do this, type in your terminal:
```
conda install -c conda-forge scrapy
conda install -c conda-forge geckodriver
pip install selenium
```
You must also have Firefox installed.

## Run
To run the spider, type `scrapy runspider mapspider.py -o output.json`.

