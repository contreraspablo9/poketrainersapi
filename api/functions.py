from requests import get
import json

def apicall(url): 
    response = get(url).json()
    return response

def delete(model_str, model, response, serializer, status, pk=None): 
    if pk is None: 
        return response(
            {
                f'values':f'Error, no {model_str} id was provided, please add it at the end of the URL'
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        instance = model.objects.get(pk=pk)
    except model.DoesNotExist:
        return response({'details':f'The {model_str} with id: {pk} does not exist'},status=status.HTTP_404_NOT_FOUND)

    instance.delete()
    instance = serializer(instance).data
    return response({'values':instance}, status=status.HTTP_202_ACCEPTED)