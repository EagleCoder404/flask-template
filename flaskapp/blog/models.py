import mongoengine as me

class BlogPost(me.Document):
    title = me.StringField(required=True)
    body = me.StringField(required=True)
