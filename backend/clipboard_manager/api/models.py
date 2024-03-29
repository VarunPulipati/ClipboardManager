from django.db import models

class Shortcut(models.Model):
    identifier = models.CharField(max_length=100)
    keys = models.CharField(max_length=200)
    action = models.CharField(max_length=10)  # "copy" or "paste"

    def __str__(self):
        return self.identifier
