from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers
from cards.models import Set, Card


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ["id", "name", "color", "starred", "created_by", "last_visited"]
        # read_only_fields = ["id"]


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            "id",
            "name",
            "set",
            "starred",
            "question",
            "answer",
            "image_url",
            "created_by",
        ]
        # read_only_fields = ["id", "set"]
