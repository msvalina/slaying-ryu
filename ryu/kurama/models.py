import datetime
from django.db import models

class TaskList(models.Model):
    """ Task List model """
    task_list_id = models.CharField(max_length=100)
    title = models.CharField(max_length=50, primary_key=True)
    updated = models.DateTimeField('last modification time')
    self_link = models.URLField('tasks list url')

    def __unicode__(self):
        return self.title

    def updated_on(self):
        return self.updated.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        """ Metadata for TaskList model fields """
        # Sort ascending by title field
        ordering = ['title']
        # When using latest() return latest by completed field
        get_latest_by = ['-updated']

class Task(models.Model):
    """ Task model """
    task_list = models.ForeignKey(TaskList)
    task_id = models.CharField(max_length=100, primary_key=True)
    tag = models.CharField(max_length=20, null=True, blank=True)
    tag_name = models.CharField(max_length=40, null=True, blank=True)
    title = models.CharField(max_length=200)
    updated = models.DateTimeField('last modification time')
    self_link = models.URLField('task url')
    parent = models.CharField(max_length=100, null=True, blank=True)
    position = models.BigIntegerField()
    notes = models.CharField(max_length=1000, null=True, blank=True)
    status = models.CharField(max_length=15)
    due = models.DateTimeField('task due', null=True, blank=True)
    completed = models.DateTimeField('completed on')

    def __unicode__(self):
        return self.title

    class Meta:
        """ Metadata for Task model fields """
        # Sort descending "-" by completed field
        ordering = ['-completed']
        # When using latest() return latest by completed field
        get_latest_by = 'completed'
        order_with_respect_to = 'task_list'

class Project(models.Model):
    """ Project model """
    tag = models.CharField(max_length=10)
    name = models.CharField(max_length=30, primary_key=True)
    position = models.BigIntegerField()
    description = models.CharField(max_length=1000, null=True, blank=True)
    status = models.CharField(max_length=15)
    due = models.DateTimeField('task due', null=True, blank=True)
    completed = models.DateTimeField('completed on', null=True, blank=True)
    def __unicode__(self):
        return self.name + " tag: " + self.tag

    class Meta:
        """ Metadata for Project model fields """
        # Sort same as postions in gtasks
        ordering = ['position']
