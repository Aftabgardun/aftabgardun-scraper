from mongoengine import *

alias_lists = ['buffer-db', 'main-db'] # list of aliases
dbs = ['kallemahi', 'aftsabgardun'] # list of databases
for alias, db in zip(alias_lists, dbs):
    register_connection(alias, db)

#from sqlalchemy.dialects.mysql import BIGINT
class PPerson(Document):
    '''Person'''
    name = StringField(max_length=100, required=True)
    email = StringField(max_length=150)
    birthdate = DateTimeField()
    webpages = ListField(URLField())
    occupation = StringField()
    organizations = ListField(ReferenceField("Organization"))
    papers = ListField(ReferenceField("PPaper"))
    keywords = ListField(StringField())
    photo = URLField()
    meta = {
        'indexes': [
            {
                'fields': ['name']
            },
            {
                'fields': ['email']
            }
        ],
        "db_alias": 'main-db'
    }
    
class PPaper(Document):
    '''Paper'''
    title = StringField(max_length=300, required=True)
    digest = StringField()
    publicationtype = StringField()
    authors = ListField(ReferenceField("PPerson"))
    date = DateTimeField()
    publisher = StringField()
    keywords = ListField(StringField())
    content = URLField()
    citedby = ListField(ReferenceField("PPaper"))
    cites = ListField(ReferenceField("PPaper"))
    
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
        "db_alias": 'main-db'
    }
    
class Organization(Document):
    '''Organization'''
    name = StringField(max_length=100, required=True)
    location = StringField()
    webpage = URLField()
    photo = URLField()
    members = ListField(ReferenceField("PPerson"))
    description = StringField()
    meta = {
        'indexes': [
            {
                'fields': ['name']
            }
        ],
        "db_alias": 'main-db'
    }
    
    
    
