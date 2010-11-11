# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserProfile'
        db.create_table('server_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('credit', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('experience', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('reputation', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('server', ['UserProfile'])

        # Adding model 'ShipAttributes'
        db.create_table('server_shipattributes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('weight', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('speed', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('acceleration', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('sockets', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('bombs', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('server', ['ShipAttributes'])

        # Adding model 'ShipModel'
        db.create_table('server_shipmodel', (
            ('shipattributes_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['server.ShipAttributes'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('price', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('server', ['ShipModel'])

        # Adding model 'Upgrade'
        db.create_table('server_upgrade', (
            ('shipattributes_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['server.ShipAttributes'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('price', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('server', ['Upgrade'])

        # Adding model 'Ship'
        db.create_table('server_ship', (
            ('shipattributes_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['server.ShipAttributes'], unique=True, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ships', unique=True, to=orm['auth.User'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['server.ShipModel'])),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('experience', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('server', ['Ship'])

        # Adding M2M table for field upgrades on 'Ship'
        db.create_table('server_ship_upgrades', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ship', models.ForeignKey(orm['server.ship'], null=False)),
            ('upgrade', models.ForeignKey(orm['server.upgrade'], null=False))
        ))
        db.create_unique('server_ship_upgrades', ['ship_id', 'upgrade_id'])

        # Adding model 'Battle'
        db.create_table('server_battle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('map', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.Map'])),
            ('rounds', self.gf('django.db.models.fields.IntegerField')(default=5)),
        ))
        db.send_create_signal('server', ['Battle'])

        # Adding model 'ShipsInBattle'
        db.create_table('server_shipsinbattle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ship', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.Ship'])),
            ('battle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.Battle'])),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('kills', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lives', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('server', ['ShipsInBattle'])

        # Adding unique constraint on 'ShipsInBattle', fields ['ship', 'battle']
        db.create_unique('server_shipsinbattle', ['ship_id', 'battle_id'])

        # Adding model 'Map'
        db.create_table('server_map', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('players', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('reputation', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('server', ['Map'])

        # Adding model 'Message'
        db.create_table('server_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_from', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('user_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('subject', self.gf('django.db.models.fields.TextField')(default='')),
            ('text', self.gf('django.db.models.fields.TextField')(default='')),
            ('viewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('server', ['Message'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'ShipsInBattle', fields ['ship', 'battle']
        db.delete_unique('server_shipsinbattle', ['ship_id', 'battle_id'])

        # Deleting model 'UserProfile'
        db.delete_table('server_userprofile')

        # Deleting model 'ShipAttributes'
        db.delete_table('server_shipattributes')

        # Deleting model 'ShipModel'
        db.delete_table('server_shipmodel')

        # Deleting model 'Upgrade'
        db.delete_table('server_upgrade')

        # Deleting model 'Ship'
        db.delete_table('server_ship')

        # Removing M2M table for field upgrades on 'Ship'
        db.delete_table('server_ship_upgrades')

        # Deleting model 'Battle'
        db.delete_table('server_battle')

        # Deleting model 'ShipsInBattle'
        db.delete_table('server_shipsinbattle')

        # Deleting model 'Map'
        db.delete_table('server_map')

        # Deleting model 'Message'
        db.delete_table('server_message')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Map']"}),
            'rounds': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'ships': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'battles'", 'symmetrical': 'False', 'through': "orm['server.ShipsInBattle']", 'to': "orm['server.Ship']"})
        },
        'server.map': {
            'Meta': {'object_name': 'Map'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'players': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'reputation': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'server.message': {
            'Meta': {'object_name': 'Message'},
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
            'upgrades': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['server.Upgrade']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ships'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'server.shipattributes': {
            'Meta': {'object_name': 'ShipAttributes'},
            'acceleration': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'bombs': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sockets': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'speed': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '100'})
        },
        'server.shipmodel': {
            'Meta': {'object_name': 'ShipModel', '_ormbases': ['server.ShipAttributes']},
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'shipattributes_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['server.ShipAttributes']", 'unique': 'True', 'primary_key': 'True'})
        },
        'server.shipsinbattle': {
            'Meta': {'unique_together': "(('ship', 'battle'),)", 'object_name': 'ShipsInBattle'},
            'battle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Battle']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kills': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'lives': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ship': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Ship']"})
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
            'credit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'experience': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reputation': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['server']
