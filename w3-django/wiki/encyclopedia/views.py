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
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })


def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown2.markdown(util.get_entry(title)),
        "form": NewSearchForm()
    })


def search(request):
    query = "query not set"

    # get current list of entries
    entries = util.list_entries()

    # convert all entries in list to lowercase
    entries = [entry.lower() for entry in entries]

    # get search query 
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"].lower()

            # check if the query exists
            if query in entries:
                return render(request, "encyclopedia/search.html", {
                    "query": query,
                    "form": NewSearchForm(),
                    "entry": markdown2.markdown(util.get_entry(query))
                })
            else:
                return render(request, "encyclopedia/index.html", {
                    "entries": util.list_entries(),
                    "form": NewSearchForm(),
                })

        else:
            query = "form is not valid"
            return render(request, "encyclopedia/index.html", {
                "form": NewSearchForm()
            })
    
    return render(request, "encyclopedia/index.html", {
        "form": NewSearchForm()
    })


def create(request):
    return render(request, "encyclopedia/create.html", {
        "form": NewSearchForm()
    })


def edit(request):
    return render(request, "encyclopedia/edit.html", {
        "form": NewSearchForm()
    })