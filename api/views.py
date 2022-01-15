from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

import json 
from api import models, serializers
from django.db.models import Count

class Trainers(APIView): 
    ''' Pokemon trainers administration '''
    def get(self, request, pk=None, alias=None): 
        many = False
        if pk is not None: 
            try: 
                trainer_data = models.TrainersDataT.objects.get(pk=pk)
                trainer_data.teams_quantity = len(models.TeamsDataT.objects.filter(trainer_id=trainer_data.trainer_id))
                results = trainer_data
            except models.TrainersDataT.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif alias is not None: 
            try: 
                trainer_data = models.TrainersDataT.objects.get(alias=alias)
                trainer_data.teams_quantity = len(models.TeamsDataT.objects.filter(trainer_id=trainer_data.trainer_id))
                results = trainer_data
            except models.TrainersDataT.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND)
        else: 
            trainer_data = models.TrainersDataT.objects.all()
            results = trainer_data.annotate(teams_quantity=Count('teamsdatat__team_id')).order_by('trainer_id')
            many = True
        
        paginator = PageNumberPagination()
        if many:
            results = paginator.paginate_queryset(results, request)
        
        results = serializers.TrainerSerializer(results, many=many).data
        return Response(
            {
                'count':models.TrainersDataT.objects.count(),
                'next':paginator.get_next_link(),
                'previous':paginator.get_previous_link(),
                'values':results, 
            }
        )

    def post(self, request, **kwargs): 
        serializer = serializers.TrainerSerializer(data=request.data)
        if serializer.is_valid():
            #checamos que no sea un alias repetido:
            exist = models.TrainersDataT.objects.filter(alias=serializer.data['alias'])
            if len(exist) > 0: 
                return Response({'detail':f'Alias {serializer.data["alias"]} already exists, please try another one '}, status=status.HTTP_409_CONFLICT)
            new_trainer = models.TrainersDataT(
                name=serializer.data['name'], 
                alias=serializer.data['alias'], 
                age=serializer.data['age']
            )
            new_trainer.save()
            new_trainer = serializers.TrainerSerializer(new_trainer).data
            return Response(new_trainer, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):

        return Response()

    def delete(self, request, pk=None, alias=None): 
        print(request)
        return Response()

class Teams(APIView): 
    ''' Pokemon teams administration '''
    def get(self, request, pk=None): 
        many = False
        if pk is not None: 
            try: 
                teams_data = models.TeamsDataT.objects.get(pk=pk)
            except models.TeamsDataT.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND)
        else: 
            teams_data = models.TeamsDataT.objects.all().values()
            many = True
        if many: 
            paginator = PageNumberPagination()
            results = paginator.paginate_queryset(teams_data, request)
        else: 
            results = teams_data
        teams_data = serializers.TeamSerializer(results, many=many).data
        return Response(teams_data)

        

    def post(self, request, **kwargs): 
        serializer = serializers.TeamSerializer(data=request.data)
        if serializer.is_valid(): 
            #el trainer_id es valido? 
            trainer = models.TrainersDataT.objects.filter(pk=serializer.data['trainer_id'])
            if len(trainer) == 0: 
                return Response({'details':f"trainer with id: {serializer.data['trainer_id']} does not exist, please try with a valid trainer_id"}, status=status.HTTP_404_NOT_FOUND)
            new_team = models.TeamsDataT(
                name = serializer.data['name'],
                trainer_id=serializer.data['trainer_id']
            )
            new_team.save()
            new_team = serializers.TeamSerializer(new_team).data
            return Response(new_team, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request): 
        return Response()

    def delete(self, request): 
        
        return Response()

class TeamMembers(APIView): 
    ''' Pokemon team members administration '''
    def get(self, request, pk=None): 
        many = False
        if pk is not None: 
            try: 
                team_member = models.TeamMembersT.objects.get(pk=pk)
            except models.TeamMembersT.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            team_member = models.TeamMembersT.objects.all().values()
            many = True
        if many: 
            paginator = PageNumberPagination()
            results = paginator.paginate_queryset(team_member, request)
        else: 
            results = team_member
        team_member = serializers.TeamSerializer(results, many=many).data
        return Response(team_member)

    def post(self, request): 

        return Response()

    def put(self, request): 
        return Response()

    def delete(self, request): 
        
        return Response()