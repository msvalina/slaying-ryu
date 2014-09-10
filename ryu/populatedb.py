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
from kurama.models import Task, TasksList, Project

class PopulateDB:

    client_id = ""
    client_secret = ""
    apikey = ""
    service = None

    def __init__(self):
        if (os.path.isfile("tasks.dat")):
            self.getService()
            self.setEnv()
        else:
            try:
                with open("keys.txt", "r") as self.f:
                    self.client_id = self.f.readline().rstrip()
                    self.client_secret = self.f.readline().rstrip()
                    self.apikey = self.f.readline().rstrip()
            except IOError:
                self.client_id = raw_input("Enter your client id: ")
                self.client_secret = raw_input("Enter your client secret: ")
                self.apikey = raw_input("Enter your api key: ")
                self.writeAuth()
            self.getService()
            self.setEnv()

    def writeAuth(self):
        with open("keys.txt", "w") as self.fw:
            self.fw.write(str(self.client_id) + "\n")
            self.fw.write(str(self.client_secret) + "\n")
            self.fw.write(str(self.apikey) + "\n")

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
            client_id = self.client_id,
            client_secret = self.client_secret,
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

        # Create an httplib2.Http object to handle our HTTP requests and authorize it
        # with our good Credentials.
        http = httplib2.Http()
        http = credentials.authorize(http)

        # Build a service object for interacting with the API. Visit
        # the Google APIs Console
        # to get a developerKey for your own application.
        # I used API key for Browser applications
        self.service = build(serviceName='tasks', version='v1', http=http,
                             developerKey=self.apikey)

    def setEnv(self):
        # Seting python and djagno env var
        ryudir = os.path.dirname(os.path.realpath(__file__))
        sys.path.append(ryudir)
        os.environ['DJANGO_SETTINGS_MODULE'] = 'ryu.settings'

    def getTaskLists(self):
        tasklists = self.service.tasklists().list().execute()
        # Save every tasklist that's in usedLists to database
        usedLists = ['01-Im&Ds', '02-Im&Nds', '03-Ni&Ds', '04-Ni&Nds']
        for tl in tasklists['items']:
            if (tl['title'] in usedLists):
                print "Saving task list: "
                print tl['title']
                listEntry = TasksList(tasksListId = tl['id'],
                                      title = tl['title'],
                                      updated = tl['updated'],
                                      selfLink = tl['selfLink'])
                listEntry.save()

                # Get complited tasks from January first 2014 until today
                today = date.today().strftime('%Y-%m-%dT00:00:00Z')
                tasks = self.service.tasks().list(
                            tasklist=tl['id'],
                            completedMin="2014-01-01T00:00:00Z",
                            completedMax=today,
                            showHidden="True").execute()

                for t in tasks['items']:
                    print t['title']
                    # Get special tag "=" which is in form "=Commit last changes"
                    # Every other task is in form "$rn$ Pay your rent dude"
                    if (t['title'][0] == "="):
                        foundTag = t['title'][0]
                        foundTitle = t['title'][1:]
                    else:
                        foundTag = string.split(t['title'])[0].strip()
                        foundTitle  = string.split(t['title'], ' ', 1)[1].strip()
                    # Save fetched task in corresponding db field
                    taskEntry = Task(tasksList = listEntry,
                                     taskId = t['id'],
                                     tag = foundTag,
                                     title = foundTitle,
                                     updated = t['updated'],
                                     selfLink = t['selfLink'],
                                     parent = t.get('parent', None),
                                     position = t['position'],
                                     notes = t.get('notes', None),
                                     status = t['status'],
                                     due = t.get('due', None),
                                     completed = t['completed'])
                    taskEntry.save()

    def getProjectLists(self):
        tasklists = self.service.tasklists().list().execute()
        for tl in tasklists['items']:
            if (tl['title'] == "Projects list"):
                print tl['title']
                tasks = self.service.tasks().list(tasklist=tl['id']).execute()
                for t in tasks['items']:
                    projectEntry = Project(
                        tag = string.split(t['title'],"-")[0].strip(),
                        name = string.split(t['title'],"-")[1].strip(),
                        position = t['position'],
                        notes = t.get('notes', None),
                        status = t['status'],
                        due = t.get('due', None),
                        completed = t.get('completed', None))
                    projectEntry.save()
                    print t['title']

def main():
    populateDB = PopulateDB()
    populateDB.getTaskLists()
    populateDB.getProjectLists()

if __name__ == '__main__':
    main()
