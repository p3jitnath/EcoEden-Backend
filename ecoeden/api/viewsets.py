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

class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()

class PhotoFeedViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.filter(visible=True)
    http_method_names = ['get']

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

from rest_framework.pagination import PageNumberPagination

class LeaderboardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

class LeaderboardViewSet(viewsets.ModelViewSet):
    pagination_class = LeaderboardPagination
    queryset = get_user_model().objects.order_by('-score', '-collections', '-posts', '-verifications', 'first_name')
    serializer_class = UserSerializer
    http_method_names = ['get']

class TrashCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = TrashCollectionSerializer
    queryset = TrashCollection.objects.all()

class TrashCollectionActivityViewSet(viewsets.ModelViewSet):
    serializer_class = TrashCollectionActivitySerializer
    queryset = TrashCollectionActivity.objects.all()