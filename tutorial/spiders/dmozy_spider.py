import scrapy
import time, random
from tutorial.items import DmozyItem

starturl = "https://scholar.google.com/citations?user=lboyQG8AAAAJ&hl=en&oi=ao"


class DmozySpider(scrapy.Spider):
    name = "dmozy"
    """top articles of google scholar profile"""
    allowed_domains = ["dmoz.org"]
    start_urls = [
        starturl,
    ]
    
    def parse(self, response):
        item = DmozyItem()
        base = response.xpath("/html/body//div[@id='gsc_bdy']")

        baseInfo = base.xpath("div[@class='gsc_lcl']/div[@id='gsc_prf']")
        item['author'] = baseInfo.xpath("div[@id='gsc_prf_i']/div[@id='gsc_prf_in']/text()").extract()[0]
        item['position'] = baseInfo.xpath("div[@id='gsc_prf_i']/div[@class='gsc_prf_il']/text()").extract()[0]
        item['keywords'] = baseInfo.xpath("div[@id='gsc_prf_i']/div[@class='gsc_prf_il']/a[@class='gsc_prf_ila']/text()").extract()
        item['homePage'] = baseInfo.xpath("div[@id='gsc_prf_i']/div[@id='gsc_prf_ivh']/a/@href").extract()[0]

        coAuthors = []

        for coAuthor in base.xpath("div[@id='gsc_rsb']/div[@id='gsc_rsb_co']/ul/li"):
            try:
                coAuthors.append(dict(
                    name=coAuthor.xpath("a/text()").extract()[0],
                    link=coAuthor.xpath("a/@href").extract()[0]
                ))

            except:
                pass

        item['coAuthors'] = coAuthors
        del coAuthors

        articles = []

        for art in base.xpath("div[@id='gsc_art']/form/table/tbody/tr"):
            try:
                articles.append(dict(
                    name=art.xpath("td[@class='gsc_a_t']/a/text()").extract()[0],
                    link=art.xpath("td[@class='gsc_a_t']/a/@href").extract()[0]
                ))

            except:
                pass

        item['articles'] = articles
        del articles

        yield item
        time.sleep(random.randrange(1, 5))
