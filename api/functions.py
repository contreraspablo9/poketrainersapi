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

def put(instance_str, response, status, rest_serializer, model, request, pk):
    def add_params(make_changes): 
        def inner(): 

            if pk is None: 
                return response(
                    {'details':f'Error, no {instance_str} id was provided. Please, add it at the end of the URL'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = rest_serializer(data=request.data)
            if serializer.is_valid(): 
                try: 
                    instance = model.objects.get(pk=pk)
                except model.DoesNotExist: 
                    return response(status=status.HTTP_404_NOT_FOUND)
                instance = make_changes(instance, serializer.data, rest_serializer)
                
                return response(
                    {'values':instance}, 
                    status=status.HTTP_202_ACCEPTED
                )
            return response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return inner
    return add_params