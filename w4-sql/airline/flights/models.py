from django.db import models

# class called flight, inherits from Model
class Flight(models.Model):
    origin = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)
    duration = models.IntegerField()

    # def __str__(self):
    #     return f"{self.origin} to {self.destination}, {self.duration}"

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



# class Airport(models.Model):
#     code = models.ForeignKey(max_length=3, )
#     city = models.ForeignKey(max_length=64, )

#     def __str__(self):
#         return f"{self.city} ({self.code})"