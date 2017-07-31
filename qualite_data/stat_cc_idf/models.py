# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class VerifNombreEntites(models.Model):
    type_object = models.CharField(max_length=10, blank=True, null=True)
    city_object_type = models.CharField(max_length=250, blank=True, primary_key=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"aaa_qualite_donnees"."verif_nombre_entites"'

    def get_type_object(self):
        return self.type_object
        
    def get_city_object_type(self):
        return self.city_object_type
        
    def get_count(self):
        return self.count