import scrapy
import time, random
from tutorial.items import DmozItem, DmozyArticle
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
        for sel in response.xpath("/html/body//div[@id='gs_bdy']/div[@role='main']//div[@class='gsc_1usr gs_scl']"):
            link = sel.xpath("div[@class='gsc_1usr_photo']/a/@href").extract()[0]
            time.sleep(random.randrange(6, 10))
            yield scrapy.Request(baseurl + link, callback=self.parse_person, dont_filter=True)
    

    def parse_person(self, response):
        item = DmozItem()
        base = response.xpath("/html/body//div[@id='gsc_bdy']")

        baseInfo = base.xpath("div[@class='gsc_lcl']/div[@id='gsc_prf']")
        item['itemtype'] = "Person"
        item['photo'] = baseInfo.xpath("div[@id='gsc_prf_pu']/a/img/@src").extract()[0]
        item['author'] = baseInfo.xpath("div[@id='gsc_prf_i']/div[@id='gsc_prf_in']/text()").extract()[0]
        item['position'] = baseInfo.xpath("div[@id='gsc_prf_i']/div[@class='gsc_prf_il']/text()").extract()[0]
        item['keywords'] = baseInfo.xpath("div[@id='gsc_prf_i']/div[@class='gsc_prf_il']/a[@class='gsc_prf_ila']/text()").extract()
        item['homePage'] = baseInfo.xpath("div[@id='gsc_prf_i']/div[@id='gsc_prf_ivh']/a/@href").extract()[0]
        item['mail'] = baseInfo.xpath("div[@id='gsc_prf_i']/div[@id='gsc_prf_ivh']/text()").extract()[0]\
            .replace('Verified email at ', '').replace(' - ', '')
        item['link'] = response.url

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

        time.sleep(random.randrange(2, 5))
        
        exporter.export_item(item)
        return item
        
    
    
    def parse_article(self, response):
        time.sleep(random.randrange(2, 5))
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
        
        item['itemtype'] = 'Paper'
        exporter.export_item(item)
        yield item
