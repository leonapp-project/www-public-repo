from django.db import models


class Scanner(models.Model):
    name = models.CharField(max_length=255)
    pin = models.CharField(max_length=6)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'scanners'


# class FakeModel(models.Model):
#     name = models.CharField(max_length=255)
#     pin = models.CharField(max_length=6)
#     count = models.PositiveIntegerField(default=0)
#
#     def __str__(self):
#         return self.name
