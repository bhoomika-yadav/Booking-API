from django.db import models

# Create your models here.
# booking_app/models.py

from django.utils.timezone import now

class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    total_slots = models.IntegerField()
    available_slots = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.date_time}"

class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booking_time = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.client_name} - {self.fitness_class.name}"

