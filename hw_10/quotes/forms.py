from django.forms import ModelForm, CharField, TextInput, DateField, DateInput, ModelChoiceField, \
     Select, Textarea
from .models import Author, Quote, Tag


class AuthorForm(ModelForm):
    fullname = CharField(max_length=50, widget=TextInput(attrs={'class': 'form-control'}))
    born_date = DateField(widget=DateInput(attrs={'class': 'form-control'}))
    born_location = CharField(max_length=100, widget=TextInput(attrs={'class': 'form-control'}))
    description = CharField(max_length=1000, widget=Textarea(attrs={'rows': 10, 'cols': 100}))

    class Meta:
        model = Author
        fields = ('fullname', 'born_date', 'born_location', 'description')


class TagForm(ModelForm):
    class TagForm(ModelForm):
        name = CharField(max_length=25, required=True, widget=TextInput(attrs={'class': 'form-control'}))

        class Meta:
            model = Tag
            fields = ['name']


class QuoteForm(ModelForm):
    quote = CharField(max_length=1000, widget=TextInput(attrs={'class': 'form-control'}))
    author = ModelChoiceField(queryset=Author.objects.all().order_by('fullname'),
                              widget=Select(attrs={"class": "form-select"}))

    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].widget.attrs['class'] = 'select2'