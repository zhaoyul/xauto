# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'keywords_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='parent_category', null=True, to=orm['keywords.MainKeywordService'])),
            ('can_add', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='category_owner', null=True, to=orm['auth.User'])),
            ('date_add', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'keywords', ['Category'])

        # Adding unique constraint on 'Category', fields ['parent', 'name']
        db.create_unique(u'keywords_category', ['parent_id', 'name'])

        # Adding model 'MainKeywordService'
        db.create_table(u'keywords_mainkeywordservice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_system', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('icon', self.gf('django.db.models.fields.CharField')(default='user', max_length=100)),
            ('event_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'keywords', ['MainKeywordService'])

        # Adding model 'SubCategKeywords'
        db.create_table(u'keywords_subcategkeywords', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100, db_index=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='main_subcateg_keyword', null=True, to=orm['keywords.MainKeywordService'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_system', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('event_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('migrated', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'keywords', ['SubCategKeywords'])

        # Adding model 'KeywordService'
        db.create_table(u'keywords_keywordservice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='main_keyword', null=True, to=orm['keywords.MainKeywordService'])),
            ('keyword', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('sub_category', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sub_category', null=True, to=orm['keywords.SubCategKeywords'])),
            ('link_keyword', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, db_index=True, blank=True)),
            ('link_keyword2', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, db_index=True, blank=True)),
            ('link_keyword3', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, db_index=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_system', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_event', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_add', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('event_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('date_add', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('migrated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'keywords', ['KeywordService'])

        # Adding model 'UserKeywordService'
        db.create_table(u'keywords_userkeywordservice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_keyword', null=True, to=orm['keywords.MainKeywordService'])),
            ('keyword', self.gf('django.db.models.fields.CharField')(default='', max_length=100, db_index=True)),
            ('sub_category', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_sub_category', null=True, to=orm['keywords.SubCategKeywords'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='author_keywords', null=True, to=orm['auth.User'])),
            ('is_rejected', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_accepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reason', self.gf('django.db.models.fields.CharField')(default='', max_length=100, db_index=True)),
            ('date_migrated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='author_keywords_event', null=True, to=orm['event.Event'])),
            ('nbr_same', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('origin', self.gf('django.db.models.fields.CharField')(default='event', max_length=50)),
            ('mode', self.gf('django.db.models.fields.CharField')(default='user', max_length=50)),
            ('email_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('event_posted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'keywords', ['UserKeywordService'])

        # Adding model 'ForbiddenUserKeywordService'
        db.create_table(u'keywords_forbiddenuserkeywordservice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('keyword', self.gf('django.db.models.fields.CharField')(default='', max_length=100, db_index=True)),
            ('is_forbidden', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('reason', self.gf('django.db.models.fields.CharField')(default='', max_length=100, db_index=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'keywords', ['ForbiddenUserKeywordService'])

        # Adding model 'KeywordService2'
        db.create_table(u'keywords_keywordservice2', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='main_keyword2', null=True, to=orm['keywords.MainKeywordService2'])),
            ('keyword', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='main_category2', null=True, to=orm['keywords.Category'])),
            ('sub_category', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sub_category2', null=True, to=orm['keywords.SubCategKeywords2'])),
            ('link_keyword', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, db_index=True, blank=True)),
            ('link_keyword2', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, db_index=True, blank=True)),
            ('link_keyword3', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, db_index=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_system', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_job_catpage', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_provider_catpage', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_header_search', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_account_page', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('can_add', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('job_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('provider_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('date_add', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('migrated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'keywords', ['KeywordService2'])

        # Adding model 'SubCategKeywords2'
        db.create_table(u'keywords_subcategkeywords2', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100, db_index=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='main_subcateg_keyword2', null=True, to=orm['keywords.MainKeywordService2'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_system', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('job_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('provider_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('migrated', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'keywords', ['SubCategKeywords2'])

        # Adding model 'MainKeywordService2'
        db.create_table(u'keywords_mainkeywordservice2', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_system', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('icon', self.gf('django.db.models.fields.CharField')(default='user', max_length=100)),
            ('job_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('provider_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'keywords', ['MainKeywordService2'])


    def backwards(self, orm):
        # Removing unique constraint on 'Category', fields ['parent', 'name']
        db.delete_unique(u'keywords_category', ['parent_id', 'name'])

        # Deleting model 'Category'
        db.delete_table(u'keywords_category')

        # Deleting model 'MainKeywordService'
        db.delete_table(u'keywords_mainkeywordservice')

        # Deleting model 'SubCategKeywords'
        db.delete_table(u'keywords_subcategkeywords')

        # Deleting model 'KeywordService'
        db.delete_table(u'keywords_keywordservice')

        # Deleting model 'UserKeywordService'
        db.delete_table(u'keywords_userkeywordservice')

        # Deleting model 'ForbiddenUserKeywordService'
        db.delete_table(u'keywords_forbiddenuserkeywordservice')

        # Deleting model 'KeywordService2'
        db.delete_table(u'keywords_keywordservice2')

        # Deleting model 'SubCategKeywords2'
        db.delete_table(u'keywords_subcategkeywords2')

        # Deleting model 'MainKeywordService2'
        db.delete_table(u'keywords_mainkeywordservice2')


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
        u'keywords.category': {
            'Meta': {'ordering': "['can_add', 'name']", 'unique_together': "[('parent', 'name')]", 'object_name': 'Category'},
            'can_add': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'category_owner'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'parent_category'", 'null': 'True', 'to': u"orm['keywords.MainKeywordService']"})
        },
        u'keywords.forbiddenuserkeywordservice': {
            'Meta': {'object_name': 'ForbiddenUserKeywordService'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_forbidden': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'db_index': 'True'})
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
        u'keywords.keywordservice2': {
            'Meta': {'object_name': 'KeywordService2'},
            'can_add': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'main_category2'", 'null': 'True', 'to': u"orm['keywords.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_account_page': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_header_search': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_job_catpage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_provider_catpage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_system': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'keyword': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'link_keyword': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'link_keyword2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'link_keyword3': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'migrated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'main_keyword2'", 'null': 'True', 'to': u"orm['keywords.MainKeywordService2']"}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'provider_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'sub_category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sub_category2'", 'null': 'True', 'to': u"orm['keywords.SubCategKeywords2']"})
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
        u'keywords.mainkeywordservice2': {
            'Meta': {'object_name': 'MainKeywordService2'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'icon': ('django.db.models.fields.CharField', [], {'default': "'user'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_system': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'db_index': 'True'}),
            'provider_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
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
        u'keywords.subcategkeywords2': {
            'Meta': {'object_name': 'SubCategKeywords2'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_system': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'migrated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'main_subcateg_keyword2'", 'null': 'True', 'to': u"orm['keywords.MainKeywordService2']"}),
            'provider_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
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

    complete_apps = ['keywords']