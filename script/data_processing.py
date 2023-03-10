import os
from datetime import datetime
from bs4 import BeautifulSoup


# NEED TO ADD SESSION OPTIONS FOR ADVANCED SCRAPPING
class Capturing:
    """Class object that takes care of capturing the html content as well as storing it inside correct folder for further processing"""

    def __init__(self, data, name="Indeed", flag=0):
        self.name = name
        self.data = data
        self.flag = flag
        self.currentDateAndTime = datetime.now().strftime("%m-%d-%H:%M:%S")
        with open(
            f"../logs/{self.currentDateAndTime}_{self.name}.html", "w"
        ) as file_object:
            file_object.write(self.data)

    def destroy_file(self):
        if self.flag == 1:
            os.remove(f"../logs/{self.currentDateAndTime}_{self.name}.html")
        else:
            print("\n\n\nCANT DELETE FILE BECAUSE OF FLAG\n\n\n")

    def destroy_all_files(self):
        try:
            filelist = [f for f in os.listdir("../logs") if f.endswith(".html")]
            for f in filelist:
                os.remove(os.path.join("../logs", f))
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
            f"../results/{self.currentDateAndTime}_{self.name}.txt", "w"
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
        df.to_excel(f"../results/{self.currentDateAndTime}_{self.name}.xlsx", index=False)

    def export_email(self, email_addr):
        pass

    def destroy_all_files(self):
        try:
            filelist = [f for f in os.listdir("../results") if f.endswith(".txt")]
            for f in filelist:
                os.remove(os.path.join("../results", f))
        except FileNotFoundError:
            pass





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
