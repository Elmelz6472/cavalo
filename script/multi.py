import asyncio
from playwright.async_api import Playwright, async_playwright


async def browse(url: str, playwright: Playwright):
    browser = await playwright.chromium.launch(timeout=150000, headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto(url)
    print(f"browsing {url}")
    #await browser.close()


async def main():
    urls = ["https://google.com", "https://facebook.com", "https://twitter.com"]

    async with async_playwright() as playwright:
        tasks = []
        for url in urls:
            task = asyncio.create_task(browse(url, playwright))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
