from mongoengine import *

connect(host="mongodb+srv://PWHomeWork:123321@cluster0.duijelz.mongodb.net/PWHomeWork82?retryWrites=true&w=majority",
        ssl=True)


class MessageInfo(Document):
    fullname = StringField(max_length=50)
    email = EmailField()
    message = StringField()
    status = BooleanField(default=False)
