# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'Ship', fields ['user']
        db.delete_unique('server_ship', ['user_id'])


    def backwards(self, orm):
        
        # Adding unique constraint on 'Ship', fields ['user']
        db.create_unique('server_ship', ['user_id'])


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'server.battle': {
            'Meta': {'object_name': 'Battle'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Map']"}),
            'rounds': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'ships': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'battles'", 'symmetrical': 'False', 'through': "orm['server.ShipsInBattle']", 'to': "orm['server.Ship']"})
        },
        'server.map': {
            'Meta': {'object_name': 'Map'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'players': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'reputation': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'server.message': {
            'Meta': {'object_name': 'Message'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'user_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'user_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'server.ship': {
            'Meta': {'object_name': 'Ship', '_ormbases': ['server.ShipAttributes']},
            'experience': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': "orm['server.ShipModel']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'shipattributes_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['server.ShipAttributes']", 'unique': 'True', 'primary_key': 'True'}),
            'upgrades': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['server.Upgrade']", 'symmetrical': 'False', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ships'", 'to': "orm['auth.User']"})
        },
        'server.shipattributes': {
            'Meta': {'object_name': 'ShipAttributes'},
            'acceleration': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'bombRange': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'bombs': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sockets': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'speed': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '100'})
        },
        'server.shipmodel': {
            'Meta': {'object_name': 'ShipModel', '_ormbases': ['server.ShipAttributes']},
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'shipattributes_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['server.ShipAttributes']", 'unique': 'True', 'primary_key': 'True'})
        },
        'server.shipsinbattle': {
            'Meta': {'unique_together': "(('ship', 'battle'),)", 'object_name': 'ShipsInBattle'},
            'battle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Battle']"}),
            'confirmed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kills': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'lives': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ship': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Ship']"}),
            'user_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'server.upgrade': {
            'Meta': {'object_name': 'Upgrade', '_ormbases': ['server.ShipAttributes']},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'shipattributes_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['server.ShipAttributes']", 'unique': 'True', 'primary_key': 'True'})
        },
        'server.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'credit': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'experience': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reputation': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['server']
