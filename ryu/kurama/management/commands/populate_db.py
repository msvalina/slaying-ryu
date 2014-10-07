#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import string
import gflags
import httplib2
import shutil
from subprocess import check_output
from os.path import basename, dirname, abspath, join
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from datetime import date, timedelta
from django.core.management.base import AppCommand, CommandError
from django.core.management import call_command
from south.models import MigrationHistory
from kurama.models import TaskList, Task, Project

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
KEYS_FILE = SCRIPT_DIR + "/keys.txt"
TASKS_DAT = SCRIPT_DIR + "/tasks.dat"

def auth_helper():
    """ Setup and return authentication variables"""
    auth_vars = {}

    try:
        with open(KEYS_FILE, "r") as kfile:
            client_id = kfile.readline().rstrip()
            client_secret = kfile.readline().rstrip()
            api_key = kfile.readline().rstrip()
    except IOError:
        client_id = raw_input("Enter your client id: ")
        client_secret = raw_input("Enter your client secret: ")
        api_key = raw_input("Enter your api key: ")
        write_auth(client_id, client_secret, api_key)

    auth_vars = {'client_id': client_id,
                 'client_secret': client_secret,
                 'api_key': api_key}

    return auth_vars

def write_auth(client_id, client_secret, api_key):
    """ Writing entered clinet_id, client_secret and api_key """
    with open(KEYS_FILE, "w") as kfile:
        kfile.write(str(client_id) + "\n")
        kfile.write(str(client_secret) + "\n")
        kfile.write(str(api_key) + "\n")

def get_service(client_id='', client_secret='', api_key=''):
    """ Setup 0Auth 2.0 service for """

    flags = gflags.FLAGS
    # Set up a Flow object to be used if we need to authenticate. This
    # sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
    # the information it needs to authenticate. Note that it is called
    # the Web Server Flow, but it can also handle the flow for native
    # applications
    # The client_id and client_secret are copied from the API Access tab on
    # the Google APIs Console
    flow = OAuth2WebServerFlow(
        client_id=client_id,
        client_secret=client_secret,
        scope='https://www.googleapis.com/auth/tasks',
        user_agent='PopulateDB/0.0.1')

    # To disable the local server feature, uncomment the following line:
    flags.auth_local_webserver = False

    # If the Credentials don't exist or are invalid, run through the native
    # client flow. The Storage object will ensure that if successful the
    # good Credentials will get written back to a file.
    storage = Storage(TASKS_DAT)
    credentials = storage.get()
    if credentials is None or credentials.invalid == True:
        credentials = run(flow, storage)

    # Create an httplib2.Http object to handle our HTTP requests and
    # authorize it with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)

    # Build a service object for interacting with the API. Visit the Google APIs
    # Console to get a developerKey for your own application.
    # I used API key for Browser applications
    service = build(serviceName='tasks', version='v1', http=http,
        developerKey=api_key)

    return service

def set_env():
    """ Setting python and django env var """
    ryu_dir = os.path.dirname(os.path.realpath(__file__))
    print ryu_dir
    sys.path.append(ryu_dir)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'ryu.settings'

class Command(AppCommand):
    help = """
    Clear app (with manage.py sqlclear) and south migrations for app and
    populate DB"""
    def handle_app(self, app, verbosity=1, **options):
        printer = Printer(verbosity=verbosity)
        app_name = basename(dirname(app.__file__))
        migrations_dir = abspath(join(dirname(app.__file__), 'migrations'))
        py_mng = "python manage.py "
        printer('Clearing ' + app_name)
        cmd = py_mng + "sqlclear %s | python manage.py dbshell " % app_name
        printer(check_output(cmd, shell=True), verbosity=2)
        printer('Deleting migrations dir')
        try:
            shutil.rmtree(migrations_dir)
        except OSError:
            printer('Failed to delete migrations folder, probably doesnt exist')
        printer('Creating initial schemamigration')
        cmd2 = py_mng + "schemamigration --initial %s" % app_name
        printer(check_output(cmd2, shell=True), verbosity=2)
        printer('Syncing database')
        cmd3 = py_mng + "syncdb"
        printer(check_output(cmd3, shell=True), verbosity=2)
        printer("Fake zero migrate")
        cmd4 = py_mng + "migrate --fake %s zero" % app_name
        printer(check_output(cmd4, shell=True), verbosity=2)
        printer("Migarating to new initial")
        cmd5 = py_mng + "migrate %s" % app_name
        printer(check_output(cmd5, shell=True), verbosity=2)
        populate_db = PopulateDB()
        populate_db.get_task_lists()

class Printer(object):
    """ Printer object for printing output"""
    def __init__(self, verbosity=1):
        self.verbosity = int(verbosity)
    def __call__(self, out, verbosity=1, prefix='***'):
        if verbosity <= self.verbosity:
            print prefix, out

class PopulateDB(object):
    """ Populates database with fetched tasklists and tasks """
    # TODO Query tasklists service api only once in __init__
    service = None
    def __init__(self):
        auth_vars = auth_helper()
        self.service = get_service(auth_vars)
        set_env()

    def get_task_lists(self):
        """ Fetch tasklists and tasks and save them in django model """
        # TODO separate fetching from saving
        tag_dict = self.get_project_lists()
        meta_dict = self.get_meta_info()
        task_lists = self.service.tasklists().list().execute()
        # Save every tasklist that's in used_lists to database
        used_lists = ['01-Im&Ds', '02-Im&Nds', '03-Ni&Ds', '04-Ni&Nds']
        for tskl in task_lists['items']:
            if tskl['title'] in used_lists:
                print "Saving task list: "
                print tskl['title']
                list_entry = TaskList(task_list_id=tskl['id'],
                                     title=tskl['title'],
                                     info=meta_dict.get(tskl['title'], None),
                                     updated=tskl['updated'],
                                     self_link=tskl['selfLink'])
                list_entry.save()

                # Get completed tasks from January first 2014 until today
                # actually tomorrow because of otherwise it won't fetch todays
                # completed tasks - wired I know...
                tommorow = date.today() + timedelta(1)
                tommorow = tommorow.strftime('%Y-%m-%dT00:00:00Z')
                tasks = self.service.tasks().list(
                    tasklist=tskl['id'],
                    completedMin="2014-01-01T00:00:00Z",
                    completedMax=tommorow,
                    showHidden="True").execute()
                self.save_tasks(tasks, list_entry, tag_dict)

                while 'nextPageToken' in tasks:
                    tasks = self.service.tasks().list(
                        tasklist=tskl['id'],
                        completedMin="2014-01-01T00:00:00Z",
                        completedMax=tommorow,
                        showHidden="True",
                        pageToken=tasks['nextPageToken']).execute()
                    self.save_tasks(tasks, list_entry, tag_dict)

    def save_tasks(self, tasks, list_entry, tag_dict):
        """ Save fetched tasks to model """
        for tsk in tasks['items']:
            # Set default task tag to *raz* in case there is no tag in
            # Project List
            task_tag = "*raz*"
            tag_name = "razno"
            task_title = tsk['title'].strip()
            print tsk['title']

            # Get task tag from tag_dict insted of directly spliting
            # from task name, so now task which has tag without space
            # before title can be recongnized correctly
            for tag in tag_dict:
                if tag in tsk['title']:
                    task_tag = tag
                    tag_name = tag_dict.get(task_tag, None)
                    task_title = string.replace(tsk['title'], tag, "")
                    task_title = task_title.strip()
            # Save fetched task in corresponding db field
            task_entry = Task(task_list=list_entry,
                             task_id=tsk['id'],
                             tag=task_tag,
                             tag_name=tag_name,
                             title=task_title,
                             updated=tsk['updated'],
                             self_link=tsk['selfLink'],
                             parent=tsk.get('parent', None),
                             position=tsk['position'],
                             notes=tsk.get('notes', None),
                             status=tsk['status'],
                             due=tsk.get('due', None),
                             completed=tsk['completed'])
            task_entry.save()


    def get_project_lists(self):
        """ Fetch Project List from task api, save it to model and return list
        of tags with full names in dictionary """
        task_lists = self.service.tasklists().list().execute()
        tag_dict = {}
        for tskl in task_lists['items']:
            if tskl['title'] == "Projects list":
                print tskl['title']
                tasks = self.service.tasks().list(tasklist=tskl['id']).execute()
                for tsk in tasks['items']:
                    tag = string.split(tsk['title'], "-")[0].strip()
                    title = string.split(tsk['title'], "-")[1].strip()
                    projectEntry = Project(
                        tag=tag,
                        name=title,
                        position=tsk['position'],
                        description=tsk.get('notes', None),
                        status=tsk['status'],
                        due=tsk.get('due', None),
                        completed=tsk.get('completed', None))
                    print "Saving project entry: " + tsk['title']
                    projectEntry.save()
                    tag_dict[tag] = title
        return tag_dict

    def get_meta_info(self):
        """ Fetch Meta info about task lists from task list "Meta list" """
        task_lists = self.service.tasklists().list().execute()
        meta_dict = {}
        for tskl in task_lists['items']:
            if tskl['title'] == "Meta list":
                print tskl['title']
                tasks = self.service.tasks().list(tasklist=tskl['id']).execute()
                for tsk in tasks['items']:
                    list_name = tsk['title']
                    list_info = tsk['notes']
                    print list_name
                    print list_info
                    meta_dict[list_name] = list_info

        return meta_dict

def main():
    populate_db = PopulateDB()
    populate_db.get_task_lists()

if __name__ == '__main__':
    main()
