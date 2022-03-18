from django.http import response
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authtoken.models import Token
from users.api import serializers
from users.api.serializers import registerSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer


@api_view(["POST"])
def register_user(request):
    """
    Response object for the api is created if the data obtained serializers is successfully validated
    """
    serializer = registerSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        data["response"] = "User registered successfully!"
        data["email"] = user.email
        data["username"] = user.username
        token = Token.objects.get(user=user).key
        data["token"] = token
        response = {"success": True, "data": data}
    else:
        data = serializer.errors
        response = {"success": "False", "data": data}

    return Response(response, status=status.HTTP_200_OK)


@api_view(["POST"])
def login_user(request):
    """
    Modifying the obtain_auth_token method present in rest_framework.authtoken.views to create a custom response
    """
    serializer_class = AuthTokenSerializer
    serializer = serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]
    token, created = Token.objects.get_or_create(user=user)
    response = {"success": True, "token": token.key}
    return Response(response, status=status.HTTP_200_OK)


@api_view(["POST"])
def logout_user(request):
    request.user.token.delete()
    return Response("User Logged out successfully")
