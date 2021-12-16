from django.db import models

class Template(models.Model):
    name = models.TextField(blank=False, null=False)
    url = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.name
