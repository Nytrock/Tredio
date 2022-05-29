from django.forms import CharField, Form, Select


class SearchForm(Form):
    search = CharField(max_length=100, required=False)
    location = Select()
