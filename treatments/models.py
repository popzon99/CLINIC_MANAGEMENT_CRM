# from django.db import models

# class Speciality(models.Model):
#     name = models.CharField(max_length=100)
#     # Add other fields as needed
#     # ...

# class Treatment(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     specialities = models.ManyToManyField(Speciality)
#     # Add other fields as needed
#     # ...

# from django.db import models

# class Treatment(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()

#     def __str__(self):
#         return self.name

# class Package(models.Model):
#     treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     duration = models.PositiveIntegerField(help_text="Duration in minutes")
#     includes = models.TextField()
#     available = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name
