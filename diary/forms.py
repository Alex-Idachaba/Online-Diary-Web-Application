from django.db.models import fields
from .models import Entry
from django.forms import ModelForm

class EntryForm(ModelForm):

    class Meta:
        model = Entry
        fields = ['title', 'body']