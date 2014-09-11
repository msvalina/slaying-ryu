import datetime
from django.db import models

class TaskLists(models.Model):
    taskListId = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=50)
    updated = models.DateTimeField('last modification time')
    selfLink = models.URLField('tasks list url')
    def __unicode__(self):
        out  = self.title + " updated: " + \
                self.updated.strftime('%Y-%m-%d %H:%M:%S')
        return out

class Task(models.Model):
    taskList = models.ForeignKey(TaskLists)
    taskId = models.CharField(max_length=100, primary_key=True)
    tag = models.CharField(max_length=20, null=True, blank=True)
    title = models.CharField(max_length=200)
    updated = models.DateTimeField('last modification time')
    selfLink = models.URLField('task url')
    parent = models.CharField(max_length=100, null=True, blank=True)
    position = models.BigIntegerField()
    notes = models.CharField(max_length=1000, null=True, blank=True)
    status = models.CharField(max_length=15)
    due = models.DateTimeField('task due', null=True, blank=True)
    completed = models.DateTimeField('completed on')
    def __unicode__(self):
        return "Task: " + self.title

class Project(models.Model):
    tag = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    position = models.BigIntegerField()
    description = models.CharField(max_length=1000, null=True, blank=True)
    notes = models.CharField(max_length=1000, null=True, blank=True)
    status = models.CharField(max_length=15)
    due = models.DateTimeField('task due', null=True, blank=True)
    completed = models.DateTimeField('completed on', null=True, blank=True)
    def __unicode__(self):
        return "Project: " + self.name + " tag: " + self.tag
