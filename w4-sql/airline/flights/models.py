from django.db import models


class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"


# class called flight, inherits from Model
class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def is_valid_flight(self):
        return self.origin != self.destination or self.duration > 0

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"


class Passenger(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"

# NOTE: each model must be added to admin.py

# NOTE: This is how to use and test the Flight model
# These 2 lines on initial creation/update only: 
# $ python3 manage.py makemigrations
# $ python3 manage.py migrate

# After creation/update: 
# $ python3 manage.py shell
# >>> from flights.models import Flight
# >>> f = Flight(origin="New York", destination="London", duration=415)
# >>> f.save()
# >>> f
# <Flight: Flight object (1)>
# >>> f.origin
# 'New York'
# >>> f.destination
# 'London'
# >>> f.duration
# 415
# >>> Flight.objects.all()
# <QuerySet [<Flight: Flight object (1)>]>