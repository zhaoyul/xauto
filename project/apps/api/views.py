# -*- coding: utf-8 -*-
import uuid
import math
from datetime import datetime, time
from random import randrange
from hashlib import sha1
from api.permissions import IsEventAuthorOrReadOnly, IsEventDateAuthorOrReadOnly, IsAccountOwnerOrReadOnly
from api.utils import get_time_display

import pytz
from django.utils import timezone
from django_countries import countries
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import (login as auth_login, logout, authenticate)
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.files.base import ContentFile
from django.conf import settings
from rest_framework.generics import (ListAPIView, RetrieveAPIView, DestroyAPIView, ListCreateAPIView, UpdateAPIView)
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from event.models import Event, EventDate, EventImage
from event.serializers import (EventSerializer, EventDetailsSerializer,
                               EventModelSerializer, EventDateSerializer)
from account.serializers import (UserProfileSerializer, UserSerializer,
                                 NewProfileSerializer, EmailSerializer)
from account.models import UserProfile
from multiuploader.serializers import (MultiuploaderImageSerializer,
                                       CoordinatedPhotoSerializer)
from multiuploader.models import MultiuploaderImage


if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail, send_html_mail
else:
    from django.core.mail import send_mail


class EventsListView(ListAPIView):
    """
    Returns Event list
    """
    permission_classes = (AllowAny,)
    serializer_class = EventSerializer

    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        filter_by = self.request.GET.get('filter_by', '')
        own_events = self.request.GET.get('own_events', False)

        lat = self.request.GET.get('lat', '')
        lon = self.request.GET.get('lon', '')

        user = self.request.user

        if len(search_text) >= 1:
            queryset = Event.objects.filter((Q(title__icontains=search_text) |
                                             Q(event_dates__city__icontains=search_text) |
                                             Q(event_dates__state__icontains=search_text))).distinct()
        else:
            queryset = Event.objects.all()

        if own_events == 'true':
            if user.is_active:
                queryset = queryset.filter(author=user.profile)
            else:
                queryset = queryset.none()

        if filter_by == 'following':
            if not user.is_authenticated():
                queryset = queryset.none()
            elif user.is_active:
                queryset = queryset.filter(followed=user.profile)

        if filter_by == 'live':
            queryset = queryset.filter(event_dates__start_date__lt=timezone.now(),
                                       event_dates__end_date__gt=timezone.now()).distinct()

        #TODO: might be better convert 5 degrees to kilometers
        if filter_by == 'nearby':
            if lon and lat:
                neardates = EventDate.objects.filter(
                    (Q(latitude__gt=float(lat) - 5) & Q(latitude__lt=float(lat) + 5)),
                    (Q(longitude__gt=float(lon) - 5) & Q(longitude__lt=float(lon) + 5))).distinct()

                #sort by distance
                near = []
                for d in neardates:
                    distance = abs(d.longitude - float(lon)) + abs(d.latitude - float(lat))
                    near.append((d.event.id, distance))
                near.sort(key=lambda item: item[1])
                ids = []
                for el in near:
                    evid = el[0]
                    if not evid in ids:
                        ids.append(evid)
                queryset = queryset.filter(id__in=ids)[:5]

        return queryset


class EventDetailsView(RetrieveAPIView):
    """
    Returns Event details
    """
    permission_classes = (AllowAny,)
    serializer_class = EventDetailsSerializer
    model = Event
    lookup_field = 'slug'


class TimezonesListView(APIView):
    """
    Returns all available timezones
    """

    def get(self, request, *args, **kwargs):
        ret = []
        for tz_name in pytz.common_timezones:
            tz = pytz.timezone(tz_name)
            offset = datetime.now(tz).strftime('%z')
            ret.append({'value': tz_name, 'label': '{} ({})'.format(tz_name, offset)})
        return Response(ret, status=status.HTTP_200_OK)


class CountriesListView(APIView):
    """
    Returns all available countries
    """

    def get(self, request, *args, **kwargs):
        ret = [{'value': c[0], 'label': c[1]} for c in list(countries)]
        return Response(ret, status=status.HTTP_200_OK)


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
            ff = photo['file'].split(",")
            if len(ff) > 1:
                ff = ff[1]
            else:
                ff = photo['file']
            imageObj.image.save(
                photo['name'],
                ContentFile(ff.decode('base64')),
                save=False
            )
            imageObj.userprofile = profile
            event_date = photo.get('event_date', None)
            if event_date:
                imageObj.event_date = EventDate.objects.get(id=event_date)
            imageObj.save()
            i += 1

        return Response({'success': True}, status=status.HTTP_200_OK)


class EventViewSet(ModelViewSet):
    """
    Returns Event CRUD methods
    """
    permission_classes = (IsAuthenticated, IsEventAuthorOrReadOnly)
    serializer_class = EventModelSerializer
    model = Event
    lookup_field = 'slug'

    def pre_save(self, obj):
        if not obj.author:
            obj.author = self.request.user.profile

        main_image = self.request.DATA.get('main_image_obj', {})
        if main_image:
            imageObj = EventImage()
            if "data:" in main_image['file']:
                main_image['file'] = str(main_image['file']).split(",")[-1]
            imageObj.image.save(
                main_image['name'],
                ContentFile(main_image['file'].decode('base64'))
            )
            obj.main_image = imageObj


class EventDateViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsEventDateAuthorOrReadOnly)
    serializer_class = EventDateSerializer
    model = EventDate

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            # permissions check
            if serializer.object.event.author == request.user.profile:
                self.pre_save(serializer.object)
                self.object = serializer.save(force_insert=True)
                self.post_save(self.object, created=True)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED,
                                headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LastDateView(RetrieveAPIView):
    """
    Copy last date button
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = EventDateSerializer
    model = Event

    def retrieve(self, request, *args, **kwargs):
        self.object = self.get_object()
        date = self.object.get_latest_date()
        serializer = self.get_serializer(date)
        return Response(serializer.data)


class EventAllImagesView(ListCreateAPIView):
    """
    Show all photos of the album
    """
    permission_classes = (IsAuthenticated, IsEventAuthorOrReadOnly)
    model = Event

    def list(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get('slug')

        event = Event.objects.get(slug=slug, author=user.profile)
        imgs = []

        mi = MultiuploaderImage.objects.filter(event_date__in=EventDate.objects.filter(event=event))
        for m in mi:
            imgs.append((m.id, m.thumb_url(250, 250)))

        return Response(imgs, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Set event photo
        """
        user = request.user
        slug = kwargs.get('slug')

        event = Event.objects.get(slug=slug, author=user.profile)

        #setting image
        sset = self.request.DATA.get('id', None)
        message = 'Invalid parameters'
        if sset:
            try:
                img = MultiuploaderImage.objects.get(id=sset)
                new = EventImage()
                new.image = img.image
                new.save()
                event.main_image = new
                event.save()
                data = {'id': event.main_image.id}
                headers = self.get_success_headers(data)
                return Response(data, status=status.HTTP_201_CREATED,
                                headers=headers)
            except MultiuploaderImage.DoesNotExist:
                message = 'Image not found'

        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)


class DeletePhotoView(DestroyAPIView):
    """
    Delete my photo
    """
    permission_classes = (IsAuthenticated,)
    model = MultiuploaderImage

    def get_queryset(self):
        profile = self.request.user.profile
        return MultiuploaderImage.objects.filter(userprofile=profile)


class UnassignPicture(UpdateAPIView):
    """
    Unassing photo from event date - only if event belongs to the user
    """
    permission_classes = (IsAuthenticated,)
    model = MultiuploaderImage

    def get_queryset(self):
        profile = self.request.user.profile
        return MultiuploaderImage.objects.filter(event_date__event__author=profile)

        # def put(self, request, picture_id, *args, **kwargs):
        #     user = request.user
        #     picture = MultiuploaderImage.objects.get(id=picture_id)
        #     if picture.event_date:
        #         event = picture.event_date.event
        #         if event.author.user == user:
        #             picture.delete()
        #
        #     return Response({}, status=status.HTTP_200_OK)


class EventDatePhotoManageView(APIView):
    """
    Manage photo for event date
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, *args, **kwargs):
        data = {}
        DateObj = EventDate.objects.get(id=id)
        data["DateObjLocation"] = DateObj.location_name and DateObj.location_name + ' -' or ''
        data["DateObjDate"] = DateObj.get_date_display()
        data["DateObjImgs"] = []
        imgs = MultiuploaderImage.objects.filter(event_date=DateObj)
        for img in imgs:
            data["DateObjImgs"].append({"id": img.id, "image": img.image.url})
        return Response(data, status=status.HTTP_200_OK)


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
            if user.profile.followed_events.filter(slug=slug).exists():
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
        search_text = self.request.GET.get('search_text', '').lower()
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
        user = request.user
        search_text = self.request.GET.get('search_text', '')
        data = {'response': 'Available'}
        if user.is_authenticated() and user.username.lower() == search_text.lower():
            data = {'response': ''}
        elif UserProfile.objects.filter(user__username=search_text).exists():
            data = {'response': 'Unavailable'}

        return Response(data, status=status.HTTP_200_OK)


class UserProfileViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAccountOwnerOrReadOnly)
    serializer_class = UserProfileSerializer
    model = UserProfile
    lookup_field = 'slug'

    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        filter_by = self.request.GET.get('filter_by', '')
        user = self.request.user

        if len(search_text) >= 1:
            queryset = UserProfile.objects.filter(
                Q(user__first_name__icontains=search_text) |
                Q(user__last_name__icontains=search_text) |
                Q(city__icontains=search_text) |
                Q(state__icontains=search_text)
            ).distinct()
        else:
            queryset = UserProfile.objects.all()

        if filter_by == 'following' and user.is_active:
            queryset = queryset.filter(followed=user.profile)

        if filter_by == 'followers' and user.is_active:
            queryset = queryset.filter(followed_profiles=user.profile)

        return queryset

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

    # TODO: refactor
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


class DatesHavingMyPhotosByEventListView(APIView):
    """
    Returns current user dates grouped by events
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        profile = self.request.user.profile
        event_dates = EventDate.objects.filter(event_upload_images__userprofile=profile).order_by('-start_date').distinct()

        events = {}
        for event_date in event_dates:
            event = events.setdefault(event_date.event.title, [])

            event.append({"id": event_date.id,
                          "title": event_date.feature_headline,
                          "date": event_date.get_date_display(),
                          })
        ret = []
        for key, value in events.iteritems():
            ret.append({'title': key, 'dates': value})
        return Response(ret, status=status.HTTP_200_OK)


class DatesHavingMyPhotosByDateListView(APIView):
    """
    Returns current user dates grouped by events
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        profile = self.request.user.profile
        dates = MultiuploaderImage.objects.filter(userprofile=profile).\
            distinct().datetimes('upload_date', 'day', order="DESC", tzinfo=profile.timezone)
        ret = []
        for date in dates:
            ret.append({'label': get_time_display(date), 'date': datetime.strftime(date, '%Y-%m-%d')})
        return Response(ret, status=status.HTTP_200_OK)


class DatesHavingMyOrphanedPhotosView(APIView):
    """
    Returns list of dates that have current user's images
    that are not assigned to any Events (EventDates)
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        profile = self.request.user.profile
        objs = MultiuploaderImage.objects.filter(event_date=None, userprofile=profile)
        # TODO: use set here for unique entries
        data = []
        dates = []
        for o in objs:
            dt = o.upload_date.strftime('%Y-%m-%d')
            if dt not in dates:
                dates.append(dt)
                data.append(o.upload_date)
        return Response(data, status=status.HTTP_200_OK)


class MyOrphanedPhotosListView(APIView):
    """
    Returns current user photos that are not in albums (not assigned to any Event (EventDate))
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        profile = self.request.user.profile

        queryset = MultiuploaderImage.objects.filter(event_date=None,
                                                     userprofile=profile)

        dt = request.GET.get('dt')
        if dt:
            upload_date = datetime.strptime(dt, '%Y-%m-%d').date()
            day_start = datetime.combine(upload_date, time.min).replace(tzinfo=profile.timezone)
            day_end = datetime.combine(upload_date, time.max).replace(tzinfo=profile.timezone)

            queryset = queryset.filter(upload_date__range=(day_start, day_end))

        objs_list = [{"id": o.id, "image": o.image.url} for o in queryset]
        return Response(objs_list, status=status.HTTP_200_OK)


class MyPhotosListView(ListAPIView):
    """
    Returns current user's photos
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MultiuploaderImageSerializer

    def get_queryset(self):
        profile = self.request.user.profile
        queryset = MultiuploaderImage.objects.filter(userprofile=profile)

        id = self.request.GET.get('eventdate_id')
        if id:
            dt = EventDate.objects.get(id=id)
            queryset = queryset.filter(event_date=dt)

        dt = self.request.GET.get('dt')
        if dt:
            upload_date = datetime.strptime(dt, '%Y-%m-%d').date()
            day_start = datetime.combine(upload_date, time.min).replace(tzinfo=profile.timezone)
            day_end = datetime.combine(upload_date, time.max).replace(tzinfo=profile.timezone)

            queryset = queryset.filter(upload_date__range=(day_start, day_end))

        return queryset


class ToggleFavoritePicture(APIView):
    """
    Adding Picture to favorites
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request, picture_id, *args, **kwargs):
        user = request.user
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            return Response({'success': False, 'message': 'User profile doesn\'t exist'},
                            status=status.HTTP_403_FORBIDDEN)
        try:
            picture = MultiuploaderImage.objects.get(id=picture_id)
        except MultiuploaderImage.DoesNotExist:
            return Response({'success': False, 'message': 'Picture doesn\'t exist'},
                            status=status.HTTP_400_BAD_REQUEST)

        if profile.favorite_images.filter(id=picture_id).exists():
            profile.favorite_images.remove(picture)
        else:
            profile.favorite_images.add(picture)
        return Response({'success': True}, status=status.HTTP_200_OK)


class FavoritePicturesListView(ListAPIView):
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
                Q(event_date__start_date__lt=timezone.now()) &
                Q(event_date__end_date__gt=timezone.now())
            )
        else:
            queryset = MultiuploaderImage.objects.filter(
                Q(event_date__start_date__lt=timezone.now()) &
                Q(event_date__end_date__gt=timezone.now())
            )
        return queryset


class ReportPictureView(APIView):
    """
    Flagging Picture as inappropriate
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request, picture_id, *args, **kwargs):
        picture = MultiuploaderImage.objects.get(id=picture_id)
        picture.is_inappropriate = True
        picture.save()

        #email to admin
        user = request.user
        email_body = render_to_string('emails/picture_report_email.html',
                                      {'user': user,
                                       'title': 'Picture report',
                                       'site_name': settings.SITE_NAME,
                                       'domain': request.build_absolute_uri(reverse('index')),
                                       'picture_id': picture_id}
        )

        manager_emails = [t[1] for t in settings.MANAGERS]

        if "mailer" in settings.INSTALLED_APPS:
            send_html_mail("Picture report", email_body, email_body,
                           settings.DEFAULT_FROM_EMAIL, manager_emails)
        else:
            send_mail("Picture report", email_body,
                      settings.DEFAULT_FROM_EMAIL, manager_emails)

        return Response({}, status=status.HTTP_200_OK)


def make_userjson(user):
    image_url = ""
    image_url2 = ""
    if user.profile.thumbnail_image:
        image_url = user.profile.get_main_image(32, 21)
    if user.profile.main_image:
        image_url2 = user.profile.get_thumbnail(32, 21)
    user_data = {
        'id': user.pk,
        'email': user.email,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'fullName': user.get_full_name(),
        'admin': user.is_superuser,
        'main_image': image_url,
        'thumbnail_image': image_url2,
        'slug': user.profile.slug,
        'following': {
            'profiles': [x.slug for x in user.profile.followed_profiles.all()],
            'events': [x.slug for x in user.profile.followed_events.all()],
        }
    }
    return user_data


class LoginView(APIView):
    """Logs user in. Returns user object
    """
    permission_classes = (AllowAny,)

    #@method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        user_data = None
        email = request.DATA.get('email', '')
        password = request.DATA.get('password', '')
        user = authenticate(email=email, password=password)
        if user:
            if not user.is_active:
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
                user.profile.activationtoken = sha1("%sxauto%s" %
                                                    (randrange(1, 1000), randrange(1, 1000))).hexdigest()
                user.profile.save()
                reset_link = request.build_absolute_uri(
                    reverse('change-password',
                            args=(user.profile.activationtoken,))
                )

                # change Django url to Angular url
                reset_link = reset_link.replace("{}/api/change_password".format(settings.APP_PREFIX),
                                                "/#/account/changePassword")

                email_body = render_to_string('emails/reset_password_email.html',
                                              {'user': user,
                                               'title': 'Password reset',
                                               'site_name': settings.SITE_NAME,
                                               'reset_link': reset_link}
                )
                if "mailer" in settings.INSTALLED_APPS:
                    send_html_mail("Reset Password", email_body, email_body,
                                   settings.DEFAULT_FROM_EMAIL, [user.email])
                else:
                    send_mail("Reset Password", email_body,
                              settings.DEFAULT_FROM_EMAIL, [user.email])

                return Response({'success': True})
            except User.DoesNotExist:
                return Response(
                    {'email': ["User with this email address doesn't exist"]},
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

        pw1 = user_data.get('password_1', '1')
        pw2 = user_data.get('password_2', '2')
        if pw1 != pw2:
            error = {'password_1': ['Passwords do not match']}
            error['password_2'] = ['']
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(data=user_data)
        profile_serializer = NewProfileSerializer(data=request.DATA)
        print user_serializer.errors
        if user_serializer.is_valid() and profile_serializer.is_valid():
            email = user_serializer.data.get('email', None)
            timezone = request.DATA.get('timezone', None)
            full_name = user_data.get('full_name', None)

            error = None

            if not email:
                error = {'email': ['This field is required.']}
            if not timezone:
                error = {'timezone': ['This field is required.']}
            if not full_name:
                error = {'full_name': ['This field is required.']}
            if error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            try:
                User.objects.get(email=email)
                error = {'email': ['User with given email already exists']}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                user_serializer.object.set_password(pw1)
                user_serializer.object.is_active = True
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

                profile_serializer.object.activationtoken = sha1("%sxauto%s" %
                                                                 (randrange(1, 1000), randrange(1, 1000))).hexdigest()

                profile_serializer.object.user = user_serializer.object
                profile_serializer.save()

                #activation (old)
                '''activation_link = request.build_absolute_uri(
                    reverse('activate-profile',
                    args=(profile_serializer.object.activationtoken,))
                )

                email_body = render_to_string('emails/activation_email.html',
                    {'user': user_serializer.object,
                     'title': 'Registration',
                     'site_name': settings.SITE_NAME,
                     'domain': request.build_absolute_uri(reverse('index')),
                     'activation_link': activation_link}
                )
                if "mailer" in settings.INSTALLED_APPS:
                    send_html_mail("Welcome to Xauto", email_body, email_body,
                        settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
                else:
                    send_mail("Welcome to Xauto", email_body,
                        settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)

                # return authentication token
                token, created = Token.objects.get_or_create(
                    user=user_serializer.object)'''

                #auth new user

                user = authenticate(email=user_serializer.object.email, password=pw1)
                auth_login(request, user)

                return Response(None, status=status.HTTP_201_CREATED)

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


class CoordinatedPhotoUploader(APIView):
    """
    Creates image and assigns it to the closest event

    var data = {};
    data['coords'] = {"lon": 2.12, "lat": -3.53};
    data['file'] = "data:image/jpg|;base64,........"
    Events.uploadCoordinatedPhoto(data);

    """
    permission_classes = (IsAuthenticated,)

    def haversine_distance(self, origin, destination):
        lat1, lon1 = origin
        lat2, lon2 = destination
        radius = 6372.797

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
                                                      * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(
            dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c
        return d

    def findEventFromCoords(self, lon=0, lat=0, radius=50):
        """
            Find first matching event for given coordinates (lon, lat) within radius (in km)
        """
        now = timezone.now()

        # TODO: in case of multiple events we can try to reduce radius
        for event_date in EventDate.objects.filter(start_date__lt=now, end_date__gt=now):
            distance = self.haversine_distance((lat, lon), (event_date.latitude, event_date.longitude))
            if distance < radius:
                return event_date

        return None

    def post(self, request, *args, **kwargs):
        profile = self.request.user.profile
        serializer = CoordinatedPhotoSerializer(data=request.DATA)
        if serializer.is_valid():
            imageObj = MultiuploaderImage()
            imageObj.image.save(
                serializer.object["file"].name,
                serializer.object["file"],
                save=False
            )
            imageObj.userprofile = profile
            if "coords" in serializer.object:
                lon = serializer.object["coords"]["lon"]
                lat = serializer.object["coords"]["lat"]

                imageObj.event_date = self.findEventFromCoords(lon, lat)
                imageObj.longitude = lon
                imageObj.latitude = lat
            imageObj.save()
            return Response({}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
