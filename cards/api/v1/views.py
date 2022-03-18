from functools import partial
from os import name
from django.http import response
from rest_framework import serializers, views, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from cards.api.v1.serializers import CardSerializer, SetSerializer
from cards.models import Card, Set
import datetime


class SetAPIView(views.APIView):
    """
    API view for Sets
    """

    serializer_class = SetSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        if pk:
            try:
                set_instance = Set.objects.get(id=pk)
                serializer = SetSerializer(set_instance)
                response = {"success": True, "data": serializer.data}
            except:
                response = {
                    "success": "False",
                    "message": "Data invalid. Operation unsuccesful",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            set_instance = Set.objects.filter(created_by=request.user)
            serializer = SetSerializer(set_instance, many=True)
            response = {"success": True, "data": serializer.data}

        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data["created_by"] = request.user.id
        data["last_visited"] = datetime.datetime.now()
        serializer = self.serializer_class(data=data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {"success": True, "message": "Set added successfully"}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {
                "success": "False",
                "message": "Data invalid. Operation unsuccesful",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        data = request.data
        try:
            set_instance = Set.objects.get(id=pk)
            set_instance.last_visited = datetime.datetime.now()
            serializer = SetSerializer(set_instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {"success": True, "message": "Set updated successfully"}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {
                "success": "False",
                "message": "Invalid set. Operation unsuccesful",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            set_instance = Set.objects.get(id=pk)
            set_instance.delete()
            response = {"success": True, "message": "Set deleted successfully"}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {
                "success": "False",
                "message": "Invalid set. Operation unsuccesful",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CardAPIView(views.APIView):
    """
    API view for Card Model
    """

    serializer_class = CardSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        if pk:
            try:
                card_instance = Card.objects.get(id=pk, created_by=request.user)
                serializer = CardSerializer(card_instance)
                response = {"success": True, "data": serializer.data}
            except:
                response = {
                    "success": "False",
                    "message": "Card not present. Operation unsuccessful",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            set_instance = Set.objects.get(
                created_by=request.user, id=request.query_params["set_id"]
            )
            card = Card.objects.filter(set=set_instance, created_by=request.user)
            serializer = CardSerializer(card, many=True)
            response = {"success": True, "data": serializer.data}

        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data["created_by"] = request.user.id
        serializer = self.serializer_class(data=data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {"success": True, "message": "Card added successfully"}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {
                "success": "False",
                "message": "Data invalid. Operation unsuccesful",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        data = request.data
        try:
            card_instance = Card.objects.get(id=pk, created_by=request.user)
            serializer = SetSerializer(card_instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {"success": True, "message": "Card updated successfully"}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {
                "success": "False",
                "message": "Invalid card. Operation unsuccesful",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            card_instance = Card.objects.get(id=pk, created_by=request.user)
            card_instance.delete()
            response = {"success": True, "message": "Card deleted successfully"}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {
                "success": "False",
                "message": "Card not found. Operation unsuccessful",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
