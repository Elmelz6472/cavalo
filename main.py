import sys
import time
from parsel import Selector
from playwright.sync_api import sync_playwright
from abc import ABC, abstractmethod


URL = "https://ca.indeed.com/"


class Navigation(ABC):
    def __init__(self, name, url, keywords, location):
        self.name = name.lower()
        self.url = url
        self.keywords = keywords
        self.location = location

    def path(self, name):
        if (self.name)== "indeed":
            dict_path = {
                "keywords": "#text-input-what",
                "location": "#text-input-where",
                "submit": "#jobsearch > button",
                "change": "data-testid=pagination-page-next",
            }
            return dict_path

    def inputs(self, name):
        if self.name == "indeed":
            dict_inputs = {
                "keywords": self.keywords,
                "location": self.location
            }
            return dict_inputs

    def waiting(self, selector=False, delay=0):
        if delay > 0 and selector==False:
            self.page.wait_for_timeout(delay)

        elif delay == 0 and selector != False:
            self.page.wait_for_selector(selector)

        else:
            self.page.wait_for_load_state('domcontentloaded')

    def go_to(self, URL):
        self.page.goto(URL, wait_until='networkidle')

    def scroll_to_end_page(self, element_to_see):
        while True:
            self.page.mouse.wheel(0, 250)
            self.waiting(delay=350)
            if self.page.locator(element_to_see).is_visible():
                break



class Client(Navigation):
    def __init__(self, name, url, keywords, location, depth=0):
        self.name = name
        self.url = url
        self.keywords = keywords
        self.location = location
        self.depth = depth

        super(Client, self).__init__(self.name, self.url, self.keywords, self.location)


        self.browser = None
        self.context = None
        self.page = None
        with sync_playwright() as playwright:
            self.run(playwright)

    def sendKeys(self, locator, input_words, delay=0):
        self.page.locator(locator).fill('')
        self.waiting(delay=100)
        self.page.locator(locator).type(input_words, delay=delay)



    def clicking(self, locator):
            self.page.locator(locator).click(force=True)
            self.waiting(delay=100)



    def scan_page(self, next_selector):
        self.waiting()
        self.waiting(delay=100)
        print("scanning page")
        self.scroll_to_end_page(element_to_see=next_selector)

        self.waiting(delay=1200)

        f = open("info.txt", "w")
        f.write(self.page.content())
        f.close()

        self.clicking(next_selector)


    def run(self, playwright: "Playwright") -> None:

        self.browser = playwright.chromium.launch(timeout=150000, headless=False)
        self.context = self.browser.new_context()
        self.context.tracing.start(screenshots=True, snapshots=True)

        self.page = self.context.new_page()

        selector_inputs = self.path(self.name)
        selector_write = self.inputs(self.name)

        self.page.set_default_navigation_timeout(10000)

        self.go_to(URL)

        self.waiting(selector_inputs["keywords"])
        self.waiting(selector_inputs["location"])



        # Add keywords (search bar)
        self.sendKeys(selector_inputs["keywords"], selector_write["keywords"], delay=100)
        self.waiting(delay=250)

        # Write where you want to search
        self.sendKeys(selector_inputs["location"], selector_write["location"], delay=100)
        self.waiting(delay=250)

        # Click submit
        self.clicking(selector_inputs["submit"])

        # FIRST INITIAL SCAN OF PAGE
        self.scan_page(selector_inputs["change"])


        # LOOP THROUGH X times
        # for _ in range(self.depth):
        #     self.scan_page(selector_inputs["change"])

    # def export_content(self):








class Collector(Client):
    def __init__(self, name, url, keywords, location):
        self.name = name
        self.url = url
        self.keywords = keywords
        self.location = location
        # super(Collector, self).__init__(self.name, self.url, self.keywords, self.location)

    def parse(self):
        self.parsed_data = []

        with open("info.txt") as f:
            selector = Selector(text=f.read())
            x = selector.css('div::attr(class)')
            # print(x.getall())
            for i in x.getall():
                print(i)
                print("\n\n\n")

        # return self.parsed_data










# client = Client("indeed", URL, "journalier de production", "laval", depth=3)
# Collector(client)
lol = Collector("indeed", URL, "journalier de production", "laval")
lol.parse()

# Client("indeed", URL, sys.argv[1], sys.argv[2])
