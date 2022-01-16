from rest_framework import serializers
from api import models

class TrainerSerializer(serializers.ModelSerializer): 
    trainer_id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    alias = serializers.CharField()
    age = serializers.IntegerField()
    creation_date = serializers.DateTimeField(required=False)
    teams_quantity = serializers.IntegerField(required=False)

    class Meta: 
        model = models.TrainersDataT
        fields = ['trainer_id', 'name', 'alias', 'age', 'creation_date', 'teams_quantity']

class TeamSerializer(serializers.ModelSerializer): 
    team_id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    creation_date = serializers.DateTimeField(required=False)
    trainer = TrainerSerializer()
    members_quantity = serializers.IntegerField(required=False)

    class Meta: 
        model = models.TeamsDataT
        fields = ['team_id', 'name', 'creation_date', 'trainer', 'members_quantity']
        read_only_fields = ('trainer',)
        depth = 1

class TeamMemberSerializer(serializers.ModelSerializer): 
    member_id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    pokemon_id = serializers.IntegerField()
    url = serializers.CharField(required=False)
    teams = TeamSerializer(read_only=True) 

    class Meta:
        model = models.TeamMembersT
        fields = ['member_id', 'name', 'pokemon_id', 'url', 'teams']
        read_only_fields = ('teams', )
        depth = 2

class PostTeamMemberSerializer(serializers.Serializer): 
    pokemon_id = serializers.IntegerField()
    team_id = serializers.IntegerField()

class PostTeamSerializer(serializers.Serializer): 
    name = serializers.CharField()
    trainer_id = serializers.CharField()