from audioop import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def index (request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

def login_request(request):
    return render(request, "login.html")