from django.db import models


class Cities(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class Countries(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    cities = models.ManyToManyField(Cities, blank=True)
    indicatif = models.CharField(max_length=200, blank=True, null=True)
    monnaie = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return str(self.name)


