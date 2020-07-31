from django.db import IntegrityError
from django.conf import settings
from rest_framework import serializers
from .models import *

from datetime import datetime
from .utils import update_score, update_user_score, update_trash_collection_object

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
        else:
            del data['email']
            del data['mobile']
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
            'mobile',
            'email',
            'score',
            'collections',
            'posts',
            'verifications'
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

class BaseActivitySerializer(serializers.HyperlinkedModelSerializer):

    def get_obj_str(self):
        return None
    
    def to_representation(self, obj):
        output = super().to_representation(obj)
        if obj.updated_at:
            output['updated_at'] = obj.updated_at
        return output

    class Meta:
        fields = ('id', 'created_at', 'user', 'vote')
    
    def create(self, validated_data):
        obj = validated_data[self.get_obj_str()]
        vote = validated_data['vote']

        if (vote > 0):
            obj.upvotes += 1
        elif (vote < 0):
            obj.downvotes += 1 
        obj.save()

        user = update_user_score(validated_data['user'], verify=True)
        user.save()

        return super(BaseActivitySerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        try: 
            obj = validated_data[self.get_obj_str()] 
        except: 
            obj = getattr(instance, self.get_obj_str())

        new_vote = validated_data['vote']
        old_vote = instance.vote
        
        obj = update_score(new_vote, old_vote, obj)
        obj.save()
        validated_data['updated_at'] = datetime.now()
        return super(BaseActivitySerializer, self).update(instance, validated_data)

class ActivitySerializer(BaseActivitySerializer):
    
    class Meta:
        model = Activity
        fields = BaseActivitySerializer.Meta.fields + ('photo', )

    def get_obj_str(self):
        return 'photo'

class TrashCollectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TrashCollection
        fields = ('id', 'photo', 'collector', 'collected_at', 'upvotes', 'downvotes', 'visible')

class TrashCollectionActivitySerializer(BaseActivitySerializer):
    class Meta:
        model = TrashCollectionActivity
        fields = BaseActivitySerializer.Meta.fields + ('trash_collection', )

    def get_obj_str(self):
        return 'trash_collection'  

    def create(self, validated_data):
        obj = validated_data['trash_collection']
        obj = update_trash_collection_object(obj)        
        obj.save()

        return super(TrashCollectionActivitySerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        obj = instance.trash_collection
        obj = update_trash_collection_object(obj)        
        obj.save()

        return super(TrashCollectionActivitySerializer, self).update(instance, validated_data)

class PhotoSerializer(serializers.HyperlinkedModelSerializer):

    def to_representation(self, obj):
        output = super().to_representation(obj)
        output['user'] = UserSerializer(obj.user).data

        request = self.context.get("request")
        if request.user.is_authenticated:
            user = request.user
                
            activity = ActivitySerializer(Activity.objects.filter(user=user, photo=obj), many=True, context={'request':request}).data
            output['activity'] = activity

            try:
                trash_collection_obj = TrashCollection.objects.get(photo=obj, visible=True)
                trash_collection = TrashCollectionSerializer(trash_collection_obj, context={'request':request}).data
                trash_collection_activity = TrashCollectionActivitySerializer(TrashCollectionActivity.objects.filter(user=user, trash_collection=trash_collection_obj), many=True, context={'request':request}).data
            except:
                trash_collection = {}

            output['trash_collection'] = trash_collection
            if len(trash_collection) > 0: 
                output['trash_collection']['activity'] = trash_collection_activity

        return output

    class Meta:
        model = Photo
        fields = ('id', 'image', 'user', 'created_at', 'trash', 'lat', 'lng', 'description', 
                  'upvotes', 'downvotes', 'visible')

    def create(self, validated_data):
        user = update_user_score(validated_data['user'], post=True)
        user.save()
        
        # validated_data['visible'] = True
        
        return super(PhotoSerializer, self).create(validated_data)