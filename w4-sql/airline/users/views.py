from django.contrib.auth import authenticate, login, logout
from audioop import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def index (request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None: 
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid credentials"
            })        


def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message": "Logged out"
    })