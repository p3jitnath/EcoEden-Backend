from django.conf import settings
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        password = serializers.CharField(write_only=True)
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'password',
            'email',
            'score',
            'mobile',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)

class TrashCollectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TrashCollection
        fields = ('id', 'uploader', 'uploaded_at', 'collector', 'verified', 'verified_at')
    
    def update(self, instance, validated_data):
        verified = validated_data['verified']
        uploader = validated_data['uploader']
        collector = validated_data['collector']
        if validated_data['verified'] == True:
            uploader.score = uploader.score + settings.SCORE_CREDIT
            uploader.save()
            collector.score = collector.score + settings.SCORE_CREDIT
            collector.save()
        return super(TrashCollectionSerializer, self).update(instance, validated_data)


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'image', 'created_at', 'trash', 'user', 'lat', 'lng', 'description')