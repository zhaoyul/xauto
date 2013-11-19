# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AlertEvent'
        db.create_table(u'account_alertevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='alert_user', to=orm['member.UserProfile'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='alert_user_event', null=True, to=orm['event.Event'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('distance', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('frequency', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('location_address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('activated', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_sent_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('received_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('nbr_alert', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nbr_sent', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_send_email', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'account', ['AlertEvent'])

        # Adding M2M table for field keywords on 'AlertEvent'
        m2m_table_name = db.shorten_name(u'account_alertevent_keywords')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('alertevent', models.ForeignKey(orm[u'account.alertevent'], null=False)),
            ('keywordservice', models.ForeignKey(orm[u'keywords.keywordservice'], null=False))
        ))
        db.create_unique(m2m_table_name, ['alertevent_id', 'keywordservice_id'])

        # Adding M2M table for field user_keywords on 'AlertEvent'
        m2m_table_name = db.shorten_name(u'account_alertevent_user_keywords')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('alertevent', models.ForeignKey(orm[u'account.alertevent'], null=False)),
            ('userkeywordservice', models.ForeignKey(orm[u'keywords.userkeywordservice'], null=False))
        ))
        db.create_unique(m2m_table_name, ['alertevent_id', 'userkeywordservice_id'])

        # Adding model 'AlertSystem'
        db.create_table(u'account_alertsystem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='alert_system_user', to=orm['member.UserProfile'])),
            ('signup', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('activation', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('password_recovery', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('new_message_received', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('feedback_received', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('attendee_registred', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('frequency_attendee', self.gf('django.db.models.fields.CharField')(default='immediate', max_length=15, db_index=True)),
            ('nbr_email', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nbr_alert', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_sent_email', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'account', ['AlertSystem'])

        # Adding model 'AlertSent'
        db.create_table(u'account_alertsent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='alert_sent_user', to=orm['member.UserProfile'])),
            ('alert', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='alertad_sent_user', null=True, to=orm['account.AlertEvent'])),
            ('alert_system', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='alertsys_sent_user', null=True, to=orm['account.AlertSystem'])),
            ('sent_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='alert_authored_events', to=orm['event.Event'])),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='alert_authored_message', null=True, to=orm['member.Message'])),
            ('frequency', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('type_alert', self.gf('django.db.models.fields.CharField')(default='event', max_length=10)),
        ))
        db.send_create_signal(u'account', ['AlertSent'])

        # Adding model 'Application'
        db.create_table(u'account_application', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('application', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'account', ['Application'])

        # Adding model 'Parameters'
        db.create_table(u'account_parameters', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Application'])),
            ('group', self.gf('django.db.models.fields.CharField')(default='contact', max_length=100)),
            ('key', self.gf('django.db.models.fields.CharField')(default='DEPARTMENT', max_length=100)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('sequence', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('flatpage', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('staticpage', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('enable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('help', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('array', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('url_href', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
        ))
        db.send_create_signal(u'account', ['Parameters'])


    def backwards(self, orm):
        # Deleting model 'AlertEvent'
        db.delete_table(u'account_alertevent')

        # Removing M2M table for field keywords on 'AlertEvent'
        db.delete_table(db.shorten_name(u'account_alertevent_keywords'))

        # Removing M2M table for field user_keywords on 'AlertEvent'
        db.delete_table(db.shorten_name(u'account_alertevent_user_keywords'))

        # Deleting model 'AlertSystem'
        db.delete_table(u'account_alertsystem')

        # Deleting model 'AlertSent'
        db.delete_table(u'account_alertsent')

        # Deleting model 'Application'
        db.delete_table(u'account_application')

        # Deleting model 'Parameters'
        db.delete_table(u'account_parameters')


    models = {
        u'account.alertevent': {
            'Meta': {'object_name': 'AlertEvent'},
            'activated': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'distance': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'alert_user_event'", 'null': 'True', 'to': u"orm['event.Event']"}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_send_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'alert_keywords'", 'symmetrical': 'False', 'to': u"orm['keywords.KeywordService']"}),
            'last_sent_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'location_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'nbr_alert': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_sent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'received_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alert_user'", 'to': u"orm['member.UserProfile']"}),
            'user_keywords': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'alert_user_keywords'", 'symmetrical': 'False', 'to': u"orm['keywords.UserKeywordService']"})
        },
        u'account.alertsent': {
            'Meta': {'object_name': 'AlertSent'},
            'alert': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'alertad_sent_user'", 'null': 'True', 'to': u"orm['account.AlertEvent']"}),
            'alert_system': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'alertsys_sent_user'", 'null': 'True', 'to': u"orm['account.AlertSystem']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alert_authored_events'", 'to': u"orm['event.Event']"}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'alert_authored_message'", 'null': 'True', 'to': u"orm['member.Message']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'type_alert': ('django.db.models.fields.CharField', [], {'default': "'event'", 'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alert_sent_user'", 'to': u"orm['member.UserProfile']"})
        },
        u'account.alertsystem': {
            'Meta': {'object_name': 'AlertSystem'},
            'activation': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'attendee_registred': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'feedback_received': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'frequency_attendee': ('django.db.models.fields.CharField', [], {'default': "'immediate'", 'max_length': '15', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_sent_email': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'nbr_alert': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_email': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_message_received': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password_recovery': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'signup': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alert_system_user'", 'to': u"orm['member.UserProfile']"})
        },
        u'account.application': {
            'Meta': {'object_name': 'Application'},
            'application': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        u'account.parameters': {
            'Meta': {'object_name': 'Parameters'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.Application']"}),
            'array': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'enable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'flatpage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'group': ('django.db.models.fields.CharField', [], {'default': "'contact'", 'max_length': '100'}),
            'help': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'DEPARTMENT'", 'max_length': '100'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'staticpage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url_href': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'})
        },
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
            'followed': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'event_followed_user'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['member.UserProfile']"}),
            'google_analytics': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'keywords': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_keywords'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['keywords.KeywordService']"}),
            'main_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'main'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['event.EventImageExtend']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'event_organizer'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['event.Organizer']"}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'event_user_profile'", 'null': 'True', 'to': u"orm['member.UserProfile']"}),
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
        u'keywords.keywordservice': {
            'Meta': {'object_name': 'KeywordService'},
            'can_add': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_event': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_system': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'keyword': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'link_keyword': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'link_keyword2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'link_keyword3': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'migrated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'main_keyword'", 'null': 'True', 'to': u"orm['keywords.MainKeywordService']"}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'sub_category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sub_category'", 'null': 'True', 'to': u"orm['keywords.SubCategKeywords']"})
        },
        u'keywords.mainkeywordservice': {
            'Meta': {'object_name': 'MainKeywordService'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'icon': ('django.db.models.fields.CharField', [], {'default': "'user'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_system': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'db_index': 'True'})
        },
        u'keywords.subcategkeywords': {
            'Meta': {'object_name': 'SubCategKeywords'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_system': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'migrated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'main_subcateg_keyword'", 'null': 'True', 'to': u"orm['keywords.MainKeywordService']"})
        },
        u'keywords.userkeywordservice': {
            'Meta': {'object_name': 'UserKeywordService'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'author_keywords'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_migrated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'author_keywords_event'", 'null': 'True', 'to': u"orm['event.Event']"}),
            'event_posted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_rejected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'keyword': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'db_index': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'default': "'user'", 'max_length': '50'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'nbr_same': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'origin': ('django.db.models.fields.CharField', [], {'default': "'event'", 'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_keyword'", 'null': 'True', 'to': u"orm['keywords.MainKeywordService']"}),
            'reason': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'db_index': 'True'}),
            'sub_category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_sub_category'", 'null': 'True', 'to': u"orm['keywords.SubCategKeywords']"})
        },
        u'member.comments': {
            'Meta': {'object_name': 'Comments'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'userprofile_comments'", 'to': u"orm['member.UserProfile']"}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_comments'", 'to': u"orm['event.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'send_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'member.message': {
            'Meta': {'object_name': 'Message'},
            'archived': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2'}),
            'attached': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'chain_start': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'chain'", 'null': 'True', 'to': u"orm['member.Message']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'deleted': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2'}),
            'email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'member_event_messages'", 'null': 'True', 'to': u"orm['event.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined_files': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'message_joinded_files'", 'symmetrical': 'False', 'to': u"orm['multiuploader.MultiuploaderFiles']"}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'origin': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'read_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'member_received_messages'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'removed_by': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'member_sent_messages'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '30', 'db_index': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'threads': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'message_chained_threads'", 'symmetrical': 'False', 'to': u"orm['member.MessageThread']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'event_created'", 'max_length': '30'})
        },
        u'member.messagethread': {
            'Meta': {'object_name': 'MessageThread'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'read_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'member_received_messages_thread'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'respond_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'root_message': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'root_message_key'", 'null': 'True', 'to': u"orm['member.Message']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'member_sent_messages_thread'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status_thread': ('django.db.models.fields.CharField', [], {'default': "'root'", 'max_length': '30', 'db_index': 'True'})
        },
        u'member.recoveryquestion': {
            'Meta': {'object_name': 'RecoveryQuestion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'member.userlanguage': {
            'Meta': {'object_name': 'userLanguage'},
            'code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        u'member.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'about_customer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'avg_ratings': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'}),
            'avg_ratings_efficiency': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'}),
            'avg_ratings_expense': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'}),
            'avg_ratings_knowledge': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'}),
            'avg_ratings_professionalism': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'}),
            'avg_ratings_quality': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'profile_user_comments'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['member.Comments']"}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['event.Currency']", 'null': 'True', 'blank': 'True'}),
            'date_closed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'event_for_member'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['event.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'profile_images'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['multiuploader.MultiuploaderImage']"}),
            'ip_location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'is_attendee': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_organizer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_suspended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'keywords': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'profile_keywords'", 'symmetrical': 'False', 'to': u"orm['keywords.KeywordService']"}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member.userLanguage']", 'null': 'True', 'blank': 'True'}),
            'last_notification_sent_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'location_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'main_image': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'media_mode': ('django.db.models.fields.CharField', [], {'default': "'image'", 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member.RecoveryQuestion']", 'null': 'True', 'blank': 'True'}),
            'reason_closed': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'reason_suspended': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'reviews': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'video_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'youtube_url': ('video.fields.YouTubeField', [], {'max_length': '100', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        u'multiuploader.multiuploaderfiles': {
            'Meta': {'object_name': 'MultiuploaderFiles'},
            'application': ('django.db.models.fields.CharField', [], {'default': "'team'", 'max_length': '30'}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'event_upload_files'", 'null': 'True', 'to': u"orm['event.Event']"}),
            'file_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_data': ('django.db.models.fields.CharField', [], {'max_length': '90', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'upload_messages_files'", 'null': 'True', 'to': u"orm['member.Message']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'upload_files'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'multiuploader.multiuploaderimage': {
            'Meta': {'object_name': 'MultiuploaderImage'},
            'about': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'application': ('django.db.models.fields.CharField', [], {'default': "'team'", 'max_length': '30'}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'event_upload_images'", 'null': 'True', 'to': u"orm['event.Event']"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django_resized.forms.ResizedImageField', [], {'max_length': '100', 'max_width': '800', 'max_height': '600'}),
            'image_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'is_inappropriate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_irrelevant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'key_data': ('django.db.models.fields.CharField', [], {'max_length': '90', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'size': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'userprofile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'profile_images'", 'null': 'True', 'to': u"orm['member.UserProfile']"})
        }
    }

    complete_apps = ['account']