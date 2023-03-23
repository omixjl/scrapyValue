import asyncio
import json
import pyppeteer

async def scraper():
    browser = await pyppeteer.launch()
    page = await browser.newPage()
    await page.goto("https://www.asicminervalue.com/")
    await page.waitForSelector("tbody tr", visible=True) 
    
    asic_data = await page.evaluate('''() => {
        const asics = Array.from(document.querySelectorAll('.odd'));
    
        return asics.map(asic => {
            return {
                modelo: asic.querySelector('td:nth-of-type(1) div div a span:nth-of-type(1)').textContent + ' '
                        + asic.querySelector('td:nth-of-type(1) div div a span:nth-of-type(2)').textContent,

                hashrate: asic.querySelector('td:nth-of-type(3) div span:nth-of-type(1)').textContent
                        + asic.querySelector('td:nth-of-type(3) div span:nth-of-type(2)').textContent,

                rentabilidad: document.querySelector("#datatable_profitability > tbody > tr:nth-child(1) > td.text-center.sorting_1 > div > div.rentabilitylabel.color50");
            };
        });
    }''')

    with open("asic_data.json", "w") as outfile:
        json.dump(asic_data, outfile, indent=2)
        
    await browser.close()

asyncio.run(scraper())