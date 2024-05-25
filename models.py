# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Oauth(models.Model):
    type = models.CharField(max_length=20)
    grade = models.IntegerField()
    okey = models.CharField(max_length=32)
    expiration = models.DateTimeField()
    access_to = models.JSONField()
    commento = models.TextField()

    class Meta:
        managed = False
        db_table = 'OAuth'


class OauthMap(models.Model):
    oauth = models.CharField(db_column='OAuth', max_length=33)  # Field name made lowercase.
    email = models.CharField(max_length=80, blank=True, null=True)
    username = models.CharField(max_length=16, blank=True, null=True)
    password = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'OAuth_map'


class Accessi(models.Model):
    type = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    ip = models.CharField(max_length=42)
    website = models.CharField(max_length=40, blank=True, null=True)
    path = models.CharField(max_length=80)
    uniq = models.CharField(max_length=32)
    auth_key = models.CharField(max_length=80, blank=True, null=True)
    display_name = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accessi'


class Acquisti(models.Model):
    user_id = models.IntegerField()
    date_purchased = models.DateTimeField()
    ticket_type = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'acquisti'


class Consumazioni(models.Model):
    ticket_code = models.CharField(max_length=17)
    ticket_type = models.CharField(max_length=12)
    ticket_id = models.IntegerField()
    date_scanned = models.DateTimeField()
    scanner_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'consumazioni'


class Services(models.Model):
    tag = models.CharField(max_length=32)
    status = models.CharField(max_length=12)
    comment = models.TextField()
    last_ping = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'services'


class UserWhitelist(models.Model):
    email = models.CharField(unique=True, max_length=80)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    class_section = models.CharField(max_length=3)
    class_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_whitelist'


class Utenti(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField()
    class_section = models.CharField(max_length=3)
    can_buy_tickets = models.IntegerField()
    username = models.CharField(unique=True, max_length=16)
    class_number = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'utenti'
