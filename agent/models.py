from mongoengine import *

#from sqlalchemy.dialects.mysql import BIGINT
class Person(Document):
    '''Person'''
    name = StringField(max_length=100, required=True)
    email = StringField(max_length=150)
    birthdate = DateTimeField()
    webpages = ListField(URLField())
    occupation = StringField()
    organizations = ListField(ReferenceField("Organization"))
    papers = ListField(ReferenceField("Paper"))
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
        ]
    }
    
class Paper(Document):
    '''Paper'''
    title = StringField(max_length=300, required=True)
    digest = StringField()
    publicationtype = StringField()
    authors = ListField(ReferenceField("Person"))
    date = DateTimeField()
    publisher = StringField()
    keywords = ListField(StringField())
    content = URLField()
    citedby = ListField(ReferenceField("Paper"))
    cites = ListField(ReferenceField("Paper"))
    
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
    
class Organization(Document):
    '''Organization'''
    name = StringField(max_length=100, required=True)
    location = StringField()
    webpage = URLField()
    photo = URLField()
    members = ListField(ReferenceField("Person"))
    description = StringField()
    meta = {
        'indexes': [
            {
                'fields': ['name']
            }
        ]
    }
    
    
    
