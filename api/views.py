from rest_framework.response import Response
from rest_framework.views import APIView

# from api import serializers
import json 


class PokeTrainersApi(APIView): 
    ''' API para la administracion de entrenadores, equipos y pokemones '''

    