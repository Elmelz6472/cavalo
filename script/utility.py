import time
import glob
import os

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
        lst_files = [f for f in os.listdir("../results") if f.endswith(".txt")]
        num_files = len(lst_files)
        num_jobs = 0
        for file in lst_files:
            with open(f"../results/{file}", "r") as file_object:
                lines = [line.rstrip() for line in file_object]
                for line in lines:
                    if line.startswith("Compagie name"):
                        num_jobs += 1


        num_files_html = len([f for f in os.listdir("../logs") if f.endswith(".html")])

        print(
            f"Scanned a total of {num_jobs} jobs stored in {num_files} result files.\nData is stored in {num_files_html} html files"
        )

    def cleanup_all_files(self, flag=0):
        files = glob.glob('../logs/*')
        for f in files:
            os.remove(f)
        if flag:
            files = glob.glob('../results/*')
            for f in files:
                os.remove(f)

