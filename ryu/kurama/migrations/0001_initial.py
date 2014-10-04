# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TaskList'
        db.create_table(u'kurama_tasklist', (
            ('task_list_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('self_link', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'kurama', ['TaskList'])

        # Adding model 'Task'
        db.create_table(u'kurama_task', (
            ('task_list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kurama.TaskList'])),
            ('task_id', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('tag_name', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('self_link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('parent', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.BigIntegerField')()),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('due', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('completed', self.gf('django.db.models.fields.DateTimeField')()),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'kurama', ['Task'])

        # Adding model 'Project'
        db.create_table(u'kurama_project', (
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, primary_key=True)),
            ('position', self.gf('django.db.models.fields.BigIntegerField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('due', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('completed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'kurama', ['Project'])


    def backwards(self, orm):
        # Deleting model 'TaskList'
        db.delete_table(u'kurama_tasklist')

        # Deleting model 'Task'
        db.delete_table(u'kurama_task')

        # Deleting model 'Project'
        db.delete_table(u'kurama_project')


    models = {
        u'kurama.project': {
            'Meta': {'ordering': "['position']", 'object_name': 'Project'},
            'completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'due': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'position': ('django.db.models.fields.BigIntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'kurama.task': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'Task'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'completed': ('django.db.models.fields.DateTimeField', [], {}),
            'due': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.BigIntegerField', [], {}),
            'self_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'tag_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'task_list': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kurama.TaskList']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'kurama.tasklist': {
            'Meta': {'ordering': "['title']", 'object_name': 'TaskList'},
            'info': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'self_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'task_list_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['kurama']