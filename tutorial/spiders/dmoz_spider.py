import scrapy
from urlparse import parse_qs, urlsplit
from tutorial.items import DmozItem, DmozyArticle
from scrapy.exporters import JsonItemExporter
import mongoengine
import models

mongoengine.connect('kallemahi')

starturl = "https://scholar.google.com/citations?view_op=search_authors&mauthors=mohsen+sharifi&hl=en&oi=ao"
starturl2 = "https://www.base-search.net/Search/Results?lookfor=adel+torkaman+rahmani"
baseurl = "https://scholar.google.com"
baseurl2 = "https://www.base-search.net"

google_scholar_papers_page_size = 20

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
        
starturl = "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=abdollahi+azgomi"
starturl = "https://scholar.google.com/citations?view_op=search_authors&mauthors=abdollahi+azgomi&hl=en&oi=ao"
starturl = "https://scholar.google.com/citations?view_op=search_authors&mauthors=behrouz+minaei&hl=en&oi=ao"

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        starturl
    ]
    start_urls2 = [
        #starturl2
    ]

    def closed(self, reason):
        exporter.finish_exporting()
        exporterfile.close()
    
    def start_requests(self):
        self.state['seen_users'] = []
        self.state['seen_paper'] = []
        self.state['seen_users2'] = []
        self.state['seen_papers2'] = []

        while (len(self.start_urls) > 0):
             yield scrapy.Request(self.start_urls.pop(0), callback=self.parse, dont_filter=True)
        while (len(self.start_urls2) > 0):
            yield scrapy.Request(self.start_urls2.pop(0), callback=self.parse_search2, dont_filter=True)


    def parse(self, response):
        for sel in response.xpath("/html/body//div[@id='gs_bdy']/div[@role='main']//div[@class='gsc_1usr gs_scl']"):
            link = sel.xpath("div[@class='gsc_1usr_photo']/a/@href").extract()[0]
            linkId = parse_qs(urlsplit(link).query)['user'][0]
            print("Got Link:" + linkId)
            if linkId not in self.state['seen_users']:
                self.state['seen_users'].append(linkId)
                yield scrapy.Request(baseurl + link + "&cstart=0&pagesize=" + str(google_scholar_papers_page_size), callback=self.parse_person, dont_filter=True)
    

    def parse_person(self, response):
        item = DmozItem()
        print ("Scraping Person:" + response.url)
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
            print("Error: Person has no Name:" + response.url)
            return
        
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
        
        
        
        p = models.Person(name=item['name'])
        p.googleid = item['dmozid']
        p.email = item['mail']
        if (item['homePage']):
            p.webpages.append(item['homePage'])
        p.occupation = item['position']
        if (item['photo']):
            p.photo = baseurl + item['photo']
        p.keywords.extend(item['keywords'])
        
        
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
                if (name not in p.papers):
                    p.papers.append(name)
                
            except:
                pass

        if not (base.xpath("div[@id='gsc_art']/form/div[@id='gsc_lwp']/div/button[@id='gsc_bpf_next'][@disabled]")):
            cstart = parse_qs(urlsplit(response.url).query)['cstart'][0]
            newstart = str(int(cstart) + google_scholar_papers_page_size)
            yield scrapy.Request(response.url.replace('cstart=' + cstart, 'cstart=' + newstart),
                           callback=self.parse_paper_list, dont_filter=True, meta={"person": p})


        item['articles'] = articles
        del articles
        
        p.save()
        #exporter.export_item(item)
        print ("Scraped Person:" + item['name'])
        yield item
    
    
    def parse_article(self, response):
        item = DmozyArticle()
        print ("Scraping Paper:" + response.url)
        base = response.xpath("/html/body/div[@id='gs_top']/div[@id='gs_bdy']/div[@id='gs_ccl']/div[@id='gsc_ccl']")
        
        try:
            item['name'] = base.xpath("div[@id='gsc_title_wrapper']/div[@id='gsc_title']/a/text()").extract()[0]
        
        except:
            try:
                item['name'] = base.xpath("div[@id='gsc_title_wrapper']/div[@id='gsc_title']/text()").extract()[0]

            except:
                print "Bug:" + response.url
                return
        
        try:
            item['link'] = base.xpath("div[@id='gsc_title_wrapper']/div[@id='gsc_title_gg']/div/a/@href").extract()[0]
        
        except:
            item['link'] = ""
        
        item['date'] = ""
        item['description'] = ""
        item['publisher'] = ""
        item['authors'] = []
        
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
        #exporter.export_item(item)
        p = models.Paper(title=item['name'])
        if (item['description']):
            p.digest = item['description']
        if (item['publisher']):
            p.publisher = item['publisher']
        if (item['link']):
            p.content = item['link']
        p.authors.extend([i.strip() for i in item['authors']])
        p.save()
        
        print ("Scraped Paper:" + item['name'])
        yield item


    def parse_paper_list(self, response):
        userId = parse_qs(urlsplit(response.url).query)['user'][0]
        p = response.meta['person']
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
                if (name not in p.papers):
                    p.articles.append(name)

            except:
                pass
        print("New Page Read for " + userId)
        if not (base.xpath("div[@id='gsc_art']/form/div[@id='gsc_lwp']/div/button[@id='gsc_bpf_next'][@disabled]")):
            print("Raftam safe baadi")
            cstart = parse_qs(urlsplit(response.url).query)['cstart'][0]
            newstart = str(int(cstart) + google_scholar_papers_page_size)
            yield scrapy.Request(response.url.replace('cstart=' + cstart, 'cstart=' + newstart),
                           callback=self.parse_paper_list, dont_filter=True, meta={"person": p})



    def parse_search2(self, response):
        base = response.xpath("/html/body/div[@id='Box1forIe']/div[@id='Box2forIe']")

        for i in base.xpath("div[@id='ResultsDrilldowns']/div[@id='ResultsBox']/form/div[@class='Results']"):
            item = DmozyArticle()
            item['itemtype'] = 'Paper'
            item['name'] = i.xpath("h2/a/text()").extract()[0].strip()
            if item['name'] == 'Title not available':
                continue

            if item['name'] not in self.state['seen_papers2']:
                self.state['seen_papers2'].append(item['name'])
            else:
                continue

            item['link'] = i.xpath("h2/a/@href").extract()[0]
            item['date'] = ""
            item['description'] = ""
            item['publisher'] = ""
            item['authors'] = []

            for j in i.xpath("div[@class='ResultsContent']/div[@class='DottedLineLeftForIe']/div[@class='Metadata']/div[@class='Item']"):
                try:
                    k = j.xpath("div[@class='ItemLeft_en']/text()").extract()[0]
                    v = j.xpath("div[@class='ItemRight_en']/text()").extract()[0]
                except:
                    continue

                if k == 'Publisher:':
                    item['publisher'] = v
                elif k == 'Year of Publication:':
                    item['date'] = v
                elif k == 'Author:':
                    for p in j.xpath("div[@class='ItemRight_en']/div[@class='Hidden']/a"):
                        n = p.xpath('text()').extract()[0].strip()
                        l = p.xpath('@href').extract()[0]
                        item['authors'].append(n)
                        if n not in self.state['seen_users2']:
                            self.state['seen_users2'].append(n)
                            oo = models.Person.objects(name__iexact=n).first()
                            if oo == None:
                                o = models.Person(name=n)
                                o.papers.append(item['name'])
                                o.save()
                                print('person2 added: ' + n)
                            else:
                                oo.papers.append(item['name'])
                                oo.save()
                            if 'script' not in l:
                                yield scrapy.Request(baseurl2 + l, callback=self.parse_search2, dont_filter=True)

            p = models.Paper(title=item['name'])
            if (item['description']):
                p.digest = item['description']
            if (item['publisher']):
                p.publisher = item['publisher']
            if (item['link']):
                p.content = item['link']
            p.authors.extend([i.strip() for i in item['authors']])
            p.save()

            yield item
            print ("Scraped2: " + item['name'])
