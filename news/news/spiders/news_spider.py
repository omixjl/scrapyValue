from pathlib import Path

from bs4 import BeautifulSoup


from selenium import webdriver
from selenium.webdriver.common.by import By

import scrapy
import threading

class NewsSpider(scrapy.Spider):
    name = "news"

    def start_requests(self):
        urls = [
            'https://es.beincrypto.com/mineria/',
            'https://www.criptonoticias.com/categorias/mineria/',
            'https://es.cointelegraph.com/tags/mining',
    
        ]
        for url in urls:
            if 'beincrypto' in url:
               yield scrapy.Request(url=url, callback=self.parse_bein)
            if 'cointelegraph' in url:
                yield scrapy.Request(url=url,  callback=self.parse_coin)    
            elif 'criptonoticias' in url:
               yield scrapy.Request(url=url, callback=self.parse_cripto)
         
    #EXTRAER CONTENIDO DE CADA NOTICIA DE BEINCRYPTO
    def parse_bein(self, response):  
        for bein in response.xpath('//main/div[2]/div')[:1]:
           
            enlace = bein.xpath('.//a/@href').get()
            if enlace and "https://es.beincrypto.com/resumen-semanal-beincrypto" not in enlace:
               yield response.follow(enlace, self.analizar_bein)

    def analizar_bein(self, response):
        cuerpo = response.xpath('//main/article/div/div[1]/div[4]/div[1]')
        content = BeautifulSoup(cuerpo.get(), 'html.parser').text.replace('\n', '')

        yield {
            'Contenido': content
        }      
     
    #EXTRAER CONTENIDO DE CADA NOTICIA DE CRIPTONOTICIAS
    def parse_cripto(self, response):       
        for cripto in response.xpath('//article')[:1]: 
            
            enlace = cripto.xpath('.//div[1]/a/@href').get()
            yield response.follow(enlace, self.analizar_cripto)
         
    def analizar_cripto(self,response):
        #cuerpo = response.xpath('//html/body/div[2]/div[5]/div[1]/div[1]/div/div/div/div[3]/div/div/div[2]/div[2]/*[not(self::div[1] or self::div[3])]')
        cuerpo = response.xpath('//html/body/div[2]/div[5]/div[1]/div[1]/div/div/div/div[3]/div/div/div[2]/div[2]')
        content = BeautifulSoup(cuerpo.get(), 'html.parser').text.replace('\n', '')

        yield {
            'Contenido': content
        }           
      
        
          
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        #self.browser_lock = threading.Lock()
        self.browser = webdriver.Chrome(options=options)
        
    #He limitado a las 7 primeras minitaturas porque tiene scroll infinito
    def parse_coin(self, response):
            self.browser.implicitly_wait(3)
            
            for coin in response.css('#__layout > div > div.layout__wrp > main > div > div > div.tag-page__rows > div.tag-page__posts-col > div > ul > li')[:1]:
                    
                    enlace = coin.css('article > a::attr(href)').get()
                    yield response.follow(enlace, self.analizar_coin)
            
    def analizar_coin(self, response):
        cuerpo = response.css('.post__article > div.post__content-wrapper > div.post-content')
        content = BeautifulSoup(cuerpo.get(), 'html.parser').text.replace('\n', '')

        yield {
            'Contenido': content
        }      
        
        self.browser.quit()
    
    