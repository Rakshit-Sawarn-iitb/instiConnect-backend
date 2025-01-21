from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *


@api_view(['GET'])
def get_many_blog(request):
    blog_objs = Blog.objects.all()
    serializer = blogSerializer(blog_objs , many = True)
    return Response({ 'user_no' : 200 , 'content' : serializer.data})

@api_view(['GET'])
def get_one_blog(request , id):
    try:

        blog_objs = Blog.objects.get(id = id)
        serializer = blogSerializer(blog_objs , many = True)
        return Response({ 'user_no' : 200 , 'content' : serializer.data})

    except Exception as e:
        print(e)
        return Response({ 'user_no' : 403 , 'content' : 'invalid id'})


@api_view(['POST'])
def post_blog(request):
    data = request.data
    print(data)
    serializer = blogSerializer(data = request.data)
    if not serializer.is_valid():
        print(serializer.errors)
        return Response({ 'user_no' : 200 ,'errors' : serializer.errors , 'content' : 'something went wrong'})
    serializer.save()
    return Response({ 'user_no' : 200 , 'content' : data})

@api_view(['DELETE'])
def delete_blog(request , id):
    try:

        blog_objs = Blog.objects.get(id = id)
        blog_objs.delete()
        return Response({ 'user_no' : 200 , 'content' : 'deleted'})
    except Exception as e:
        print(e)
        return Response({ 'user_no' : 403 , 'content' : 'invalid id'})


@api_view(['POST'])
def like_blog(request, id):
    try:

        blog_obj = Blog.objects.get(id=id)
        
        # Increment the likes count
        blog_obj.likes += 1
        blog_obj.save()

        serializer = blogSerializer(blog_obj)

        return Response({
            'user_no': 200,
            'content': 'Blog liked successfully',
            'likes': blog_obj.likes,
            'blog': serializer.data
        })
    except Blog.DoesNotExist:
        return Response({
            'user_no': 404,
            'content': 'Blog not found'
        })
    except Exception as e:
        print(e)
        return Response({
            'user_no': 500,
            'content': 'Something went wrong'
        })


