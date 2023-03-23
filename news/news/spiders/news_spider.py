from pathlib import Path

from bs4 import BeautifulSoup

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

import scrapy


class NewsSpider(scrapy.Spider):
    name = "news"

    def start_requests(self):
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
        #headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        
        #headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}
        urls = [
            'https://es.beincrypto.com/mineria/',
            'https://www.criptonoticias.com/categorias/mineria/',
            'https://es.cointelegraph.com/tags/mining',
    
        ]
        for url in urls:
            if 'beincrypto' in url:
                yield scrapy.Request(url=url, callback=self.parse_bein)
            elif 'criptonoticias' in url:
               yield scrapy.Request(url=url, callback=self.parse_cripto)
            elif 'cointelegraph' in url:
                yield scrapy.Request(url=url,  callback=self.parse_coin)
            
    def parse_bein(self, response):  
        for bein in response.xpath('//html/body/div[2]/div[2]/main/div[2]/div'):
            imagen = bein.xpath('.//a/figure/img/@data-src').get()
            titulo = bein.xpath('.//div[2]/h3/a/text()').get()

            # Seguir el enlace a la noticia completa
            enlace = bein.xpath('.//a/@href').get()
            yield response.follow(enlace, self.analizar_noticia, meta={'imagen': imagen, 'titulo': titulo})

    def analizar_noticia(self, response):
        # Extraer información de la noticia completa
        imagen = response.meta['imagen']
        titulo = response.meta['titulo']
        cuerpo = response.xpath('//html/body/div[2]/div[2]/main/article/div/div[1]/div[4]/div[1]')

        content = BeautifulSoup(cuerpo.get(), 'html.parser').text.replace('\n', '')

        yield {
            'Titulo': titulo,
            'Imagen': imagen,
            'Contenido': content
        }      
    
     
    def parse_cripto(self, response):       
        for cripto in response.xpath('//html/body/div[3]/div[5]/div/div[1]/div[2]/div/div[4]/div[1]/div/div[2]/div/div[1]/div[1]/article'): 
            yield{
            'Titulo': cripto.xpath('.//div[2]/h3/a/text()').get(),
            'Imagen': cripto.xpath('.//div[1]/a/div/picture/img/@data-src').get(),
            'Contenido': cripto.xpath('.//div[2]/div[2]/p[1]/text()').extract_first(), 
        }
    
    def parse_coin(self, response):       
          for coin in response.xpath('//*[@id="__layout"]/div/div[1]/main/div/div/div[3]/div[1]/div/ul/li'):
            
            yield{
            'Titulo': coin.xpath('//article/div/div[1]/a/span/text()').get(),
            'Imagen': coin.xpath('//article/a/figure/div/img/@data-src').get(),
            'Contenido': coin.xpath('//article/div/p/text()').extract_first(),
        }
            
              