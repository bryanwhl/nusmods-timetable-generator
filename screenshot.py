import asyncio
from pyppeteer import launch
from datetime import datetime


def generate_screenshot(url):
    file_path = f'photos/timetable_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.png'

    async def main():
        browser = await launch()
        page = await browser.newPage()
        await page.setViewport({'width': 1200, 'height': 1000})
        await page.goto(url)
        await page.waitFor(1000)
        await page.screenshot({'path': file_path, 'clip': {'x': 150, 'y': 140, 'width': 1060, 'height': 385}})
        await browser.close()

    asyncio.get_event_loop().run_until_complete(main())
    return "/" + file_path

if __name__ == "__main__":
    x = generate_screenshot("https://nusmods.com/timetable/sem-2/share?CS2030=LEC:2,LAB:06,REC:02&CS2040S=TUT:02,REC:03,LEC:1&CS2100=LEC:2,LAB:14,TUT:14&GER1000=TUT:D17&IS1103=")
    print(x)
