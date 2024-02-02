from django.db import models

class ImageModel(models.Model):
    """Image representation"""
    image = models.ImageField(upload_to='images/',
                             verbose_name='image',)

class GeneratedImage(models.Model):
    """Generated image representation"""
    class Status(models.TextChoices):
        COMPLETED = 'C', 'COMPLETED'
        READY = 'R', 'READY'
        ERROR = 'E', 'ERROR'

    original_image = models.ImageField(upload_to='images/',
                             verbose_name='original_image',)
    generated_image = models.ImageField(upload_to='generated/',
                             verbose_name='generated_image',)
    status = models.CharField(max_length=2, choices=Status.choices,
                             default=Status.READY)
