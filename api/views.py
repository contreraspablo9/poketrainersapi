from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination

# from api import serializers
import json 
from api import models, serializers

class Trainers(APIView, LimitOffsetPagination): 
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
        if pk is None and alias is None: 
            paginator = LimitOffsetPagination()
            results = paginator.paginate_queryset(trainer_data, request)
        else: 
            results = trainer_data
        trainer_data = serializers.TrainerSerializer(results, many=many).data
        return Response(trainer_data)

    def post(self, request, **kwargs): 
        serializer = serializers.TrainerSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            new_trainer = models.TrainersDataT(
                name=serializer.data['name'], 
                alias=serializer.data['alias'], 
                age=serializer.data['age']
            )
            new_trainer.save()
            new_trainer = serializers.TrainerSerializer(new_trainer).data
            return Response(new_trainer, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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