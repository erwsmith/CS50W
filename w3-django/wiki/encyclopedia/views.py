import markdown2

from django import forms
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from . import util


class NewSearchForm(forms.Form):
    query = forms.CharField(label="Search Encyclopedia", max_length=100)

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(label="Content", max_length=10000)


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
    # get search query 
    if request.method == "POST":
        # get text entered in form
        form = NewSearchForm(request.POST)
        # validate form submission
        if form.is_valid():
            # clean data and set all letters to lowercase
            query = form.cleaned_data["query"]
            # get current list of entries
            entries = util.list_entries()
            # create list of lowercased entries
            entries_lower = [e.lower() for e in entries]
            # if the query exists, go directly to its page
            if query.lower() in entries_lower:
                return HttpResponseRedirect(reverse('encyclopedia:entry', kwargs=({"title":query})))
            # setup list of partial matches
            searchResult = []
            partialMatch = False
            for e in entries:
                if query.lower() in e.lower():
                    partialMatch = True
                    searchResult.append(e)
            # return partial matches
            if partialMatch:
                return render(request, "encyclopedia/index.html", {
                "entries": searchResult,
                "form": NewSearchForm()
            })
            else:
                return HttpResponse('Page not found')
        # if form text is invalid
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(),
                "form": NewSearchForm()
            })
    # if request method is not POST
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })


def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('encyclopedia:entry', kwargs=({"title":title})))
        else:
            return HttpResponse('invalid form')

    else:
        return render(request, "encyclopedia/create.html", {
            "form": NewSearchForm()
        })


def edit(request, title):
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": NewSearchForm()
    })