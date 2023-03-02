import sys
import os
import shutil
import time
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from abc import ABC, abstractmethod

# NEED TO ADD SESSION OPTIONS FOR ADVANCED SCRAPPING

URL = "https://ca.indeed.com/"


class Capturing:
    def __init__(self, data, name="Indeed", flag=0):
        self.name = name
        self.data = data
        self.flag = flag
        self.currentDateAndTime = datetime.now().strftime("%m-%d-%H:%M")
        with open(
            f"logs/{self.currentDateAndTime}_{self.name}.html", "w"
        ) as file_object:
            file_object.write(self.data)

    def destroy_file(self):
        if self.flag == 1:
            os.remove(f"logs/{self.currentDateAndTime}_{self.name}.html")
        else:
            print("\n\n\nCANT DELETE FILE BECAUSE OF FLAG\n\n\n")

    def destroy_all_files(self):
        filelist = [f for f in os.listdir("logs") if f.endswith(".html")]
        os.remove(os.path.join("logs", f))


class Export:
    def __init__(self, data, name="Indeed", flag=0):
        self.name = name
        self.data = data
        self.currentDateAndTime = datetime.now().strftime("%m-%d-%H:%M")

    def export_txt(self):
        dct = self.data
        with open(
            f"results/{self.currentDateAndTime}_{self.name}.txt", "w"
        ) as file_object:
            for job in dct:
                file_object.write(f"Compagie name: {dct[job]['CompanyName']}")
                file_object.write("\n\t")
                file_object.write(f"Job title: {dct[job]['JobTitle']}")
                file_object.write("\n\t")
                file_object.write(f"MetaData: ")
                for data in dct[job]["MetaData"]:
                    file_object.write("\n\t")
                    file_object.write(data)

                file_object.write(f"Job Card Shelf: ")
                for data in dct[job]["JobCardShelf"]:
                    file_object.write("\n\t")
                    file_object.write(data)

                file_object.write(f"Job Snippet: {dct[job]['JobSnippet']}")

                file_object.write("\n\n\n")

    def export_excel(self):
        df = pd.DataFrame(data=self.data, index=[1])
        df.to_excel(f"results/{self.currentDateAndTime}_{self.name}.xlsx", index=False)

    def export_email(self, email_addr):
        pass

    def destroy_all_files(self):
        shutil.rmtree("results")


class Navigation(ABC):
    def __init__(self, name, url, keywords, location):
        self.name = name.lower()
        self.url = url
        self.keywords = keywords
        self.location = location

    def path(self, name):
        if (self.name) == "indeed":
            dict_path = {
                "keywords": "#text-input-what",
                "location": "#text-input-where",
                "submit": "#jobsearch > button",
                "change": "data-testid=pagination-page-next",
            }
            return dict_path

    def inputs(self, name):
        if self.name == "indeed":
            dict_inputs = {"keywords": self.keywords, "location": self.location}
            return dict_inputs

    def waiting(self, selector=False, delay=0):
        if delay > 0 and selector == False:
            self.page.wait_for_timeout(delay)

        elif delay == 0 and selector != False:
            self.page.wait_for_selector(selector)

        else:
            self.page.wait_for_load_state("domcontentloaded")

    def go_to(self, URL):
        self.page.goto(URL, wait_until="networkidle")

    def scroll_to_end_page(self, element_to_see):
        while True:
            self.page.mouse.wheel(0, 220)
            self.waiting(delay=800)
            if self.page.locator(element_to_see).is_visible():
                break
            # ADD METHOD TO GET OVER POPUP


class Client(Navigation):
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

        f = open("info.txt", "w")
        f.write(self.page.content())
        f.close()

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


# flag 0=write to file, keep file after program has runned, 1=write to file, destroy file after program has runned


class Parser:
    def __init__(self, file, **args):
        self.file = file
        self.list_args = [args for args in args]
        with open(self.file, "r") as file_object:
            self.file_loaded = BeautifulSoup(file_object, "lxml")

    def print_out(self):
        print(self.file_loaded.prettify())

    def print_job(self, dct):
        for job in dct:
            print(f"Compagie name: {dct[job]['CompanyName']}")
            print(f"Job title: {dct[job]['JobTitle']}")
            print(f"MetaData: {dct[job]['MetaData']}")
            print(f"Job Snippet: {dct[job]['JobSnippet']}")
            print(f"Job Card Shelf: {dct[job]['JobCardShelf']}")
            print("\n\n\n")

    def parse(self):
        dct = {}
        all_job_offer = self.file_loaded.find_all(class_="job_seen_beacon")
        for idx, job_offer in enumerate(all_job_offer):
            dct_info = {
                "CompanyName": job_offer.find(class_="companyName").get_text(),
                "JobTitle": job_offer.find(class_="jcs-JobTitle").get_text(),
                "MetaData": [
                    i.get_text() for i in job_offer.find_all(class_="metadata")
                ],
                "JobSnippet": [job_offer.find(class_="job-snippet").get_text()],
                "JobCardShelf": [
                    i.get_text() for i in job_offer.find_all(class_="jobCardShelf")
                ],
            }

            dct[idx] = dct_info

        self.print_job(dct)
        return dct


# client = Client("indeed", URL, "journalier de production", "laval", depth=3)
# # Collector(client)
# lol.parse()

# lol = Collector("indeed", URL, "journalier de production", "laval")
# Client("indeed", URL, sys.argv[1], sys.argv[2], sys.argv[3])

# Client("indeed", URL, "journalier de production", "laval")
p = Parser("logs/02-27-19:49_Indeed.html")

info = p.parse()

e = Export(info)
e.export_txt()
e.destroy_all_files()
