# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class VerifFieldMesh(models.Model):
    count = models.IntegerField(blank=True, primary_key=True)
    
    class Meta:
        managed = False
        db_table = 'verif_field_mesh'


class VerifHousehold(models.Model):
    count = models.IntegerField(blank=True, primary_key=True)
    
    class Meta:
        managed = False
        db_table = 'verif_household'


class VerifInvalidGeometry(models.Model):
    st_isvalid = models.NullBooleanField()
    object_id = models.CharField(max_length=250, blank=True, primary_key=True)
    city_object_type = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'verif_invalid_geometry'


class VerifNombreEntites(models.Model):
    type_object = models.CharField(max_length=30, blank=True, null=True)
    city_object_type = models.CharField(max_length=250, blank=True, primary_key=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'verif_nombre_entites'


class VerifProjection(models.Model):
    st_srid = models.IntegerField(blank=True, null=True)
    object_id = models.CharField(max_length=250, blank=True, null=True)
    city_object_type = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'verif_projection'


class VerifTypeInductrySector(models.Model):
    zone = models.CharField(max_length=250, blank=True, primary_key=True)
    value = models.IntegerField(blank=True, null=True)
    sector = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'verif_type_inductry_sector'


class VerifUrbanProjectCapacity(models.Model):
    object_id = models.CharField(max_length=50, blank=True, primary_key=True)
    usage = models.TextField(blank=True, null=True)
    area = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'verif_urban_project_capacity'
