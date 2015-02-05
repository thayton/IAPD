from django.db import models

class IapdFirm(models.Model):
    query_name = models.CharField(max_length=64)
    legal_name = models.CharField(max_length=64)
    other_name = models.CharField(max_length=64)

    sec_number = models.CharField(max_length=12)

    address = models.TextField()
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.query_name
