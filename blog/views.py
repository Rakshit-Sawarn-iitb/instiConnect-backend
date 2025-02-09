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
    data['username'] = request.user.id  # Attach the authenticated user

    serializer = blogSerializer(data=data)
    if not serializer.is_valid():
        return Response({'status': 400, 'errors': serializer.errors, 'message': 'Something went wrong'})

    serializer.save()
    return Response({'status': 200, 'message': 'Blog posted successfully'})

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
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_blog(request, id):
    try:
        blog_obj = Blog.objects.get(id=id)
        
        # Decrement the likes count
        if blog_obj.likes > 0:
            blog_obj.likes -= 1
            blog_obj.save()
        else:
            return Response({
                'user_no': 400,
                'content': 'Cannot have negative likes'
            })

        serializer = blogSerializer(blog_obj)

        return Response({
            'user_no': 200,
            'content': 'Blog unliked successfully',
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_one_blog_title(request, title):
    try:
        blog_objs = Blog.objects.get(title=title)
        serializer = blogSerializer(blog_objs)
        return Response({ 'user_no': 200, 'content': serializer.data })
    except Blog.DoesNotExist:
        return Response({ 'user_no': 404, 'content': 'Blog not found' })
    except Exception as e:
        print(e)
        return Response({ 'user_no': 403, 'content': 'Invalid request' })




from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Blog
from .serializers import blogSerializer

# Function to calculate cosine similarity between input text and blog content
def calculate_similarity(input_text, blog_texts):
    # Combine input text with blog texts for vectorization
    all_texts = [input_text] + blog_texts
    vectorizer = TfidfVectorizer(stop_words='english')  # Using TF-IDF and removing stopwords
    tfidf_matrix = vectorizer.fit_transform(all_texts)  # Create the tf-idf matrix

    # Calculate cosine similarity for input_text against each blog's text
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    return cosine_similarities

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_similar_blogs(request, input_text):
    try:
        # Fetch all blog objects from the database
        blogs = Blog.objects.all()
        
        # Extract blog content (assuming 'text' is the field holding the blog content)
        blog_texts = [blog.text for blog in blogs]

        # Calculate cosine similarities
        similarities = calculate_similarity(input_text, blog_texts)

        # Set a threshold for similarity (e.g., 0.7)
        threshold = 0.2
        similar_blogs = []

        # Loop through the cosine similarities and filter based on threshold
        for idx, sim in enumerate(similarities):
            if sim >= threshold:
                similar_blogs.append(blogs[idx])  # Append the blog whose similarity is above the threshold

        # Serialize the similar blogs
        serializer = blogSerializer(similar_blogs, many=True)
        
        if similar_blogs:
            return Response({'user_no': 200, 'content': serializer.data})
        else:
            return Response({'user_no': 404, 'content': 'No similar blogs found'})

    except Blog.DoesNotExist:
        return Response({'user_no': 404, 'content': 'Blog not found'})
    except Exception as e:
        print(e)
        return Response({'user_no': 403, 'content': 'Invalid request'})


