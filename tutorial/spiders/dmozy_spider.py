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
        coAuthorsLink = []

        for coAuthor in base.xpath("div[@id='gsc_rsb']/div[@id='gsc_rsb_co']/ul/li"):
            try:
                coAuthors.append(coAuthor.xpath("a/@href").extract()[0])
                coAuthorsLink.append(coAuthor.xpath("a/text()").extract()[0])

            except:
                pass

        item['coAuthors'] = coAuthors
        item['coAuthorsLink'] = coAuthorsLink

        del coAuthorsLink, coAuthors

        cites = []
        years = []
        topic = []
        authors = []
        link = []

        for art in base.xpath("div[@id='gsc_art']/form/table/tbody/tr"):
            try:
                cites.append(art.xpath("td[@class='gsc_a_c']/a/text()").extract()[0])
                years.append(art.xpath("td[@class='gsc_a_y']/span/text()").extract()[0])
                topic.append(art.xpath("td[@class='gsc_a_t']/a/text()").extract()[0])
                authors.append(art.xpath("td[@class='gsc_a_t']/div[@class='gs_gray']/text()").extract()[0].split(', '))
                link.append(art.xpath("td[@class='gsc_a_t']/a/@href").extract()[0])

            except:
                pass

        item['articleTopics'] = topic
        item['articleAuthors'] = authors
        item['articleCitedBy'] = cites
        item['articleYear'] = years
        item['articleLink'] = link

        del topic, authors, cites, years, link

        yield item
        time.sleep(random.randrange(1, 5))
