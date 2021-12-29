import scrapy


url= "https://www.chefkoch.de/rezepte/zufallsrezept/"


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ["https://www.chefkoch.de/rezepte/zufallsrezept/"]

    def parse(self, response):
        table = response.xpath("/html/body/main/article[2]/table")
        rows = table.xpath("//tr")
        for row in rows:
            for i in row.xpath("td//text()".extract()):
                print(i)

