import asyncio
import csv
from bs4 import BeautifulSoup

from pyppeteer import launch


async def get_html():
    browser = await launch()
    page = await browser.newPage()
    await page.goto("https://www.asicminervalue.com/")

    await page.waitForSelector("tbody tr", visible=True)

    html = await page.content()
    await browser.close()
    return html


html = asyncio.get_event_loop().run_until_complete(get_html())
soup = BeautifulSoup(html, "html.parser")

asics = []
asic_rows = soup.select("tbody tr")

for asic in asic_rows:
    modelo = asic.select_one("td:nth-of-type(1) div div a span:nth-of-type(1)").text
    modelo += " " + asic.select_one("td:nth-of-type(1) div div a span:nth-of-type(2)").text
    hashrate = asic.select_one("td:nth-of-type(3) div span:nth-of-type(1)").text
    hashrate += asic.select_one("td:nth-of-type(3) div span:nth-of-type(2)").text
    algoritmo = asic.select_one("td:nth-of-type(6) div").text
    rentabilidad = (asic.select_one("td:nth-of-type(7) div div span:nth-child(1)").text or '') + (asic_row.select_one("td:nth-of-type(7) div div span:nth-child(2)").text or '')

    asics.append({
        "modelo": modelo,
        "hashrate": hashrate,
        "algoritmo": algoritmo,
        "rentabilidad": rentabilidad
    })

with open("asics.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["modelo", "hashrate", "algoritmo", "rentabilidad"])
    writer.writeheader()
    writer.writerows(asics)