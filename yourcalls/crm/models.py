from django.db import models


# Create your models here.

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField( max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city =  models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)
    phone1 = models.CharField(max_length=50)
    phone2 = models.CharField( max_length=50, default='', blank=True)
    phone3 = models.CharField(max_length=50, default='', blank=True)

    def __str__(self):
        return(f"{self.first_name} {self.last_name}")


class RecordsFile(models.Model):
    file = models.FileField(upload_to='files', max_length=100)