from django.forms import CharField, Form


class SearchForm(Form):
    search = CharField(max_length=100, required=False)
