# myapp/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
        )

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name',)  # Đảm bảo trường "name" là duy nhất
