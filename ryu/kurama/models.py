from django.db import models

class TasksList(models.Model):
    tasksListId = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=50)
    updated = models.DateTimeField('last modification time')
    selfLink = models.URLField('tasks list url')

class Task(models.Model):
    tasksList = models.ForeignKey(TasksList)
    taskId = models.CharField(max_length=100, primary_key=True)
    tag = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    updated = models.DateTimeField('updated')
    selfLink = models.URLField('task url')
    parent = models.CharField(max_length=100)
    positon = models.BigIntegerField()
    notes = models.CharField(max_length=1000)
    status = models.CharField(max_length=15)
    due = models.DateTimeField('task due')
    completed = models.DateTimeField('completed on')
    deleted = models.BooleanField()
    hidden = models.BooleanField()
    linkDescp = models.CharField(max_length=200)
    linkUrl = models.URLField()
    linkType = models.CharField(max_length=20)

