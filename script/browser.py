import os
from playwright.sync_api import sync_playwright
from abc import ABC, abstractmethod
from data_processing import Parser, Export, Capturing
from utility import Utility


class Navigation(ABC):
    """Abstract class that can render navigation on different sites more easily"""

    def __init__(self, name, url, keywords, location):
        self.name = name.lower()
        self.url = url
        self.keywords = keywords
        self.location = location

    def path(self, name):
        """path function that helps navigated with js selector inside of playwright"""
        if self.name == "indeed":
            dict_path = {
                "keywords": "#text-input-what",
                "location": "#text-input-where",
                "submit": "#jobsearch > button",
                "change": "data-testid=pagination-page-next",
            }
            return dict_path

    def inputs(self, name):
        """input functions that helps accessing inputs fields with js selector inside of playwright and based of the name of the target"""
        if self.name == "indeed":
            dict_inputs = {"keywords": self.keywords, "location": self.location}
            return dict_inputs

    def waiting(self, selector=False, delay=0):
        """Helper function that provides a higher level for controlling the flow of playwright on actions such as waiting for loading, explicitly waiting and so on..."""
        if delay > 0 and selector == False:
            self.page.wait_for_timeout(delay)

        elif delay == 0 and selector != False:
            self.page.wait_for_selector(selector)

        else:
            self.page.wait_for_load_state("domcontentloaded")

    def go_to(self, URL):
        """Helper function that can help with accessing new URLS"""
        self.page.goto(URL, wait_until="networkidle")

    def scroll_to_end_page(self, element_to_see):
        while True:
            self.page.mouse.wheel(0, 220)
            self.waiting(delay=800)
            if self.page.locator(element_to_see).is_visible():
                break
            # ADD METHOD TO GET OVER POPUP


class Client(Navigation):
    """Client class browses through indeed based on "site name" URL, "job query", location and depth level"""

    def __init__(
        self, name, url, keywords="journalier de production", location="MTL", depth=0
    ):
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
        self.page.locator(locator).fill("")
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

        self.clicking(next_selector)

    def get_html(self):
        return self.page.content()

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
        self.sendKeys(
            selector_inputs["keywords"], selector_write["keywords"], delay=100
        )
        self.waiting(delay=250)

        # Write where you want to search
        self.sendKeys(
            selector_inputs["location"], selector_write["location"], delay=100
        )
        self.waiting(delay=250)

        # Click submit
        self.clicking(selector_inputs["submit"])

        # FIRST INITIAL SCAN OF PAGE
        self.scan_page(selector_inputs["change"])

        data = self.get_html()
        capturing = Capturing(data)

        # LOOP THROUGH X times
        for _ in range(int(self.depth)):
            self.scan_page(selector_inputs["change"])
            data = self.get_html()
            capturing = Capturing(data)

    def get_html_files(self):
        filelist = [f for f in os.listdir("../logs") if f.endswith(".html")]
        return filelist


if __name__ == "__main__":
    URL = "https://ca.indeed.com/"
    util = Utility()

    util.cleanup_all_files()

    client = Client("indeed", URL, depth=3)  # Do the initial search
    files = client.get_html_files()  # Get all of the html files

    for file in files:
        p = Parser(f"../logs/{file}")
        info = p.parse()  # get the dictionnary of the necessary information
        Export(info).export_txt()

    util.count_jobs()
    print(f"Whole process took a total of {util.get_elapsed_time()} seconds")
