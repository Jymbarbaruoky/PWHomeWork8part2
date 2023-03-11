from mongoengine import *

connect(host="mongodb+srv://PWHomeWork:123321@cluster0.duijelz.mongodb.net/PWHomeWork82?retryWrites=true&w=majority",
        ssl=True)


class ClientInfo(Document):
    fullname = StringField(max_length=50)
    email = EmailField()
    phone = StringField()
    best_message_is_email = BooleanField(default=True)
    best_message_is_sms = not best_message_is_email
    status = BooleanField(default=False)
