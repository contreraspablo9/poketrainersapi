from requests import get
import json

def apicall(url): 
    response = get(url).json()
    return response
