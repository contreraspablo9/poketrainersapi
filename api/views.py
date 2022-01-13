from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# from api import serializers
import json 
from api import models, serializers

class Trainers(APIView): 
    ''' Pokemon trainers administration '''
    def get(self, request, pk=None, alias=None): 
        many = False
        if pk is not None: 
            try: 
                trainer_data = models.TrainersDataT.objects.get(pk=pk)
            except models.TrainersDataT.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif alias is not None: 
            try: 
                trainer_data = models.TrainersDataT.objects.get(alias=alias)
            except models.TrainersDataT.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND)
        else: 
            trainer_data = models.TrainersDataT.objects.all().values()
            many = True

        trainer_data = serializers.TrainerSerializer(trainer_data, many=many).data
        return Response(trainer_data)

    def post(self, request): 

        return Response()

    def put(self, request):

        return Response()

    def delete(self, request): 
        
        return Response()

class Teams(APIView): 
    ''' Pokemon teams administration '''
    def get(self, request): 
        
        return Response()

    def post(self, request): 

        return Response()

    def put(self, request): 
        return Response()

    def delete(self, request): 
        
        return Response()

class TeamMembers(APIView): 
    ''' Pokemon team members administration '''
    def get(self, request): 
        
        return Response()

    def post(self, request): 

        return Response()

    def put(self, request): 
        return Response()

    def delete(self, request): 
        
        return Response()