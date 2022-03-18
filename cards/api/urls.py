from django.urls import path, include

urlpatterns = [path("v1/", include("cards.api.v1.urls"))]
