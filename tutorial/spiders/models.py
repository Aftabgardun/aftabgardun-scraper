from mongoengine import *

#from sqlalchemy.dialects.mysql import BIGINT
class Person(Document):
    '''Person'''
    name = StringField(max_length=100, required=True)
    googleid = StringField(max_length=100)
    email = StringField(max_length=150)
    webpages = ListField(URLField())
    occupation = StringField()
    papers = ListField(StringField())
    keywords = ListField(StringField())
    photo = URLField()
    maindbid = StringField()
    
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
        ]
    }
    
class Paper(Document):
    '''Paper'''
    title = StringField(max_length=300, required=True)
    digest = StringField()
    publicationtype = StringField()
    authors = ListField(StringField())
    date = DateTimeField()
    publisher = StringField()
    keywords = ListField(StringField())
    content = URLField()
    maindbid = StringField()
    
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
        ]
    }

    
    
    
