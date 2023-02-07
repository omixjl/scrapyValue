const fs = require('fs');

const scraperObject = {
    url: 'https://www.asicminervalue.com/',
    async scraper(browser) {
        let page = await browser.newPage();
        console.log(`Navigating to ${this.url}...`);
        await page.goto(this.url);
        const asicData = await page.evaluate(() => {
            const asics = Array.from(document.querySelectorAll('tbody tr'));
            return asics.map(asic => {
                return {
                    modelo: asic.querySelector('td:nth-of-type(1) div div a span:nth-of-type(1)')?.textContent + ' '
                        + asic.querySelector('td:nth-of-type(1) div div a span:nth-of-type(2)')?.textContent,

                    hashrate: asic.querySelector('td:nth-of-type(3) div span:nth-of-type(1)')?.textContent
                        + asic.querySelector('td:nth-of-type(3) div span:nth-of-type(2)')?.textContent,

                    algoritmo: asic.querySelector('td:nth-of-type(6) div')?.textContent,

                    rentabilidad: (asic.querySelector('td:nth-of-type(7) div div span:nth-of-type(1)')?.textContent || '')
                        + asic.querySelector('td:nth-of-type(7) div div span:nth-of-type(2)')?.textContent,
                };
            });
        });
        fs.writeFileSync('asicData.json', JSON.stringify(asicData, null, 1));
        await browser.close();
    }

}



module.exports = scraperObject;