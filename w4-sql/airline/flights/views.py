from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Flight, Passenger


def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })


def flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })


def book(request, flight_id):
    if request.method == "POST":
        
        # get flight object
        flight = Flight.objects.get(pk=flight_id)
        
        # get passenger object with passenger integer
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        
        # add row to table for passenger's new flight booking
        passenger.flights.add(flight)

        # redirect to 'flight' page, sending flight.id as arg
        return HttpResponseRedirect(reverse("flight", args=(flight.id,)))