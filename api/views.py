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

    def put(self, request, pk=None, **kwargs): 
        @fn.put('trainer', Response, status, serializers.TrainerSerializer, models.TrainersDataT, request, pk)
        def modify_trainer(trainer, data, serializer): 
            trainer.name = data['name']
            trainer.alias = data['alias']
            trainer.age = data['age']
            trainer.save()
            trainer = serializer(trainer).data
            return trainer

        return modify_trainer()
   
    def delete  (self, request, pk=None, **kwargs):
        return fn.delete('trainer', models.TrainersDataT, Response, serializers.TrainerSerializer, status, pk)


class Teams(APIView, PageNumberPagination): 
    ''' Pokemon teams administration '''
    def get(self, request, pk=None): 
        if pk is not None: 
            try: 
                team_data = models.TeamsDataT.objects.get(pk=pk)
                results = [team_data]
            except models.TeamsDataT.DoesNotExist: 
                return Response(status = status.HTTP_404_NOT_FOUND)
        else: 
            team_data = models.TeamsDataT.objects.all()
            results = team_data

        for index in range(len(results)): 
            results[index].members_quantity = models.TeamMembersT.objects.filter(teams=results[index]).count()
            print(results[index].members_quantity)
        results = self.paginate_queryset(results, request)
        results = serializers.TeamSerializer(results, many=True).data
        return Response(
            {
                'count':self.page.paginator.count, 
                'next':self.get_next_link(), 
                'previous':self.get_previous_link(), 
                'values':results
            }, 
            status=status.HTTP_200_OK
        )
        

    def post(self, request, **kwargs): 
        serializer = serializers.PostTeamSerializer(data=request.data)
        if serializer.is_valid(): 
            new_team = models.TeamsDataT(
                name = serializer.data['name'], 
                trainer = models.TrainersDataT.objects.get(pk=serializer.data['trainer_id'])
            )
            new_team.save()
            new_team = serializers.TeamSerializer(new_team).data
            return Response(
                {'values':new_team},
                status = status.HTTP_201_CREATED
            )
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None, **kwargs): 
        @fn.put('team', Response, status, serializers.PostTeamSerializer, models.TeamsDataT, request, pk)
        def modify_team(team, data, serializer): 
            team.name = data['name']
            team.trainer_id = data['trainer_id']
            team.save()
            team = serializer(team).data
            return team

        return modify_team()

    def delete  (self, request, pk=None, **kwargs):
        return fn.delete('team', models.TeamsDataT, Response, serializers.TeamSerializer, status, pk)

class TeamMembers(APIView,PageNumberPagination): 
    ''' Pokemon team members administration '''
    pokeapi_url = 'https://pokeapi.co/api/v2/pokemon/'
    def get(self, request, pk=None, name=None): 
        pokemon_data = fn.apicall(self.pokeapi_url + '?limit=1200')['results']

        if pk is not None: 
            try: 
                member_data = models.TeamMembersT.objects.get(pk=pk)
                results = [member_data]
            except models.TeamMembersT.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND)
        else: 
            results = models.TeamMembersT.objects.all().order_by('member_id')
        
        for index in range(len(results)): 
            results[index].name = pokemon_data[results[index].pokemon_id - 1]['name']
            results[index].url = pokemon_data[results[index].pokemon_id -1]['url']


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
        serializer = serializers.PostTeamMemberSerializer(data=request.data)
        if serializer.is_valid(): 
            try: 
                team_instance = models.TeamsDataT.objects.get(pk=serializer.data['team_id'])
            except models.TeamsDataT.DoesNotExist:
                return Response({'details':f"Error, the team with id {serializer.data['team_id']} does not exist"},status=status.HTTP_404_NOT_FOUND)
            pokemon_data = fn.apicall(self.pokeapi_url + '?limit=3000')['results']
            if serializer.data['pokemon_id'] > len(pokemon_data) - 1:
                return Response({'details':f"Error, pokemon with id {serializer.data['pokemon_id']} does not exist"},status=status.HTTP_404_NOT_FOUND)

            team_members = models.TeamMembersT.objects.filter(teams=team_instance).count()
            if team_members >= 6:
                return Response({'detail':f"Team {team_instance.name} has reached maximum members limit"}, status=status.HTTP_401_UNAUTHORIZED)
            new_member = models.TeamMembersT(
                pokemon_id=serializer.data['pokemon_id'], 
                teams=team_instance
            )
            new_member.save()
            new_member.name = pokemon_data[new_member.pokemon_id - 1]['name']
            new_member.url = self.pokeapi_url + str(new_member.pokemon_id)

            new_member = serializers.TeamMemberSerializer(new_member).data
            return Response(
                {'values':new_member}, 
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, **kwargs): 
        @fn.put('member', Response, status, serializers.PostTeamMemberSerializer, models.TeamMembersT, request, pk)
        def modify_team(member, data, serializer): 
            member.pokemon_id = data['pokemon_id']
            member.team_id = data['team_id']
            member.save()
            member = serializer(member).data
            return member

        return modify_team()

    def delete  (self, request, pk=None, **kwargs):
        return fn.delete('member', models.TeamMembersT, Response, serializers.TeamMemberSerializer, status, pk)