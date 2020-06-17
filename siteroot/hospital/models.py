from django.db.models import *
from django.contrib.auth.models import User
from django.urls import reverse


class SickList(Model):
    doctor = ForeignKey(User, on_delete=CASCADE)
    title = CharField(max_length=200)
    created_at = DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('sicklist_by_id', kwargs={'sicklist_id': self.id})

    def __str__(self):
        return f"{self.title}, doctor: {self.doctor.username}"


class Record(Model):
    sick_list = ForeignKey(SickList, on_delete=CASCADE)
    person = CharField(max_length=200)
    condition = CharField(max_length=100)
    medicines = TextField(max_length=200)
    text = TextField(max_length=4096)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def is_modified(self):
        return (self.created_at - self.updated_at).total_seconds() > 0

    is_modified.boolean = True

    def __str__(self):
        return f"id: {self.id} sicklist: {self.sick_list.id}"

# Create your models here.
