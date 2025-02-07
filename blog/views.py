from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_many_blog(request):
    blog_objs = Blog.objects.all()
    serializer = blogSerializer(blog_objs , many = True)
    return Response({ 'user_no' : 200 , 'content' : serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_one_blog(request , id):
    try:

        blog_objs = Blog.objects.get(id = id)
        serializer = blogSerializer(blog_objs )
        return Response({ 'user_no' : 200 , 'content' : serializer.data})

    except Exception as e:
        print(e)
        return Response({ 'user_no' : 403 , 'content' : 'invalid id'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def delete_blog(request , id):
    try:

        blog_objs = Blog.objects.get(id = id)
        blog_objs.delete()
        return Response({ 'user_no' : 200 , 'content' : 'deleted'})
    except Exception as e:
        print(e)
        return Response({ 'user_no' : 403 , 'content' : 'invalid id'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
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


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_blog(request , id):
    try:

        blog_obj = Blog.objects.get(id=id)
        serializer = blogSerializer(blog_obj, data=request.data, partial=True)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({ 'user_no' : 200 ,'errors' : serializer.errors , 'content' : 'something went wrong'})
        serializer.save()
        return Response({ 'user_no' : 200 , 'content' : serializer.data})
    except Exception as e:
        print(e)
        return Response({ 'user_no' : 403 , 'content' : 'invalid id'})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sort_by_like(request):
    sort_by = request.query_params.get('sort_by', 'likes')

    blog_objs = Blog.objects.all().order_by('-likes')  # Descending order by likes

    serializer = blogSerializer(blog_objs, many=True)

    return Response({'user_no': 200, 'content': serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sort_by_date(request):
    sort_by = request.query_params.get('sort_by', 'likes')

    blog_objs = Blog.objects.all().order_by('-date')  # Ascending order by data

    serializer = blogSerializer(blog_objs, many=True)

    return Response({'user_no': 200, 'content': serializer.data})