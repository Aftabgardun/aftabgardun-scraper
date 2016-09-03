import scrapy
import time, random
from tutorial.items import DmozItem, DmozyItem
from scrapy.exporters import JsonItemExporter

starturl = "https://scholar.google.com/citations?view_op=search_authors&mauthors=mohsen+sharifi&hl=en&oi=ao"
baseurl = "https://scholar.google.com"

exporterfile = open("items.json",'wb')
exporter = JsonItemExporter(exporterfile)
exporter.start_exporting()

urls = [
        "https://scholar.google.com/citations?view_op=search_authors&mauthors=mohsen+sharifi&hl=en&oi=ao",
        "https://scholar.google.com/citations?view_op=search_authors&mauthors=adel+rahmani&hl=en&oi=ao",
        "https://scholar.google.com/citations?view_op=search_authors&mauthors=behrouz+minaie&hl=en&oi=ao",
        "https://scholar.google.com/citations?view_op=search_authors&mauthors=peyman+kabiri&hl=en&oi=ao",
        "https://scholar.google.com/citations?view_op=search_authors&mauthors=nasser+mozayyeni&hl=en&oi=ao",
        "https://scholar.google.com/citations?view_op=search_authors&mauthors=jahed&hl=en&oi=ao",
        "https://scholar.google.com/citations?view_op=search_authors&mauthors=saeid+parsa&hl=en&oi=ao"]

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        starturl
    ] + urls
    
    def closed(self, reason):
        exporter.finish_exporting()
        exporterfile.close()
    
    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse,
                                    dont_filter=True)
                                    
    def parse(self, response):
        #print(response.xpath("/html/body//div[@id='gs_bdy']/div[@role='main']//div[@class='gsc_1usr gs_scl']"))
        for sel in response.xpath("/html/body//div[@id='gs_bdy']/div[@role='main']//div[@class='gsc_1usr gs_scl']"):
            #print sel.extract()
            link = sel.xpath("div[@class='gsc_1usr_photo']/a/@href").extract()[0]
            image = sel.xpath("div[@class='gsc_1usr_photo']/a/img/@src").extract()[0]
            name = u''.join(sel.xpath("div[@class='gsc_1usr_text']/h3[@class='gsc_1usr_name']/a//text()").extract())
            afflication = u''.join(sel.xpath("div[@class='gsc_1usr_text']/div[@class='gsc_1usr_aff']/text()").extract())
            email = u''.join(sel.xpath("div[@class='gsc_1usr_text']/div[@class='gsc_1usr_emlb']/text()").extract())
            item = DmozItem()
            item['name'] = name
            item['link'] = link
            item['desc'] = afflication
            item['mail'] = email
            item['photo'] = image
            item['itemtype'] = "Person"
            time.sleep(random.randrange(6, 10))
            yield scrapy.Request(baseurl + item['link'], callback=self.parse_person, dont_filter=True)
            #print(res)
            #yield item
            #exporter.export_item(item)
            #title = sel.xpath('a/text()').extract()
            #link = sel.xpath('a/@href').extract()
            #desc = sel.xpath('text()').extract()
            #print title, link, desc
    
    
    def parse_person(self, response):
        item = DmozyItem()
        base = response.xpath("/html/body//div[@id='gsc_bdy']")

        baseInfo = base.xpath("div[@class='gsc_lcl']/div[@id='gsc_prf']")
        item['itemtype'] = "Person"
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
        print ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
        time.sleep(random.randrange(1, 5))
        
        exporter.export_item(item)
        return item
