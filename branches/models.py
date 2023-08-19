from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()
    is_working = models.BooleanField(default=True)

    def __str__(self):
        return self.name


