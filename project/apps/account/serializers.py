# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework import serializers

from account.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'full_name')

    def get_full_name(self, obj):
        return obj.get_full_name()


class NewProfileSerializer(serializers.ModelSerializer):
    user = serializers.Field(source='user.username')

    class Meta:
        model = UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    A serializer for ``UserProfile``.
    """
    user = UserSerializer(source='user')
    main_image = serializers.SerializerMethodField('get_main_image')
    thumbnail_image = serializers.SerializerMethodField('get_thumbnail_image')
    srv_followersCount = serializers.SerializerMethodField('srv_followers_count')
    srv_followingCount = serializers.SerializerMethodField('srv_following_count')
    srv_photosCount = serializers.SerializerMethodField('srv_photos_count')
    srv_following = serializers.SerializerMethodField('get_srv_following')

    class Meta(object):
        model = UserProfile

    def get_thumbnail_image(self, obj):
        if obj.thumbnail_image:
            return obj.thumbnail_image.url

    def get_main_image(self, obj):
        if obj.main_image:
            return obj.main_image.url

    def srv_followers_count(self, obj):
        return obj.followed.count()

    def srv_following_count(self, obj):
        return obj.followed_profiles.count() + obj.followed_events.count()

    def srv_photos_count(self, obj):
        return obj.profile_images.count()

    def get_srv_following(self, obj):
        view = self.context['view']
        user = view.request.user
        try:
            if user.profile.followed_profiles.filter(id=obj.id).count():
                return True
        except:
            pass
        return False


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()