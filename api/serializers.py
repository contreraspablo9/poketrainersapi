from rest_framework import serializers
from api import models

class TrainerSerializer(serializers.ModelSerializer): 
    ''' Serializer for trainer data, works when creating, retrieving, updating and deleting  '''
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
    ''' Serializer for team data, use only to retrieve '''
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
    ''' Serializer for members data, use only to retrieve '''
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
    ''' Serializer for members data, use to create and update '''
    pokemon_id = serializers.IntegerField()
    team_id = serializers.IntegerField()

class PostTeamSerializer(serializers.Serializer): 
    ''' Serializer for team data, use to create and update '''
    name = serializers.CharField()
    trainer_id = serializers.CharField()