import mongoengine

import models

import utility
    
    
class Person(mongoengine.Document):
    '''Person'''
    name = mongoengine.StringField(max_length=100, required=True)
    googleid = mongoengine.StringField(max_length=100)
    email = mongoengine.StringField(max_length=150)
    webpages = mongoengine.ListField(mongoengine.URLField())
    occupation = mongoengine.StringField()
    papers = mongoengine.ListField(mongoengine.StringField())
    keywords = mongoengine.ListField(mongoengine.StringField())
    photo = mongoengine.URLField()
    maindbid = mongoengine.StringField()
    meta = {
        'indexes': [
            {
                'fields': ['name']
            },
            {
                'fields': ['googleid']
            },
            {
                'fields': ['email']
            },
            {
                'fields': ['maindbid']
            }
        ],
        "db_alias": 'buffer-db'
    }
    
class Paper(mongoengine.Document):
    '''Paper'''
    title = mongoengine.StringField(max_length=300, required=True)
    digest = mongoengine.StringField()
    publicationtype = mongoengine.StringField()
    authors = mongoengine.ListField(mongoengine.StringField())
    date = mongoengine.DateTimeField()
    publisher = mongoengine.StringField()
    keywords = mongoengine.ListField(mongoengine.StringField())
    content = mongoengine.URLField()
    maindbid = mongoengine.StringField()
    
    meta = {
        'indexes': [
            {
                'fields': ['title']
            },
            {
                'fields': ['authors']
            },
            {
                'fields': ['keywords']
            },
            {
                'fields': ['publisher']
            },
            {
                'fields': ['digest']
            },
            {
                'fields': ['date']
            },
            {
                'fields': ['maindbid']
            }
        ],
        "db_alias": 'buffer-db'
    }
    
for i in Person.objects():
    i.maindbid = None
    i.save()
for i in Paper.objects():
    i.maindbid = None
    i.save()

k = Person.objects(maindbid=None)
for i in k:
    p2 = models.PPerson.objects(name__iexact=i.name)
    cont = False
    for g in p2:
        sim = utility.getPersonSimilarity(g, i)
        if (sim >= 0.6):
            cont = True
            i.maindbid = str(g.id)
            i.save()
            break
    if (cont):
        continue
    p = models.PPerson(name=i.name)
    p.email = i.email
    p.keywords.extend(i.keywords)
    p.occupation = i.occupation
    p.photo = i.photo
    print("Added person ", p.name)
    p.save()
    i.maindbid = str(p.id)
    i.save()
    #i.maindbid


k = Paper.objects(maindbid=None)
for i in k:
    pp = models.PPaper.objects(title__iexact=i.title)
    cont = False
    for p2 in pp:
        if (p2.digest and i.digest):
            sim = utility.getStringSimilarity(p2.digest, i.digest)
            if (sim < 0.8):
                continue
        i.maindbid = str(p2.id)
        i.save()
        cont = True
    if (cont):
        continue
    p = models.PPaper(title=i.title)
    p.digest = i.digest
    p.keywords.extend(i.keywords)
    p.publisher = i.publisher
    p.content = i.content
    
    print("Added paper ", p.title)
    p.save()
    i.maindbid = str(p.id)
    i.save()

k = models.PPerson.objects()
for i in k:
    ps = Person.objects(maindbid=str(i.id))
    for j in ps:
        for k in j.papers:
            papers = models.PPaper.objects(title__iexact=k)
            for p in papers:
                u = Paper.objects(maindbid=str(p.id))
                ok = False
                for j in u:
                    if (i.name.strip().lower() in [ppp.strip().lower() for ppp in j.authors]):
                        ok = True
                        break
                if (ok):
                    if (i not in p.authors):
                        p.authors.append(i)
                    if (p not in i.papers):
                        i.papers.append(p)
                        print("Done " + i.name + " <=> " + p.title)
                    i.save()
                    p.save()
                    
