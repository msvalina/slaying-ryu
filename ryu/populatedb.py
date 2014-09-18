#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import string
import gflags
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from datetime import date, timedelta
from kurama.models import TaskList, Task, Project

class PopulateDB:

    clientID = ""
    clientSecret = ""
    apiKey = ""
    service = None

    def __init__(self):
        if os.path.isfile("tasks.dat"):
            self.getService()
            self.setEnv()
        else:
            try:
                with open("keys.txt", "r") as self.f:
                    self.clientID = self.f.readline().rstrip()
                    self.clientSecret = self.f.readline().rstrip()
                    self.apiKey = self.f.readline().rstrip()
            except IOError:
                self.clientID = raw_input("Enter your client id: ")
                self.clientSecret = raw_input("Enter your client secret: ")
                self.apiKey = raw_input("Enter your api key: ")
                self.writeAuth()
            self.getService()
            self.setEnv()

    def writeAuth(self):
        with open("keys.txt", "w") as self.fw:
            self.fw.write(str(self.clientID) + "\n")
            self.fw.write(str(self.clientSecret) + "\n")
            self.fw.write(str(self.apiKey) + "\n")

    def getService(self):
        FLAGS = gflags.FLAGS

        # Set up a Flow object to be used if we need to authenticate. This
        # sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
        # the information it needs to authenticate. Note that it is called
        # the Web Server Flow, but it can also handle the flow for native
        # applications
        # The client_id and client_secret are copied from the API Access tab on
        # the Google APIs Console
        FLOW = OAuth2WebServerFlow(
            client_id = self.clientID,
            client_secret = self.clientSecret,
            scope='https://www.googleapis.com/auth/tasks',
            user_agent='PopulateDB/0.0.1')

        # To disable the local server feature, uncomment the following line:
        FLAGS.auth_local_webserver = False

        # If the Credentials don't exist or are invalid, run through the native
        # client flow. The Storage object will ensure that if successful the
        # good Credentials will get written back to a file.
        storage = Storage('tasks.dat')
        credentials = storage.get()
        if credentials is None or credentials.invalid == True:
            credentials = run(FLOW, storage)

        # Create an httplib2.Http object to handle our HTTP requests and
        # authorize it with our good Credentials.
        http = httplib2.Http()
        http = credentials.authorize(http)

        # Build a service object for interacting with the API. Visit
        # the Google APIs Console
        # to get a developerKey for your own application.
        # I used API key for Browser applications
        self.service = build(serviceName='tasks', version='v1', http=http,
                             developerKey=self.apiKey)

    def setEnv(self):
        # Seting python and djagno env var
        ryuDir = os.path.dirname(os.path.realpath(__file__))
        sys.path.append(ryuDir)
        os.environ['DJANGO_SETTINGS_MODULE'] = 'ryu.settings'

    def getTaskLists(self):
        tagList = self.getProjectLists()
        taskLists = self.service.tasklists().list().execute()
        # Save every tasklist that's in usedLists to database
        usedLists = ['01-Im&Ds', '02-Im&Nds', '03-Ni&Ds', '04-Ni&Nds']
        for tl in taskLists['items']:
            if tl['title'] in usedLists:
                print "Saving task list: "
                print tl['title']
                listEntry = TaskList(taskListId=tl['id'],
                                      title=tl['title'],
                                      updated=tl['updated'],
                                      selfLink=tl['selfLink'])
                listEntry.save()

                # Get completed tasks from January first 2014 until today
                today = date.today().strftime('%Y-%m-%dT00:00:00Z')
                tasks = self.service.tasks().list(
                            tasklist=tl['id'],
                            completedMin="2014-01-01T00:00:00Z",
                            completedMax=today,
                            showHidden="True").execute()

                for tsk in tasks['items']:
                    # Set default task tag to *raz* in case there is no tag in
                    # Project List
                    taskTag = "*raz*"
                    taskTitle = tsk['title'].strip()
                    print tsk['title']

                    # Get task tag from tagList insted of directly spliting from
                    # task name, so now task which has tag without space before
                    # title can be recongnized correctly
                    for tag in tagList:
                        if tag in tsk['title']:
                            taskTag = tag
                            taskTitle = string.replace(tsk['title'], tag, "")
                            taskTitle = taskTitle.strip()
                    # Save fetched task in corresponding db field
                    taskEntry = Task(taskList=listEntry,
                                     taskId=tsk['id'],
                                     tag=taskTag,
                                     title=taskTitle,
                                     updated=tsk['updated'],
                                     selfLink=tsk['selfLink'],
                                     parent=tsk.get('parent', None),
                                     position=tsk['position'],
                                     notes=tsk.get('notes', None),
                                     status=tsk['status'],
                                     due=tsk.get('due', None),
                                     completed=tsk['completed'])
                    taskEntry.save()

    def getProjectLists(self):
        taskLists = self.service.tasklists().list().execute()
        tagList = []
        for tl in taskLists['items']:
            if tl['title'] == "Projects list":
                print tl['title']
                tasks = self.service.tasks().list(tasklist=tl['id']).execute()
                for tsk in tasks['items']:
                    tag = string.split(tsk['title'], "-")[0].strip()
                    title = string.split(tsk['title'], "-")[1].strip()
                    projectEntry = Project(
                        tag=tag,
                        name=title,
                        position=tsk['position'],
                        notes=tsk.get('notes', None),
                        status=tsk['status'],
                        due=tsk.get('due', None),
                        completed=tsk.get('completed', None))
                    projectEntry.save()
                    tagList.append(tag)
                    print tsk['title']
        return tagList

def main():
    populateDB = PopulateDB()
    populateDB.getTaskLists()

if __name__ == '__main__':
    main()
