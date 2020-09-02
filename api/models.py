from django.db import models

class Scraper(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(max_length=115, unique=True, default="N/D", verbose_name='Moneda')
    frequency = models.IntegerField(default=0, verbose_name='Frecuencia')

