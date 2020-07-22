from .viewsets import *
from rest_framework import routers
from django.urls import path, include

from api import views

router = routers.DefaultRouter()

router.register('photos', PhotoViewSet, basename='photo')
router.register('users', UserViewSet)

router.register('feed', PhotoFeedViewSet, basename='feed')
router.register('activity', ActivityViewSet)
router.register('leaderboard', LeaderboardViewSet, basename='leaderboard')

router.register('trash_collection', TrashCollectionViewSet)
router.register('trash_collection_activity', TrashCollectionActivityViewSet)

urlpatterns = [
    path('auth/', views.obtain_expiring_auth_token, name='auth'),
    path('', include(router.urls))
]