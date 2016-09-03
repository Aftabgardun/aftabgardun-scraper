import scrapy
import time, random
from tutorial.items import DmozItem

starturl = "https://scholar.google.com/citations?view_op=search_authors&mauthors=mohsen+sharifi&hl=en&oi=ao"

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        starturl,
        "https://scholar.google.com/citations?view_op=search_authors&mauthors=mohsen+sharifi&hl=en&oi=ao",
        "https://scholar.google.com/citations?view_op=search_authors&mauthors=adel+rahmani&hl=en&oi=ao",
        "https://scholar.google.com/citations?view_op=search_authors&mauthors=behrouz+minaie&hl=en&oi=ao",
        "https://scholar.google.com/citations?view_op=search_authors&mauthors=peyman+kabiri&hl=en&oi=ao",
        "https://scholar.google.com/citations?view_op=search_authors&mauthors=nasser+mozayyeni&hl=en&oi=ao",
        "https://scholar.google.com/citations?view_op=search_authors&mauthors=jahed&hl=en&oi=ao",
        "https://scholar.google.com/citations?view_op=search_authors&mauthors=saeid+parsa&hl=en&oi=ao",
    ]
    
    def parse(self, response):
        #print(response.xpath("/html/body//div[@id='gs_bdy']/div[@role='main']//div[@class='gsc_1usr gs_scl']"))
        for sel in response.xpath("/html/body//div[@id='gs_bdy']/div[@role='main']//div[@class='gsc_1usr gs_scl']"):
            #print sel.extract()
            link = sel.xpath("div[@class='gsc_1usr_photo']/a/@href").extract()[0]
            image = sel.xpath("div[@class='gsc_1usr_photo']/a/img/@src").extract()[0]
            name = u''.join(sel.xpath("div[@class='gsc_1usr_text']/h3[@class='gsc_1usr_name']/a//text()").extract())
            afflication = u''.join(sel.xpath("div[@class='gsc_1usr_text']/div[@class='gsc_1usr_aff']/text()").extract())
            email = u''.join(sel.xpath("div[@class='gsc_1usr_text']/div[@class='gsc_1usr_emlb']/text()").extract())
            print image
            print link
            print name
            print afflication
            print email
            item = DmozItem()
            item['name'] = name
            item['link'] = link
            item['desc'] = afflication
            item['mail'] = email
            item['photo'] = image
            yield item
            time.sleep(random.randrange(6, 10))
            #title = sel.xpath('a/text()').extract()
            #link = sel.xpath('a/@href').extract()
            #desc = sel.xpath('text()').extract()
            #print title, link, desc
        
