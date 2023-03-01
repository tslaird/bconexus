from typing import List
from django.db import models

class environment_variables(models.Model):
    value = models.CharField(max_length=500)

    class Meta:
        manage = False
        db_table='environment_variables'

class external_data_point(models.Model):
    name=models.CharField(max_length=255)
    url=models.CharField(max_length=255)

    class Meta:
        manage = False
        db_table='external_data_point'

class uri(models.Model):
    filename=models.CharField(max_length=255)
    uri = models.CharField(max_length=500)
    access_time=models.DateTimeField()
    sha1_checksum=models.CharField(max_length=500)

    class Meta:
        manage = False
        db_table='uri'

class software_prerequisite(models.Model):
    name=models.CharField(max_length=255)
    version=models.CharField(max_length=255)
    uri = models.OneToOneField(uri,verbose_name="uri")

    class Meta:
        manage = False
        db_table='software_prerequisite'


class execution_domain(models.Model):    
    script_driver = models.CharField(max_length=500)
    script = models.ManyToManyField(uri, verbose_name="script")
    software_prerequisites = models.ManyToManyField(software_prerequisite, verbose_name="software_prerequisites")
    external_data_points = models.ManyToManyField(external_data_point, verbose_name="external_data_points")    
    environment_variables=models.OneToOneField(environment_variables,verbose_name="environment_variables")    

    class Meta:
        manage = False
        db_table='execution_domain'




    
