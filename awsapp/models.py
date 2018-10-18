from django.db import models

# Create your models here.
class Image(models.Model):
    image_id =models.CharField(max_length=200)
    image_name = models.CharField(max_length=200)

class Instance(models.Model):
    instance_id = models.CharField(max_length=200)
    instance_name = models.CharField(max_length=200)
    image_id = models.ForeignKey(Image, on_delete=models.DO_NOTHING)
