from django.contrib.auth import get_user_model
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from django.conf import settings

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny, )
        return super(UserViewSet, self).get_permissions()

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        # AUTHENTICATION 
        if settings.AUTHENTICATION_ENABLED:
            user = self.request.user
            if not user.is_superuser:
                queryset = get_user_model().objects.filter(username=user.username)
        return queryset

# class TrashCollectionViewSet(viewsets.ModelViewSet):
#     serializer_class = TrashCollectionSerializer
#     queryset = TrashCollection.objects.all()

class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()

class PhotoFeedViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()

class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()

    def get_queryset(self):
        queryset = Photo.objects.all()
        # AUTHENTICATION 
        if settings.AUTHENTICATION_ENABLED:
            user = self.request.user
            if not user.is_superuser:
                queryset = Photo.objects.filter(user=user)
        return queryset
