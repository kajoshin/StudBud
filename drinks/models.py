from django.db import models


class Drink(models.Model):
    name = models.CharField(max_length= 200)
    description = models.CharField(max_length=500)

    objects = models.Manager()

    def __str__(self):
        return '{}: {}'.format(self.name, self.description)
