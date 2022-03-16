# imports
from django.db import models

# Create your models here.
# to do list model


class Todo_list(models.Model):
    title = models.CharField(max_length=255)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title
