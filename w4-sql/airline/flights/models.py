from django.db import models

# class called flight, inherits from Model
class Flight(models.Model):
    origin = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)
    duration = models.IntegerField()

    # def __str__(self):
    #     return f"{self.origin} to {self.destination}, {self.duration}"


# class Airport(models.Model):
#     code = models.ForeignKey(max_length=3, )
#     city = models.ForeignKey(max_length=64, )

#     def __str__(self):
#         return f"{self.city} ({self.code})"