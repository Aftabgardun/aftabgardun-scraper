import mongoengine
import models


alias_lists = ['buffer-db', 'main-db'] # list of aliases
dbs = ['kallemahi', 'aftsabgardun'] # list of databases
for alias, db in zip(alias_lists, dbs):
    mongoengine.register_connection(alias, db)
    
    
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
            }
        ],
        "db_alias": 'buffer-db'
    }
    
k = Person.objects(maindbid=None)
for i in k:
    
    i.maindbid
