from rest_framework import serializers

class TrainerSerializer(serializers.Serializer): 
    trainer_id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    alias = serializers.CharField()
    age = serializers.IntegerField()
    creation_date = serializers.DateTimeField(required=False)
    teams_quantity = serializers.IntegerField(required=False)

class TeamSerializer(serializers.Serializer): 
    team_id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    creation_date = serializers.DateTimeField(required=False)
    trainer_id = serializers.IntegerField()