# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Currency'
        db.create_table(u'event_currency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('country_code', self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
        ))
        db.send_create_signal(u'event', ['Currency'])

        # Adding model 'YoutubeVideoId'
        db.create_table(u'event_youtubevideoid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('video_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='youtube_videos', to=orm['event.Event'])),
        ))
        db.send_create_signal(u'event', ['YoutubeVideoId'])

        # Adding model 'EventImage'
        db.create_table(u'event_eventimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['event.Event'])),
            ('latitude', self.gf('django.db.models.fields.FloatField')(default=0.0, db_index=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(default=0.0, db_index=True)),
        ))
        db.send_create_signal(u'event', ['EventImage'])

        # Adding model 'EventDate'
        db.create_table(u'event_eventdate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='event_available_date', to=orm['event.Event'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_event_date', to=orm['auth.User'])),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('feature_headline', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('feature_detail', self.gf('django.db.models.fields.TextField')()),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['event.Currency'], null=True, blank=True)),
            ('attend_free', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('exhibit_free', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('attend_price_from', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('attend_price_to', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('exhibit_price_from', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('exhibit_price_to', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'event', ['EventDate'])

        # Adding model 'Organizer'
        db.create_table(u'event_organizer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('organization_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('organization_desc', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='organizer_event', to=orm['auth.User'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='selected_organizer_event', null=True, to=orm['event.Event'])),
            ('remove_past_events', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_saved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('include_social_link', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('shortname', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('facebook_id', self.gf('django.db.models.fields.CharField')(default='', max_length=250, null=True, blank=True)),
            ('twitter_id', self.gf('django.db.models.fields.CharField')(default='', max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'event', ['Organizer'])

        # Adding M2M table for field events on 'Organizer'
        m2m_table_name = db.shorten_name(u'event_organizer_events')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('organizer', models.ForeignKey(orm[u'event.organizer'], null=False)),
            ('event', models.ForeignKey(orm[u'event.event'], null=False))
        ))
        db.create_unique(m2m_table_name, ['organizer_id', 'event_id'])

        # Adding M2M table for field venues on 'Organizer'
        m2m_table_name = db.shorten_name(u'event_organizer_venues')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('organizer', models.ForeignKey(orm[u'event.organizer'], null=False)),
            ('venue', models.ForeignKey(orm[u'event.venue'], null=False))
        ))
        db.create_unique(m2m_table_name, ['organizer_id', 'venue_id'])

        # Adding model 'Venue'
        db.create_table(u'event_venue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('organizer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='organizer_venue', null=True, to=orm['event.Organizer'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_venue', to=orm['auth.User'])),
            ('venue', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('address', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('address_2', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('country_short', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('longaddress', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('zoom', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('is_saved', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'event', ['Venue'])

        # Adding model 'Event'
        db.create_table(u'event_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='authored_event', null=True, to=orm['auth.User'])),
            ('duration', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('number', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=30, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='new', max_length=15, db_index=True)),
            ('eventSize', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('capacity', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('shortname', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='event_venue', null=True, on_delete=models.SET_NULL, to=orm['event.Venue'])),
            ('organizer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='event_organizer', null=True, on_delete=models.SET_NULL, to=orm['event.Organizer'])),
            ('started_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 19, 0, 0), null=True, blank=True)),
            ('closed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('archived_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('published_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('expire_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('main_image', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='main', null=True, on_delete=models.SET_NULL, to=orm['event.EventImageExtend'])),
            ('video_cache', self.gf('django.db.models.fields.CharField')(default='[]', max_length=255)),
            ('youtube_url', self.gf('video.fields.YouTubeField')(max_length=100, blank=True)),
            ('video_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('google_analytics', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('instructions', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
        ))
        db.send_create_signal(u'event', ['Event'])

        # Adding M2M table for field available_dates on 'Event'
        m2m_table_name = db.shorten_name(u'event_event_available_dates')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'event.event'], null=False)),
            ('eventdate', models.ForeignKey(orm[u'event.eventdate'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'eventdate_id'])

        # Adding M2M table for field event_date on 'Event'
        m2m_table_name = db.shorten_name(u'event_event_event_date')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'event.event'], null=False)),
            ('eventdate', models.ForeignKey(orm[u'event.eventdate'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'eventdate_id'])

        # Adding model 'Feedback'
        db.create_table(u'event_feedback', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='event_feedback', to=orm['event.Event'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='feedback_author', to=orm['auth.User'])),
            ('given_author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='given_feedback_author', null=True, to=orm['auth.User'])),
            ('send_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('feedback_status', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('feedback_mode', self.gf('django.db.models.fields.CharField')(default='customer', max_length=50)),
            ('recommend', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'event', ['Feedback'])

        # Adding M2M table for field rating on 'Feedback'
        m2m_table_name = db.shorten_name(u'event_feedback_rating')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feedback', models.ForeignKey(orm[u'event.feedback'], null=False)),
            ('feedbackrating', models.ForeignKey(orm[u'event.feedbackrating'], null=False))
        ))
        db.create_unique(m2m_table_name, ['feedback_id', 'feedbackrating_id'])

        # Adding model 'RatingValue'
        db.create_table(u'event_ratingvalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('index', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('keyword', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'event', ['RatingValue'])

        # Adding model 'FeedbackRating'
        db.create_table(u'event_feedbackrating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('rate_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['event.RatingValue'])),
            ('rating', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='rating_author', null=True, to=orm['auth.User'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='feedbackrating_event', null=True, to=orm['event.Event'])),
        ))
        db.send_create_signal(u'event', ['FeedbackRating'])

        # Adding model 'EventImageExtend'
        db.create_table(u'event_eventimageextend', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('order', self.gf('xauto_lib.orderable.OrderingField')()),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='event_images', to=orm['event.Event'])),
            ('latitude', self.gf('django.db.models.fields.FloatField')(default=0.0, db_index=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(default=0.0, db_index=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'event', ['EventImageExtend'])

        # Adding model 'flagEvent'
        db.create_table(u'event_flagevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='flag_an_event', to=orm['event.Event'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='flag_ad_author', to=orm['auth.User'])),
            ('reason', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('email_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('message_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('review', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('remove_event', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_email', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_review', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('response', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'event', ['flagEvent'])


    def backwards(self, orm):
        # Deleting model 'Currency'
        db.delete_table(u'event_currency')

        # Deleting model 'YoutubeVideoId'
        db.delete_table(u'event_youtubevideoid')

        # Deleting model 'EventImage'
        db.delete_table(u'event_eventimage')

        # Deleting model 'EventDate'
        db.delete_table(u'event_eventdate')

        # Deleting model 'Organizer'
        db.delete_table(u'event_organizer')

        # Removing M2M table for field events on 'Organizer'
        db.delete_table(db.shorten_name(u'event_organizer_events'))

        # Removing M2M table for field venues on 'Organizer'
        db.delete_table(db.shorten_name(u'event_organizer_venues'))

        # Deleting model 'Venue'
        db.delete_table(u'event_venue')

        # Deleting model 'Event'
        db.delete_table(u'event_event')

        # Removing M2M table for field available_dates on 'Event'
        db.delete_table(db.shorten_name(u'event_event_available_dates'))

        # Removing M2M table for field event_date on 'Event'
        db.delete_table(db.shorten_name(u'event_event_event_date'))

        # Deleting model 'Feedback'
        db.delete_table(u'event_feedback')

        # Removing M2M table for field rating on 'Feedback'
        db.delete_table(db.shorten_name(u'event_feedback_rating'))

        # Deleting model 'RatingValue'
        db.delete_table(u'event_ratingvalue')

        # Deleting model 'FeedbackRating'
        db.delete_table(u'event_feedbackrating')

        # Deleting model 'EventImageExtend'
        db.delete_table(u'event_eventimageextend')

        # Deleting model 'flagEvent'
        db.delete_table(u'event_flagevent')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'event.currency': {
            'Meta': {'object_name': 'Currency'},
            'country': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'country_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'})
        },
        u'event.event': {
            'Meta': {'object_name': 'Event'},
            'archived_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'authored_event'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'available_dates': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'select_event_date'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['event.EventDate']"}),
            'capacity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'closed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'eventSize': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'event_date': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'available_date_for_your_event'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['event.EventDate']"}),
            'expire_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'google_analytics': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'main_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'main'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['event.EventImageExtend']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'event_organizer'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['event.Organizer']"}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'shortname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 19, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '15', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'event_venue'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['event.Venue']"}),
            'video_cache': ('django.db.models.fields.CharField', [], {'default': "'[]'", 'max_length': '255'}),
            'video_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'youtube_url': ('video.fields.YouTubeField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'event.eventdate': {
            'Meta': {'object_name': 'EventDate'},
            'attend_free': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'attend_price_from': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'attend_price_to': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_event_date'", 'to': u"orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['event.Currency']", 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_available_date'", 'to': u"orm['event.Event']"}),
            'exhibit_free': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'exhibit_price_from': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'exhibit_price_to': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'feature_detail': ('django.db.models.fields.TextField', [], {}),
            'feature_headline': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'event.eventimage': {
            'Meta': {'object_name': 'EventImage'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['event.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'})
        },
        u'event.eventimageextend': {
            'Meta': {'object_name': 'EventImageExtend'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_images'", 'to': u"orm['event.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'order': ('xauto_lib.orderable.OrderingField', [], {})
        },
        u'event.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feedback_author'", 'to': u"orm['auth.User']"}),
            'comment': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_feedback'", 'to': u"orm['event.Event']"}),
            'feedback_mode': ('django.db.models.fields.CharField', [], {'default': "'customer'", 'max_length': '50'}),
            'feedback_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'given_author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'given_feedback_author'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'rating': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'feedback_list_rating'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['event.FeedbackRating']"}),
            'recommend': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'event.feedbackrating': {
            'Meta': {'object_name': 'FeedbackRating'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'rating_author'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'feedbackrating_event'", 'null': 'True', 'to': u"orm['event.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'rate_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['event.RatingValue']"}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'event.flagevent': {
            'Meta': {'object_name': 'flagEvent'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flag_ad_author'", 'to': u"orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'date_email': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_review': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'email_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flag_an_event'", 'to': u"orm['event.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'remove_event': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'response': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'review': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'event.organizer': {
            'Meta': {'object_name': 'Organizer'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organizer_event'", 'to': u"orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'selected_organizer_event'", 'null': 'True', 'to': u"orm['event.Event']"}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'event_for_user'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['event.Event']"}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include_social_link': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_saved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'organization_desc': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'organization_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'remove_past_events': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shortname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'twitter_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'venues': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'venue_for_user'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['event.Venue']"})
        },
        u'event.ratingvalue': {
            'Meta': {'object_name': 'RatingValue'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'keyword': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'event.venue': {
            'Meta': {'object_name': 'Venue'},
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'country_short': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_saved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'longaddress': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'organizer_venue'", 'null': 'True', 'to': u"orm['event.Organizer']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_venue'", 'to': u"orm['auth.User']"}),
            'venue': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'zoom': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'event.youtubevideoid': {
            'Meta': {'object_name': 'YoutubeVideoId'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'youtube_videos'", 'to': u"orm['event.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'video_id': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['event']