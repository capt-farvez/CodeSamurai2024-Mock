from django.db import models

<<<<<<< HEAD
# Create your models here.
=======
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    price = models.FloatField()
>>>>>>> 2b6ef28819abbe7bff7d55ad8b21c9d7ccda9f86
