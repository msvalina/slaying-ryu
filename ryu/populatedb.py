#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import gflags
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from datetime import date, timedelta
from kurama.models import Task, TasksList

class Auth():

    client_id = ""
    client_secret = ""
    apikey = ""

    def __init__(self):
        if (os.path.isfile("tasks.dat")):
            self.get_service()
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
                self.write_auth()
            self.get_service()

    def write_auth(self):
        with open("keys.txt", "w") as self.fw:
            self.fw.write(str(self.client_id) + "\n")
            self.fw.write(str(self.client_secret) + "\n")
            self.fw.write(str(self.apikey) + "\n")

    def get_service(self):
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
        service = build(serviceName='tasks', version='v1', http=http,
               developerKey=self.apikey)

        return service

def set_env():
    # Seting python and djagno env var 
    ryudir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(ryudir)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'ryu.settings'

def main():
    service = Auth().get_service()
    tasklists = service.tasklists().list().execute()

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
            tasks = service.tasks().list(tasklist=tl['id'],
                            completedMin="2014-01-01T00:00:00Z",
                            completedMax=today,
                            showHidden="True").execute()
            for t in tasks['items']:
                print t['title']
                taskEntry = Task(tasksList = listEntry,
                                taskId = t['id'],
                                # TODO tag = getProjectTag(t['title'])
                                tag = t['title'][:3],
                                title = t['title'],
                                updated = t['updated'],
                                selfLink = t['selfLink'],
                                parent = t.get('parent', None),
                                position = t['position'],
                                notes = t.get('notes', None),
                                status = t['status'],
                                # due = t.get('due', '1970-01-01'),
                                due = t.get('due', None),
                                completed = t['completed'])
                taskEntry.save()
    # TODO  Write function that will get list of "tasks"/projects from task list
    # "Projects list"

if __name__ == '__main__':
    set_env()
    main()

