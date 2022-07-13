# import markdown2

from django.shortcuts import render
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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