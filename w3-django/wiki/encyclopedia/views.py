import markdown2

from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from . import util


class NewSearchForm(forms.Form):
    query = forms.CharField(label="Search Encyclopedia", max_length=100)


# VIEWS
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown2.markdown(util.get_entry(title))
    })


def search(request):
    query = "query placeholder"
    return render(request, "encyclopedia/search.html", {
        "query": query
    })


def create(request):
    return render(request, "encyclopedia/create.html")


def edit(request):
    return render(request, "encyclopedia/edit.html")


# def random(request):
#     return render(request, "encyclopedia/TODO.html")


# TODO Convert from markdown to HTML
# print(markdown2.markdown("*boo!*"))
# or use `html = markdown_path(PATH)`
    # output: u'<p><em>boo!</em></p>\n'

# markdowner = Markdown()
# markdowner.convert("*boo!*")
    # output: u'<p><em>boo!</em></p>\n'

# markdowner.convert("**boom!**")
    # output: u'<p><strong>boom!</strong></p>\n'