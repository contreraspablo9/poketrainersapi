from django.db import models


class TeamMembersT(models.Model):
    member_id = models.AutoField(primary_key=True)
    pokemon_id = models.IntegerField()
    team_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'team_members_t'


class TeamsDataT(models.Model):
    team_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    creation_date = models.DateTimeField(auto_now=True)
    trainer_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'teams_data_t'


class TrainersDataT(models.Model):
    trainer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    age = models.IntegerField()
    creation_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'trainers_data_t'
