from rest_framework import serializers
from api import models

class TrainerSerializer(serializers.Serializer): 
    trainer_id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    alias = serializers.CharField()
    age = serializers.IntegerField()
    creation_date = serializers.DateTimeField(required=False)
    teams_quantity = serializers.IntegerField(required=False)

class TeamSerializer(serializers.ModelSerializer): 
    team_id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    creation_date = serializers.DateTimeField(required=False)
    trainer_id = serializers.IntegerField()

    class Meta: 
        model = models.TeamsDataT
        fields = ['team_id', 'name', 'creation_date', 'trainer_id']

class TeamMemberSerializer(serializers.ModelSerializer): 
    member_id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    pokemon_id = serializers.IntegerField()
    url = serializers.CharField(required=False)
    teams = TeamSerializer() 


    class Meta:
        model = models.TeamMembersT
        fields = ['member_id', 'name', 'pokemon_id', 'teams', 'url']
