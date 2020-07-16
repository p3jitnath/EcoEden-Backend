from django.db import IntegrityError
from django.conf import settings
from rest_framework import serializers
from .models import *

from datetime import datetime

class UserSerializer(serializers.ModelSerializer):

    def to_representation(self, obj):
        data = super().to_representation(obj)
        user = email = mobile = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            email, mobile = (obj.email, obj.mobile) if user.id == obj.pk else (None, None)
        if email and mobile:
            data['email']  = email
            data['mobile'] = mobile
        return data

    class Meta:
        model = User
        password = serializers.CharField(write_only=True)
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'password',
            'score'
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

# class TrashCollectionSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = TrashCollection
#         fields = ('id', 'uploader', 'uploaded_at', 'photo', 'collector', 'verified', 'verified_at')
    
#     def update(self, instance, validated_data):
#         verified = validated_data['verified']
#         uploader = validated_data['uploader']
#         collector = validated_data['collector']
#         if validated_data['verified'] == True:
#             uploader.score = uploader.score + settings.SCORE_CREDIT
#             uploader.save()
#             collector.score = collector.score + settings.SCORE_CREDIT
#             collector.save()
#         return super(TrashCollectionSerializer, self).update(instance, validated_data)

class ActivitySerializer(serializers.HyperlinkedModelSerializer):

    def to_representation(self, obj):
        output = super().to_representation(obj)
        if obj.updated_at:
            output['updated_at'] = obj.updated_at
        return output

    class Meta:
        model = Activity
        fields = ('id', 'created_at', 'user', 'photo', 'vote')

    def create(self, validated_data):
        photo = validated_data['photo']
        vote = validated_data['vote']
        if (vote > 0):
            photo.upvotes += 1
        elif (vote < 0):
            photo.downvotes += 1 
        photo.save()
        return super(ActivitySerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        photo = validated_data['photo']
        new_vote = validated_data['vote']
        old_vote = instance.vote
        
        if new_vote == 0 : 
            if old_vote < 0:
                photo.downvotes -= 1
            elif old_vote > 0:
                photo.upvotes -= 1
        elif new_vote > 0 : 
            if old_vote < 0:
                photo.downvotes -= 1
                photo.upvotes += 1
            elif old_vote == 0:
                photo.upvotes += 1
        elif new_vote < 0 : 
            if old_vote > 0:
                photo.upvotes -= 1
                photo.downvotes += 1
            elif old_vote == 0:
                photo.downvotes += 1

        photo.save()
        validated_data['updated_at'] = datetime.now()
        return super(ActivitySerializer, self).update(instance, validated_data)

class PhotoSerializer(serializers.HyperlinkedModelSerializer):

    def to_representation(self, obj):
        output = super().to_representation(obj)
        output['user'] = UserSerializer(obj.user).data

        request = self.context.get("request")
        if request.user.is_authenticated:
            user = request.user
            objects = ActivitySerializer(Activity.objects.filter(user=user, photo=obj), many=True, context={'request':request}).data
            if objects is not None:
                output['activity'] = objects

        return output

    class Meta:
        model = Photo
        fields = ('id', 'image', 'user', 'created_at', 'trash', 'lat', 'lng', 'description', 
                  'upvotes', 'downvotes')