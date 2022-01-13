from rest_framework.response import Response
from rest_framework.views import APIView

# from api import serializers
import json 

def error_output(message, values = []):
    return {
        'message':message, 
        'error': True, 
        'values': values
    }

def succes_output(message, values): 
    return {
        'message':message, 
        'error': False, 
        'values': values
    }

class Trainers(APIView): 
    ''' Pokemon trainers administration '''
    def get(self, request): 
        #retrieve members of a team

        #retrieve teams of a trainer

        #retrieve all trainers
        return Response()

    def post(self, request): 

        return Response()

    def put(self, request): 
        return Response()

    def delete(self, request): 
        
        return Response()

class Teams(APIView): 
    ''' Pokemon teams administration '''
    def get(self, request): 
        #retrieve members of a team

        #retrieve teams of a trainer

        #retrieve all trainers
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
        #retrieve members of a team

        #retrieve teams of a trainer

        #retrieve all trainers
        return Response()

    def post(self, request): 

        return Response()

    def put(self, request): 
        return Response()

    def delete(self, request): 
        
        return Response()