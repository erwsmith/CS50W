from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render


tasks = []


class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    # priority = forms.IntegerField(label="Priority", min_value=1, max_value=3)


# VIEWS
def index(request):
    return render(request, "tasks/index.html", {
        "tasks": tasks
    })


def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            # get data from form and add to tasks list
            task = form.cleaned_data["task"]
            tasks.append(task)
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })

    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })