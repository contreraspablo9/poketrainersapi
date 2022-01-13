# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TeamMembersT(models.Model):
    member_id = models.IntegerField(primary_key=True)
    pokemon_id = models.IntegerField()
    team_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'team_members_t'


class TeamsDataT(models.Model):
    team_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    creation_date = models.DateTimeField()
    trainer_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'teams_data_t'


class TrainersDataT(models.Model):
    trainer_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    age = models.IntegerField()
    creation_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'trainers_data_t'
