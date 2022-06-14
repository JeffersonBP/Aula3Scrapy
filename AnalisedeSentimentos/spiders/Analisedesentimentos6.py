import scrapy
class Analisedesentimentos6Spider(scrapy.Spider):
    name = 'Analisedesentimentos6'
    
    start_urls = ['https://www.aosfatos.org/']
# entra no menu da pagina busvando os links 
    def parse(self, response):
        links = response.xpath('//*[@id="menu"]/div/div/nav/ul[2]/li[1]/div/div/ul/li/a[re:test(@href, "checamos")]/@href').getall()
        for link in links:
            text_pag = f"https://www.aosfatos.org/{link}"
            yield scrapy.Request(text_pag, callback=self.categoria)
#gera todos os links das paginas para envoiar para o proximo parss            

    def categoria(self,response):
        noticias = response.xpath('/html/body/main/section/div/div/section/div/a/@href').getall()
        for noticia_url in noticias:
            text_pag2 = f"https://www.aosfatos.org{noticia_url}"
            yield scrapy.Request(text_pag2, callback=self.parss_noticias)             
#retira todas as informações para gravar no csv
    def parss_noticias(self,response):
        
        for  corpo in response.css('.default-container'):
            titulos = " ".join(corpo.xpath('/html/body/main/section/div/article/h1/text()').get().split())            
            textos = " ".join(corpo.xpath('/html/body/main/section/div/article/p/text()').getall())
            yield {
            'TITULO':titulos.encode('utf8') ,
            'TEXTO': textos.encode('utf8'),
            'DATA':' '.join(response.css('.publish-date::text').get().split()),
            'AUTOR': ' '.join(response.css('.author::text').get().split())
            }
            yield scrapy.Request('https://www.aosfatos.org/noticias/',callback=self.pross_pag)
#lopp para buscar todas as paginas
    def pross_pag(self,response):
        for i in range (1,154):
            text_pag4 = f"https://www.aosfatos.org/noticias/checamos/?page={i}"
            yield scrapy.Request(text_pag4,callback=self.categoria)
        
        