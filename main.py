#!/usr/bin/env python
#
# Byte 4 Version 1
#
# Copyright 2/2014 Jennifer Mankoff
#
# Licensed under GPL v3 (http://www.gnu.org/licenses/gpl.html)
#

# standard imports
import webapp2
import json
from google.appengine.api import files
from google.appengine.api import memcache
from apiclient.discovery import build
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from oauth2client.appengine import AppAssertionCredentials
from django.utils import simplejson
import httplib2
import urllib


import logging

# import for checking whether we are running on localhost or remotely
import os

# make sure to add this to app.yaml too
from webapp2_extras import jinja2


# BigQuery API Settings
_PROJECT_NUMBER = '278388745819'

# Define your production Cloud SQL instance information.
_DATABASE_NAME = 'tweets:election_tweets'

logging.info("setting up credentials")
credentials = AppAssertionCredentials(scope='https://www.googleapis.com/auth/bigquery')
http        = credentials.authorize(httplib2.Http(memcache))
service     = build("bigquery", "v2", http=http)
logging.info("done setting up credentials")

# we are adding a new class that will
# help us to use jinja. MainHandler will sublclass this new
# class (BaseHandler), and BaseHandler is in charge of subclassing
# webapp2.RequestHandler
def to_json(data):
    json.encode(data)

class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.

        return jinja2.get_jinja2(app=self.app)



    # lets jinja render our response
    def render_response(self, _template, context):
        values = {'url_for': self.uri_for}


        logging.info(context)
        values.update(context)
        self.response.headers['Content-Type'] = 'text/html'

        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **values)
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.write(rv)


class MainHandler(BaseHandler):
    def get(self):
        """default landing page"""

        #====================================================================
        # Sample query for getting #births by state
        #====================================================================

        states = []

        logging.info("running query 1")
        query_string = "SELECT AVG(sentiment)*1000 FROM [tweets.election_tweets] WHERE (REGEXP_MATCH(location,r'(Pune)')) AND (REGEXP_MATCH(text,r'(Modi)'));".format(_DATABASE_NAME)
        births = self.run_query(query_string, filename='data/states.json')
        # similar to the google SQL work we did in byte4, the stuff we
        # care about is in rows
        rows = births[u'rows']
        for row in rows:
            name = row[u'f'][0][u'v']
            state = {'y': unicode.encode(name), 'x':'Modi'}
            states = states + [state]


        logging.info("running query 2")
        query_string = "SELECT AVG(sentiment)*1000 FROM [tweets.election_tweets] WHERE (REGEXP_MATCH(location,r'(Pune)')) AND (REGEXP_MATCH(text,r'(Kejriwal)'));".format(_DATABASE_NAME)
        births = self.run_query(query_string, filename='data/states.json')
        # similar to the google SQL work we did in byte4, the stuff we
        # care about is in rows
        rows = births[u'rows']
        for row in rows:
            name = row[u'f'][0][u'v']
            state = {'y': unicode.encode(name), 'x':'Kejriwal'}
            states = states + [state]



        array = dict()
        array['values'] = states
        array['key'] = 'Sentiment'
        array['color'] = '#2ca02c'


        outer_array = []
        outer_array.append(array)




        context = {"states": states, "data": (json.dumps(outer_array, separators=(',', ':'), indent=4).decode('utf8'))}

        # and render the response
        self.render_response('index.html', context)


    # run the query specified in query_string, but if local open filename instead
    def run_query(self, query_string, filename=None, timeout=10000):
        if (os.getenv('SERVER_SOFTWARE') and
            os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):


            # set up the query
            query = {'query':query_string, 'timeoutMs':timeout}
            logging.info(query)
            # service is the oauth2 setup that we created above
            jobCollection = service.jobs()
            # project number is the project number you should have
            # defined in your app
            return jobCollection.query(projectId=_PROJECT_NUMBER,body=query).execute()
        else:
            # open the data stored in a file called filename
            logging.info("loading file")
            try:
                fp = open(filename)
                return simplejson.load(fp)
            except IOError:
                logging.info("failed to load file %s", filename)
                return None
            except TypeError:
                return None

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

