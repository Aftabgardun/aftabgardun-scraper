import scrapy
from urlparse import parse_qs, urlsplit
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
    ]

    def closed(self, reason):
        exporter.finish_exporting()
        exporterfile.close()
    
    def start_requests(self):
        self.state['seen_user'] = []
        self.state['seen_paper'] = []

        while (len(self.start_urls) > 0):
            u = self.start_urls.pop(0)
            ret = scrapy.Request(u, callback=self.parse,
                                    dont_filter=True)
            yield ret
            print(ret)

    def parse(self, response):
        for sel in response.xpath("/html/body//div[@id='gs_bdy']/div[@role='main']//div[@class='gsc_1usr gs_scl']"):
            link = sel.xpath("div[@class='gsc_1usr_photo']/a/@href").extract()[0]
            linkId = parse_qs(urlsplit(link).query)['user'][0]
            if linkId not in self.state['seen_users']:
                self.state['seen_users'].append(linkId)
                yield scrapy.Request(baseurl + link + "&cstart=0&pagesize=100", callback=self.parse_person, dont_filter=True)
    

    def parse_person(self, response):
        item = DmozItem()
        base = response.xpath("/html/body//div[@id='gsc_bdy']")

        baseInfo = base.xpath("div[@class='gsc_lcl']/div[@id='gsc_prf']")
        item['itemtype'] = "Person"
        
        item['dmozid'] = parse_qs(urlsplit(response.url).query)['user'][0]
        try:
            item['photo'] = baseInfo.xpath("div[@id='gsc_prf_pu']/a/img/@src").extract()[0]
        except:
            item['photo'] = ''

        try:
            item['name'] = baseInfo.xpath("div[@id='gsc_prf_i']/div[@id='gsc_prf_in']/text()").extract()[0]
        except:
            item['name'] = ''

        try:
            item['position'] = baseInfo.xpath("div[@id='gsc_prf_i']/div[@class='gsc_prf_il']/text()").extract()[0]
        except:
            item['position'] = ''

        try:
            item['keywords'] = baseInfo.xpath(
                "div[@id='gsc_prf_i']/div[@class='gsc_prf_il']/a[@class='gsc_prf_ila']/text()").extract()
        except:
            item['keywords'] = ''

        try:
            item['homePage'] = baseInfo.xpath("div[@id='gsc_prf_i']/div[@id='gsc_prf_ivh']/a/@href").extract()[0]
        except:
            item['homePage'] = ''

        try:
            item['mail'] = baseInfo.xpath("div[@id='gsc_prf_i']/div[@id='gsc_prf_ivh']/text()").extract()[0] \
                .replace('Verified email at ', '').replace(' - ', '')
        except:
            item['mail'] = ''

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
                link = art.xpath("td[@class='gsc_a_t']/a/@href").extract()[0]
                name = art.xpath("td[@class='gsc_a_t']/a/text()").extract()[0]
                articles.append(dict(
                    name=name,
                    link=link
                ))

                if (name not in self.state['seen_paper']):
                    self.state['seen_paper'].append(name)
                    yield scrapy.Request(baseurl + link, callback=self.parse_article, dont_filter=True)
                
            except:
                pass

        if not (base.xpath("div[@id='gsc_art']/form/div[@id='gsc_lwp']/div/button[@id='gsc_bpf_next'][@disabled]")):
            cstart = parse_qs(urlsplit(response.url).query)['cstart'][0]
            newstart = str(int(cstart) + 100)
            scrapy.Request(response.url.replace('cstart=' + cstart, 'cstart=' + newstart),
                           callback=self.parse_paper_list, dont_filter=True)


        item['articles'] = articles
        del articles
        
        exporter.export_item(item)
        print ("Scraped Person:" + item['name'])
        yield item
    
    
    def parse_article(self, response):
        item = DmozyArticle()

        base = response.xpath("/html/body/div[@id='gs_top']/div[@id='gs_bdy']/div[@id='gs_ccl']/div[@id='gsc_ccl']")

        try:
            item['name'] = base.xpath("div[@id='gsc_title_wrapper']/div[@id='gsc_title']/a/text()").extract()[0]

        except:
            return

        try:
            item['link'] = base.xpath("div[@id='gsc_title_wrapper']/div[@id='gsc_title_gg']/div/a/@href").extract()[0]

        except:
            pass

        for i in base.xpath("div[@id='gsc_table']/div[@class='gs_scl']"):
            try:
                k = i.xpath("div[@class='gsc_field']/text()").extract()[0]
                v = i.xpath("div[@class='gsc_value']/text()").extract()[0]
                
                if (k == 'Authors'):
                    item['authors'] = v.split(',')
                    for lk in item['authors']:
                        yield scrapy.Request("https://scholar.google.com/citations?view_op=search_authors&mauthors=" +
                                             "+".join(lk.strip().lower().split(' ')) + "&hl=en&oi=ao",
                                             callback=self.parse, dont_filter=True)
                            
                        
                elif (k == 'Publication date'):
                    item['date'] = v

                elif (k == 'Description'):
                    item['description'] = v

                elif (k == 'Publisher'):
                    item['publisher'] = v

            except:
                pass
        
        item['itemtype'] = 'Paper'
        exporter.export_item(item)
        
        print ("Scraped Paper:" + item['name'])
        yield item


    def parse_paper_list(self, response):
        userId = parse_qs(urlsplit(response.url).query)['user'][0]

        base = response.xpath("/html/body//div[@id='gsc_bdy']")

        articles = []
        for art in base.xpath("div[@id='gsc_art']/form/table/tbody/tr"):
            try:
                link = art.xpath("td[@class='gsc_a_t']/a/@href").extract()[0]
                name = art.xpath("td[@class='gsc_a_t']/a/text()").extract()[0]
                articles.append(dict(
                    name=name,
                    link=link
                ))

                if (name not in self.state['seen_paper']):
                    self.state['seen_paper'].append(name)
                    yield scrapy.Request(baseurl + link, callback=self.parse_article, dont_filter=True)

            except:
                pass

        if not (base.xpath("div[@id='gsc_art']/form/div[@id='gsc_lwp']/div/button[@id='gsc_bpf_next'][@disabled]")):
            cstart = parse_qs(urlsplit(response.url).query)['cstart'][0]
            newstart = str(int(cstart) + 100)
            yield scrapy.Request(response.url.replace('cstart=' + cstart, 'cstart=' + newstart),
                           callback=self.parse_paper_list, dont_filter=True)
