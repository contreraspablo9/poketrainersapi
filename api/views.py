from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

import json 
from api import models, serializers
from django.db.models import Count, Value, functions, TextField

from api import functions as fn

class Trainers(APIView, PageNumberPagination): 
    ''' Pokemon trainers administration '''
    def get(self, request, pk=None, alias=None): 
        if pk is not None: 
            try: 
                trainer_data = models.TrainersDataT.objects.get(pk=pk)
                trainer_data.teams_quantity = models.TeamsDataT.objects.filter(trainer_id=trainer_data.trainer_id).count()
                results = [trainer_data]
            except models.TrainersDataT.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif alias is not None: 
            try: 
                trainer_data = models.TrainersDataT.objects.get(alias=alias)
                trainer_data.teams_quantity = models.TeamsDataT.objects.filter(trainer_id=trainer_data.trainer_id).count()
                results = [trainer_data]
            except models.TrainersDataT.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND)
        else: 
            trainer_data = models.TrainersDataT.objects.all()
            results = trainer_data.annotate(teams_quantity=Count('teams__team_id')).order_by('trainer_id')
        
        results = self.paginate_queryset(results, request)
        results = serializers.TrainerSerializer(results, many=True).data
        return Response(
            {
                'count':self.page.paginator.count,
                'next':self.get_next_link(),
                'previous':self.get_previous_link(),
                'values':results, 
            }, 
            status=status.HTTP_200_OK
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
            return Response(
                {
                    'values':new_trainer
                }, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):

        return Response()

    def delete(self, request, pk=None, alias=None): 
        print(request)
        return Response()

class Teams(APIView, PageNumberPagination): 
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

class TeamMembers(APIView,PageNumberPagination): 
    ''' Pokemon team members administration '''
    def get(self, request, pk=None, name=None): 
        pokeapi_url = 'https://pokeapi.co/api/v2/pokemon/'
        pokemon_data = fn.apicall(pokeapi_url + '?limit=1200')['results']

        if pk is not None: 
            try: 
                member_data = models.TeamMembersT.objects.get(pk=pk)
                # member_data.name = pokemon_data[member_data.pokemon_id - 1]['name']
                # member_data.url = pokeapi_url + str(member_data.pokemon_id)
                results = [member_data]
            except models.TeamMembersT.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND)
        else: 
            member_data = models.TeamMembersT.objects.all().order_by('member_id')
            results = member_data.annotate(url = functions.Concat(Value(pokeapi_url), 'pokemon_id', output_field=TextField()))
        
        for index in range(len(results)): 
            results[index].name = pokemon_data[index]['name']
            results[index].url = pokemon_data[index]['url']


        results = self.paginate_queryset(results, request)
        results = serializers.TeamMemberSerializer(results, many=True).data
        return Response(
            {
                'count':self.page.paginator.count, 
                'next':self.get_next_link(), 
                'previous': self.get_previous_link(), 
                'values': results
            }, 
            status=status.HTTP_200_OK
        )

    def post(self, request, **kwargs): 
        serializer = serializers.TeamMemberSerializer(data=request.data)
        if serializer.is_valid(): 
            print("llegamos hasta aca")
            new_member = models.TeamMembersT(
                pokemon_id=serializer.data['pokemon_id'], 
                team_id=models.TeamsDataT.objects.get(pk=serializer.data['team_id']).team_id
            )
            new_member.save()
            new_member = serializers.TeamMemberSerializer([new_member]).data
            return Response(
                {
                    'values':new_member
                }, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request): 
        return Response()

    def delete(self, request): 
        
        return Response()