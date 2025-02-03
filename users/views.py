from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password


@api_view(['POST'])
def registration(request):
    serializer = UserSerializer(data = request.data)
    if not serializer.is_valid():
        return Response({'status' : 403, 'errors' : serializer.errors, 'message' : 'something went wrong!'})
    else:
        serializer.save()
        return Response({'status' : 200, 'content' : request.data, 'message' : 'Registered successfully.'})

@api_view(['POST'])
def login(request):
    email = request.data.get('email_id')
    password = request.data.get('password')

    if not email or not password:
        return Response({'status': 400, 'message': 'Email and password are required'})

    try:
        user = User.objects.get(email_id=email)
    except User.DoesNotExist:
        return Response({'status': 404, 'message': 'User not found'})

    if not check_password(password, user.password):
        return Response({'status': 401, 'message': 'Invalid credentials'})

    refresh = RefreshToken.for_user(user)
    return Response({
        'status': 200,
        'message': 'Login successful',
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_list(request):
    user_objs = User.objects.all()
    serializer = UserSerializer(user_objs, many = True)
    return Response({'status' : 200,'content' : serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_one_user(request,name):
    print("hello world")
    print("Request Headers:", request.headers)
    try:
        user_obj = User.objects.get(name = name)
        serializer = UserSerializer(user_obj)
        return Response({'status' : 200,'content' : serializer.data})
    except Exception as e:
        print(e)
        return Response({'status' : 403, 'message' : 'user not found'})
    
@api_view(['patch'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def delete_account(request,id):
    try:
        user_obj = User.objects.get(id =id)
        user_obj.delete()
        return Response({'status' : 200, 'message' : 'deleted'})
    except Exception as e:
        return Response({'status' : 403, 'message' : 'invalid id'})
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def sort_by_followers(request):
    user_objs = User.objects.all().order_by('-followers')
    serializer = UserSerializer(user_objs, many = True)
    return Response({'status' : 200,'content' : serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_connection_request(request):
    sender_id = request.data.get('sender_id')
    receiver_id = request.data.get('receiver_id')

    if not sender_id or not receiver_id:
        return Response({'status' : 400, 'message' : "senderid and receiver id are required"})
    
    sender = get_object_or_404(User, id = sender_id)
    receiver = get_object_or_404(User, id = receiver_id)

    if sender == receiver:
        return Response({'status' : 400, 'message' : 'Cannot send request to yourself'})
    if sender in receiver.connection_requests.all():
        return Response({'status' : 400, 'message' : 'Request already sent'})
    if sender in receiver.connections.all():
        return Response({'status' : 400, 'message' : 'Already Connected'})
    
    receiver.connection_requests.add(sender)
    return Response({'status' : 200, 'message' : 'Request sent successfully'})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_connection_request(request):
    sender_id = request.data.get('sender_id')
    receiver_id = request.data.get('receiver_id')

    if not sender_id or not receiver_id:
        return Response({'status' : 400, 'message' : "senderid and receiver id are required"})
    
    sender = get_object_or_404(User, id = sender_id)
    receiver = get_object_or_404(User, id = receiver_id)

    if sender not in receiver.connection_requests.all():
        return Response({'status' : 400, 'message' : 'no pending requests from this user'})
    if sender in receiver.connections.all():
        return Response({'status' : 400, 'message' : 'Already Connected'})
    
    receiver.connection_requests.remove(sender)
    receiver.connections.add(sender)
    return Response({'status' : 200, 'message' : 'Connected'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_connection_request(request):
    sender_id = request.data.get('sender_id')
    receiver_id = request.data.get('receiver_id')

    if not sender_id or not receiver_id:
        return Response({'status' : 400, 'message' : "senderid and receiver id are required"})
    
    sender = get_object_or_404(User, id = sender_id)
    receiver = get_object_or_404(User, id = receiver_id)

    if sender not in receiver.connection_requests.all():
        return Response({'status' : 400, 'message' : 'no pending requests from this user'})
    if sender in receiver.connections.all():
        return Response({'status' : 400, 'message' : 'Already Connected'})
    
    receiver.connection_requests.remove(sender)
    return Response({'status' : 200})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_connection_requests(request,id):
    try:
        connection_request = User.objects.get(id = id).connection_requests.all().values('id')
        return Response({'status' : 200, 'content' : list(connection_request)})
    except Exception as e:
        return Response({'status' : 403, 'message' : 'user does not exist'})
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_connections(request,id):
    try:
        connections = User.objects.get(id = id).connections.all().values('id')
        print(connections)
        return Response({'status' : 200, 'content' : list(connections)})
    except Exception as e:
        return Response({'status' : 403, 'message' : 'user does not exist'})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def disconnect(request):
    sender_id = request.data.get('sender_id')
    receiver_id = request.data.get('receiver_id')

    if not sender_id or not receiver_id:
        return Response({'status' : 400, 'message' : "senderid and receiver id are required"})
    
    sender = get_object_or_404(User, id = sender_id)
    receiver = get_object_or_404(User, id = receiver_id)

    if sender not in receiver.connections.all():
        return Response({'status' : 400, 'message' : 'Already disconnected'})
    
    receiver.connection_requests.remove(sender)
    sender.connection_requests.remove(receiver)
    return Response({'status' : 200, 'message' : 'Disconnected'})



