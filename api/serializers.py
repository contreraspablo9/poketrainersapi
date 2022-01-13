from rest_framework import serializers

class TrainerSerializer(serializers.Serializer): 
    trainer_id = serializers.IntegerField()
    name = serializers.CharField()
    alias = serializers.CharField()
    age = serializers.IntegerField()
    creation_date = serializers.DateTimeField()