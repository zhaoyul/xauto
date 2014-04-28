# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def add_cur(self, orm, country, country_code, currency, symbol):
        orm.Currency.objects.get_or_create(country=country,
                                           country_code=country_code,
                                           currency=currency,
                                           symbol=symbol)

    def forwards(self, orm):
        #orm.Currency.objects.all().delete()

        self.add_cur(orm,"Argentina","","ARS","$")
        self.add_cur(orm,"Australia","","AUD","$")
        self.add_cur(orm,"Brazil","","BRL","R$")
        self.add_cur(orm,"Canada","","CAD","$")
        self.add_cur(orm,"China","","CNY","¥")
        self.add_cur(orm,"Czech Republic","","CZK","Kč")

        self.add_cur(orm,"Denmark","","DKK","kr")
        self.add_cur(orm,"Egypt","","EGP","£")

        self.add_cur(orm,"Hong Kong","","HKD","$")
        self.add_cur(orm,"Hungary","","HUF","Ft")

        self.add_cur(orm,"Iceland","","ISK","kr")
        self.add_cur(orm,"India","","INR","")
        self.add_cur(orm,"Indonesia","","IDR","Rp")
        self.add_cur(orm,"Iran","","IRR","")

        self.add_cur(orm,"Israel","","ILS","₪")
        self.add_cur(orm,"Japan","","JPY","¥")
        self.add_cur(orm,"Korea","","KRW","₩")
        self.add_cur(orm,"Lebanon","","LBP","£")

        self.add_cur(orm,"Malaysia","","MYR","RM")
        self.add_cur(orm,"Mexico","","MXN","$")
        self.add_cur(orm,"New Zealand","","NZD","$")
        self.add_cur(orm,"Norway","","NOK","kr")
        self.add_cur(orm,"Oman","","OMR","﷼")

        self.add_cur(orm,"Philippines","","PHP","₱")
        self.add_cur(orm,"Poland","","PLN","zł")
        self.add_cur(orm,"Qatar","","QAR","﷼")
        self.add_cur(orm,"Romania","","RON","lei")
        self.add_cur(orm,"Russia","","RUB","руб")

        self.add_cur(orm,"Saudi Arabia","","SAR","﷼")
        self.add_cur(orm,"Singapore","","SGD","$")
        self.add_cur(orm,"South Africa","","ZAR","R")
        self.add_cur(orm,"Sweden","","SEK","kr")
        self.add_cur(orm,"Switzerland","","CHF","CHF")
        self.add_cur(orm,"Thailand","","THB","฿")
        self.add_cur(orm,"Turkey","","TRY","")
        self.add_cur(orm,"United Arab Emirates","","AED","")
        self.add_cur(orm,"United Kingdom","","GBP","£")
        self.add_cur(orm,"United States","","USD","$")
        self.add_cur(orm,"Viet Nam","","VND","₫")
        self.add_cur(orm,"Yemen","","YER","﷼")

        #with euro
        self.add_cur(orm,"Austria","","EUR","€")
        self.add_cur(orm,"Belgium","","EUR","€")
        self.add_cur(orm,"Bulgaria","","EUR","€")
        self.add_cur(orm,"Croatia","","EUR","€")
        self.add_cur(orm,"Cyprus","","EUR","€")
        self.add_cur(orm,"Czech Republic","","EUR","€")

        self.add_cur(orm,"Denmark","","EUR","€")
        self.add_cur(orm,"Estonia","","EUR","€")
        self.add_cur(orm,"Finland","","EUR","€")
        self.add_cur(orm,"France","","EUR","€")
        self.add_cur(orm,"Germany","","EUR","€")
        self.add_cur(orm,"Greece","","EUR","€")
        self.add_cur(orm,"Hungary","","EUR","€")
        self.add_cur(orm,"Ireland","","EUR","€")
        self.add_cur(orm,"Italy","","EUR","€")
        self.add_cur(orm,"Latvia","","EUR","€")
        self.add_cur(orm,"Lithuania","","EUR","€")
        self.add_cur(orm,"Luxembourg","","EUR","€")
        self.add_cur(orm,"Malta","","EUR","€")
        self.add_cur(orm,"Netherlands","","EUR","€")
        self.add_cur(orm,"Poland","","EUR","€")
        self.add_cur(orm,"Portugal","","EUR","€")
        self.add_cur(orm,"Romania","","EUR","€")
        self.add_cur(orm,"Slovakia","","EUR","€")
        self.add_cur(orm,"Slovenia","","EUR","€")
        self.add_cur(orm,"Spain","","EUR","€")
        self.add_cur(orm,"Sweden","","EUR","€")
        self.add_cur(orm,"United Kingdom","","EUR","€")



    def backwards(self, orm):
        orm.Currency.objects.filter(country_code='').delete()
        "Write your backwards methods here."

    models = {
        u'account.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'activationtoken': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'null': 'True', 'db_column': "'activationToken'", 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'followed': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'followed_profiles'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['account.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'location_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'main_image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '255'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name'"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'thumbnail_image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'0.0'", 'max_length': '30'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
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
            'about': ('django.db.models.fields.TextField', [], {}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'authored_event'", 'null': 'True', 'to': u"orm['account.UserProfile']"}),
            'capacity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'eventSize': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'followed': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'followed_events'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['account.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'main'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['event.EventImage']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'short_link': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '50'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'short_link'"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '15', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'event.eventdate': {
            'Meta': {'object_name': 'EventDate'},
            'address_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'attend_free': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'attend_price_from': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'attend_price_to': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'country_short': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['event.Currency']", 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_dates'", 'to': u"orm['event.Event']"}),
            'exhibit_free': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'exhibit_price_from': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'exhibit_price_to': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'feature_detail': ('django.db.models.fields.TextField', [], {}),
            'feature_headline': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'location_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'shared': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'shared_dates'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['account.UserProfile']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        u'event.eventimage': {
            'Meta': {'object_name': 'EventImage'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['event']
    symmetrical = True
