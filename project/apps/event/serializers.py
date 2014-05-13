# -*- coding: utf-8 -*-
from rest_framework import serializers

from event.models import Event, EventImage, EventDate, Currency
from multiuploader.serializers import MultiuploaderImageSerializer
from django.conf import settings
from account.serializers import UserProfileSerializer
from django_countries import countries


class TimezoneField(serializers.CharField):

    def to_native(self, value):
        value = value.zone
        return super(TimezoneField, self).to_native(value)


class EventImageSerializer(serializers.ModelSerializer):
    """
    A serializer for ``EventImage``.
    """

    class Meta(object):
        model = EventImage


class EventDateSerializer(serializers.ModelSerializer):
    currency_choices = [(c.id, c.currency) for c in Currency.objects.all().order_by('currency')]
    currency = serializers.ChoiceField(choices=currency_choices, source="currency.id")
    country = serializers.ChoiceField(choices=[(c[0], c[1]) for c in list(countries)], source="country")
    timezone_new = TimezoneField()

    class Meta:
        model = EventDate

    def restore_object(self, attrs, instance=None):
        if "currency.id" in attrs and attrs['currency.id']:
            attrs["currency"] = Currency.objects.get(pk=attrs["currency.id"])
            del attrs["currency.id"]
        return super(EventDateSerializer, self).restore_object(attrs, instance)


class AlbumSerializer(serializers.ModelSerializer):
    photos = MultiuploaderImageSerializer(source='event_upload_images', read_only=True)
    date = serializers.SerializerMethodField('get_date')
    active = True

    class Meta:
        model = EventDate

    def get_date(self, obj):
        view = self.context['view']
        return obj.start_date #.strftime('%B %d, %Y %H:%M:%S')


class EventModelSerializer(serializers.ModelSerializer):
    dates = EventDateSerializer(source='event_dates', read_only=True)
    can_edit = serializers.SerializerMethodField('get_can_edit')

    class Meta:
        model = Event
        fields = ('id', 'title', 'about', 'eventSize', 'short_link',
                  'main_image', 'author', 'dates', 'slug', 'can_edit')

    def get_can_edit(self, obj):
        view = self.context['view']
        user = view.request.user
        if user.is_staff or obj.author == user:
            return True
        return False


class EventSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField('get_photo')
    photo_small = serializers.SerializerMethodField('get_photo_small')
    srv_followersCount = serializers.SerializerMethodField('srv_followers_count')
    srv_photosCount = serializers.SerializerMethodField('srv_photos_count')
    date_info = serializers.SerializerMethodField('get_date_info')
    author_name = serializers.SerializerMethodField('get_author_name')
    author_photo = serializers.SerializerMethodField('get_author_photo')
    author_slug = serializers.SerializerMethodField('get_author_slug')
    srv_live = serializers.SerializerMethodField('get_srv_live')
    srv_following = serializers.SerializerMethodField('get_srv_following')

    class Meta:
        model = Event
        fields = ('id', 'title', 'about', 'eventSize', 'srv_followersCount',
                  'srv_photosCount', 'photo', 'photo_small', 'date_info', 'author_name', 'slug',
                  'author_photo', 'author_slug', 'srv_live', 'srv_following')

    def get_photo(self, obj):
        if obj.main_image:
            return obj.thumb_url(560, 400)

    def get_photo_small(self, obj):
        if obj.main_image:
            return obj.thumb_url(50, 36)

    def srv_followers_count(self, obj):
        return obj.followed.count()

    def srv_photos_count(self, obj):
        return obj.event_upload_images().count()

    def get_author_name(self, obj):
        if obj.author:
            return obj.author.get_full_name()
        return ""

    def get_author_slug(self, obj):
        if obj.author:
            return obj.author.slug
        return ""

    def get_author_photo(self, obj):
        if obj.author and obj.author.thumbnail_image:
            return obj.author.get_thumbnail(80, 77)
        return ""

    def get_srv_live(self, obj):
        view = self.context['view']
        return obj.is_live_streaming(view.request.user)

    def get_srv_following(self, obj):
        view = self.context['view']
        user = view.request.user
        if hasattr(user, 'profile'):
            return user.profile.followed_events.filter(id=obj.id).exists()
        return False

    def get_date_info(self, obj):
        nearest_date = obj.get_nearest_date()
        if nearest_date:
            ci = nearest_date.city or u''
            co = nearest_date.country or u''
            comma = ci and co and u', ' or u''
            location = u'{}{}{}'.format(ci, comma, co)

            return {
                "date": nearest_date.start_date,
                "timezone": nearest_date.timezone_new,
                "startTime": nearest_date.start_date.strftime('%H:%M'),
                "endTime": nearest_date.end_date and nearest_date.end_date.strftime('%H:%M') or None,
                "city": nearest_date.city,
                "state": nearest_date.state,
                "country": nearest_date.country,
                "country_name": nearest_date.country.name,
                "location": location,
                "featureHeadline": nearest_date.feature_headline,
                "attend_free": nearest_date.attend_free,
                "attend_low": nearest_date.attend_price_from,
                "attend_high": nearest_date.attend_price_to,
                "attend_currency": nearest_date.currency,
            }
        return {
        }


class EventDetailsSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField('get_photo')
    srv_followersCount = serializers.SerializerMethodField('srv_followers_count')
    srv_photosCount = serializers.SerializerMethodField('srv_photos_count')
    srv_futureDates = serializers.SerializerMethodField('get_future_date')
    author_name = serializers.SerializerMethodField('get_author_name')
    author_photo = serializers.SerializerMethodField('get_author_photo')
    srv_live = serializers.SerializerMethodField('get_srv_live')
    srv_following = serializers.SerializerMethodField('get_srv_following')
    albums = AlbumSerializer(source='event_dates', read_only=True)
    profile = UserProfileSerializer(source='author', read_only=True)
    gotolink = serializers.SerializerMethodField('get_gotolink')

    class Meta:
        model = Event
        fields = ('id', 'title', 'about', 'eventSize', 'srv_followersCount',
                  'srv_photosCount', 'photo', 'srv_futureDates', 'author_name',
                  'author_photo', 'srv_live', 'srv_following', 'albums', 'profile', 'slug', 'gotolink')

    def get_photo(self, obj):
        if obj.main_image:
            return obj.thumb_url(1500, 290)

    def get_gotolink(self, obj):
        near = obj.get_nearest_date()
        if near:
            if near.latitude and near.longitude:
                return settings.GOTO_BUTTON_URL.format(lat=near.latitude, lon=near.longitude)
        return ""

    def srv_followers_count(self, obj):
        return obj.followed.count()

    def srv_photos_count(self, obj):
        return obj.event_upload_images().count()

    def get_author_name(self, obj):
        if obj.author:
            return obj.author.get_full_name()
        return ""

    def get_author_photo(self, obj):
        if obj.author and obj.author.thumbnail_image:
            return obj.author.get_thumbnail(50, 48)
        return ""

    def get_srv_live(self, obj):
        view = self.context['view']
        return obj.is_live_streaming(view.request.user)

    # TODO: refactor
    def get_srv_following(self, obj):
        view = self.context['view']
        user = view.request.user
        try:
            if user.profile.followed_events.filter(id=obj.id).count():
                return True
        except:
            pass
        return False

    def get_future_date(self, obj):
        future_dates = []
        for future_date in obj.get_future_dates():
            future_dates.append({
                "date": future_date.start_date,
                "startTime": future_date.start_date.strftime('%H:%M'),
                "endTime": future_date.end_date.strftime('%H:%M'),
                "addr1": future_date.address_1,
                "addr2": future_date.address_2,
                "city": future_date.city,
                "state": future_date.state,
                "zip": future_date.zipcode,
                "country": future_date.country,
                "featureHeadline": future_date.feature_headline,
                "featureDetail": future_date.feature_detail,
                "attend_free": future_date.attend_free,
                "attend_low": future_date.attend_price_from,
                "attend_high": future_date.attend_price_to,
                "attend_currency": future_date.currency,
            })
        return future_dates
