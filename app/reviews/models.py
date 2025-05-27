from django.db import models
from django.core.exceptions import ValidationError

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, related_name='manufacturers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'country')
        verbose_name = "Manufacturer"
        verbose_name_plural = "Manufacturers"

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(Manufacturer, related_name='cars', on_delete=models.CASCADE)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()

    class Meta:
        unique_together = ('name', 'manufacturer')
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def clean(self):
        if self.end_year < self.start_year:
            raise ValidationError('End year cannot be earlier than start year')

    def __str__(self):
        return self.name


class Comment(models.Model):
    email = models.EmailField()
    car = models.ForeignKey(Car, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Comment by {self.email} on {self.car}"
