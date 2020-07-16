from .viewsets import *
from rest_framework import routers
from django.urls import path, include
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register('feed', PhotoFeedViewSet)
router.register('activity', ActivityViewSet)
router.register('photos', PhotoViewSet)
router.register('users', UserViewSet)
# router.register('trash_collection', TrashCollectionViewSet)

urlpatterns = [
    path('auth/', views.obtain_auth_token, name='auth'),
    path('', include(router.urls))
]
