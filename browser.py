import sys
import os
import glob
import time
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from abc import ABC, abstractmethod

# NEED TO ADD SESSION OPTIONS FOR ADVANCED SCRAPPING

URL = "https://ca.indeed.com/"


class Capturing:
    """Class object that takes care of capturing the html content as well as storing it inside correct folder for further processing"""

    def __init__(self, data, name="Indeed", flag=0):
        self.name = name
        self.data = data
        self.flag = flag
        self.currentDateAndTime = datetime.now().strftime("%m-%d-%H:%M:%S")
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
        try:
            filelist = [f for f in os.listdir("logs") if f.endswith(".html")]
            for f in filelist:
                os.remove(os.path.join("logs", f))
        except FileNotFoundError:
            pass


class Export:
    def __init__(self, data, name="Indeed", flag=0):
        self.name = name
        self.data = data
        self.currentDateAndTime = datetime.now().strftime("%m-%d-%H:%M:%S")

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
        try:
            filelist = [f for f in os.listdir("results") if f.endswith(".txt")]
            for f in filelist:
                os.remove(os.path.join("results", f))
        except FileNotFoundError:
            pass


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
        filelist = [f for f in os.listdir("logs") if f.endswith(".html")]
        return filelist


# flag 0=write to file, keep file after program has runned, 1=write to file, destroy file after program has runned


class Parser:
    """Class object that handles of the parsing based on 1 SINGLE HTML FILE (1 FILE PER CLASS INSTANCE)"""

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


class Utility:
    def __init__(self):
        self.time1 = time.time()
        self.dct = {}

    def generate_checkpoint(self, name):
        return {name: time.time()}

    def get_elapsed_time(self, name1=None, name2=None):
        if name1 and name2:
            return (self.dct)[name2] - (self.dct)[name1]
        elif name1 and not name2:
            return (self.dct)[name1] - (self.time1)
        elif not name1 and name2:
            return (self.dct)[name2] - (self.time1)
        else:
            return time.time() - self.time1
        return time.time() - self.time1

    def count_jobs(self):
        lst_files = [f for f in os.listdir("results") if f.endswith(".txt")]
        num_files = len(lst_files)
        num_jobs = 0
        for file in lst_files:
            with open(f"results/{file}", "r") as file_object:
                lines = [line.rstrip() for line in file_object]
                for line in lines:
                    if line.startswith("Compagie name"):
                        num_jobs += 1


        num_files_html = len([f for f in os.listdir("logs") if f.endswith(".html")])



        print(
            f"Scanned a total of {num_jobs} jobs stored in {num_files} result files.\nData is stored in {num_files_html} html files"
        )

    def cleanup_all_files(self, flag=0):
        files = glob.glob('logs/*')
        for f in files:
            os.remove(f)
        if flag:
            files = glob.glob('results/*')
            for f in files:
                os.remove(f)




if __name__ == "__main__":
    util = Utility()

    util.cleanup_all_files(flag=1)

    client = Client("indeed", URL, depth=3)  # Do the initial search
    files = client.get_html_files()  # Get all of the html files

    for file in files:
        p = Parser(f"logs/{file}")
        info = p.parse()  # get the dictionnary of the necessary information
        Export(info).export_txt()

    util.count_jobs()
    print(f"Whole process took a total of {util.get_elapsed_time()} seconds")
