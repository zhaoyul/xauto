# -*- coding: utf-8 -*-
import uuid
from datetime import datetime
from random import randrange
from hashlib import sha1

#from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import (login as auth_login, logout, authenticate)
from django.template.loader import render_to_string
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.files.base import ContentFile

from rest_framework.generics import (ListAPIView, RetrieveAPIView)
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated

from event.models import Event, EventDate, EventImage
from event.serializers import (EventSerializer, EventDetailsSerializer,
    EventModelSerializer, EventDateSerializer, AlbumSerializer)
from account.serializers import (UserProfileSerializer, UserSerializer,
    NewProfileSerializer, EmailSerializer)
from account.models import UserProfile
from multiuploader.serializers import MultiuploaderImageSerializer
from multiuploader.models import MultiuploaderImage

from django.core.mail import send_mail

class EventsListView(ListAPIView):
    """
    Returns Event list
    """
    permission_classes = (AllowAny,)
    serializer_class = EventSerializer

    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        queryset = Event.objects.filter(title__startswith=search_text)
        own_events = self.request.GET.get('own_events', False)
        if own_events == 'true':
            queryset = queryset.filter(author=self.request.user.profile)
        return queryset


class EventDetailsView(RetrieveAPIView):
    """
    Returns Event details
    """
    permission_classes = (AllowAny,)
    serializer_class = EventDetailsSerializer
    model = Event
    lookup_field = 'slug'


class AlbumPhotosUploader(APIView):
    """
    Creates multiple instances of images
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        profile = self.request.user.profile
        i = 0
        for index, photo in enumerate(self.request.DATA):
            imageObj = MultiuploaderImage()
            imageObj.image.save(
                photo['name'],
                ContentFile(photo['file'].decode('base64')),
                save=False
            )
            imageObj.userprofile = profile
            event_date = photo.get('event_date', None)
            if event_date:
                imageObj.event_date = EventDate.objects.get(id=event_date)
            imageObj.save()
            i += 1

        return Response({}, status=status.HTTP_200_OK)


class EventViewSet(ModelViewSet):
    """
    Returns Event CRUD methods
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = EventModelSerializer
    model = Event
    lookup_field = 'slug'

    def pre_save(self, obj):
        if not obj.author:
            obj.author = self.request.user.profile

        main_image = self.request.DATA.get('main_image_obj', {})
        if main_image:
            imageObj = EventImage()
            imageObj.image.save(
                main_image['name'],
                ContentFile(main_image['file'].decode('base64'))
            )
            obj.main_image = imageObj

'''
class EventEditView2(APIView):
    serializer_class = EventModelSerializer
    model = Event

    def post(self, request, *args, **kwargs):
        event = EventModelSerializer(data=request.DATA)
        event_image = EventImageSerializer(data=request.DATA,
                                           files=request.FILES)
        print "???"
        print request.FILES
        if event.is_valid() and event_image.is_valid():
            event_image_object = event_image.save(force_insert=True)
            user = self.request.user
            event.object.author = user.profile
            event.object.main_image = event_image_object
            event.save(force_insert=True)
            return Response(event.data, status=status.HTTP_201_CREATED)

        errors = event.errors
        errors.update(event_image.errors)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
'''


class EventDateViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventDateSerializer
    model = EventDate


class FollowEventView(APIView):
    """
    Adding current user as follower of event
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request, slug, *args, **kwargs):
        user = request.user
        event = Event.objects.get(slug=slug)
        srv_following = False
        try:
            if user.profile.followed_events.filter(slug=slug).count():
                user.profile.followed_events.remove(event)
            else:
                user.profile.followed_events.add(event)
                srv_following = True

            data = {
                'srv_followersCount': event.followed.count(),
                'srv_following': srv_following
            }

            return Response(data, status=status.HTTP_200_OK)
        except:
            pass
        return Response({}, status=status.HTTP_403_FORBIDDEN)


class CheckShortLinkView(APIView):
    """
    Checks database to determine availability of short link.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        search_text = self.request.GET.get('search_text', '')
        data = {'response': 'Available'}
        if Event.objects.filter(short_link=search_text).count():
            data = {'response': 'Unavailable'}

        return Response(data, status=status.HTTP_200_OK)


class CheckUsernameView(APIView):
    """
    Checks database to determine availability of username.
    """
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        search_text = self.request.GET.get('search_text', '')
        data = {'response': 'Available'}
        if UserProfile.objects.filter(name=search_text).count():
            data = {'response': 'Unavailable'}

        return Response(data, status=status.HTTP_200_OK)


class UserProfileViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserProfileSerializer
    model = UserProfile
    lookup_field = 'slug'

    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        return UserProfile.objects.filter(
            Q(name__startswith=search_text) |
            Q(user__first_name__startswith=search_text) |
            Q(user__last_name__startswith=search_text)
        )

    def pre_save(self, obj):
        user_data = self.request.DATA.get('user', {})
        thumbnail_image = self.request.DATA.get('thumbnail_image_obj', {})
        main_image = self.request.DATA.get('main_image_obj', {})

        full_name = user_data.get('full_name', '').split(' ')
        user_data['first_name'] = full_name[0]

        if thumbnail_image:
            obj.thumbnail_image.save(thumbnail_image['name'],
                ContentFile(thumbnail_image['file'].decode('base64')),
                save=False)
        if main_image:
            obj.main_image.save(main_image['name'],
                ContentFile(main_image['file'].decode('base64')),
                save=False)

        if len(full_name) > 1:
            user_data['last_name'] = ' '.join(full_name[1:])

        user_serializer = UserSerializer(obj.user, data=user_data)

        if user_serializer.is_valid():
            password = user_data.get('password_1', '')
            if password:
                if password == user_data.get('password_2', ''):
                    user_serializer.object.set_password(password)

            user_serializer.save()


class FollowProfileView(APIView):
    """
    Adding current user as follower of Profile
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request, slug, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(slug=slug)
        srv_following = False
        try:
            if user.profile.followed_profiles.filter(slug=slug).count():
                user.profile.followed_profiles.remove(profile)
            else:
                user.profile.followed_profiles.add(profile)
                srv_following = True

            data = {
                'srv_followersCount': profile.followed.count(),
                'srv_following': srv_following
            }

            return Response(data, status=status.HTTP_200_OK)
        except:
            pass
        return Response({}, status=status.HTTP_403_FORBIDDEN)


class ProfileMyPhotosListView(ListAPIView):
    """
    Returns current user photos
    """
    permission_classes = (IsAuthenticated,)

    serializer_class = AlbumSerializer

    def get_queryset(self):
        profile = self.request.user.profile
        return EventDate.objects.filter(id__in=
            profile.profile_images.values_list('event_date_id', flat=True))


class ProfileFavoritesListView(ListAPIView):
    """
    Returns favorite images for current user
    """
    permission_classes = (IsAuthenticated,)

    serializer_class = MultiuploaderImageSerializer

    def get_queryset(self):
        profile = self.request.user.profile

        return MultiuploaderImage.objects.filter(favorite_by__id=profile.id)


class StreamListView(ListAPIView):
    """
    Returns real-time images from Events or Profiles being followed
    """
    permission_classes = (AllowAny,)

    serializer_class = MultiuploaderImageSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_active:
            profile = user.profile

            events_ids = Event.objects.filter(
                Q(author_id__in=profile.followed.values_list('id', flat=True)) |
                Q(followed__id=profile.id)
            )
            queryset = MultiuploaderImage.objects.filter(
                Q(event_date__event_id__in=events_ids) &
                Q(event_date__start_date__lt=datetime.now()) &
                Q(event_date__end_date__gt=datetime.now())
            )
        else:
            queryset = MultiuploaderImage.objects.filter(
                Q(event_date__start_date__lt=datetime.now()) &
                Q(event_date__end_date__gt=datetime.now())
            )

        return queryset


class FavoritePictureView(APIView):
    """
    Adding Picture to favorites
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request, picture_id, *args, **kwargs):
        user = request.user
        picture = MultiuploaderImage.objects.get(id=picture_id)
        try:
            if user.profile.favorite_images.filter(id=picture_id).count():
                user.profile.favorite_images.remove(picture)
            else:
                user.profile.favorite_images.add(picture)

            return Response({}, status=status.HTTP_200_OK)
        except:
            pass
        return Response({}, status=status.HTTP_403_FORBIDDEN)


class ReportPictureView(APIView):
    """
    Flagging Picture as inappropriate
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request, picture_id, *args, **kwargs):
        picture = MultiuploaderImage.objects.get(id=picture_id)
        picture.is_inappropriate = True
        picture.save()

        return Response({}, status=status.HTTP_200_OK)


def make_userjson(user):
    image_url = ""
    if user.profile.thumbnail_image:
        image_url = user.profile.thumbnail_image.url
    user_data = {
        'id': user.pk,
        'email': user.email,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'fullName': user.get_full_name(),
        'admin': user.is_superuser,
        'main_image': image_url,
        'slug': user.profile.slug
    }
    return user_data


class LoginView(APIView):
    """Logs user in. Returns user object
    """
    permission_classes = (AllowAny,)

    #@method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        user_data = None
        email = request.DATA.get('email')
        password = request.DATA.get('password')
        user = authenticate(email=email, password=password)
        if user:
            print 1
            if not user.is_active:
                print 2
                return Response({"message": "Account not active, you must "
                    "activate your account by clicking the validation link in "
                    "the confirmation email sent to you."},
                    status=status.HTTP_403_FORBIDDEN)
            auth_login(request, user)
            user_data = make_userjson(user)

        data = {'user': user_data}
        return Response(data, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    """Returns current user object
    """
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user_data = None
        user = request.user
        if user.is_authenticated():
            user_data = make_userjson(user)
        data = {'user': user_data}
        return Response(data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """Logs user out. Returns empty user object.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user_data = None
        user = request.user
        if user.is_authenticated():
            logout(request)
        data = {'user': user_data}
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class ActivateView(APIView):
    """
    Activates a new user.
    """
    permission_classes = (AllowAny,)

    def get(self, request, activation_key, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(activationtoken=activation_key)
            profile.activationtoken = ""
            profile.user.is_active = True
            profile.user.save()
            profile.save()
            return redirect('/')
        except UserProfile.DoesNotExist:
            return Response({'error': "Wrong token"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """
    Resets password and sends mail with link to changing password.
    """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email_serializer = EmailSerializer(data=request.DATA)
        if email_serializer.is_valid():
            try:
                email = email_serializer.data.get('email', None)
                user = User.objects.get(email=email)
                user.profile.activationtoken = sha1("%sovahi%s" %
                    (randrange(1, 1000), randrange(1, 1000))).hexdigest()
                user.profile.save()
                reset_link = request.build_absolute_uri(
                    reverse('change-password',
                    args=(user.profile.activationtoken,))
                )
                reset_link = reset_link.replace("api/change_password", "#/account/changePassword")
                email_body = render_to_string('emails/reset_password_email.html',
                    {'user': user,
                     'reset_link': reset_link}
                )

                send_mail("Reset Password", email_body,
                    settings.DEFAULT_FROM_EMAIL, [user.email])

                return redirect('/')
            except User.DoesNotExist:
                return Response(
                    {'error': "User with this email address doesn't exist"},
                    status=status.HTTP_400_BAD_REQUEST)

        return Response(email_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    Changes password
    """
    permission_classes = (AllowAny,)

    def put(self, request, activation_key, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(activationtoken=activation_key)
            profile.activationtoken = ""
            password = request.DATA.get('password_1', uuid.uuid4())
            profile.user.set_password(password)
            profile.user.save()
            profile.save()
            return Response({}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'error': "Wrong token"}, status=status.HTTP_400_BAD_REQUEST)

class RegistrationView(APIView):
    """
    Creates a new user.
    Returns: token (auth token)   .
    """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        user_data = request.DATA.get('user', {})
        thumbnail_image = self.request.DATA.get('thumbnail_image_obj', {})
        main_image = self.request.DATA.get('main_image_obj', {})
        full_name = user_data.get('full_name', '').split(' ')
        user_data['first_name'] = full_name[0]
        if len(full_name) > 1:
            user_data['last_name'] = ' '.join(full_name[1:])

        user_serializer = UserSerializer(data=user_data)
        profile_serializer = NewProfileSerializer(data=request.DATA)
        if user_serializer.is_valid() and profile_serializer.is_valid():

            email = user_serializer.data.get('email', None)

            try:
                User.objects.get(email=email)
                error = {'error': 'User already exists'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                user_serializer.object.username = profile_serializer.object.name
                password = user_data.get('password_1', uuid.uuid4())
                user_serializer.object.set_password(password)
                user_serializer.object.is_active = False
                user_serializer.save()

                if thumbnail_image:
                    profile_serializer.object.thumbnail_image.save(
                        thumbnail_image['name'],
                        ContentFile(thumbnail_image['file'].decode('base64')),
                        save=False
                    )
                if main_image:
                    profile_serializer.object.main_image.save(
                        main_image['name'],
                        ContentFile(main_image['file'].decode('base64')),
                        save=False
                    )

                profile_serializer.object.activationtoken = sha1("%sovahi%s" %
                    (randrange(1, 1000), randrange(1, 1000))).hexdigest()

                profile_serializer.object.user = user_serializer.object
                profile_serializer.save()

                activation_link = request.build_absolute_uri(
                    reverse('activate-profile',
                    args=(profile_serializer.object.activationtoken,))
                )

                email_body = render_to_string('emails/activation_email.html',
                    {'user': user_serializer.object,
                     'activation_link': activation_link}
                )

                send_mail("Welcome to Xauto", email_body,
                    settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)

                # return authentication token
                token, created = Token.objects.get_or_create(
                    user=user_serializer.object)
                data = {'token': token.key}
                return Response(data, status=status.HTTP_201_CREATED)

        errors = user_serializer.errors
        errors.update(profile_serializer.errors)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class ConfigurationView(APIView):
    """
    Returns json with configuration and urls.
    """
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        config = {
            'photostream': {
                'url': settings.SOCKET_STREAMER_FULL_URL
            }
        }
        return Response(config, status=status.HTTP_200_OK)
