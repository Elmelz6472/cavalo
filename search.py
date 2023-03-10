import os
import asyncio
import time
from browser import Utility
from playwright.async_api import Playwright, async_playwright


"""Loop through every single website in result file.
    Try doing it by requests, else try with quick playwright script.
            -Quick regex search for 'contact, phone number, HR, email...' """


"""Add a mathematical approach to rank the best sites"""

GOOGLE_URL = "https://google.com"

async def browse(url: str, playwright: Playwright):
    browser = await playwright.chromium.launch(timeout=150000, headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto(GOOGLE_URL)
   # print(f"browsing {url}")
    search_bar = page.locator('input[name="q"]')
    await search_bar.fill(url)
    await search_bar.press("Enter")

    time.sleep(3)

    await page.wait_for_selector("#search")
    first_result = page.locator('#search a').first()
    await first_result.click()
    #await browser.close()
    print("done")


class Search:
    def __init__(self):
        self.lst = [f for f in os.listdir("results") if f.endswith(".txt")]
        self.lst_company = []

    def quick_launch(self):
        """Should try asynchronous job """
        pass

    def get_company_lst(self) -> list:
        for file in self.lst:
            with open(f"results/{file}", "r") as file_object:
                lines = [line.rstrip() for line in file_object]
                for line in lines:
                    if line.startswith("Compagie name"):
                        self.lst_company.append(line[line.index(": ") + 2:-1]) #TRUUUUSTTT
        return self.lst_company

    def print_out(self):
        print(self.lst_company)



async def main():
    urls = Search().get_company_lst()
    # urls = ["https://google.com", "https://facebook.com", "https://twitter.com"]

    async with async_playwright() as playwright:
        tasks = []
        for url in urls[0:2]:
            task = asyncio.create_task(browse(url, playwright))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
