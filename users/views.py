from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *


@api_view(['POST'])
def registration(request):
    serializer = UserSerializer(data = request.data)
    if not serializer.is_valid():
        return Response({'status' : 403, 'errors' : serializer.errors, 'message' : 'something went wrong!'})
    else:
        serializer.save()
        return Response({'status' : 200, 'content' : request.data, 'message' : 'Registered successfully.'})
    
@api_view(['GET'])
def get_users_list(request):
    user_objs = User.objects.all()
    serializer = UserSerializer(user_objs, many = True)
    return Response({'status' : 200,'content' : serializer.data})

@api_view(['GET'])
def get_one_user(request,id):
    try:
        user_obj = User.objects.get(id = id)
        serializer = UserSerializer(user_obj)
        return Response({'status' : 200,'content' : serializer.data})
    except Exception as e:
        return Response({'status' : 403, 'message' : 'invalid id'})
    
@api_view(['patch'])
def update(request,id):
    try:
        user_obj = User.objects.get(id = id)
        serializer = UserSerializer(user_obj, data = request.data, partial = True)
        if not serializer.is_valid():
            return Response({'status' : 403, 'errors' : serializer.errors, 'message' : 'something went wrong!'})
        else:
            serializer.save()
            return Response({'status' : 200, 'content' : serializer.data, 'message' : 'Updated successfully.'})
    except Exception as e:
        return Response({'status' : 403, 'message' : 'invalid id'})
    
@api_view(['DELETE'])
def delete_account(request,id):
    try:
        user_obj = User.objects.get(id =id)
        user_obj.delete()
        return Response({'status' : 200, 'message' : 'deleted'})
    except Exception as e:
        return Response({'status' : 403, 'message' : 'invalid id'})
    
@api_view(['PATCH'])
def follow(request,id):
    try:
        user_obj = User.objects.get(id = id)
        user_obj.followers += 1
        user_obj.save()
        serializer = UserSerializer(user_obj, partial = True)
        return Response({'status' : 200, 'content' : serializer.data, 'message' : 'followed'})
    except Exception as e:
        return Response({'status' : 403, 'message' : 'invalid id'})
    
@api_view(['GET'])
def sort_by_followers(request):
    user_objs = User.objects.all().order_by('-followers')
    serializer = UserSerializer(user_objs, many = True)
    return Response({'status' : 200,'content' : serializer.data})


    
        
