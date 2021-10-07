from django.db import models


# Create your models here.
class Document(models.Model):
    filename = models.FileField(upload_to='files/')
