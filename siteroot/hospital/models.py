from django.db.models import *

class SickList(Model):
    title = CharField(max_length=200)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

class Record(Model):
    sick_list = ForeignKey(SickList, on_delete=CASCADE)
    condition = CharField(max_length=100)
    medicines = TextField(max_length=200)
    text = TextField(max_length=4096)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

# Create your models here.
