from typing import List
from django.db import models


class uri(models.Model):
    filename=models.CharField(max_length=255)
    uri = models.CharField(max_length=500)
    access_time=models.DateTimeField()
    sha1_checksum=models.CharField(max_length=500)

    class Meta:
        manage = False
        db_table='uri'


class input_domain(models.Model):
    uri =models.OneToOneField(uri)

    class Meta:
        manage = False
        db_table='input_domain'


class output_domain(models.Model):
    uri=models.OneToOneField(uri)
    media_type=models.CharField(max_length=500)

    class Meta:
        manage = False
        db_table='output_domain'


class io_domain(models.Model):
    input_domain=models.ManyToManyField(input_domain)
    output_domain=models.ManyToManyField(output_domain)

    class Meta:
        manage = False
        db_table='io_domain'





    
