from django.db import models
from django.urls import reverse


class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, related_name='elements')

    def get_absolute_url(self):
        return reverse('elem', kwargs={'name': self.name})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.url == '':
            self.url = self.get_absolute_url()
        super().save(*args, **kwargs)

class Menu(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)

    def get_absolute_url(self):
        return reverse('menu', kwargs={'name': self.name})

    def save(self, *args, **kwargs):
        if self.url == '':
            self.url = self.get_absolute_url()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name