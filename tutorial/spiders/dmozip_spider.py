import scrapy
import time, random
from tutorial.items import DmozyArticle

starturl = "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=lboyQG8AAAAJ&citation_for_view=lboyQG8AAAAJ:u5HHmVD_uO8C"

class DmozipSpider(scrapy.Spider):
    name = "dmozip"
    """articles property of google scholar"""
    allowed_domains = ["dmoz.org"]
    start_urls = [
        starturl,
    ]

    def parse(self, response):
        item = DmozyArticle()
        base = response.xpath("/html/body/div[@id='gs_top']/div[@id='gs_bdy']/div[@id='gs_ccl']/div[@id='gsc_ccl']")

        item['name'] = base.xpath("div[@id='gsc_title_wrapper']/div[@id='gsc_title']/a/text()").extract()[0]
        try:
            item['link'] = base.xpath("div[@id='gsc_title_wrapper']/div[@id='gsc_title_gg']/div/a/@href").extract()[0]

        except:
            pass

        for i in base.xpath("div[@id='gsc_table']/div[@class='gs_scl']"):
            try:
                k = i.xpath("div[@class='gsc_field']/text()").extract()
                v = i.xpath("div[@class='gsc_value']/text()").extract()

                if (k == 'Authors'):
                    item['authors'] = v.split(',')

                elif (k == 'Publication date'):
                    item['date'] = v

                elif (k == 'Description'):
                    item['description'] = k

                elif (k == 'Publisher'):
                    item['publisher'] = k

            except:
                pass


        yield item
        time.sleep(random.randrange(1, 5))
