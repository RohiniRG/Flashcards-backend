from django.urls import path, include
from rest_framework import routers
from .views import CardAPIView, SetAPIView
from rest_framework.urlpatterns import format_suffix_patterns

# router = routers.SimpleRouter(trailing_slash=False)
# router.register("set", SetViewset, basename="set")

urlpatterns = [
    path("set/", SetAPIView.as_view(), name="set"),
    path("set/<uuid:pk>/", SetAPIView.as_view(), name="set"),
    path("card/", CardAPIView.as_view(), name="card"),
    path("card/<uuid:pk>/", CardAPIView.as_view(), name="card"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
